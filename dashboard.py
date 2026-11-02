import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Klinik Diyabet Risk Değerlendirme Sistemi",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# KOYU TEMA VE YÜKSEK KONTRASTLI MODERN CSS
st.markdown("""
    <style>
    /* Koyu Arka Plan */
    .stApp {
        background-color: #0e1117 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f1f5f9 !important;
    }
    
    /* Başlıklar ve Metinler */
    h1, h2, h3, h4, label, .stMarkdown {
        color: #f8fafc !important;
        font-weight: 600;
    }

    /* Form Input Kutuları */
    div[data-baseweb="input"] {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
    }
    
    /* Input İçerisindeki Yazı ve Oklar */
    input {
        color: #f8fafc !important;
    }

    /* Sekme Tasarımı */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #1e293b;
        border-radius: 8px 8px 0px 0px;
        color: #cbd5e1 !important;
        font-weight: 600;
        padding: 10px 24px;
        border: 1px solid #334155;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #0284c7 !important;
    }

    /* Sonuç Kartları */
    .result-card {
        padding: 24px;
        border-radius: 12px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    /* Diyabet - Kırmızı */
    .card-diabetic {
        background-color: #450a0a;
        border-left: 8px solid #ef4444;
        color: #fecaca !important;
    }
    
    /* Yüksek Risk - Turuncu */
    .card-high-risk {
        background-color: #431407;
        border-left: 8px solid #f97316;
        color: #ffedd5 !important;
    }
    
    /* Orta Risk - Sarı */
    .card-medium-risk {
        background-color: #422006;
        border-left: 8px solid #eab308;
        color: #fef9c3 !important;
    }
    
    /* Düşük Risk - Yeşil */
    .card-low-risk {
        background-color: #052e16;
        border-left: 8px solid #22c55e;
        color: #dcfce7 !important;
    }

    /* Tıbbi Uyarı Kutusu */
    .disclaimer-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 18px;
        font-size: 0.9rem;
        color: #94a3b8 !important;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. ORİJİNAL HESAPLANAN KLİNİK MODEL AĞIRLIKLARI (w_i)
# PostgreSQL Lojistik Regresyon MLE Analiz Sonuçları
w_age = 0.2741    # %27.41 (Yaş)
w_bmi = 0.1466    # %14.66 (BMI)
w_hba1c = 0.5793  # %57.93 (HbA1c)

# BAŞLIK
st.title("Klinik Diyabet Risk Değerlendirme ve Analiz Sistemi")
st.write("")

# SEKMELER
tab1, tab2 = st.tabs(["Klinik Risk Değerlendirme Paneli", "Parametre Etki Ağırlıkları"])

# ----------------------------------------------------
# SEKME 1: KLİNİK RİSK DEĞERLENDİRME PANELİ
# ----------------------------------------------------
with tab1:
    st.subheader("Hasta Biyometrik ve Laboratuvar Veri Girişi")
    
    c1, c2, c3 = st.columns(3)
    input_age = c1.number_input("Yaş (Yıl)", min_value=1, max_value=120, value=45)
    input_bmi = c2.number_input("Vücut Kitle İndeksi - BMI (kg/m²)", min_value=10.0, max_value=70.0, value=28.5, step=0.1)
    input_hba1c = c3.number_input("Glikozile Hemoglobin - HbA1c (%)", min_value=3.0, max_value=15.0, value=6.2, step=0.1)

    # Risk Skoru Hesabı
    norm_age = (input_age - 0.08) / (80.0 - 0.08)
    norm_bmi = (input_bmi - 10.0) / (95.0 - 10.0)
    norm_hba1c = (input_hba1c - 3.5) / (9.0 - 3.5)
    
    patient_risk_score = w_age * norm_age + w_bmi * norm_bmi + w_hba1c * norm_hba1c

    st.write("")
    st.subheader("Klinik Değerlendirme Raporu")

    # SONUÇ KARTLARI
    if input_hba1c >= 6.5:
        st.markdown(f"""
            <div class="result-card card-diabetic">
                <h3 style="margin-top:0; color:#fca5a5 !important;">KLİNİK TANI: DİYABET</h3>
                <p style="font-size: 1.05rem; margin-bottom: 0; color:#fecaca !important;">
                    Laboratuvar HbA1c değeriniz <strong>%{input_hba1c:.1f}</strong> seviyesindedir. 
                    Uluslararası diyabet tanı kriterlerine göre (HbA1c ≥ %6.5) bireyde <strong>Diyabet</strong> mevcuttur.
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:
        if patient_risk_score > 0.40:
            st.markdown(f"""
                <div class="result-card card-high-risk">
                    <h3 style="margin-top:0; color:#fdba74 !important;">RİSK KATEGORİSİ: YÜKSEK RİSK GRUBU</h3>
                    <p style="font-size: 1.05rem; margin-bottom: 0; color:#ffedd5 !important;">
                        HbA1c seviyeniz klinik tanı eşiğinin altında olmasına rağmen; yüksek yaş ve BMI parametrelerinizin bileşimi metabolik açıdan <strong>yüksek diyabet riski</strong> taşımaktadır.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        elif patient_risk_score > 0.22:
            st.markdown(f"""
                <div class="result-card card-medium-risk">
                    <h3 style="margin-top:0; color:#fde047 !important;">RİSK KATEGORİSİ: ORTA DÜZEY RİSK</h3>
                    <p style="font-size: 1.05rem; margin-bottom: 0; color:#fef9c3 !important;">
                        Klinik parametreleriniz orta düzeyde risk taşımaktadır. Yaşam tarzı düzenlemeleri ve düzenli metabolik takip önerilmektedir.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div class="result-card card-low-risk">
                    <h3 style="margin-top:0; color:#86efac !important;">RİSK KATEGORİSİ: DÜŞÜK RİSK</h3>
                    <p style="font-size: 1.05rem; margin-bottom: 0; color:#dcfce7 !important;">
                        Mevcut verileriniz ve laboratuvar sonuçlarınız metabolik açıdan düşük risk aralığındadır.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # TIBBİ BİLGİLENDİRME
    st.markdown("""
        <div class="disclaimer-box">
            <strong>Tıbbi Uyarı ve Yasal Bilgilendirme:</strong> Bu panelde sunulan değerlendirmeler, biyoistatistiksel ve matematiksel modelleme algoritmalarına dayanmaktadır. Verilen çıktılar bilgilendirme amaçlı olup kesin tıbbi teşhis yerine geçmez. Doğrulama ve tedavi planlaması için mutlaka uzman bir hekime başvurunuz.
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# SEKME 2: PARAMETRE ETKİ AĞIRLIKLARI
# ----------------------------------------------------
with tab2:
    st.subheader("Klinik Parametrelerin Risk Üzerindeki Göreli Etki Dağılımı")
    st.write("Veri setindeki değişkenlerin diyabet oluşumunu açıklama güçlerinin oransal dağılımı aşağıda sunulmuştur:")

    chart_data = pd.DataFrame({
        'Klinik Parametre': ['HbA1c Seviyesi (%)', 'Yaş (Yıl)', 'Vücut Kitle İndeksi - BMI (kg/m²)'],
        'Etki Payı': [w_hba1c, w_age, w_bmi]
    })

    fig_pie = px.pie(
        chart_data, 
        values='Etki Payı', 
        names='Klinik Parametre',
        hole=0.4,
        color_discrete_sequence=['#0284c7', '#38bdf8', '#7dd3fc']
    )
    
    fig_pie.update_traces(
        textinfo='percent+label',
        textposition='outside',
        textfont_size=14,
        textfont_color='#f8fafc',
        marker=dict(line=dict(color='#0e1117', width=2))
    )
    
    fig_pie.update_layout(
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(font=dict(color='#f8fafc'))
    )

    st.plotly_chart(fig_pie, use_container_width=True)
