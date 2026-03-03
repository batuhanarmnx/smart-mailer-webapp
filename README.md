# 🚀 Smart Mailer WebApp

Smart Mailer, web tabanlı, dinamik ve kullanıcı dostu bir **Toplu E-Posta Gönderim Platformudur**. Özellikle kişiselleştirilmiş şablonları Excel verileriyle birleştirerek ve Google OAuth (Gmail API) entegrasyonu sayesinde saniyeler içinde binlerce kullanıcıya güvenle mail göndermenizi sağlar. İsteğe bağlı olarak klasik SMTP ayarlarıyla da çalışabilir.

![Smart Mailer Görseli (Eklenecek)](https://via.placeholder.com/800x400?text=Smart+Mailer+Dashboard)

---

## ✨ Özellikler

- **⚡ Dinamik Veri Entegrasyonu:** Excel dosyalarını (`.xlsx`) yükleyerek otomatik bir şekilde alıcılarınızı tablo biçiminde listeleyin.
- **🎨 Etiket Bazlı (Tag-Based) Şablon Tasarımcı:** Gelişmiş sürükle bırak araçlarıyla boğuşmanıza gerek yok! `[Şirket Ekle]`, `[Yetkili Ekle]` gibi hazır butonlarla şablonlarınızı çok rahat tasarlayabilirsiniz. 
- **🔑 Çift Katmanlı Gönderim Seçenekleri:**
    - **Google OAuth Login (Sıfır Ayar):** Tek tıkla "Google Girişi" yapın, doğrudan kendi Gmail'iniz üzerinden API kullanılarak sınırsız gönderim yapın (Şifre veya SMTP ayarı girmeden!).
    - **Klasik SMTP (Manuel Ayar):** İsterseniz Ayarlar sayfasından kendi kurumsal SMTP portlarınızı (Ör: Outlook, Yandex, Şirket Maili vb.) manuel girerek de çalışabilirsiniz.
- **📩 Taslak Kaydetme:** Hazırladığınız şablonları isimlendirerek kaydedebilir, sonradan tek bir tıklamayla geri yükleyebilirsiniz.
- **📱 Responsive Mobil Uyumlu: ** Modern ve estetik UI/UX standartlarına göre tasarlanmış mobil uyumlu arayüz.
- **🔐 Tam Güvenlik:** Excel verileriniz ve Google kimlik oturumlarınız tamamen lokal ve izole bir şekilde backend'de işlenir. 

---

## 🛠 Kullanılan Teknolojiler

**Backend (Sunucu):**
* [Python 3.9+](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) - Modern ve çok hızlı (Asynchronous) Python web framework'ü.
* **Uvicorn** - ASGI Sunucusu
* **Google API Client** (OAuth 2.0 & Gmail API)
* **Authlib** (Session Middleware)
* **Pandas / Openpyxl** (Excel Veri Okuma)

**Frontend (Kullanıcı Arayüzü):**
* **HTML5 / CSS3 / Vanilla Javascript**
* [Bootstrap 5.3](https://getbootstrap.com/)
* [FontAwesome](https://fontawesome.com/) (İkonlar)
* [Quill.js Rich Text Editor](https://quilljs.com/)

---

## 🚀 Kurulum Adımları

Uygulamayı kendi lokal sunucunuzda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın.

### 1️⃣ Projeyi İndirin ve Bağımlılıkları Kurun
Çalışma dizininizde terminali açın:
```bash
# Projeyi bilgisayarınıza klonlayın (Veya ZIP Olarak indirin)
cd smart-mailer-webapp

# Python sanal ortamı (virtual environment) oluşturun
python -m venv venv

# Sanal ortamı aktifleştirin
# Windows için (PowerShell):
.\venv\Scripts\Activate.ps1
# Mac/Linux için:
source venv/bin/activate

# Gerekli bütün kütüphaneleri (FastAPI, Google Auth vs.) tek seferde yükleyin
pip install -r requirements.txt
```

### 2️⃣ Ortam Değişkenleri (.env) Tanımlaması
Uygulamanın çalışması ve özellikle **Google OAuth girişinin yapılabilmesi için** API anahtarlarına ihtiyacı vardır. 
Projenin ana dizinine `.env` adında bir dosya oluşturun ve içine şu bilgileri ekleyin:
```env
GOOGLE_CLIENT_ID=sizin_client_id_kodunuz.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=sizin_secret_kodunuz
```
> ***Not:*** Bu kodları `console.cloud.google.com` üzerinden yeni bir proje oluşturup **APIs & Services > Credentials** ekranından (Web Application) seçerek almalısınız.


### 3️⃣ Uygulamayı Çalıştırın!
Her şey hazırsa, sunucuyu basit bir komutla ayağa kaldırın:
```bash
python app.py
```
Terminalde `Uvicorn running on http://0.0.0.0:8000` mesajını gördüğünüzde her şey tamamdır!

Tarayıcınızı açın ve **[http://localhost:8000](http://localhost:8000)** adresine gidin.

---

## 📸 Ekran Görüntüleri ve Kullanım Rehberi

**1. Veri Yükleme (Excel):**
Sağ üst bölümden **"Şablon İndir"** diyerek örnek formatlı Excel numunesini bilgisayarınıza indirin. Sütunlarına dokunmadan satırları kendi verileriniz ile doldurun ve uygulamadaki bulut alanına sürükleyin. Altta tüm veriler anında Grid yapısında belirecektir.

**2. Mail Düzenleme:**
Müşteri için mailinizi yazarken *"{Sirket_Adi} Merhabalar"* yazmanıza hiç gerek yok. Buton kümesinden **[Şirket Adı Ekle]** ye bastığınızda o metin kendisi yerleşecek ve toplu gönderimde her şirket kendi adıyla maili teslim alacaktır.

**3. Gönderimi Devretme / Log Takibi:**
Eğer Google ile Oturum Açtıysanız hiçbir SMTP ayosu doldurmadan Google şifrelemesi ile mailler otomatik çıkar. İşlem terminalde her saniye 1 mail atılacak bir Spam Güvenlik önlemiyle tasarlanmıştır.

---

## 📄 Lisans
Bu proje geliştiriciye ait telif hakları ile korunmaktadır. Proje açık kaynak (Open Source) olup MIT veya özel lisans altında dağıtılabilir. Daha fazla bilgi için proje sahibiyle iletişime geçin.

**Geliştirici:** ✨ Batuhan Aytaç (Fair Teknoloji A.Ş)
