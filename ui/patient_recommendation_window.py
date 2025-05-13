from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget
from database.db_manager import DBManager

class PatientRecommendationWindow(QDialog):
    def __init__(self, hasta_id):
        super().__init__()
        self.setWindowTitle("🧠 Atanmış Öneriler")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.bilgi_label = QLabel("✅ Doktorunuz tarafından size atanmış öneriler:")
        self.list_widget = QListWidget()

        layout.addWidget(self.bilgi_label)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        self.db = DBManager(password="Necmettin2004")
        self.yukle_oneriler(hasta_id)
        self.db.kapat()

    def yukle_oneriler(self, hasta_id):
        try:
            query = """
                SELECT r.belirtiler, d.ad, e.ad, a.tarih
                FROM assigned_recommendations a
                JOIN recommendation_rules r ON a.rule_id = r.id
                LEFT JOIN diet_types d ON r.diyet_id = d.id
                LEFT JOIN exercise_types e ON r.egzersiz_id = e.id
                WHERE a.hasta_id = %s
                ORDER BY a.tarih DESC
            """
            self.db.cursor.execute(query, (hasta_id,))
            veriler = self.db.cursor.fetchall()

            if not veriler:
                self.list_widget.addItem("⛔ Henüz size özel bir öneri atanmadı.")
            else:
                for belirtiler, diyet, egzersiz, tarih in veriler:
                    self.list_widget.addItem(f"📅 {tarih} - Diyet: {diyet or 'Yok'} | Egzersiz: {egzersiz or 'Yok'}\n📍 Belirtiler: {belirtiler}")

        except Exception as e:
            self.list_widget.addItem(f"⚠️ Hata: {e}")
