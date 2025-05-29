from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
from database.db_manager import DBManager

class GraphWindow(QDialog):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("Günlük Kan Şekeri Grafiği")
        self.setMinimumSize(850, 500)

        self.hasta_id = hasta_id

        layout = QVBoxLayout(self)

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        self.show_button = QPushButton("Grafiği Göster")
        self.show_button.clicked.connect(self.grafik_ciz)
        layout.addWidget(self.show_button)

        self.canvas = FigureCanvas(Figure(figsize=(8, 5)))
        layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()
        self.grafik_ciz()

    def grafik_ciz(self):
        try:
            tarih = self.date_edit.date().toPyDate().strftime("%Y-%m-%d")
            db = DBManager(password="Hekim11322..")
            db.cursor.execute("""
                SELECT zaman_dilimi, seviye FROM measurements
                WHERE hasta_id = %s AND tarih = %s
            """, (self.hasta_id, tarih))
            veriler = db.cursor.fetchall()
            db.kapat()

            self.ax.clear()

            if not veriler:
                self.ax.text(0.5, 0.5, "Seçilen tarih için ölçüm verisi yok.", ha='center', va='center', fontsize=14)
                self.canvas.draw()
                return

            dilimler = ['sabah', 'ogle', 'ikindi', 'aksam', 'gece']
            seviye_dict = {d: None for d in dilimler}

            for zaman_dilimi, seviye in veriler:
                if zaman_dilimi in seviye_dict:
                    seviye_dict[zaman_dilimi] = seviye

            x = [d.capitalize() for d in dilimler]
            y = [seviye_dict[d] if seviye_dict[d] is not None else 0 for d in dilimler]

            renkler = []
            for val in y:
                if val == 0:
                    renkler.append("gray")
                elif val < 70:
                    renkler.append("blue")
                elif val <= 110:
                    renkler.append("green")
                elif val <= 150:
                    renkler.append("orange")
                elif val <= 200:
                    renkler.append("red")
                else:
                    renkler.append("darkred")

            self.ax.bar(x, y, color=renkler)
            self.ax.set_title(f"Kan Şekeri Değerleri ({tarih})")
            self.ax.set_ylabel("mg/dL")
            self.ax.set_xlabel("Zaman Dilimi")
            self.ax.set_ylim(0, 300)
            self.ax.grid(axis='y', linestyle='--', alpha=0.7)

            for i, val in enumerate(y):
                if val != 0:
                    self.ax.text(i, val + 5, f"{val}", ha='center')

            legend_labels = [
                "< 70 mg/dL (Hipoglisemi)",
                "70-110 mg/dL (Normal)",
                "111-150 mg/dL (Orta)",
                "151-200 mg/dL (Yüksek)",
                "> 200 mg/dL (Çok Yüksek)",
                "0 (Eksik)"
            ]
            legend_colors = ["blue", "green", "orange", "red", "darkred", "gray"]
            handles = [self.ax.bar(0, 0, color=color)[0] for color in legend_colors]
            self.ax.legend(handles, legend_labels, loc='upper left')

            self.canvas.draw()

        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Grafik gösterilemedi: {e}", ha='center', va='center', fontsize=12)
            self.canvas.draw()
