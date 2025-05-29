class PatientSymptom:
    def __init__(self, hasta_id, symptom_id, tarih):
        self.hasta_id = hasta_id
        self.symptom_id = symptom_id
        self.tarih = tarih

    def __repr__(self):
        return f"<PatientSymptom hasta_id={self.hasta_id}, symptom_id={self.symptom_id}, tarih={self.tarih}>"
