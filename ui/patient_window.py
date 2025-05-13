from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from ui.measurement_form import MeasurementForm
from ui.daily_tracking_form import DailyTrackingForm
from ui.patient_recommendation_window import PatientRecommendationWindow  # 👈 yeni pencere eklendi

class PatientWindow(QWidget):
    def __init__(self, hasta_adi, hasta_id):
        super().__init__()
        print("✅ PatientWindow başlatıldı")
        print("📌 PatientWindow açıldı.")
        self.setWindowTitle("Hasta Paneli")
        self.setGeometry(100, 100, 400, 400)
        self.hasta_adi = hasta_adi
        self.hasta_id = hasta_id

        self.label = QLabel(f"🧍‍♂️ Hoş geldiniz, {hasta_adi}")
        self.label.setStyleSheet("font-size: 16px;")

        self.button_olcum = QPushButton("📥 Ölçüm Girişi")
        self.button_olcum.clicked.connect(self.olcum_formu_ac)

        self.button_takip = QPushButton("📝 Günlük Takip")
        self.button_takip.clicked.connect(self.takip_formu_ac)

        self.button_oneriler = QPushButton("🧠 Önerilerim")
        self.button_oneriler.clicked.connect(self.onerileri_goster)

        self.button_goster = QPushButton("📊 Kan Şekeri Takibi (yakında)")
        self.button_goster.clicked.connect(self.takip_goster)

        self.button_cikis = QPushButton("🚪 Çıkış Yap")
        self.button_cikis.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_olcum)
        layout.addWidget(self.button_takip)
        layout.addWidget(self.button_oneriler)
        layout.addWidget(self.button_goster)
        layout.addWidget(self.button_cikis)

        self.setLayout(layout)

    def olcum_formu_ac(self):
        print("➡ Ölçüm formuna girildi")
        try:
            if self.hasta_id is None:
                raise ValueError("Hasta ID eksik!")
            pencere = MeasurementForm(self.hasta_id)
            pencere.exec_()
        except Exception as e:
            print(f"❌ Ölçüm formu hatası: {e}")
            QMessageBox.critical(self, "Hata", f"Form açılamadı: {e}")

    def takip_formu_ac(self):
        print("📆 Günlük takip formu açılıyor...")
        try:
            pencere = DailyTrackingForm(self.hasta_id)
            pencere.exec_()
        except Exception as e:
            print(f"❌ Takip formu hatası: {e}")
            QMessageBox.critical(self, "Hata", f"Takip formu açılamadı: {e}")

    def onerileri_goster(self):
        print("🧠 Öneri penceresi açılıyor...")
        try:
            pencere = PatientRecommendationWindow(self.hasta_id)
            pencere.exec_()
        except Exception as e:
            print(f"❌ Öneri görüntüleme hatası: {e}")
            QMessageBox.critical(self, "Hata", f"Öneri penceresi açılamadı: {e}")

    def takip_goster(self):
        QMessageBox.information(self, "Bilgi", "Bu özellik yakında eklenecek.")
