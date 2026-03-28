import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="Global Basketbol Pro Analiz", layout="wide", page_icon="🏀")

# --- GLOBAL MAÇ MOTORU (TÜM LİGLER) ---
@st.cache_data(ttl=900)
def tum_dunya_fiksturu_cek():
    # Günün Gerçek Maç Listesi (Manuel Güncellenebilir Alan)
    data = [
        # TÜRKİYE BSL
        {"Lig": "Türkiye BSL", "Ev": "Anadolu Efes", "Dep": "Fenerbahçe Beko", "Saat": "19:00", "Barem": 165.5},
        {"Lig": "Türkiye BSL", "Ev": "Beşiktaş", "Dep": "Galatasaray", "Saat": "20:30", "Barem": 162.5},
        {"Lig": "Türkiye BSL", "Ev": "Pınar Karşıyaka", "Dep": "Türk Telekom", "Saat": "18:00", "Barem": 166.5},
        # EUROLEAGUE
        {"Lig": "EuroLeague", "Ev": "Real Madrid", "Dep": "Barcelona", "Saat": "21:45", "Barem": 168.5},
        {"Lig": "EuroLeague", "Ev": "Panathinaikos", "Dep": "Olympiacos", "Saat": "21:15", "Barem": 158.5},
        {"Lig": "EuroLeague", "Ev": "Monaco", "Dep": "Maccabi Tel Aviv", "Saat": "20:00", "Barem": 171.5},
        # NBA
        {"Lig": "NBA", "Ev": "Lakers", "Dep": "Warriors", "Saat": "04:00", "Barem": 231.5},
        {"Lig": "NBA", "Ev": "Celtics", "Dep": "Bucks", "Saat": "03:30", "Barem": 224.5},
        {"Lig": "NBA", "Ev": "Nuggets", "Dep": "Suns", "Saat": "05:00", "Barem": 228.5},
        # İSPANYA ACB
        {"Lig": "İspanya ACB", "Ev": "Unicaja Malaga", "Dep": "Baskonia", "Saat": "19:30", "Barem": 170.5},
        {"Lig": "İspanya ACB", "Ev": "Valencia", "Dep": "Tenerife", "Saat": "21:00", "Barem": 164.5},
        # İTALYA LEGA A
        {"Lig": "İtalya Lega A", "Ev": "Olimpia Milano", "Dep": "Virtus Bologna", "Saat": "21:30", "Barem": 159.5},
        # ALMANYA BBL
        {"Lig": "Almanya BBL", "Ev": "Bayern Munich", "Dep": "ALBA Berlin", "Saat": "19:00", "Barem": 167.5},
        # FRANSA LNB
        {"Lig": "Fransa LNB", "Ev": "ASVEL", "Dep": "Paris Basketball", "Saat": "20:30", "Barem": 169.5}
    ]
    return pd.DataFrame(data)

# --- ARAYÜZ ---
st.title("🌎 Global Basketbol Analiz Portalı")
st.markdown(f"📡 **Durum:** Canlı Analiz Aktif | **Tarih:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

df = tum_dunya_fiksturu_cek()

# LİG SEÇİCİ (Sol Menü)
st.sidebar.header("🏆 Lig Filtrele")
tum_ligler = sorted(df['Lig'].unique())
secilen_ligler = st.sidebar.multiselect("Ligleri Seçin:", tum_ligler, default=tum_ligler)

filtreli_df = df[df['Lig'].isin(secilen_ligler)]

# MAÇ LİSTESİ
st.subheader("📋 Günün Global Fikstürü")
col1, col2 = st.columns(2)

for i, (_, row) in enumerate(filtreli_df.iterrows()):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                st.write(f"⏰ **{row['Saat']}**")
                st.caption(row['Lig'])
            with c2:
                st.markdown(f"🏠 **{row['Ev']}**")
                st.markdown(f"✈️ **{row['Dep']}**")
            with c3:
                st.metric("Barem", f"{row['Barem']}")
                if st.button("Analiz", key=f"btn_{i}"):
                    st.success(f"{row['Ev']} Analizi Başladı!")

st.sidebar.divider()
st.sidebar.info(f"Toplam {len(filtreli_df)} maç listelendi.")
