from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel, QPushButton, QMessageBox
from database.db_manager import DBManager
from ui.patient_detail_window import PatientDetailWindow  # ↓ oluşturacağız

class PatientListWindow(QDialog):
    def __init__(self, doktor_id):
        super().__init__()
        self.setWindowTitle("Hastalarım")
        self.setGeometry(150, 150, 400, 300)
        self.doktor_id = doktor_id

        layout = QVBoxLayout()
        self.label = QLabel("👥 Kayıtlı Hastalar:")
        self.list_widget = QListWidget()
        self.btn_detay = QPushButton("📋 Seçili Hastayı Görüntüle")
        self.btn_detay.clicked.connect(self.detay_goster)

        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.btn_detay)
        self.setLayout(layout)

        self.db = DBManager(password="Necmettin2004")
        self.hastalar = self.db.doktorun_hastalarini_getir(doktor_id)  # Liste halinde saklıyoruz

        for h in self.hastalar:
            self.list_widget.addItem(f"{h.ad} {h.soyad} - TC: {h.tc_no}")

        self.db.kapat()

    def detay_goster(self):
        secilen_index = self.list_widget.currentRow()
        if secilen_index == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçin.")
            return

        hasta = self.hastalar[secilen_index]
        self.detay_pencere = PatientDetailWindow(hasta)
        self.detay_pencere.exec_()
