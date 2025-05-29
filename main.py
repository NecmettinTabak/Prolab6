from PyQt5.QtWidgets import QApplication
import sys
from database.db_manager import DBManager
from models.kullanici import User
import pymysql
from ui.kayit_ol_penceresi import LoginWindow


def doktor_ekle():
    db = DBManager(password="Hekim11322..")
    kullanici = User(
        id=None,
        tc_no="88888888888",
        ad="Ferhat",
        soyad="Göçer",
        email="caresizAsk@example.com",
        sifre="111111",
        cinsiyet="Erkek",
        dogum_tarihi="1992-08-01",
        rol="doktor",
        profil_resmi=None,
        doktor_id=None
    )
    db.kullanici_ekle(kullanici)
    db.kapat()

def diet_ve_egzersiz_ekle():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Hekim11322..",
            database="diyabet_takip",
            charset="utf8mb4"
        )
        cursor = conn.cursor()
        diyetler = [("Az Şekerli Diyet",), ("Şekersiz Diyet",), ("Dengeli Beslenme",)]
        egzersizler = [("Yürüyüş",), ("Koşu",), ("Klinik",)]

        cursor.executemany("INSERT IGNORE INTO diet_types (ad) VALUES (%s)", diyetler)
        cursor.executemany("INSERT IGNORE INTO exercise_types (ad) VALUES (%s)", egzersizler)

        conn.commit()
        print("📌 Diyet ve egzersiz türleri eklendi.")
    except Exception as e:
        print(f"❌ Diyet/egzersiz eklenemedi: {e}")
    finally:
        cursor.close()
        conn.close()




if __name__ == "__main__":
    doktor_ekle()


    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
