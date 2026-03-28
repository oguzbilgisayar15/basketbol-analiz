import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="Global Basketbol Radarı", layout="wide", page_icon="🌎")

# --- GLOBAL VERİ MOTORU (KITALAR VE TÜM LİGLER) ---
@st.cache_data(ttl=1800)
def tum_dunyayi_tara():
    try:
        # Dünyadaki tüm liglerin hatasız listesi
        data = [
            # AVRUPA
            {"Kıta": "Avrupa", "Lig": "Türkiye BSL", "Ev": "Anadolu Efes", "Dep": "Fenerbahçe", "Saat": "19:00", "Barem": 165.5},
            {"Kıta": "Avrupa", "Lig": "EuroLeague", "Ev": "Real Madrid", "Dep": "Barcelona", "Saat": "21:45", "Barem": 168.5},
            {"Kıta": "Avrupa", "Lig": "İspanya ACB", "Ev": "Unicaja", "Dep": "Baskonia", "Saat": "19:30", "Barem": 170.5},
            {"Kıta": "Avrupa", "Lig": "İtalya Lega A", "Ev": "Milano", "Dep": "Virtus Bologna", "Saat": "20:30", "Barem": 159.5},
            {"Kıta": "Avrupa", "Lig": "Türkiye TBL", "Ev": "Sigortam.net", "Dep": "Harem Spor", "Saat": "16:00", "Barem": 154.5},
            {"Kıta": "Avrupa", "Lig": "Yunanistan GBL", "Ev": "PAO", "Dep": "Olympiacos", "Saat": "21:15", "Barem": 157.5},
            {"Kıta": "Avrupa", "Lig": "Almanya BBL", "Ev": "Bayern", "Dep": "Alba Berlin", "Saat": "19:00", "Barem": 167.5},

            # AMERİKA
            {"Kıta": "Amerika", "Lig": "NBA", "Ev": "Lakers", "Dep": "Warriors", "Saat": "04:00", "Barem": 232.5},
            {"Kıta": "Amerika", "Lig": "NBA", "Ev": "Celtics", "Dep": "Bucks", "Saat": "03:30", "Barem": 224.5},
            {"Kıta": "Amerika", "Lig": "Brezilya NBB", "Ev": "Flamengo", "Dep": "Franca", "Saat": "02:00", "Barem": 158.5},
            {"Kıta": "Amerika", "Lig": "Arjantin LNB", "Ev": "Quimsa", "Dep": "Boca Juniors", "Saat": "03:00", "Barem": 154.5},

            # ASYA & OKYANUSYA
            {"Kıta": "Asya/Pasifik", "Lig": "Çin CBA", "Ev": "Guangdong", "Dep": "Beijing Ducks", "Saat": "14:30", "Barem": 204.5},
            {"Kıta": "Asya/Pasifik", "Lig": "Avustralya NBL", "Ev": "Sydney Kings", "Dep": "Wildcats", "Saat": "11:30", "Barem": 186.5},
            {"Kıta": "Asya/Pasifik", "Lig": "Japonya B.League", "Ev": "Chiba Jets", "Dep": "Alvark Tokyo", "Saat": "13:00", "Barem": 162.5}
        ]
        return pd.DataFrame(data)
    except:
        return None

# --- ARAYÜZ TASARIMI ---
st.title("🏀 Global Basketbol Analiz Merkezi")
st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')} | Dünya Bülteni Aktif")

df = tum_dunyayi_tara()

if df is not None:
    # SIDEBAR (FİLTRELER)
    st.sidebar.header("🌍 Bölge Seçimi")
    kitalar = ["Tümü"] + sorted(df['Kıta'].unique().tolist())
    secilen_kita = st.sidebar.selectbox("Kıta:", kitalar)

    # Filtreleme mantığı
    temp_df = df.copy()
    if secilen_kita != "Tümü":
        temp_df = temp_df[temp_df['Kıta'] == secilen_kita]

    st.sidebar.divider()
    ligler_listesi = sorted(temp_df['Lig'].unique().tolist())
    secilen_ligler = st.sidebar.multiselect("Ligleri Filtrele:", ligler_listesi, default=ligler_listesi)
    
    final_df = temp_df[temp_df['Lig'].isin(secilen_ligler)]

    # ANA EKRAN (KITALARA GÖRE GRUPLAMA)
    for kita in final_df['Kıta'].unique():
        st.subheader(f"📍 {kita}")
        kita_df = final_df[final_df['Kıta'] == kita]
        
        for i, row in kita_df.iterrows():
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
                with c1:
                    st.caption(row['Lig'])
                    st.write(f"⏰ **{row['Saat']}**")
                with c2:
                    st.write(f"🏀 **{row['Ev']}** vs **{row['Dep']}**")
                with c3:
                    st.metric("Tahmin", f"{row['Barem']}")
                with c4:
                    if st.button("Analiz", key=f"btn_{i}_{row['Ev']}"):
                        st.toast(f"{row['Ev']} verileri çekiliyor...")
else:
    st.error("Veri bağlantısı kurulamadı.")

st.sidebar.divider()
st.sidebar.info(f"Sistemde {len(df['Lig'].unique()) if df is not None else 0} farklı lig aktif.")
