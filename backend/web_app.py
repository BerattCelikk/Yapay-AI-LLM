from flask import Flask, request, render_template, jsonify  # Flask web framework bileşenleri
import os  # İşletim sistemi işlemleri için modül
from llm_pipeline import summarize_lab_report, extract_patient_info, format_summary_with_html, generate_patient_recommendations  # Özel fonksiyonlar
from markupsafe import Markup  # HTML güvenli işleme için
import uuid  # Benzersiz ID oluşturmak için
from datetime import datetime  # Tarih işlemleri için

app = Flask(__name__)  # Flask uygulaması oluşturma
UPLOAD_FOLDER = "uploads"  # Yüklenen dosyaların kaydedileceği klasör
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Klasörü oluşturma (yoksa)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB dosya yükleme limiti

@app.route("/", methods=["GET", "POST"])  # Ana sayfa route'u
def index():
    error = None  # Hata mesajı
    summary = None  # Analiz özeti
    filename = None  # Dosya adı
    patient_info = None  # Hasta bilgileri
    recommendations = None  # Öneriler
    
    if request.method == "POST":  # Form gönderildiyse
        file = request.files.get("lab_file")  # Yüklenen dosyayı alma
        if file and file.filename:  # Dosya ve dosya adı varsa
            if not file.filename.lower().endswith('.txt'):  # Dosya .txt değilse
                error = "Please upload a .txt file"  # Hata mesajı
            else:
                try:
                    # Benzersiz dosya adı oluşturma (tarih + orijinal ad)
                    unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
                    filename = os.path.join(UPLOAD_FOLDER, unique_filename)  # Dosya yolu
                    file.save(filename)  # Dosyayı kaydetme
                    
                    # Hasta bilgilerini çıkarma
                    with open(filename, "r", encoding="utf-8") as f:
                        content = f.read()  # Dosya içeriğini okuma
                    patient_info = extract_patient_info(content)  # Hasta bilgilerini çıkarma
                    
                    # Raporu özetleme
                    summary_text = summarize_lab_report(filename)
                    
                    # HTML formatına dönüştürme
                    summary = format_summary_with_html(summary_text, patient_info)
                    
                    # Önerileri oluşturma
                    recommendations = generate_patient_recommendations(summary_text)
                    
                except Exception as e:
                    error = f"Error processing file: {str(e)}"  # Hata mesajı
        else:
            error = "Please select a file to upload"  # Dosya seçilmedi hatası
    
    # Yüklenen dosyaları listeleme
    uploaded_files = []
    if os.path.exists(UPLOAD_FOLDER):  # Upload klasörü varsa
        uploaded_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.txt')]  # Sadece .txt dosyaları
        # Dosyaları değiştirilme tarihine göre sıralama (yeniden eskiye)
        uploaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
    
    # Şablonu render etme ve değişkenleri gönderme
    return render_template(
        "index.html", 
        summary=Markup(summary) if summary else None,  # HTML güvenli işleme
        recommendations=Markup(recommendations) if recommendations else None,  # HTML güvenli işleme
        filename=filename,
        patient_info=patient_info,
        error=error,
        uploaded_files=uploaded_files
    )

@app.route("/view_file/<filename>")  # Dosya görüntüleme route'u
def view_file(filename):
    """Yüklenen dosyanın içeriğini göster"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)  # Dosya yolu
        if os.path.exists(filepath):  # Dosya varsa
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()  # Dosya içeriğini okuma
            return f"<pre>{content}</pre>"  # Ön biçimlendirilmiş metin olarak döndürme
        else:
            return "File not found", 404  # Dosya bulunamadı hatası
    except Exception as e:
        return f"Error reading file: {str(e)}", 500  # Dosya okuma hatası

@app.route("/delete_file/<filename>", methods=["POST"])  # Dosya silme route'u (POST)
def delete_file(filename):
    """Dosyayı sil"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)  # Dosya yolu
        if os.path.exists(filepath):  # Dosya varsa
            os.remove(filepath)  # Dosyayı silme
            return jsonify({"success": True, "message": "File deleted successfully"})  # Başarı mesajı
        else:
            return jsonify({"success": False, "message": "File not found"}), 404  # Dosya bulunamadı hatası
    except Exception as e:
        return jsonify({"success": False, "message": f"Error deleting file: {str(e)}"}), 500  # Silme hatası

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Uygulamayı çalıştırma (tüm IP'lerden erişilebilir, debug modunda)