class PatientExercise:
    def __init__(self, hasta_id, egzersiz_id, tarih, yapildi_mi=False):
        self.hasta_id = hasta_id
        self.egzersiz_id = egzersiz_id
        self.tarih = tarih
        self.yapildi_mi = yapildi_mi

    def __repr__(self):
        return f"<PatientExercise hasta_id={self.hasta_id}, egzersiz_id={self.egzersiz_id}, tarih={self.tarih}, yapildi_mi={self.yapildi_mi}>"
