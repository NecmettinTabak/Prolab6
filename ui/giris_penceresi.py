from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt
from database.db_manager import DBManager
from logic.sifreleme import hash_sifre
from ui.doktor_penceresi import DoctorWindow
from ui.hasta_penceresi import PatientWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diyabet Takip Sistemi - Giriş")
        self.showMaximized()


        self.title_label = QLabel("🩺 Diyabet Takip Sistemi")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50;")


        self.group_box = QGroupBox("Giriş Paneli")
        self.group_box.setStyleSheet("QGroupBox { font-size: 18px; padding: 20px; }")

        self.label_tc = QLabel("T.C. Kimlik No:")
        self.input_tc = QLineEdit()
        self.input_tc.setPlaceholderText("11 haneli T.C. Kimlik Numaranız")

        self.label_sifre = QLabel("Şifre:")
        self.input_sifre = QLineEdit()
        self.input_sifre.setEchoMode(QLineEdit.Password)
        self.input_sifre.setPlaceholderText("Şifrenizi girin")

        self.button_giris = QPushButton("Giriş Yap")
        self.button_giris.clicked.connect(self.giris_yap)

        group_layout = QVBoxLayout()
        group_layout.addWidget(self.label_tc)
        group_layout.addWidget(self.input_tc)
        group_layout.addWidget(self.label_sifre)
        group_layout.addWidget(self.input_sifre)
        group_layout.addWidget(self.button_giris)
        self.group_box.setLayout(group_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addStretch()
        main_layout.addWidget(self.group_box, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def giris_yap(self):
        tc_no = self.input_tc.text()
        sifre = self.input_sifre.text()
        sifre = hash_sifre(sifre)

        db = DBManager(password="Hekim11322..")
        user = db.kullanici_getir(tc_no, sifre)
        db.kapat()

        if user:
            QMessageBox.information(self, "Giriş Başarılı", f"Hoş geldiniz, {user.ad}!")

            if user.rol == "doktor":
                self.panel = DoctorWindow(user.ad, user.id)
                self.panel.show()
                self.hide()
            else:
                print(f"🧪 Hasta ID geldi mi?: {user.id}")
                self.panel = PatientWindow(user.ad, user.id)
                self.panel.show()
                self.hide()

        else:
            QMessageBox.warning(self, "Hatalı Giriş", "T.C. No veya şifre hatalı.")
