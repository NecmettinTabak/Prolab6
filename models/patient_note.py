class PatientNote:
    def __init__(self, id, hasta_id, doktor_id, not_metni, tarih):
        self.id = id
        self.hasta_id = hasta_id
        self.doktor_id = doktor_id
        self.not_metni = not_metni
        self.tarih = tarih

    def __repr__(self):
        return f"<Not: Doktor {self.doktor_id} → Hasta {self.hasta_id} | {self.tarih}>"
