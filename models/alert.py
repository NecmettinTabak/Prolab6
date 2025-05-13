class Alert:
    def __init__(self, id, hasta_id, tarih, uyarı_tipi, mesaj):
        self.id = id
        self.hasta_id = hasta_id
        self.tarih = tarih
        self.uyarı_tipi = uyarı_tipi
        self.mesaj = mesaj

    def __repr__(self):
        return f"Alert({self.id}, {self.hasta_id}, {self.tarih}, {self.uyarı_tipi}, {self.mesaj})"
