from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
from database.db_manager import DBManager
from models.hasta_diyet import PatientDiet
from models.hasta_egzersiz import PatientExercise
from datetime import date

class DailyTrackingForm(QDialog):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("Günlük Takip")
        self.setFixedSize(300, 200)
        self.hasta_id = hasta_id

        self.egzersiz_checkbox = QCheckBox("Bugün egzersiz yaptım")
        self.diyet_checkbox = QCheckBox("Bugün diyetime uydum")
        self.kaydet_button = QPushButton("Kaydet")
        self.kaydet_button.clicked.connect(self.verileri_kaydet)

        layout = QVBoxLayout()
        layout.addWidget(self.egzersiz_checkbox)
        layout.addWidget(self.diyet_checkbox)
        layout.addWidget(self.kaydet_button)
        self.setLayout(layout)

    def verileri_kaydet(self):
        egzersiz = self.egzersiz_checkbox.isChecked()
        diyet = self.diyet_checkbox.isChecked()
        bugun = date.today().strftime("%Y-%m-%d")

        db = DBManager(password="Hekim11322..")

        if egzersiz:
            db.hasta_egzersiz_ekle(PatientExercise(hasta_id=self.hasta_id, egzersiz_id=1, tarih=bugun, yapildi_mi=True))

        if diyet:
            db.hasta_diyet_ekle(PatientDiet(hasta_id=self.hasta_id, diet_id=1, tarih=bugun, uygulandi_mi=True))

        db.kapat()

        QMessageBox.information(self, "Başarılı", "Günlük takip bilgileri kaydedildi.")
        self.accept()
