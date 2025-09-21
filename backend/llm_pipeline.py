import os  # İşletim sistemi işlemleri için modül
import re  # Düzenli ifadeler (regex) için modül
import asyncio  # Asenkron programlama için modül
from ollama import AsyncClient  # Ollama AI istemcisi

async def async_summarize_lab_report(content: str, model: str = "llama3.2:latest") -> str:
    """Asenkron olarak laboratuvar raporunu özetler."""
    # AI modeline gönderilecek prompt (istek) oluşturma
    prompt = f"""Analyze the following medical lab report and provide a comprehensive, structured summary in English for patients.

Please provide:
- COMPREHENSIVE LAB REPORT ANALYSIS
- PATIENT OVERVIEW (if available)
- CRITICAL FINDINGS (most important 3-4 items)
- DETAILED RESULTS (all other findings)
- HEALTH RECOMMENDATIONS (general lifestyle suggestions)

Use ✅ for normal values, ❌ for abnormal values
Include actual values and normal ranges when possible
Focus on clinical significance in simple terms

LAB REPORT CONTENT:
{content}

ANALYSIS OUTPUT:"""
    
    try:
        # Ollama asenkron istemcisi oluşturma (localhost:11434 üzerinden)
        client = AsyncClient(host='http://localhost:11434')
        # Modeli kullanarak prompt'u işleme ve yanıt alma
        response = await client.generate(model=model, prompt=prompt)
        return response.response  # AI'dan gelen yanıtı döndürme
    except Exception as e:
        return f"Error: {str(e)}"  # Hata durumunda hata mesajı döndürme

def summarize_lab_report(file_path: str) -> str:
    """Laboratuvar raporunu özetler."""
    try:
        # Dosyayı okuma
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Asenkron fonksiyonu senkron olarak çalıştırmak için event loop oluşturma
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # Asenkron özetleme fonksiyonunu çalıştırma
        summary = loop.run_until_complete(async_summarize_lab_report(content))
        loop.close()  # Event loop'u kapatma
        
        return summary  # Özeti döndürme
    except Exception as e:
        return f"Error: {str(e)}"  # Hata durumunda hata mesajı döndürme

def extract_patient_info(content: str) -> dict:
    """Rapor içinden hasta bilgilerini çıkarır."""
    info = {}  # Hasta bilgilerini saklamak için boş sözlük
    
    # İsim bilgisini regex ile arama (case-insensitive)
    name_match = re.search(r'(?i)(hasta|patient|name|adı)[:\s]+([^\n]+)', content)
    if name_match:
        info['name'] = name_match.group(2).strip().title()  # İsmi formatlama ve kaydetme
    
    # Yaş bilgisini regex ile arama
    age_match = re.search(r'(?i)(yaş|age)[:\s]+(\d+)', content)
    if age_match:
        info['age'] = age_match.group(2)  # Yaşı kaydetme
    
    # Cinsiyet bilgisini regex ile arama
    gender_match = re.search(r'(?i)(cinsiyet|gender|sex)[:\s]+([^\n]+)', content)
    if gender_match:
        gender = gender_match.group(2).lower()  # Cinsiyeti küçük harfe çevirme
        # Kadın için farklı yazım varyasyonlarını kontrol etme
        if any(x in gender for x in ['kadın', 'female', 'kız', 'f ']): 
            info['gender'] = 'Female'
        # Erkek için farklı yazım varyasyonlarını kontrol etme
        elif any(x in gender for x in ['erkek', 'male', 'e ']): 
            info['gender'] = 'Male'
        else:
            info['gender'] = gender_match.group(2).strip()  # Bilinmeyen formatı olduğu gibi kaydetme
    
    # Tarih bilgisini regex ile arama
    date_match = re.search(r'(?i)(tarih|date)[:\s]+([0-9./-]+)', content)
    if date_match:
        info['date'] = date_match.group(2)  # Tarihi kaydetme
    
    return info  # Hasta bilgilerini döndürme

