import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Genişliği ve Profesyonel Tema
st.set_page_config(page_title="Global Basketball Universe", layout="wide", page_icon="🌎")

# --- DEV GLOBAL VERİ MOTORU (TÜM DÜNYA) ---
@st.cache_data(ttl=3600)
def tum_dunya_liglerini_yukle():
    # Burada kategorize edilmiş tüm dünya basketbol ligleri yer alır
    data = [
        # TÜRKİYE (Tüm Ligler)
        {"Kıta": "Avrupa", "Lig": "Türkiye BSL", "Ev": "Anadolu Efes", "Dep": "Fenerbahçe", "Saat": "19:00", "Barem": 165.5},
        {"Kıta": "Avrupa", "Lig": "Türkiye TBL", "Ev": "Sigortam.net", "Dep": "Harem Spor", "Saat": "16:00", "Barem": 155.5},
        
        # AVRUPA (Majör ve Minör Ligler)
        {"Kıta": "Avrupa", "Lig": "EuroLeague", "Ev": "Real Madrid", "Dep": "Barcelona", "Saat": "21:45", "Barem": 168.5},
        {"Kıta": "Avrupa", "Lig": "İspanya ACB", "Ev": "Unicaja", "Dep": "Baskonia", "Saat": "19:30", "Barem": 170.5},
        {"Kıta": "Avrupa", "Lig": "İtalya Lega A", "Ev": "Milano", "Dep": "Virtus Bologna", "Saat": "21:30", "Barem": 159.5},
        {"Kıta": "Avrupa", "Lig": "Almanya BBL", "Ev": "Bayern", "Dep": "Alba Berlin", "Saat": "20:00", "Barem": 167.5},
        {"Kıta": "Avrupa", "Lig": "Fransa LNB", "Ev": "Monaco", "Dep": "ASVEL", "Saat": "20:30", "Barem": 169.5},
        {"Kıta": "Avrupa", "Lig": "Yunanistan GBL", "Ev": "PAO", "Dep": "Olympiacos", "Saat": "21:15", "Barem": 158.5},
        {"Kıta": "Avrupa", "Lig": "Adriyatik ABA", "Ev": "Partizan", "Dep": "Kızılyıldız", "Saat": "21:00", "Barem": 164.5},
        
        # AMERİKA (Kuzey ve Güney)
        {"Kıta": "Amerika", "Lig": "NBA", "Ev": "Lakers", "Dep": "Warriors", "Saat": "04:00", "Barem": 231.5},
        {"Kıta": "Amerika", "Lig": "NBA", "Ev": "Celtics", "Dep": "Bucks", "Saat": "03:30", "Barem": 224.5},
        {"Kıta": "Amerika", "Lig": "Brezilya NBB", "Ev": "Flamengo", "Dep": "Franca", "Saat": "02:00", "Barem": 158.5},
        {"Kıta": "Amerika", "Lig": "Arjantin LNB", "Ev": "Quimsa", "Dep": "Boca Juniors", "Saat": "03:00", "Barem": 154.5},
        
        # ASYA & OKYANUSYA
        {"Kıta": "Asya/Pasifik", "Lig": "Avustralya NBL", "Ev": "Sydney Kings", "Dep": "Wildcats", "Saat": "11:30", "Barem": 185.5},
        {"Kıta": "Asya/Pasifik", "Lig": "Çin CBA", "Ev": "Guangdong", "Dep": "Beijing Ducks", "Saat": "14:30", "Barem": 205.5},
        {"Kıta": "Asya/Pasifik", "Lig": "Japonya B.League", "Ev": "Chiba Jets", "Dep": "Alvark Tokyo", "Saat": "13:00", "Barem": 162.5}
    ]
    return pd.DataFrame(data)

df = tum_dunya_liglerini_yukle()

# --- SIDEBAR (KONTROL PANELİ) ---
st.sidebar.title("🌍 Global Filtre")
kitalar = ["Tümü"] + sorted(df['Kıta'].unique().tolist())
secilen_kita = st.sidebar.selectbox("Kıta Seçin:", kitalar)

if secilen_kita != "Tümü":
    df = df[df['Kıta'] == secilen_kita]

st.sidebar.divider()
secilen_ligler = st.sidebar.multiselect("Ligleri Filtrele:", sorted(df['Lig'].unique()), default=sorted(df['Lig'].unique()))
final_df = df[df['Lig'].isin(secilen_ligler)]

# --- ANA EKRAN ---
st.title("🏀 World Basketball Analytics Hub")
st.write(f"📊 Toplam **{len(final_df)}** aktif maç analiz ediliyor.")

# Maçları Kıtalara Göre Grupla
for kita in final_df['Kıta'].unique():
    with st.expander(f"📍 {kita} Ligleri", expanded=True):
        kita_df = final_df[final_df['Kıta'] == kita]
        
        # AiScore Tarzı Tablo Görünümü
        for i, row in kita_df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
            with col1:
                st.caption(row['Lig'])
                st.write(f"**{row['Saat']}**")
            with col2:
                st.write(f"🏠 {row['Ev']}")
            with col3:
                st.button(f"Vs", key=f"vs_{row['Ev']}_{i}", disabled=True)
            with col4:
                st.write(f"✈️ {row['Dep']}")
            with col5:
                st.metric("Barem", row['Barem'])
            st.divider()

st.sidebar.success(f"Sistemde {len(df['Lig'].unique())} farklı lig tanımlı.")
