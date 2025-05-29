from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from database.db_manager import DBManager
import matplotlib.dates as mdates
from datetime import datetime

class PatientGlucoseTrendWindow(QDialog):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("📈 Kan Şekeri Zaman Grafiği")
        self.setMinimumSize(800, 500)
        self.hasta_id = hasta_id

        layout = QVBoxLayout()
        self.label = QLabel("📊 Günlük Kan Şekeri Değişimi ve Diyet/Egzersiz Etkisi")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.canvas = FigureCanvas(Figure(figsize=(7, 4)))
        layout.addWidget(self.label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.verileri_yukle()

    def verileri_yukle(self):
        db = DBManager(password="Hekim11322..")


        db.cursor.execute("""
            SELECT tarih, AVG(seviye) FROM measurements
            WHERE hasta_id = %s
            GROUP BY tarih
            ORDER BY tarih ASC
        """, (self.hasta_id,))
        glukoz_kayitlari = db.cursor.fetchall()


        db.cursor.execute("""
            SELECT DISTINCT tarih FROM patient_diets
            WHERE hasta_id = %s AND uygulandi_mi = 1
        """, (self.hasta_id,))
        diyet_tarihleri = set([row[0] for row in db.cursor.fetchall()])


        db.cursor.execute("""
            SELECT DISTINCT tarih FROM patient_exercises
            WHERE hasta_id = %s AND yapildi_mi = 1
        """, (self.hasta_id,))
        egzersiz_tarihleri = set([row[0] for row in db.cursor.fetchall()])

        db.kapat()

        if not glukoz_kayitlari:
            ax = self.canvas.figure.subplots()
            ax.text(0.5, 0.5, "Yeterli veri yok", fontsize=14, ha='center')
            self.canvas.draw()
            return


        tarih_listesi = [datetime.strptime(str(t), "%Y-%m-%d") for t, _ in glukoz_kayitlari]
        seviye_listesi = [s for _, s in glukoz_kayitlari]

        ax = self.canvas.figure.subplots()
        ax.clear()
        ax.plot(tarih_listesi, seviye_listesi, marker='o', label='Kan Şekeri')

        for i, tarih in enumerate(tarih_listesi):
            date_only = tarih.date()
            diyet = date_only in diyet_tarihleri
            egzersiz = date_only in egzersiz_tarihleri

            if diyet and egzersiz:
                ax.plot(tarih, seviye_listesi[i], marker='*', markersize=10, color='green',
                        label='Diyet + Egzersiz + Ölçüm' if i == 0 else "")
            elif diyet and not egzersiz:
                ax.plot(tarih, seviye_listesi[i], marker='P', markersize=10, color='deeppink',
                        label='Diyet + Ölçüm' if i == 0 else "")
            elif egzersiz and not diyet:
                ax.plot(tarih, seviye_listesi[i], marker='X', markersize=10, color='dodgerblue',
                        label='Egzersiz + Ölçüm' if i == 0 else "")
            else:
                ax.plot(tarih, seviye_listesi[i], marker='o', markersize=8, color='black',
                        label='Sadece Ölçüm' if i == 0 else "")

        ax.set_title("Kan Şekeri Değişimi")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("mg/dL")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
        ax.legend()
        self.canvas.draw()