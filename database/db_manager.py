import pymysql
from models.user import User
from models.measurement import Measurement
from models.patient_symptom import PatientSymptom
from models.exercise_type import ExerciseType
from models.patient_exercise import PatientExercise
from models.diet_type import DietType
from models.patient_diet import PatientDiet
from models.patient_note import PatientNote
from models.alert import Alert

class DBManager:
    def __init__(self, host="localhost", user="root", password="", database="diyabet_takip"):
        try:
            self.conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset="utf8mb4"
            )
            self.cursor = self.conn.cursor()
            print("📱 PyMySQL bağlantısı başarılı!")
            self.__tablolari_kontrol_et_ve_olustur()
        except Exception as err:
            print(f"❌ Veritabanı bağlantı hatası: {err}")

    def __tablolari_kontrol_et_ve_olustur(self):
        tablolar = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tc_no VARCHAR(11) UNIQUE NOT NULL,
                    ad VARCHAR(50),
                    soyad VARCHAR(50),
                    email VARCHAR(100),
                    sifre VARCHAR(100),
                    cinsiyet VARCHAR(10),
                    dogum_tarihi DATE,
                    rol VARCHAR(20),
                    profil_resmi TEXT,
                    doktor_id INT,
                    FOREIGN KEY (doktor_id) REFERENCES users(id) ON DELETE SET NULL
                );
            """,
            "measurements": """
                CREATE TABLE IF NOT EXISTS measurements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hasta_id INT NOT NULL,
                    tarih DATE NOT NULL,
                    saat TIME NOT NULL,
                    zaman_dilimi ENUM('sabah', 'ogle', 'ikindi', 'aksam', 'gece') NOT NULL,
                    seviye INT NOT NULL,
                    UNIQUE(hasta_id, tarih, zaman_dilimi),
                    FOREIGN KEY (hasta_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """,

            "recommendation_rules": """
                CREATE TABLE IF NOT EXISTS recommendation_rules (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    min_seker INT NOT NULL,
                    max_seker INT NOT NULL,
                    belirtiler TEXT NOT NULL,
                    diyet_id INT,
                    egzersiz_id INT,
                    FOREIGN KEY (diyet_id) REFERENCES diet_types(id) ON DELETE SET NULL,
                    FOREIGN KEY (egzersiz_id) REFERENCES exercise_types(id) ON DELETE SET NULL
                );
            """,
            "symptoms": """
                CREATE TABLE IF NOT EXISTS symptoms (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad VARCHAR(100) UNIQUE
                );
            """,
            "patient_symptoms": """
                CREATE TABLE IF NOT EXISTS patient_symptoms (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hasta_id INT NOT NULL,
                    symptom_id INT NOT NULL,
                    tarih DATE NOT NULL,
                    FOREIGN KEY (hasta_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (symptom_id) REFERENCES symptoms(id) ON DELETE CASCADE
                );
            """,
            "exercise_types": """
                CREATE TABLE IF NOT EXISTS exercise_types (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad VARCHAR(100) UNIQUE
                );
            """,
            "patient_exercises": """
                CREATE TABLE IF NOT EXISTS patient_exercises (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hasta_id INT NOT NULL,
                    egzersiz_id INT NOT NULL,
                    tarih DATE NOT NULL,
                    yapildi_mi BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (hasta_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (egzersiz_id) REFERENCES exercise_types(id) ON DELETE CASCADE
                );
            """,
            "diet_types": """
                CREATE TABLE IF NOT EXISTS diet_types (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad VARCHAR(100) UNIQUE
                );
            """,
            "patient_diets": """
                CREATE TABLE IF NOT EXISTS patient_diets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hasta_id INT NOT NULL,
                    diet_id INT NOT NULL,
                    tarih DATE NOT NULL,
                    uygulandi_mi BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (hasta_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (diet_id) REFERENCES diet_types(id) ON DELETE CASCADE
                );
            """,
            "patient_notes": """
                CREATE TABLE IF NOT EXISTS patient_notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hasta_id INT NOT NULL,
                    doktor_id INT NOT NULL,
                    not_metni TEXT,
                    tarih DATE NOT NULL,
                    FOREIGN KEY (hasta_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (doktor_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """,
            "alerts": """
                CREATE TABLE IF NOT EXISTS alerts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hasta_id INT NOT NULL,
                    tarih DATETIME NOT NULL,
                    uyari_tipi VARCHAR(50),
                    mesaj TEXT NOT NULL,
                    FOREIGN KEY (hasta_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """,
            "insulin_dose_recommendations": """
                CREATE TABLE IF NOT EXISTS insulin_dose_recommendations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    min_value INT NOT NULL,
                    max_value INT NOT NULL,
                    dose VARCHAR(10) NOT NULL
                );
            """
        }





        for ad, sorgu in tablolar.items():
            try:
                self.cursor.execute(sorgu)
                self.conn.commit()
                print(f"✅ Tablo kontrol edildi: {ad}")
            except Exception as e:
                print(f"❌ Tablo oluşturulamadı ({ad}): {e}")
    def kapat(self):
        self.cursor.close()
        self.conn.close()
        print("🔌 Bağlantı kapatıldı.")

    def kullanici_ekle(self, user: User):
        try:
            query = """
                INSERT INTO users (tc_no, ad, soyad, email, sifre, cinsiyet, dogum_tarihi, rol, profil_resmi, doktor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (
                user.tc_no, user.ad, user.soyad, user.email,
                user.sifre, user.cinsiyet, user.dogum_tarihi,
                user.rol, user.profil_resmi, user.doktor_id  # <-- doktor_id eklendi
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"✅ Kullanıcı eklendi: {user.tc_no}")
        except Exception as e:
            print(f"❌ Kullanıcı eklenemedi: {e}")

    def kullanici_getir(self, tc_no, sifre):
        try:
            query = "SELECT * FROM users WHERE tc_no = %s AND sifre = %s;"
            self.cursor.execute(query, (tc_no, sifre))
            result = self.cursor.fetchone()
            if result:
                return User(
                    id=result[0], tc_no=result[1], ad=result[2], soyad=result[3],
                    email=result[4], sifre=result[5], cinsiyet=result[6],
                    dogum_tarihi=result[7], rol=result[8], profil_resmi=result[9]
                )
            else:
                return None
        except Exception as e:
            print("❌ Giriş sorgusu hatası:", e)
            return None

    def olcum_ekle(self, measurement):
        sql = """
            INSERT INTO measurements (hasta_id, tarih, saat, zaman_dilimi, seviye)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            measurement.hasta_id,
            measurement.tarih,
            measurement.saat,
            measurement.zaman_dilimi,
            measurement.seviye
        ))
        self.conn.commit()

    def zaten_var_mi(self, hasta_id, tarih, zaman_dilimi):
        self.cursor.execute("""
            SELECT COUNT(*) FROM measurements
            WHERE hasta_id = %s AND tarih = %s AND zaman_dilimi = %s
        """, (hasta_id, tarih, zaman_dilimi))
        return self.cursor.fetchone()[0] > 0

    def semptom_tanimla(self, ad):
        try:
            self.cursor.execute("INSERT INTO symptoms (ad) VALUES (%s)", (ad,))
            self.conn.commit()
            print(f"✅ Semptom eklendi: {ad}")
        except Exception as e:
            print(f"❌ Semptom eklenemedi: {e}")

    def hasta_semptom_ekle(self, kayit: PatientSymptom):
        try:
            query = """
                INSERT INTO patient_symptoms (hasta_id, symptom_id, tarih)
                VALUES (%s, %s, %s);
            """
            values = (kayit.hasta_id, kayit.symptom_id, kayit.tarih)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("✅ Hasta semptom kaydı başarıyla eklendi.")
        except Exception as e:
            print("❌ Semptom kaydı eklenemedi:", e)

    def egzersiz_turu_ekle(self, egzersiz: ExerciseType):
        try:
            query = "INSERT INTO exercise_types (ad) VALUES (%s);"
            self.cursor.execute(query, (egzersiz.ad,))
            self.conn.commit()
            print(f"✅ Egzersiz türü eklendi: {egzersiz.ad}")
        except Exception as e:
            print(f"❌ Egzersiz türü eklenemedi: {e}")

    def hasta_egzersiz_ekle(self, kayit: PatientExercise):
        try:
            query = """
                INSERT INTO patient_exercises (hasta_id, egzersiz_id, tarih, yapildi_mi)
                VALUES (%s, %s, %s, %s);
            """
            values = (kayit.hasta_id, kayit.egzersiz_id, kayit.tarih, kayit.yapildi_mi)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("✅ Egzersiz kaydı eklendi.")
        except Exception as e:
            print("❌ Egzersiz eklenemedi:", e)

    def diyet_turu_ekle(self, diyet: DietType):
        try:
            query = "INSERT INTO diet_types (ad) VALUES (%s);"
            self.cursor.execute(query, (diyet.ad,))
            self.conn.commit()
            print(f"✅ Diyet türü eklendi: {diyet.ad}")
        except Exception as e:
            print(f"❌ Diyet türü eklenemedi: {e}")

    def hasta_diyet_ekle(self, kayit: PatientDiet):
        try:
            query = """
                INSERT INTO patient_diets (hasta_id, diet_id, tarih, uygulandi_mi)
                VALUES (%s, %s, %s, %s);
            """
            values = (kayit.hasta_id, kayit.diet_id, kayit.tarih, kayit.uygulandi_mi)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("✅ Hasta diyet kaydı eklendi.")
        except Exception as e:
            print("❌ Diyet kaydı eklenemedi:", e)

    def hasta_notu_ekle(self, note: PatientNote):
        try:
            query = """
                INSERT INTO patient_notes (hasta_id, doktor_id, not_metni, tarih)
                VALUES (%s, %s, %s, %s);
            """
            values = (note.hasta_id, note.doktor_id, note.not_metni, note.tarih)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("✅ Hasta notu eklendi.")
        except Exception as e:
            print("❌ Not eklenemedi:", e)

    def hasta_notlarini_getir(self, hasta_id):
        try:
            query = "SELECT * FROM patient_notes WHERE hasta_id = %s ORDER BY tarih DESC"
            self.cursor.execute(query, (hasta_id,))
            results = self.cursor.fetchall()
            return [PatientNote(*row) for row in results]
        except Exception as e:
            print("❌ Notlar alınamadı:", e)
            return []

    def uyarı_ekle(self, alert: Alert):
        try:
            query = """
                INSERT INTO alerts (hasta_id, tarih, uyarı_tipi, mesaj)
                VALUES (%s, %s, %s, %s);
            """
            values = (alert.hasta_id, alert.tarih, alert.uyarı_tipi, alert.mesaj)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("✅ Uyarı başarıyla eklendi.")
        except Exception as e:
            print("❌ Uyarı eklenemedi:", e)

    def hastaya_ait_uyarilar(self, hasta_id):
        try:
            query = "SELECT * FROM alerts WHERE hasta_id = %s ORDER BY tarih DESC;"
            self.cursor.execute(query, (hasta_id,))
            results = self.cursor.fetchall()
            return [Alert(*row) for row in results]
        except Exception as e:
            print("❌ Uyarılar getirilemedi:", e)
            return []

    def doktorun_hastalarini_getir(self, doktor_id):
        try:
            query = """
                SELECT * FROM users
                WHERE rol = 'hasta' AND doktor_id = %s
                ORDER BY ad ASC;
            """
            self.cursor.execute(query, (doktor_id,))
            results = self.cursor.fetchall()
            return [User(
                id=row[0], tc_no=row[1], ad=row[2], soyad=row[3],
                email=row[4], sifre=row[5], cinsiyet=row[6],
                dogum_tarihi=row[7], rol=row[8], profil_resmi=row[9],
                doktor_id=row[10]
            ) for row in results]
        except Exception as e:
            print(f"❌ Hastalar getirilemedi: {e}")
            return []
