class PatientDiet:
    def __init__(self, hasta_id, diet_id, tarih, uygulandi_mi=False):
        self.hasta_id = hasta_id
        self.diet_id = diet_id
        self.tarih = tarih
        self.uygulandi_mi = uygulandi_mi

    def __repr__(self):
        return f"<PatientDiet hasta_id={self.hasta_id}, diet_id={self.diet_id}, tarih={self.tarih}, uygulandi_mi={self.uygulandi_mi}>"
