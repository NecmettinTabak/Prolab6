from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from models.kullanici import User
from database.db_manager import DBManager
from utils.mail_yollama import hasta_mail_gonder
from PyQt5.QtWidgets import QComboBox


class PatientRegisterWindow(QDialog):
    def __init__(self, doktor_id):
        super().__init__()
        self.setWindowTitle("Yeni Hasta Kaydı")
        self.setFixedSize(300, 300)
        self.setWindowModality(Qt.ApplicationModal)
        self.doktor_id = doktor_id


        self.tc_input = QLineEdit()
        self.ad_input = QLineEdit()
        self.soyad_input = QLineEdit()
        self.cinsiyet_combo = QComboBox()
        self.cinsiyet_combo.addItems(["Erkek", "Kadın"])
        self.email_input = QLineEdit()
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)


        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.clicked.connect(self.hasta_kaydet)


        layout = QFormLayout()
        layout.addRow("T.C. No:", self.tc_input)
        layout.addRow("Ad:", self.ad_input)
        layout.addRow("Soyad:", self.soyad_input)
        layout.addRow("Cinsiyet:", self.cinsiyet_combo)
        layout.addRow("E-Posta:", self.email_input)
        layout.addRow("Şifre:", self.sifre_input)
        layout.addRow(self.btn_kaydet)

        self.setLayout(layout)

    def hasta_kaydet(self):
        tc = self.tc_input.text()
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        email = self.email_input.text()
        sifre = self.sifre_input.text()

        if not (tc and ad and soyad and email and sifre):
            QMessageBox.warning(self, "Eksik Bilgi", "Tüm alanları doldurun.")
            return

        user = User(
            id=None,
            tc_no=tc,
            ad=ad,
            soyad=soyad,
            email=email,
            sifre=sifre,
            cinsiyet=self.cinsiyet_combo.currentText(),
            dogum_tarihi="2000-01-01",
            rol="hasta",
            profil_resmi=None,
            doktor_id=self.doktor_id
        )

        db = DBManager(password="Hekim11322..")
        db.kullanici_ekle(user)
        db.kapat()

        QTimer.singleShot(100, lambda: hasta_mail_gonder(ad, email, tc, sifre))

        QMessageBox.information(self, "Başarılı", "Hasta başarıyla eklendi ve e-posta gönderildi!")
        self.accept()
