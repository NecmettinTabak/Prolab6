from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel, QPushButton, QMessageBox, QGroupBox, QCheckBox, \
    QFormLayout, QLineEdit, QHBoxLayout
from database.db_manager import DBManager
from ui.hasta_detay_penceresi import PatientDetailWindow
from ui.ilk_giris_ekrani import FirstEntryWindow


class PatientListWindow(QDialog):
    def __init__(self, doktor_id):
        super().__init__()
        self.setWindowTitle("Hastalarım")
        self.setGeometry(150, 150, 400, 300)
        self.doktor_id = doktor_id

        layout = QVBoxLayout()

        self.label = QLabel("👥 Kayıtlı Hastalar:")
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)


        self.seker_min_input = QLineEdit()
        self.seker_min_input.setPlaceholderText("Min Şeker")
        self.seker_max_input = QLineEdit()
        self.seker_max_input.setPlaceholderText("Max Şeker")

        seker_layout = QHBoxLayout()
        seker_layout.addWidget(self.seker_min_input)
        seker_layout.addWidget(self.seker_max_input)

        seker_group = QGroupBox("Kan Şekeri Aralığı")
        seker_group.setLayout(seker_layout)
        layout.addWidget(seker_group)


        self.semptomlar = ["Baş ağrısı", "Bulanık görme", "Yorgunluk", "Kilo Kaybı", "Polifaji", "Polidipsi","Nöropati", "Poliüri",
                           "Yaraların Yavaş İyileşmesi"]
        self.semptom_checkboxes = []

        semptom_form = QFormLayout()
        for belirti in self.semptomlar:
            cb = QCheckBox(belirti)
            self.semptom_checkboxes.append(cb)
            semptom_form.addRow(cb)

        semptom_group = QGroupBox("Belirtiler")
        semptom_group.setLayout(semptom_form)
        layout.addWidget(semptom_group)


        self.filter_button = QPushButton("🔍 Filtrele")
        self.filter_button.clicked.connect(self.hastalari_filtrele)
        layout.addWidget(self.filter_button)


        self.btn_detay = QPushButton("📋 Seçili Hastayı Görüntüle")
        self.btn_detay.clicked.connect(self.detay_goster)
        layout.addWidget(self.btn_detay)


        self.btn_ilk_veri = QPushButton("📅 Kan Şekeri ve Belirti Gir")
        self.btn_ilk_veri.clicked.connect(self.ilk_veri_gir)
        layout.addWidget(self.btn_ilk_veri)

        self.setLayout(layout)

        self.db = DBManager(password="Hekim11322..")
        self.hastalar = self.db.doktorun_hastalarini_getir(doktor_id)

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

    def hastalari_filtrele(self):
        min_seker = self.seker_min_input.text().strip()
        max_seker = self.seker_max_input.text().strip()
        secilen_belirtiler = [cb.text() for cb in self.semptom_checkboxes if cb.isChecked()]

        self.db = DBManager(password="Hekim11322..")
        self.hastalar = self.db.filtreli_hasta_getir(self.doktor_id, min_seker, max_seker, secilen_belirtiler)
        self.db.kapat()

        self.list_widget.clear()
        for h in self.hastalar:
            self.list_widget.addItem(f"{h.ad} {h.soyad} - TC: {h.tc_no}")

    def ilk_veri_gir(self):
        secilen_index = self.list_widget.currentRow()
        if secilen_index == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçin.")
            return

        hasta = self.hastalar[secilen_index]
        pencere = FirstEntryWindow(hasta)
        pencere.exec_()
