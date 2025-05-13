class Measurement:
    def __init__(self, hasta_id, tarih, saat, seviye):
        self.hasta_id = hasta_id
        self.tarih = tarih      # "YYYY-MM-DD"
        self.saat = saat        # "HH:MM:SS"
        self.seviye = seviye    # int (mg/dL)

    def __repr__(self):
        return f"<Measurement hasta_id={self.hasta_id}, seviye={self.seviye}, tarih={self.tarih}, saat={self.saat}>"
