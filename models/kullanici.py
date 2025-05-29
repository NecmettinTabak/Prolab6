class User:
    def __init__(self, id, tc_no, ad, soyad, email, sifre, cinsiyet, dogum_tarihi, rol, profil_resmi, doktor_id=None):
        self.id = id
        self.tc_no = tc_no
        self.ad = ad
        self.soyad = soyad
        self.email = email
        self.sifre = sifre
        self.cinsiyet = cinsiyet
        self.dogum_tarihi = dogum_tarihi
        self.rol = rol
        self.profil_resmi = profil_resmi
        self.doktor_id = doktor_id