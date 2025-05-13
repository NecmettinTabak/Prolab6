class PatientSymptom:
    def __init__(self, hasta_id, symptom_id, tarih):
        self.hasta_id = hasta_id        # users tablosundaki hasta id'si
        self.symptom_id = symptom_id    # symptoms tablosundaki semptom id'si
        self.tarih = tarih              # "YYYY-MM-DD" formatında tarih

    def __repr__(self):
        return f"<PatientSymptom hasta_id={self.hasta_id}, symptom_id={self.symptom_id}, tarih={self.tarih}>"
