from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from ui.patient_register_window import PatientRegisterWindow  # hasta kayıt ekranı
from ui.patient_list_window import PatientListWindow  # hasta listeleme ekranı

class DoctorWindow(QWidget):
    def __init__(self, doctor_adi, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.doctor_adi = doctor_adi
        self.patient_list_window = None
        self.register_window = None

        self.setWindowTitle("Doktor Paneli")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel(f"👨‍⚕️ Hoş geldiniz, Dr. {doctor_adi}")
        self.label.setStyleSheet("font-size: 16px;")

        # Butonlar
        self.button_hasta_ekle = QPushButton("🆕 Yeni Hasta Ekle")
        self.button_hasta_ekle.clicked.connect(self.hasta_ekle)

        self.button_goster = QPushButton("🔍 Hastaları Listele")
        self.button_goster.clicked.connect(self.hasta_listele)

        self.button_cikis = QPushButton("🚪 Çıkış Yap")
        self.button_cikis.clicked.connect(self.cikis_yap)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_hasta_ekle)
        layout.addWidget(self.button_goster)
        layout.addWidget(self.button_cikis)

        self.setLayout(layout)

    def hasta_ekle(self):
        self.register_window = PatientRegisterWindow(doktor_id=self.doctor_id)
        self.register_window.exec_()

    def hasta_listele(self):
        self.patient_list_window = PatientListWindow(doktor_id=self.doctor_id)
        self.patient_list_window.exec_()

    def cikis_yap(self):
        self.close()
