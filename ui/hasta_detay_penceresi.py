from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate
from database.db_manager import DBManager
import datetime
from ui.hasta_duzen_takip_penceresi import PatientAdherenceWindow
from ui.hasta_glikoz_izleme_penceresi import PatientGlucoseTrendWindow

class PatientDetailWindow(QDialog):
    def __init__(self, hasta):
        super().__init__()
        self.hasta = hasta
        self.setWindowTitle(f"{hasta.ad} {hasta.soyad} - Detaylar")
        self.setGeometry(200, 200, 500, 600)

        layout = QVBoxLayout()
        self.label = QLabel(f"🧍 Hasta: {hasta.ad} {hasta.soyad} - TC: {hasta.tc_no}")
        self.tarih_secici = QDateEdit()
        self.tarih_secici.setCalendarPopup(True)
        self.tarih_secici.setDate(QDate.currentDate())
        self.tarih_secici.dateChanged.connect(self.yenile)

        self.olcum_listesi = QListWidget()
        self.uyari_listesi = QListWidget()

        self.oneri_button = QPushButton("🧠 Öneri Göster")
        self.oneri_button.clicked.connect(self.oneri_goster)
        self.ata_button = QPushButton("✅ Öneriyi Ata")
        self.ata_button.clicked.connect(self.oneri_ata)
        self.gecmis_btn = QPushButton("📅 Diyet/Egzersiz Geçmişi")
        self.gecmis_btn.clicked.connect(self.gecmis_goster)
        self.grafik_btn = QPushButton("📈 Kan Şekeri Zaman Grafiği")
        self.grafik_btn.clicked.connect(self.grafik_goster)


        layout.addWidget(self.label)
        layout.addWidget(QLabel("📅 Tarih Seç:"))
        layout.addWidget(self.tarih_secici)

        layout.addWidget(QLabel("📊 Kan Şekeri Ölçümleri:"))
        layout.addWidget(self.olcum_listesi)

        layout.addWidget(QLabel("🔔 Uyarılar:"))
        layout.addWidget(self.uyari_listesi)

        layout.addWidget(self.grafik_btn)
        layout.addWidget(self.gecmis_btn)
        layout.addWidget(self.oneri_button)
        layout.addWidget(self.ata_button)
        self.setLayout(layout)

        self.db = DBManager(password="Hekim11322..")
        self.oneri = None
        self.yenile()
        self.db.kapat()

    def yenile(self):
        self.yukle_olcumler()
        self.yukle_uyarilar()

    def yukle_olcumler(self):
        try:
            self.olcum_listesi.clear()
            tarih_str = self.tarih_secici.date().toString("yyyy-MM-dd")

            db = DBManager(password="Hekim11322..")
            db.cursor.execute(
                "SELECT tarih, saat, seviye, zaman_dilimi FROM measurements WHERE hasta_id = %s AND tarih = %s ORDER BY saat DESC",
                (self.hasta.id, tarih_str)
            )
            sonuc = db.cursor.fetchall()

            if not sonuc:
                self.olcum_listesi.addItem("Seçilen tarihte ölçüm kaydı yok.")
            else:
                for t, s, seviye, zaman_dilimi in sonuc:
                    zaman_str = f" ({zaman_dilimi.upper()})" if zaman_dilimi else " (ZAMAN DIŞI)"
                    self.olcum_listesi.addItem(f"📅 {t} ⏰ {s} → {seviye} mg/dL{zaman_str}")

            db.kapat()
        except Exception as e:
            self.olcum_listesi.addItem(f"Hata: {e}")

    def yukle_uyarilar(self):
        try:
            self.uyari_listesi.clear()
            secili_tarih = self.tarih_secici.date().toPyDate()

            db = DBManager(password="Hekim11322..")
            db.cursor.execute(
                """
                SELECT tarih, uyarı_tipi, mesaj FROM alerts
                WHERE hasta_id = %s AND DATE(tarih) = %s
                ORDER BY tarih DESC
                """,
                (self.hasta.id, secili_tarih)
            )
            uyarilar = db.cursor.fetchall()
            db.kapat()

            if not uyarilar:
                self.uyari_listesi.addItem("Seçilen tarihte uyarı yok.")
            else:
                for tarih_saat, uyarı_tipi, mesaj in uyarilar:
                    self.uyari_listesi.addItem(f"📅 {tarih_saat} → {uyarı_tipi.upper()}: {mesaj}")

        except Exception as e:
            self.uyari_listesi.addItem(f"Hata: {e}")

    def oneri_goster(self):
        try:
            self.db = DBManager(password="Hekim11322..")
            self.db.cursor.execute(
                "SELECT seviye FROM measurements WHERE hasta_id = %s ORDER BY tarih DESC, saat DESC LIMIT 1",
                (self.hasta.id,)
            )
            result = self.db.cursor.fetchone()
            if not result:
                QMessageBox.information(self, "Bilgi", "Bu hasta için ölçüm kaydı yok.")
                return

            seviye = result[0]
            self.db.cursor.execute("""
                SELECT r.belirtiler, d.ad, e.ad, r.diyet_id, r.egzersiz_id
                FROM recommendation_rules r
                LEFT JOIN diet_types d ON r.diyet_id = d.id
                LEFT JOIN exercise_types e ON r.egzersiz_id = e.id
                WHERE %s BETWEEN r.min_seker AND r.max_seker
                LIMIT 1
            """, (seviye,))
            kural = self.db.cursor.fetchone()
            self.db.kapat()

            if kural:
                belirtiler, diyet_ad, egzersiz_ad, diyet_id, egzersiz_id = kural
                self.oneri = (diyet_id, egzersiz_id)
                mesaj = f"📌 Önerilen Diyet: {diyet_ad or 'Yok'}\n🏃‍♂️ Önerilen Egzersiz: {egzersiz_ad or 'Yok'}\n📍 Tipik Belirtiler: {belirtiler}"
                QMessageBox.information(self, "Öneri", mesaj)
            else:
                QMessageBox.information(self, "Bilgi", "Bu seviye için öneri bulunamadı.")
                self.oneri = None

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Öneri getirilemedi: {e}")

    def oneri_ata(self):
        try:
            self.db = DBManager(password="Hekim11322..")
            self.db.cursor.execute(
                "SELECT seviye FROM measurements WHERE hasta_id = %s ORDER BY tarih DESC, saat DESC LIMIT 1",
                (self.hasta.id,))
            result = self.db.cursor.fetchone()
            if not result:
                QMessageBox.information(self, "Bilgi", "Ölçüm verisi bulunamadı.")
                return

            seviye = result[0]
            self.db.cursor.execute(
                "SELECT id FROM recommendation_rules WHERE %s BETWEEN min_seker AND max_seker LIMIT 1",
                (seviye,))
            rule_result = self.db.cursor.fetchone()
            if not rule_result:
                QMessageBox.information(self, "Bilgi", "Bu seviye için öneri bulunamadı.")
                return

            rule_id = rule_result[0]
            bugun = datetime.date.today().strftime("%Y-%m-%d")
            self.db.cursor.execute(
                "SELECT id FROM assigned_recommendations WHERE hasta_id = %s AND rule_id = %s AND tarih = %s",
                (self.hasta.id, rule_id, bugun))
            if self.db.cursor.fetchone():
                QMessageBox.information(self, "Bilgi", "Bu öneri zaten atanmış.")
            else:
                self.db.cursor.execute(
                    "INSERT INTO assigned_recommendations (hasta_id, rule_id, tarih) VALUES (%s, %s, %s)",
                    (self.hasta.id, rule_id, bugun)
                )
                self.db.conn.commit()
                QMessageBox.information(self, "Başarılı", "Öneri başarıyla atandı!")
            self.db.kapat()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Öneri atanamadı: {e}")

    def gecmis_goster(self):
        self.uyum_penceresi = PatientAdherenceWindow(self.hasta.id)
        self.uyum_penceresi.exec_()

    def grafik_goster(self):
        self.grafik_penceresi = PatientGlucoseTrendWindow(self.hasta.id)
        self.grafik_penceresi.exec_()