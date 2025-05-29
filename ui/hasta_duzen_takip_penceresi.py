from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from database.db_manager import DBManager
from datetime import datetime, timedelta

class PatientAdherenceWindow(QDialog):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("\U0001F4C8 Diyet ve Egzersiz Uyum Yüzdesi")
        self.setFixedSize(700, 400)
        self.hasta_id = hasta_id

        layout = QVBoxLayout()

        self.diyet_label = QLabel("\U0001F957 Diyet Uyum Oranı")
        self.diyet_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.diyet_canvas = FigureCanvas(Figure(figsize=(4, 2)))

        self.egzersiz_label = QLabel("\U0001F3C3 Egzersiz Uyum Oranı")
        self.egzersiz_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.egzersiz_canvas = FigureCanvas(Figure(figsize=(4, 2)))

        layout.addWidget(self.diyet_label)
        layout.addWidget(self.diyet_canvas)
        layout.addWidget(self.egzersiz_label)
        layout.addWidget(self.egzersiz_canvas)
        self.setLayout(layout)

        self.grafikleri_olustur()

    def grafikleri_olustur(self):
        db = DBManager(password="Hekim11322..")


        db.cursor.execute("""
            SELECT MIN(tarih) FROM assigned_recommendations
            WHERE hasta_id = %s
        """, (self.hasta_id,))
        baslangic_tarihi_result = db.cursor.fetchone()

        if not baslangic_tarihi_result or not baslangic_tarihi_result[0]:
            self._veri_yok_yazdir("Diyet öneri verisi yok", self.diyet_canvas)
            self._veri_yok_yazdir("Egzersiz öneri verisi yok", self.egzersiz_canvas)
            db.kapat()
            return

        baslangic_tarihi = baslangic_tarihi_result[0]
        bugun = datetime.today().date()
        toplam_gun = (bugun - baslangic_tarihi).days + 1


        db.cursor.execute("""
            SELECT COUNT(DISTINCT tarih) FROM patient_diets
            WHERE hasta_id = %s AND uygulandi_mi = 1
        """, (self.hasta_id,))
        uygulanan_diyet_gun = db.cursor.fetchone()[0] or 0


        db.cursor.execute("""
            SELECT COUNT(DISTINCT tarih) FROM patient_exercises
            WHERE hasta_id = %s AND yapildi_mi = 1
        """, (self.hasta_id,))
        yapilan_egz_gun = db.cursor.fetchone()[0] or 0

        db.kapat()

        uygulanmayan_diyet = max(toplam_gun - uygulanan_diyet_gun, 0)
        yapilmayan_egz = max(toplam_gun - yapilan_egz_gun, 0)


        ax1 = self.diyet_canvas.figure.subplots()
        ax1.clear()
        if toplam_gun == 0:
            ax1.text(0.5, 0.5, "Diyet öneri verisi yok", fontsize=14, ha='center')
        else:
            ax1.pie([uygulanan_diyet_gun, uygulanmayan_diyet],
                    labels=["Uygulanan", "Uygulanmayan"],
                    autopct="%1.1f%%", startangle=140,
                    colors=["#2ecc71", "#e74c3c"])
        ax1.set_title("Diyet Uyum Oranı")
        self.diyet_canvas.draw()


        ax2 = self.egzersiz_canvas.figure.subplots()
        ax2.clear()
        if toplam_gun == 0:
            ax2.text(0.5, 0.5, "Egzersiz öneri verisi yok", fontsize=14, ha='center')
        else:
            ax2.pie([yapilan_egz_gun, yapilmayan_egz],
                    labels=["Yapılan", "Yapılmayan"],
                    autopct="%1.1f%%", startangle=140,
                    colors=["#3498db", "#f39c12"])
        ax2.set_title("Egzersiz Uyum Oranı")
        self.egzersiz_canvas.draw()

    def _veri_yok_yazdir(self, mesaj, canvas):
        ax = canvas.figure.subplots()
        ax.clear()
        ax.text(0.5, 0.5, mesaj, fontsize=14, ha='center')
        canvas.draw()