from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QTimeEdit, QDateEdit
from datetime import datetime
from models.measurement import Measurement
from database.db_manager import DBManager

def zaman_dilimini_bul(saat: int):
    if 7 <= saat < 8:
        return "sabah"
    elif 12 <= saat < 13:
        return "ogle"
    elif 15 <= saat < 16:
        return "ikindi"
    elif 18 <= saat < 19:
        return "aksam"
    elif 22 <= saat < 23:
        return "gece"
    return None

class MeasurementForm(QDialog):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("🩸 Kan Şekeri Ölçüm Girişi")
        self.setFixedSize(340, 250)
        self.hasta_id = hasta_id

        self.seviye_input = QLineEdit()
        self.seviye_input.setPlaceholderText("Örn: 110")

        self.tarih_input = QDateEdit()
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDate(datetime.now().date())

        self.saat_input = QTimeEdit()
        self.saat_input.setTime(datetime.now().time())

        self.zaman_label = QLabel("")  # boş başlat
        self.btn_kaydet = QPushButton("💾 Kaydet")
        self.btn_kaydet.clicked.connect(self.veri_kaydet)

        layout = QFormLayout()
        layout.addRow("📅 Tarih:", self.tarih_input)
        layout.addRow("⏰ Saat:", self.saat_input)
        layout.addRow(self.zaman_label)
        layout.addRow("💉 Kan Şekeri (mg/dL):", self.seviye_input)
        layout.addRow(self.btn_kaydet)
        self.setLayout(layout)

    def veri_kaydet(self):
        try:
            seviye = int(self.seviye_input.text())
            if not (20 <= seviye <= 1000):
                raise ValueError("Seviye 20 ile 1000 arasında olmalı.")

            tarih = self.tarih_input.date().toString("yyyy-MM-dd")
            saat_obj = self.saat_input.time()
            saat = saat_obj.toString("HH:mm:ss")
            saat_int = saat_obj.hour()

            zaman_dilimi = zaman_dilimini_bul(saat_int)

            if zaman_dilimi:
                self.zaman_label.setText(f"🕒 Zaman Dilimi: {zaman_dilimi.upper()}")
            else:
                self.zaman_label.setText("⏱️ Bu saat herhangi bir ölçüm diliminde değil")

            db = DBManager(password="Necmettin2004")

            if zaman_dilimi and db.zaten_var_mi(self.hasta_id, tarih, zaman_dilimi):
                QMessageBox.warning(self, "🛑 Ölçüm Tekrarı",
                    f"{zaman_dilimi.upper()} diliminde zaten ölçüm var.")
                db.kapat()
                return

            if not zaman_dilimi:
                QMessageBox.information(self, "Zaman Dışı",
                    "Bu saat ölçüm diliminde değil.\nKayıt edilecek ama ortalamaya katılmayacak.")

            olcum = Measurement(
                hasta_id=self.hasta_id,
                tarih=tarih,
                saat=saat,
                seviye=seviye,
                zaman_dilimi=zaman_dilimi
            )

            db.olcum_ekle(olcum)
            db.kapat()

            QMessageBox.information(self, "✅ Başarılı", "Ölçüm kaydedildi.")
            self.accept()

        except ValueError as ve:
            QMessageBox.warning(self, "Hatalı Giriş", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri kaydı sırasında hata oluştu:\n{e}")