def format_summary_with_html(summary: str, patient_info: dict = None) -> str:
    """Özet metnini HTML formatına dönüştürür."""
    if not summary:  # Özet yoksa
        return "<p>No analysis available</p>"  # Uygun mesaj döndürme
    
    # HTML çıktısını oluşturmaya başlama
    html_output = ""
    
    # Hasta bilgileri varsa HTML kart oluşturma
    if patient_info:
        html_output += '<div class="patient-info-card"><h4 class="section-header">Patient Information</h4><div class="row">'
        for field, value in patient_info.items():
            # Her bilgi alanı için sütun oluşturma
            html_output += f'<div class="col-md-3"><strong>{field.title()}:</strong> {value}</div>'
        html_output += '</div></div>'  # Kartı kapatma
    
    # Özet metnini satırlara ayırma
    lines = summary.split('\n')
    in_list = False  # Liste içinde olup olmadığını takip etme
    in_sub_list = False  # Alt liste içinde olup olmadığını takip etme
    
    # Her satırı işleme
    for line in lines:
        line = line.strip()  # Satırdaki boşlukları temizleme
        if not line:  # Boş satır
            if in_list:  # Liste içindeyse listeyi kapatma
                html_output += '</ul>'
                in_list = False
            if in_sub_list:  # Alt liste içindeyse alt listeyi kapatma
                html_output += '</ul>'
                in_sub_list = False
            continue  # Sonraki satıra geçme
            
        # Bölüm başlıklarını tespit etme ve uygun HTML oluşturma
        if line.upper().startswith('COMPREHENSIVE'):
            html_output += f'<div class="report-section"><h3 class="section-header">{line}</h3>'
        elif line.upper().startswith('PATIENT'):
            html_output += f'</div><div class="report-section"><h4 class="section-header text-primary">{line}</h4>'
        elif line.upper().startswith('CRITICAL'):
            html_output += f'</div><div class="report-section critical-section"><h4 class="section-header critical-section">{line}</h4>'
        elif line.upper().startswith('DETAILED'):
            html_output += f'</div><div class="report-section"><h4 class="section-header text-info">{line}</h4>'
        elif line.upper().startswith('HEALTH'):
            html_output += f'</div><div class="report-section recommendation-section"><h4 class="section-header recommendation-section">{line}</h4>'
        # Madde işaretli liste öğelerini işleme
        elif line.startswith('•') or line.startswith('-'):
            if not in_list:  # Liste başlamamışsa başlatma
                html_output += '<ul class="medical-findings">'
                in_list = True
            # Değer durumuna göre emoji ekleme ve uygun CSS sınıfı atama
            if '❌' in line:  # Anormal değer
                html_output += f'<li class="abnormal-value-item">{line}</li>'
            elif '✅' in line:  # Normal değer
                html_output += f'<li class="normal-value-item">{line}</li>'
            else:  # Normal liste öğesi
                html_output += f'<li>{line[1:].strip()}</li>'
        # Alt liste öğelerini işleme
        elif line.startswith('* '):
            if not in_sub_list:  # Alt liste başlamamışsa başlatma
                html_output += '<ul class="medical-sub-findings">'
                in_sub_list = True
            html_output += f'<li>{line[2:].strip()}</li>'  # Alt liste öğesi ekleme
        # Düz metin satırlarını işleme
        else:
            if in_list:  # Liste içindeyse listeyi kapatma
                html_output += '</ul>'
                in_list = False
            if in_sub_list:  # Alt liste içindeyse alt listeyi kapatma
                html_output += '</ul>'
                in_sub_list = False
            html_output += f'<p>{line}</p>'  # Paragraf olarak ekleme
    
    # Açık kalan listeleri kapatma
    if in_list:
        html_output += '</ul>'
    if in_sub_list:
        html_output += '</ul>'
    
    html_output += '</div>'  # Son div'i kapatma
    
    return html_output  # HTML formatlı özeti döndürme

