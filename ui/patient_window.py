from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QFrame
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from ui.measurement_form import MeasurementForm
from ui.daily_tracking_form import DailyTrackingForm
from ui.patient_recommendation_window import PatientRecommendationWindow
from database.db_manager import DBManager

class PatientWindow(QWidget):
    def __init__(self, hasta_adi, hasta_id):
        super().__init__()
        self.setWindowTitle("Hasta Paneli")
        self.showMaximized()
        self.hasta_adi = hasta_adi
        self.hasta_id = hasta_id
        self.oneri_penceresi = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Profil çerçevesi
        self.profil_frame = QFrame()
        self.profil_frame.setFixedSize(160, 160)
        self.profil_frame.setStyleSheet("""
            QFrame {
                border: 3px solid #CCCCCC;
                border-radius: 80px;
                background-color: white;
            }
        """)

        self.profil_label = QLabel(self.profil_frame)
        self.profil_label.setGeometry(5, 5, 150, 150)
        self.profil_label.setAlignment(Qt.AlignCenter)
        self.profil_label.setStyleSheet("border-radius: 75px; background-color: transparent;")
        pixmap = QPixmap("assets/default_user.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.profil_label.setPixmap(pixmap)

        # Karşılama
        self.label = QLabel(f"🧍‍♂️ Hoş geldiniz, {hasta_adi}")
        self.label.setFont(QFont("Arial", 16))
        self.label.setAlignment(Qt.AlignCenter)

        # Butonlar
        self.button_olcum = QPushButton("📅 Ölçüm Girişi")
        self.button_takip = QPushButton("🗒 Günlük Takip")
        self.button_oneriler = QPushButton("🧠 Önerilerim")
        self.button_goster = QPushButton("📊 Kan Şekeri Takibi")
        self.button_cikis = QPushButton("🚪 Çıkış Yap")

        self.button_olcum.clicked.connect(self.olcum_formu_ac)
        self.button_takip.clicked.connect(self.takip_formu_ac)
        self.button_oneriler.clicked.connect(self.onerileri_goster)
        self.button_goster.clicked.connect(self.insulin_onerisi_goster)
        self.button_cikis.clicked.connect(self.close)

        # Yerleşim
        layout.addWidget(self.profil_frame)
        layout.addSpacing(10)
        layout.addWidget(self.label)
        layout.addSpacing(15)
        layout.addWidget(self.button_olcum)
        layout.addWidget(self.button_takip)
        layout.addWidget(self.button_oneriler)
        layout.addWidget(self.button_goster)
        layout.addWidget(self.button_cikis)

        self.setLayout(layout)

    def olcum_formu_ac(self):
        try:
            if self.hasta_id is None:
                raise ValueError("Hasta ID eksik!")
            pencere = MeasurementForm(self.hasta_id)
            pencere.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Form açılamadı: {e}")

    def takip_formu_ac(self):
        try:
            pencere = DailyTrackingForm(self.hasta_id)
            pencere.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Takip formu açılamadı: {e}")

    def onerileri_goster(self):
        try:
            if self.oneri_penceresi is None or not self.oneri_penceresi.isVisible():
                self.oneri_penceresi = PatientRecommendationWindow(self.hasta_id)
                self.oneri_penceresi.show()
            else:
                self.oneri_penceresi.raise_()
                self.oneri_penceresi.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Öneri penceresi açılamadı: {e}")

    def insulin_onerisi_goster(self):
        try:
            db = DBManager(password="Necmettin2004")
            sonuc = db.insulin_dozu_getir(self.hasta_id)
            db.kapat()

            if sonuc:
                ortalama, doz, adet = sonuc
                QMessageBox.information(self, "💉 İnsülin Önerisi",
                                        f"🔬 Ortalama Şeker: {ortalama} mg/dL\n"
                                        f"📈 Ölçüm Sayısı: {adet}\n"
                                        f"💉 Önerilen İnsülin Dozu: {doz}")
            else:
                QMessageBox.information(self, "Bilgi", "Bugün için yeterli ölçüm yok.\nEn az 3 zaman dilimi gerekir.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İnsülin önerisi alınamadı:\n{e}")
