from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
from database.db_manager import DBManager
from models.patient_diet import PatientDiet
from models.patient_exercise import PatientExercise
import datetime

class PatientDetailWindow(QDialog):
    def __init__(self, hasta):
        super().__init__()
        self.hasta = hasta
        self.setWindowTitle(f"{hasta.ad} {hasta.soyad} - Detaylar")
        self.setGeometry(200, 200, 450, 400)

        layout = QVBoxLayout()
        self.label = QLabel(f"🧍 Hasta: {hasta.ad} {hasta.soyad} - TC: {hasta.tc_no}")
        self.olcum_listesi = QListWidget()

        self.oneri_button = QPushButton("🧠 Öneri Göster")
        self.oneri_button.clicked.connect(self.oneri_goster)

        self.ata_button = QPushButton("✅ Öneriyi Ata")
        self.ata_button.clicked.connect(self.oneri_ata)

        layout.addWidget(self.label)
        layout.addWidget(QLabel("📊 Kan Şekeri Ölçümleri:"))
        layout.addWidget(self.olcum_listesi)
        layout.addWidget(self.oneri_button)
        layout.addWidget(self.ata_button)
        self.setLayout(layout)

        self.db = DBManager(password="Necmettin2004")
        self.yukle_olcumler()
        self.db.kapat()

        self.oneri = None  # Diyet ve egzersiz id'si tutulacak

    def yukle_olcumler(self):
        try:
            query = "SELECT tarih, saat, seviye FROM measurements WHERE hasta_id = %s ORDER BY tarih DESC, saat DESC"
            self.db.cursor.execute(query, (self.hasta.id,))
            sonuc = self.db.cursor.fetchall()

            if not sonuc:
                self.olcum_listesi.addItem("Hiç ölçüm kaydı yok.")
            else:
                for t, s, seviye in sonuc:
                    self.olcum_listesi.addItem(f"📅 {t} ⏰ {s} → {seviye} mg/dL")
        except Exception as e:
            self.olcum_listesi.addItem(f"Hata: {e}")

    def oneri_goster(self):
        try:
            self.db = DBManager(password="Necmettin2004")
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
        if not self.oneri:
            QMessageBox.warning(self, "Uyarı", "Önce öneriyi görüntüleyin.")
            return

        diyet_id, egzersiz_id = self.oneri
        bugun = datetime.date.today()
        db = DBManager(password="Necmettin2004")

        try:
            if diyet_id:
                db.hasta_diyet_ekle(PatientDiet(hasta_id=self.hasta.id, diet_id=diyet_id, tarih=bugun, uygulandi_mi=False))
            if egzersiz_id:
                db.hasta_egzersiz_ekle(PatientExercise(hasta_id=self.hasta.id, egzersiz_id=egzersiz_id, tarih=bugun, yapildi_mi=False))

            QMessageBox.information(self, "Başarılı", "Önerilen diyet ve egzersiz başarıyla atandı.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Atama başarısız: {e}")
        finally:
            db.kapat()
