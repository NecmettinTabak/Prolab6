from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database.db_manager import DBManager
from ui.doctor_window import DoctorWindow
from ui.patient_window import PatientWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diyabet Takip Sistemi - Giriş")
        self.setGeometry(100, 100, 300, 200)

        self.label_tc = QLabel("T.C. Kimlik No:")
        self.input_tc = QLineEdit()

        self.label_sifre = QLabel("Şifre:")
        self.input_sifre = QLineEdit()
        self.input_sifre.setEchoMode(QLineEdit.Password)

        self.button_giris = QPushButton("Giriş Yap")
        self.button_giris.clicked.connect(self.giris_yap)

        layout = QVBoxLayout()
        layout.addWidget(self.label_tc)
        layout.addWidget(self.input_tc)
        layout.addWidget(self.label_sifre)
        layout.addWidget(self.input_sifre)
        layout.addWidget(self.button_giris)
        self.setLayout(layout)

    def giris_yap(self):
        tc_no = self.input_tc.text()
        sifre = self.input_sifre.text()

        db = DBManager(password="Necmettin2004")
        user = db.kullanici_getir(tc_no, sifre)
        db.kapat()

        if user:
            QMessageBox.information(self, "Giriş Başarılı", f"Hoş geldiniz, {user.ad}!")

            if user.rol == "doktor":
                self.panel = DoctorWindow(user.ad, user.id)  # 🔴 Referans olarak atandı
                self.panel.show()
                self.hide()

            else:
                print(f"🧪 Hasta ID geldi mi?: {user.id}")

                self.panel = PatientWindow(user.ad, user.id)

            self.panel.show()
            self.hide()  # Burada kapatma en sonda

        else:
            QMessageBox.warning(self, "Hatalı Giriş", "T.C. No veya şifre hatalı.")
