from PyQt5.QtWidgets import QApplication
import sys
from database.db_manager import DBManager
from models.user import User
from ui.login_window import LoginWindow
import pymysql

def doktor_ekle():
    db = DBManager(password="Necmettin2004")

    kullanici = User(
        id=None,
        tc_no="11345678111",
        ad="Ali",
        soyad="Yılmaz",
        email="ali@example.com",
        sifre="123458",
        cinsiyet="Erkek",
        dogum_tarihi="1995-06-15",
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
            password="Necmettin2004",
            database="diyabet_takip",
            charset="utf8mb4"
        )
        cursor = conn.cursor()

        # Diyet türleri
        diyetler = [("Az Şekerli Diyet",), ("Şekersiz Diyet",), ("Dengeli Beslenme",)]
        cursor.executemany("INSERT IGNORE INTO diet_types (ad) VALUES (%s)", diyetler)

        # Egzersiz türleri
        egzersizler = [("Yürüyüş",), ("Koşu",), ("Klinik",)]
        cursor.executemany("INSERT IGNORE INTO exercise_types (ad) VALUES (%s)", egzersizler)

        conn.commit()
        print("📌 Diyet ve egzersiz türleri eklendi.")
    except Exception as e:
        print(f"❌ Diyet/egzersiz eklenemedi: {e}")
    finally:
        cursor.close()
        conn.close()

def recommendation_rules_ekle():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Necmettin2004",
            database="diyabet_takip",
            charset="utf8mb4"
        )
        cursor = conn.cursor()

        # Öneri kuralları — ID'ler doğru sıralanmalı
        rules = [
            (70, 110, "Poliüri,Yorgunluk", 1, 1),
            (111, 180, "Yorgunluk,Nöropati,Bulanık görme", 2, 3),
            (181, 1000, "Yaraların yavaş iyileşmesi,Kilo kaybı", 2, 1),
            (0, 69, "Nöropati,Polidipsi,Yorgunluk", 3, None),
        ]

        cursor.executemany("""
        INSERT IGNORE INTO recommendation_rules (min_seker, max_seker, belirtiler, diyet_id, egzersiz_id)
        VALUES (%s, %s, %s, %s, %s)
        """, rules)

        conn.commit()
        print("📌 Öneri kuralları başarıyla eklendi.")
    except Exception as e:
        print(f"❌ Veri ekleme hatası: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    doktor_ekle()
    diet_ve_egzersiz_ekle()
    recommendation_rules_ekle()

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
