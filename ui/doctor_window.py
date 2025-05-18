from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame
from PyQt5.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PyQt5.QtCore import Qt
from ui.patient_register_window import PatientRegisterWindow
from ui.patient_list_window import PatientListWindow

class DoctorWindow(QWidget):
    def __init__(self, doctor_adi, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.doctor_adi = doctor_adi
        self.patient_list_window = None
        self.register_window = None

        self.setWindowTitle("Doktor Paneli")
        self.showMaximized()  # 👈 Tam ekran başlat

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # 🖼️ Profil çerçevesi
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
        pixmap = QPixmap("assets/default_doctor.png").scaled(150, 150, Qt.KeepAspectRatioByExpanding,
                                                             Qt.SmoothTransformation)
        rounded = QPixmap(150, 150)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, 150, 150)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.profil_label.setPixmap(rounded)

        # 👨‍⚕️ Hoş geldiniz mesajı
        self.label = QLabel(f"👨‍⚕️ Hoş geldiniz, Dr. {doctor_adi}")
        self.label.setFont(QFont("Arial", 16))
        self.label.setAlignment(Qt.AlignCenter)

        # 🔘 Butonlar
        self.button_hasta_ekle = QPushButton("🆕 Yeni Hasta Ekle")
        self.button_hasta_ekle.clicked.connect(self.hasta_ekle)

        self.button_goster = QPushButton("🔍 Hastaları Listele")
        self.button_goster.clicked.connect(self.hasta_listele)

        self.button_cikis = QPushButton("🚪 Çıkış Yap")
        self.button_cikis.clicked.connect(self.cikis_yap)

        layout.addWidget(self.profil_frame)
        layout.addSpacing(10)
        layout.addWidget(self.label)
        layout.addSpacing(15)
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
