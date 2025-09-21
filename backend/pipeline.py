# Bu dosya artık sadece llm_pipeline'ı yeniden export ediyor
from llm_pipeline import (
    summarize_lab_report, 
    generate_patient_recommendations, 
    extract_patient_info,
    format_summary_with_html
)

# Pipeline fonksiyonları için kolay erişim
__all__ = [
    'summarize_lab_report',
    'generate_patient_recommendations',
    'extract_patient_info',
    'format_summary_with_html'
]