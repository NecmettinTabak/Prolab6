from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QTimeEdit, QDateEdit, QPushButton, QFormLayout, QMessageBox
from datetime import datetime
from models.measurement import Measurement
from database.db_manager import DBManager

class MeasurementForm(QDialog):
    def __init__(self, hasta_id):
        print("📥 Ölçüm formu başlatılıyor")
        super().__init__()
        self.setWindowTitle("Kan Şekeri Ölçüm Girişi")
        self.setFixedSize(300, 200)
        self.hasta_id = hasta_id

        self.seviye_input = QLineEdit()
        self.tarih_input = QDateEdit()
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDate(datetime.today())
        self.saat_input = QTimeEdit()

        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.clicked.connect(self.veri_kaydet)

        layout = QFormLayout()
        layout.addRow("Kan Şekeri (mg/dL):", self.seviye_input)
        layout.addRow("Tarih:", self.tarih_input)
        layout.addRow("Saat:", self.saat_input)
        layout.addRow(self.btn_kaydet)
        self.setLayout(layout)

    def veri_kaydet(self):
        try:
            seviye = int(self.seviye_input.text())
            if not (20 <= seviye <= 1000):
                raise ValueError("Seviye 20 ile 1000 arasında olmalı.")

            tarih = self.tarih_input.date().toString("yyyy-MM-dd")
            saat = self.saat_input.time().toString("HH:mm:ss")

            olcum = Measurement(
                hasta_id=self.hasta_id,
                tarih=tarih,
                saat=saat,
                seviye=seviye
            )

            db = DBManager(password="Necmettin2004")
            db.olcum_ekle(olcum)
            db.kapat()

            QMessageBox.information(self, "Başarılı", "Ölçüm kaydedildi.")
            self.accept()

        except ValueError as ve:
            QMessageBox.warning(self, "Geçersiz Giriş", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri kaydedilemedi: {e}")
