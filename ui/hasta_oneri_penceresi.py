from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QDateEdit
from PyQt5.QtCore import QDate
from database.db_manager import DBManager

class PatientRecommendationWindow(QDialog):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("🧠 Atanmış Öneriler")
        self.setFixedSize(420, 320)
        self.hasta_id = hasta_id

        layout = QVBoxLayout()
        self.bilgi_label = QLabel("✅ Doktorunuz tarafından size atanmış öneriler:")

        self.tarih_secici = QDateEdit()
        self.tarih_secici.setCalendarPopup(True)
        self.tarih_secici.setDate(QDate.currentDate())
        self.tarih_secici.dateChanged.connect(self.yukle_oneriler)

        self.list_widget = QListWidget()

        layout.addWidget(self.bilgi_label)
        layout.addWidget(QLabel("📅 Tarih Seç:"))
        layout.addWidget(self.tarih_secici)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        self.db = DBManager(password="Hekim11322..")
        self.yukle_oneriler()
        self.db.kapat()

    def yukle_oneriler(self):
        self.list_widget.clear()
        secilen_tarih = self.tarih_secici.date().toString("yyyy-MM-dd")

        try:
            db = DBManager(password="Hekim11322..")
            query = """
                SELECT r.belirtiler, d.ad, e.ad, a.tarih
                FROM assigned_recommendations a
                JOIN recommendation_rules r ON a.rule_id = r.id
                LEFT JOIN diet_types d ON r.diyet_id = d.id
                LEFT JOIN exercise_types e ON r.egzersiz_id = e.id
                WHERE a.hasta_id = %s AND a.tarih = %s
                ORDER BY a.tarih DESC
            """
            db.cursor.execute(query, (self.hasta_id, secilen_tarih))
            veriler = db.cursor.fetchall()
            db.kapat()

            if not veriler:
                self.list_widget.addItem("⛔ Bu tarihte atanmış bir öneri bulunamadı.")
            else:
                for belirtiler, diyet, egzersiz, tarih in veriler:
                    self.list_widget.addItem(
                        f"📅 {tarih} - Diyet: {diyet or 'Yok'} | Egzersiz: {egzersiz or 'Yok'}\n📍 Belirtiler: {belirtiler}"
                    )

        except Exception as e:
            self.list_widget.addItem(f"⚠️ Hata: {e}")

