class Alert:
    def __init__(self, hasta_id, tarih, uyarı_tipi, mesaj, id=None):
        self.id = id
        self.hasta_id = hasta_id
        self.tarih = tarih
        self.uyarı_tipi = uyarı_tipi
        self.mesaj = mesaj

    def __repr__(self):
        return f"Alert(id={self.id}, hasta_id={self.hasta_id}, tarih={self.tarih}, uyarı_tipi='{self.uyarı_tipi}', mesaj='{self.mesaj}')"