def generate_patient_recommendations(summary: str) -> str:
    """Özete dayalı hasta önerileri oluşturur."""
    if not summary:  # Özet yoksa
        return "<p>No recommendations available</p>"  # Uygun mesaj döndürme
    
    summary_lower = summary.lower()  # Özeti küçük harfe çevirme (arama için)
    html_output = '<div class="recommendations"><h4 class="section-header recommendation-section">Personalized Health Recommendations</h4>'  # Öneriler bölümü başlığı
    
    # Belirli sağlık durumlarına göre öneriler oluşturma
    # Düşük hemoglobin veya anemi için öneriler
    if any(keyword in summary_lower for keyword in ['low hemoglobin', 'anemia', 'low iron']):
        html_output += '''
        <div class="recommendation-card priority-high">
            <div class="recommendation-icon">🩸</div>
            <h5>Iron Management</h5>
            <p>Your hemoglobin levels are slightly low. Consider:</p>
            <ul class="medical-findings">
                <li>Include iron-rich foods like red meat, spinach, and lentils</li>
                <li>Combine with vitamin C sources to enhance absorption</li>
                <li>Consider iron supplements after consulting your doctor</li>
                <li>Avoid drinking tea or coffee with meals as they inhibit iron absorption</li>
            </ul>
        </div>'''
    
    # Yüksek glikoz veya diyabet için öneriler
    if any(keyword in summary_lower for keyword in ['high glucose', 'diabetes', 'blood sugar']):
        html_output += '''
        <div class="recommendation-card priority-high">
            <div class="recommendation-icon">🩸</div>
            <h5>Sugar Management</h5>
            <p>Your glucose levels need attention:</p>
            <ul class="medical-findings">
                <li>Monitor carbohydrate intake and choose complex carbs</li>
                <li>Maintain regular meal times and avoid skipping meals</li>
                <li>Limit sugary drinks and processed foods</li>
                <li>Consider regular blood sugar monitoring</li>
            </ul>
        </div>'''
    
    # Yüksek kolesterol için öneriler
    if any(keyword in summary_lower for keyword in ['high cholesterol', 'lipid', 'triglyceride']):
        html_output += '''
        <div class="recommendation-card priority-medium">
            <div class="recommendation-icon">❤️</div>
            <h5>Heart Health</h5>
            <p>Your lipid profile shows elevated levels:</p>
            <ul class="medical-findings">
                <li>Reduce saturated and trans fats in your diet</li>
                <li>Increase soluble fiber from oats, beans, and fruits</li>
                <li>Include omega-3 rich foods like fatty fish and walnuts</li>
                <li>Consider plant sterols and stanols if appropriate</li>
            </ul>
        </div>'''
    
    # Düşük D vitamini için öneriler
    if any(keyword in summary_lower for keyword in ['vitamin d', 'low vitamin d']):
        html_output += '''
        <div class="recommendation-card priority-medium">
            <div class="recommendation-icon">☀️</div>
            <h5>Vitamin D Optimization</h5>
            <p>Your Vitamin D levels are low:</p>
            <ul class="medical-findings">
                <li>Get 15-20 minutes of sun exposure daily</li>
                <li>Consume vitamin D-rich foods like fatty fish and fortified dairy</li>
                <li>Consider vitamin D supplementation after medical consultation</li>
                <li>Maintain adequate calcium intake for bone health</li>
            </ul>
        </div>'''
    
    # Karaciğer enzimleri için öneriler
    if any(keyword in summary_lower for keyword in ['alt', 'liver', 'elevated liver']):
        html_output += '''
        <div class="recommendation-card priority-high">
            <div class="recommendation-icon">💊</div>
            <h5>Liver Support</h5>
            <p>Your liver enzymes are elevated:</p>
            <ul class="medical-findings">
                <li>Avoid alcohol and limit over-the-counter medications</li>
                <li>Maintain a healthy weight through diet and exercise</li>
                <li>Consider milk thistle or other liver-supportive supplements after consultation</li>
                <li>Stay hydrated and limit processed foods</li>
            </ul>
        </div>'''
    
    # Genel sağlık önerileri (her zaman gösterilir)
    html_output += '''
    <div class="recommendation-card">
        <div class="recommendation-icon">💡</div>
        <h5>General Health Tips</h5>
        <ul class="medical-findings">
            <li><strong>Exercise:</strong> Aim for 150 minutes of moderate exercise weekly</li>
            <li><strong>Hydration:</strong> Drink 2-3 liters of water daily</li>
            <li><strong>Sleep:</strong> Ensure 7-9 hours of quality sleep per night</li>
            <li><strong>Nutrition:</strong> Focus on whole foods and balanced nutrition</li>
            <li><strong>Stress Management:</strong> Practice mindfulness or meditation techniques</li>
            <li><strong>Regular Check-ups:</strong> Schedule annual health screenings</li>
        </ul>
    </div>
    '''
    
    # Yasal uyarı metni
    html_output += '<div class="alert alert-secondary mt-3"><strong>Disclaimer:</strong> These are general suggestions based on your lab results. Always consult your healthcare provider for personalized medical advice and before making significant changes to your diet or lifestyle.</div>'
    html_output += '</div>'  # Öneriler bölümünü kapatma
    
    return html_output  # HTML formatlı önerileri döndürme