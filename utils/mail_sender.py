import smtplib
from email.message import EmailMessage
import time
import os

def send_bulk_emails(recipients: list, subject: str, body_template: str, smtp_settings: dict):
    """
    SMTP sunucusu üzerinden arka planda mail gönderimi yapar.
    Ayarları UI üzerinden gelen smtp_settings dict'inden alır.
    """
    total = len(recipients)
    print(f"[{time.strftime('%X')}] Toplam {total} adet mail gönderimi başlatılıyor...")
    
    SMTP_SERVER = smtp_settings.get("server")
    SMTP_PORT = int(smtp_settings.get("port", 465))
    SMTP_USER = smtp_settings.get("user")
    SMTP_PASSWORD = smtp_settings.get("password")
    
    try:
        # SSL ile bağlanıyoruz. Eğer 587 portu (TLS) kullanacaksanız smtplib.SMTP kullanıp server.starttls() yapmalısınız.
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            
        # SMTP sunucusuna giriş yapalım
        server.login(SMTP_USER, SMTP_PASSWORD)

        for i, recipient in enumerate(recipients, 1):
            to_email = recipient.get('Mail_Adresi')
            if not to_email:
                continue

            # {{Degiskenler}}'i gerçek verilerle değiştir
            mail_body = body_template
            for key, value in recipient.items():
                mail_body = mail_body.replace(f"{{{{{key}}}}}", str(value))
                
            # E-posta objesini oluştur
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = SMTP_USER
            msg['To'] = to_email
            
            # İçeriği ayarla (Düz metin. İsterseniz set_content(..., subtype='html') yapabilirsiniz)
            msg.set_content(mail_body)

            # Maili gönder
            server.send_message(msg)
            print(f"[{time.strftime('%X')}] {i}/{total} Gönderildi -> {to_email}")
            
            # Sunucuyu spama düşürmemek için her gönderimde 1 saniye bekletmek iyidir
            time.sleep(1)

        # İşlem bitince sunucu bağlantısını kapat
        server.quit()
        print("✅ Toplu mail gönderimi başarıyla tamamlandı.")
        
    except Exception as e:
        print(f"❌ Mail gönderimi sırasında hata oluştu: {e}")
