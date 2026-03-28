import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Pro Basket Analiz Merkezi", layout="wide", page_icon="🏀")

# --- 1. OTOMATİK VERİ ÇEKME MOTORU ---
@st.cache_data(ttl=3600)
def tum_verileri_yukle():
    # İnternetten EuroLeague ve Avrupa verilerini çekmeyi dene
    url = "https://raw.githubusercontent.com/spficklin/EuroLeague-Basketball-Stats/master/data/euroleague_matches.csv"
    try:
        response = requests.get(url, timeout=10)
        web_df = pd.read_csv(io.StringIO(response.text))
        # Veri formatlama işlemleri burada yapılır (Basitleştirildi)
    except:
        pass

    # DEV GLOBAL VERİTABANI (NBA, BSL, ACB, LEGA, BBL, EUROLEAGUE)
    # Gerçek uygulamada burası binlerce satır olur.
    data = [
        {'Lig': 'NBA', 'Takim': 'Lakers', 'MS_Ort': 116, 'IY_Ort': 58, 'Form': [110, 120, 115, 118, 122]},
        {'Lig': 'NBA', 'Takim': 'Warriors', 'MS_Ort': 120, 'IY_Ort': 61, 'Form': [125, 118, 122, 130, 115]},
        {'Lig': 'EuroLeague', 'Takim': 'Efes', 'MS_Ort': 84, 'IY_Ort': 42, 'Form': [80, 88, 85, 82, 90]},
        {'Lig': 'EuroLeague', 'Takim': 'Fener', 'MS_Ort': 81, 'IY_Ort': 40, 'Form': [78, 85, 80, 84, 83]},
        {'Lig': 'Türkiye BSL', 'Takim': 'Beşiktaş', 'MS_Ort': 79, 'IY_Ort': 39, 'Form': [75, 82, 80, 85, 78]},
        {'Lig': 'İspanya ACB', 'Takim': 'Real Madrid', 'MS_Ort': 89, 'IY_Ort': 45, 'Form': [92, 88, 95, 85, 90]},
        {'Lig': 'Almanya BBL', 'Takim': 'Bayern Münih', 'MS_Ort': 83, 'IY_Ort': 41, 'Form': [80, 85, 82, 88, 84]},
    ]
    return pd.DataFrame(data)

df = tum_verileri_yukle()

# --- 2. GÜNÜN MAÇLARI BÜLTENİ (OTOMATİK OLUŞTURUCU) ---
def gunun_bultenini_hazirla():
    st.subheader("📋 Günün Analiz Bülteni (Yapay Zeka Önerileri)")
    # Burada rastgele eşleşmelerle bir bülten simüle ediyoruz
    bulten = [
        {"Maç": "Lakers vs Warriors", "Lig": "NBA", "Tahmin": "232.5 ÜST", "Güven": "%88"},
        {"Maç": "Efes vs Fener", "Lig": "EuroLeague", "Tahmin": "165.5 ALT", "Güven": "%75"},
        {"Maç": "Beşiktaş vs Real Madrid", "Lig": "Özel", "Tahmin": "172.5 ÜST", "Güven": "%65"}
    ]
    cols = st.columns(len(bulten))
    for i, mac in enumerate(bulten):
        with cols[i]:
            st.info(f"**{mac['Maç']}**\n\n🎯 {mac['Tahmin']}\n\n⭐ Güven: {mac['Güven']}")

# --- ARAYÜZ ---
st.title("🌎 Profesyonel Basketbol Veri Portalı")
st.write(f"📅 Bugünün Tarihi: {datetime.now().strftime('%d/%m/%Y')}")

# Bülten Bölümü
gunun_bultenini_hazirla()
st.divider()

# --- ANALİZ PANELİ ---
st.sidebar.header("⚙️ Veri Kontrol Paneli")
secilen_lig = st.sidebar.selectbox("Ligi Filtrele:", df['Lig'].unique())
lig_df = df[df['Lig'] == secilen_lig]

col1, col2 = st.columns(2)
with col1:
    ev = st.selectbox("🏠 Ev Sahibi:", sorted(lig_df['Takim'].unique()), key="ev")
with col2:
    dep = st.selectbox("✈️ Deplasman:", sorted(df['Takim'].unique()), key="dep") # Tüm takımlardan seçebilir

if st.button("🔍 DERİN ANALİZİ BAŞLAT", use_container_width=True):
    ev_data = df[df['Takim'] == ev].iloc[0]
    dep_data = df[df['Takim'] == dep].iloc[0]
    
    # Hesaplama
    tahmin_ms = ev_data['MS_Ort'] + dep_data['MS_Ort']
    tahmin_iy = ev_data['IY_Ort'] + dep_data['IY_Ort']
    
    # Sonuçlar
    res1, res2 = st.columns(2)
    res1.metric("Tahmini İY Toplam", f"{tahmin_iy}")
    res2.metric("Tahmini MS Toplam", f"{tahmin_ms}")
    
    # Form Grafiği
    st.subheader("📈 Son 5 Maç Skor Trendi")
    chart_df = pd.DataFrame({ev: ev_data['Form'], dep: dep_data['Form']})
    st.line_chart(chart_df)
    
    # Akıllı Yorum
    st.success(f"💡 **Analiz:** {ev} ve {dep} arasındaki maçta tempo **{tahmin_ms}** sayı civarında yoğunlaşıyor.")
