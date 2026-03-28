import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapısı
st.set_page_config(page_title="Pro Basket Analiz v6", layout="wide", page_icon="📈")

# --- GELİŞMİŞ VERİ SETİ (AVRUPA + NBA + FORM DURUMU) ---
@st.cache_data
def dev_veritabanini_yukle():
    # 'Son_5' sütunu takımların son 5 maçtaki skorlarını temsil eder
    data = [
        # EUROLEAGUE
        {'Lig': 'EuroLeague', 'Takim': 'Efes', 'IY': 44, 'MS': 86, 'Saha': 1, 'Son_5': [82, 90, 85, 88, 85]},
        {'Lig': 'EuroLeague', 'Takim': 'Fener', 'IY': 41, 'MS': 82, 'Saha': 1, 'Son_5': [78, 85, 80, 84, 83]},
        {'Lig': 'EuroLeague', 'Takim': 'Real Madrid', 'IY': 47, 'MS': 91, 'Saha': 1, 'Son_5': [95, 88, 92, 89, 91]},
        {'Lig': 'EuroLeague', 'Takim': 'Barcelona', 'IY': 43, 'MS': 85, 'Saha': 1, 'Son_5': [80, 86, 84, 88, 87]},
        {'Lig': 'EuroLeague', 'Takim': 'Panathinaikos', 'IY': 45, 'MS': 88, 'Saha': 1, 'Son_5': [92, 85, 89, 87, 88]},
        {'Lig': 'EuroLeague', 'Takim': 'Olympiacos', 'IY': 40, 'MS': 81, 'Saha': 1, 'Son_5': [79, 82, 80, 83, 81]},
        {'Lig': 'EuroLeague', 'Takim': 'Monaco', 'IY': 46, 'MS': 89, 'Saha': 1, 'Son_5': [91, 87, 90, 88, 89]},
        
        # NBA
        {'Lig': 'NBA', 'Takim': 'Lakers', 'IY': 59, 'MS': 118, 'Saha': 1, 'Son_5': [120, 115, 118, 112, 125]},
        {'Lig': 'NBA', 'Takim': 'Warriors', 'IY': 62, 'MS': 123, 'Saha': 1, 'Son_5': [125, 120, 130, 118, 122]},
        {'Lig': 'NBA', 'Takim': 'Celtics', 'IY': 58, 'MS': 116, 'Saha': 1, 'Son_5': [118, 114, 110, 120, 116]},
        
        # TÜRKİYE BSL
        {'Lig': 'Türkiye BSL', 'Takim': 'Beşiktaş', 'IY': 40, 'MS': 81, 'Saha': 1, 'Son_5': [75, 82, 80, 88, 80]},
        {'Lig': 'Türkiye BSL', 'Takim': 'Galatasaray', 'IY': 41, 'MS': 83, 'Saha': 1, 'Son_5': [80, 85, 82, 84, 84]},
        {'Lig': 'Türkiye BSL', 'Takim': 'Karşıyaka', 'IY': 43, 'MS': 86, 'Saha': 1, 'Son_5': [88, 82, 85, 90, 85]}
    ]
    # Deplasman verilerini otomatik üret (Ortalamaları %6 düşürerek)
    full_data = []
    for d in data:
        full_data.append(d) # İç Saha
        dep = d.copy()
        dep['Saha'] = 0
        dep['IY'] = int(d['IY'] * 0.92)
        dep['MS'] = int(d['MS'] * 0.94)
        dep['Son_5'] = [int(s * 0.94) for s in d['Son_5']]
        full_data.append(dep)
        
    return pd.DataFrame(full_data)

df = dev_veritabanini_yukle()

# --- ARAYÜZ ---
st.title("📈 Pro Basketbol Form & Tahmin Analizörü")
st.markdown("Son 5 maç performansı ve iç/dış saha dinamikleriyle akıllı analiz.")

# Lig ve Takım Seçimi
st.sidebar.header("🔍 Analiz Filtreleri")
secilen_lig = st.sidebar.selectbox("Lig Seçin:", sorted(df['Lig'].unique()))
lig_df = df[df['Lig'] == secilen_lig]

col1, col2 = st.columns(2)
with col1:
    ev = st.selectbox("🏠 Ev Sahibi:", sorted(lig_df['Takim'].unique()), key="ev_p")
with col2:
    dep = st.selectbox("✈️ Deplasman:", sorted(lig_df['Takim'].unique()), key="dep_p")

if st.button("🚀 DERİNLEMESİNE ANALİZ ET", use_container_width=True):
    ev_data = lig_df[(lig_df['Takim'] == ev) & (lig_df['Saha'] == 1)].iloc[0]
    dep_data = lig_df[(lig_df['Takim'] == dep) & (lig_df['Saha'] == 0)].iloc[0]
    
    # 1. TEMEL TAHMİN
    tahmin_iy = ev_data['IY'] + dep_data['IY']
    tahmin_ms = ev_data['MS'] + dep_data['MS']
    
    # 2. FORM ANALİZİ (Son 5 Maçın Standart Sapması)
    ev_form_ort = np.mean(ev_data['Son_5'])
    dep_form_ort = np.mean(dep_data['Son_5'])
    guven_skoru = 100 - abs(ev_form_ort - ev_data['MS']) - abs(dep_form_ort - dep_data['MS'])

    # --- SONUÇLAR ---
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Beklenen İlk Yarı", f"{tahmin_iy}")
    m2.metric("Beklenen Maç Sonu", f"{tahmin_ms}")
    m3.metric("Analiz Güven Endeksi", f"%{int(guven_skoru)}")

    # GRAFİKLER
    st.subheader("📊 Form Grafiği (Son 5 Maç Trendi)")
    form_df = pd.DataFrame({
        ev: ev_data['Son_5'],
        dep: dep_data['Son_5']
    })
    st.line_chart(form_df)

    # ÖZEL TAVSİYE
    st.subheader("🎯 Bahis Strateji Notu")
    if guven_skoru > 85:
        st.success(f"✅ **YÜKSEK GÜVEN:** İki takım da istikrarlı. **{ms_tahmin}** sayı baremi çok değerli.")
    else:
        st.warning("⚠️ **DİKKAT:** Takımların form grafiği dalgalı. Alt/Üst baremlerinde daha güvenli (safe) seçeneklere yönelin.")

    # Barem Önerileri
    c_a, c_u = st.columns(2)
    c_a.info(f"🛡️ **Güvenli Alt:** {tahmin_ms + 4.5}")
    c_u.info(f"🔥 **Fırsat Üst:** {tahmin_ms - 4.5}")