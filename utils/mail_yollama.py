import smtplib
from email.mime.text import MIMEText

def hasta_mail_gonder(ad, email, tc_no, sifre):
    try:
        sender_email = ("tabaknecmettin@gmail.com")
        app_password = "gwhroovbzhfawknc"

        subject = "Diyabet Takip Sistemi - Giriş Bilgileriniz"
        body = f"""
Merhaba {ad},

Diyabet Takip Sistemi'ne giriş bilgileriniz:

T.C. Kimlik No: {tc_no}
Şifre: {sifre}

Sisteme giriş için uygulamayı açabilirsiniz.
Sağlıklı günler dileriz.
        """

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, email, message.as_string())

        print("📩 E-posta başarıyla gönderildi!")

    except Exception as e:
        print("❌ E-posta gönderim hatası:", e)
