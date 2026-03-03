import smtplib
from email.message import EmailMessage
import time
import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def send_bulk_emails(recipients: list, subject: str, body_template: str, smtp_settings: dict = None, google_token: str = None):
    """
    SMTP veya Gmail API (Google OAuth) üzerinden arka planda mail gönderimi yapar.
    """
    total = len(recipients)
    print(f"[{time.strftime('%X')}] Toplam {total} adet mail gönderimi başlatılıyor...")
    
    server = None
    service = None
    SMTP_USER = None
    
    try:
        if google_token:
            creds = Credentials(token=google_token)
            service = build('gmail', 'v1', credentials=creds)
            print("Google (Gmail) API bağlantısı kuruldu.")
        elif smtp_settings:
            SMTP_SERVER = smtp_settings.get("server")
            SMTP_PORT = int(smtp_settings.get("port", 465))
            SMTP_USER = smtp_settings.get("user")
            SMTP_PASSWORD = smtp_settings.get("password")
            
            # SSL ile bağlanıyoruz.
            if SMTP_PORT == 465:
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            else:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                
            server.login(SMTP_USER, SMTP_PASSWORD)
            print("SMTP bağlantısı kuruldu.")
        else:
            print("Hata: Ne Google hesabı API Izni ne de SMTP ayarı bulundu.")
            return

        for i, recipient in enumerate(recipients, 1):
            to_email = recipient.get('Mail_Adresi')
            if not to_email:
                continue

            mail_body = body_template
            for key, value in recipient.items():
                mail_body = mail_body.replace(f"{{{{{key}}}}}", str(value))
                
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['To'] = to_email
            if not google_token:
                msg['From'] = SMTP_USER
            
            msg.set_content(mail_body)

            if google_token:
                raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
                service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            else:
                server.send_message(msg)
                
            print(f"[{time.strftime('%X')}] {i}/{total} Gönderildi -> {to_email}")
            
            time.sleep(1)

        if server:
            server.quit()
        print("Toplu mail gönderimi başarıyla tamamlandı.")
        
    except Exception as e:
        print(f"Mail gönderimi sırasında hata oluştu: {e}")
