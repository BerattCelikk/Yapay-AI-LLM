# 🏥 YAPAY-AI: Akıllı Laboratuvar Raporu Analiz Sistemi

## 📋 Proje Özeti
**YAPAY-AI**, yapay zeka destekli laboratuvar raporu analiz platformu olarak, hastaların karmaşık tıbbi bulguları anlamasını kolaylaştıran ve kişiselleştirilmiş sağlık önerileri sunan yenilikçi bir çözümdür.

- **Demo Video:** https://www.youtube.com/watch?v=pQXLQtK243Q  
- **Canlı Demo:** https://yapay-zeka-hackathon.onrender.com/

---

## 🎯 Problem ve Çözüm

### ❌ Mevcut Problemler
- Laboratuvar raporları teknik terimler ve karmaşık veriler içerir  
- Hastalar raporları anlamakta zorlanır, kaygı düzeyleri artar  
- Doktor-hasta iletişimi zaman kısıtları nedeniyle yetersiz kalabilir  

### ✅ YAPAY-AI Çözümü
- AI destekli anlaşılır rapor özetleme  
- Görsel ve renkli vurgulama sistemi  
- Kişiselleştirilmiş sağlık önerileri  
- Kullanıcı dostu arayüz  

---

## 🛠️ Teknik Özellikler

### Backend Yapısı
- **Framework:** Flask (Python)  
- **AI Entegrasyonu:** Ollama + Llama 3.2  
- **Dosya İşleme:** Güvenli upload sistemi  
- **Veri İşleme:** Regex tabanlı hasta bilgisi çıkarma  

### Frontend Yapısı
- **HTML5/CSS3:** Responsive tasarım  
- **Bootstrap 5:** Modern UI componentleri  
- **JavaScript:** Dinamik etkileşimler  

### AI Özellikleri
- **Prompt Mühendisliği:** Optimize edilmiş tıbbi analiz prompt'u  
- **Yapılandırılmış Çıktı:** Standardize rapor formatı  
- **Anomali Tespiti:** Otomatik normal/anormal değer işaretleme  

---

## 📁 Proje Dosya Yapısı

YAPAY-AI/
├── 📁 backend/
│ ├── 📁 static/css/
│ │ └── style.css # Özel stiller
│ ├── 📁 templates/
│ │ └── index.html # Ana şablon
│ ├── 📁 uploads/ # Yüklenen dosyalar
│ ├── 📁 data/
│ │ ├── lab_summaries.csv # Örnek veriler
│ │ ├── lab_summaries.json # JSON formatında veriler
│ │ └── sample_lab_report.txt # Örnek rapor
│ ├── llm_pipeline.py # AI işlem hattı
│ ├── web_app.py # Flask uygulaması
│ └── requirements.txt # Bağımlılıklar
└── 📁 frontend/
└── index.html # Ana arayüz

## ⚙️ Kurulum Kılavuzu

### Ön Gereksinimler
- Python 3.8+  
- Ollama (yerel kurulum)  
- 8GB+ RAM (AI modeli için)  

### Adım Adım Kurulum

**1. Depoyu Klonla:**

- git clone <repository-url>
- cd YAPAY-AI
# 2. Backend Kurulumu:


- cd backend
- pip install -r requirements.txt
# 3. Ollama Kurulumu:


# Ollama'yı indir ve kur (https://ollama.ai/)
- ollama pull llama3.2:latest
# 4. Uygulamayı Başlat:


- python web_app.py
# 5. Tarayıcıda Aç:


- http://localhost:5000
# 🎮 Kullanım Kılavuzu
# 1. Dosya Yükleme
- "Choose File" butonuna tıkla

- .txt formatında laboratuvar raporu seç

- "Analyze Report" butonuna tıkla

# 2. Sonuçları İnceleme
- Hasta Bilgileri: Otomatik çıkarılan hasta verileri

- Kapsamlı Analiz: AI tarafından özetlenmiş rapor

- Kritik Bulgular: Önceliklendirilmiş önemli sonuçlar

- Öneriler: Kişiselleştirilmiş sağlık tavsiyeleri

# 3. Dosya Yönetimi
- Yüklenen dosyaları görüntüle

- Gerektiğinde dosyaları sil

# 🔧 API Endpoints
- Endpoint	Method	Açıklama
- /	GET, POST	Ana sayfa ve rapor yükleme
- /view_file/<filename>	GET	Dosya içeriğini görüntüleme
- /delete_file/<filename>	POST	Dosya silme

## 🎨 Özellikler ve Detaylar
# 🤖 AI Analiz Özellikleri
- Yapılandırılmış Özet: Standardize rapor formatı

- Değer İşaretleme: ✅ Normal / ❌ Anormal vurgulama

- Tıbbi Anlamlandırma: Klinik önem açıklamaları

# 🎯 Hasta Bilgisi Çıkarma
- İsim, yaş, cinsiyet otomatik tespit

- Tarih bilgisi çıkarma

- Regex tabanlı ileri veri işleme

# 💡 Akıllı Öneri Sistemi
- Demir Eksikliği: Beslenme ve takviye önerileri

- Diyabet: Şeker yönetimi tavsiyeleri

- Kolesterol: Kalp sağlığı önerileri

- Vitamin Eksiklikleri: Takviye ve beslenme planı

# 🚀 Performans Optimizasyonları
- Asenkron AI Çağrıları: UI donmasını önleme

- Dosya Önbellekleme: Tekrar işlemleri azaltma

- Responsive Tasarım: Mobil uyumluluk

- Hata Yönetimi: Graceful error handling

# 📊 Test Verileri
- data/sample_lab_report.txt → Örnek laboratuvar raporu

- data/lab_summaries.csv → Örnek analiz sonuçları

- data/lab_summaries.json → JSON formatında veriler

# ⚠️ Sınırlamalar ve Uyarılar
- Şu anda sadece .txt formatını destekler

- İngilizce raporlar için optimize edilmiştir

- AI model doğruluğu kullanılan modele bağlıdır

- Tıbbi teşhis aracı değildir – sadece bilgilendirme amaçlıdır
