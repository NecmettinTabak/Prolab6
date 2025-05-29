from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from database.db_manager import DBManager
from datetime import datetime

class FirstEntryWindow(QDialog):
    def __init__(self, hasta):
        super().__init__()
        self.setWindowTitle("İlk Ölçüm ve Belirti Girişi")
        self.setMinimumSize(400, 300)
        self.hasta = hasta

        self.db = DBManager(password="Hekim11322..")
        self.oneri = None

        layout = QVBoxLayout()

        self.label = QLabel(f"🧑 Hasta: {hasta.ad} {hasta.soyad} - TC: {hasta.tc_no}")
        self.glukoz_input = QLineEdit()
        self.glukoz_input.setPlaceholderText("🌿 Kan Şekeri (mg/dL)")

        self.belirti_combo = QComboBox()
        self.belirti_combo.addItems( ["Baş ağrısı", "Bulanık görme", "Yorgunluk", "Kilo Kaybı", "Polifaji","Nöropati", "Polidipsi", "Poliüri", "Yaraların Yavaş İyileşmesi"])

        self.btn_oneri_goster = QPushButton("🧠 Öneri Göster")
        self.btn_oneri_goster.clicked.connect(self.oneri_goster)

        self.btn_oneri_ata = QPushButton("✅ Öneriyi Ata")
        self.btn_oneri_ata.clicked.connect(self.oneri_ata)

        layout.addWidget(self.label)
        layout.addWidget(self.glukoz_input)
        layout.addWidget(self.belirti_combo)
        layout.addWidget(self.btn_oneri_goster)
        layout.addWidget(self.btn_oneri_ata)

        self.setLayout(layout)

    def oneri_goster(self):
        try:
            seviye = int(self.glukoz_input.text())
            belirti = self.belirti_combo.currentText()

            self.db.cursor.execute("""
                SELECT r.belirtiler, d.ad, e.ad, r.diyet_id, r.egzersiz_id
                FROM recommendation_rules r
                LEFT JOIN diet_types d ON r.diyet_id = d.id
                LEFT JOIN exercise_types e ON r.egzersiz_id = e.id
                WHERE %s BETWEEN r.min_seker AND r.max_seker
                  AND FIND_IN_SET(%s, REPLACE(r.belirtiler, ' ', ''))
            """, (seviye, belirti.replace(" ", "")))
            kural = self.db.cursor.fetchone()

            if kural:
                belirtiler, diyet_ad, egzersiz_ad, diyet_id, egzersiz_id = kural
                self.oneri = (diyet_id, egzersiz_id)
                mesaj = f"📌 Önerilen Diyet: {diyet_ad or 'Yok'}\n🏃‍♂️ Önerilen Egzersiz: {egzersiz_ad or 'Yok'}\n📍 Tipik Belirtiler: {belirtiler}"
                QMessageBox.information(self, "Öneri", mesaj)
            else:
                QMessageBox.information(self, "Bilgi", "Bu seviye ve belirti için öneri bulunamadı.")
                self.oneri = None

        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir kan şekeri seviyesi giriniz.")

    def oneri_ata(self):
        try:
            seviye = int(self.glukoz_input.text())
            belirti = self.belirti_combo.currentText()

            self.db.cursor.execute("""
                SELECT id FROM recommendation_rules
                WHERE %s BETWEEN min_seker AND max_seker
                  AND FIND_IN_SET(%s, REPLACE(belirtiler, ' ', ''))
            """, (seviye, belirti.replace(" ", "")))
            rule = self.db.cursor.fetchone()

            if not rule:
                QMessageBox.information(self, "Bilgi", "Bu seviye ve belirti için öneri bulunamadı.")
                return

            rule_id = rule[0]
            bugun = datetime.now().strftime("%Y-%m-%d")

            self.db.cursor.execute("""
                SELECT id FROM assigned_recommendations
                WHERE hasta_id = %s AND rule_id = %s AND tarih = %s
            """, (self.hasta.id, rule_id, bugun))

            if self.db.cursor.fetchone():
                QMessageBox.information(self, "Bilgi", "Bu öneri zaten atanmış.")
                return

            self.db.cursor.execute("""
                INSERT INTO assigned_recommendations (hasta_id, rule_id, tarih)
                VALUES (%s, %s, %s)
            """, (self.hasta.id, rule_id, bugun))
            self.db.conn.commit()
            QMessageBox.information(self, "Başarı", "Öneri başarıyla atandı.")

        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir kan şekeri seviyesi giriniz.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Öneri atanamadı: {e}")

