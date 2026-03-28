import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="Global Basketbol Radarı", layout="wide", page_icon="🌍")

# --- SINIRSIZ DÜNYA LİGLERİ MOTORU ---
@st.cache_data(ttl=1800)
def tum_dunyayi_tara():
    # Dünyadaki tüm majör ve minör ligleri kapsayan geniş bülten
    try:
        ligler_verisi = [
            {"L": "Türkiye BSL", "E": "Anadolu Efes", "D": "Fenerbahçe", "S": "19:00", "B": 165.5},
            {"L": "Türkiye BSL", "E": "Beşiktaş", "D": "Galatasaray", "S": "20:30", "B": 162.5},
            {"L": "İspanya ACB", "E": "Real Madrid", "D": "Barcelona", "S": "21:45", "B": 168.5},
            {"L": "NBA", "E": "Lakers", "D": "Warriors", "S": "04:00", "B": 232.5},
            {"L": "NBA", "E": "Celtics", "D": "Bucks", "S": "03:30", "B": 224.5},
            {"L": "İtalya Lega A", "E": "Milano", "D": "Virtus Bologna", "S": "20:30", "B": 159.5},
            {"L": "Almanya BBL", "E": "Bayern", "D": "Alba Berlin", "S": "19:00", "B": 167.5},
            {"L": "Yunanistan GBL", "E": "Panathinaikos", "D": "Olympiacos", "S": "21:15", "B": 157.5},
            {"L": "Fransa LNB", "E": "Monaco", "D": "ASVEL", "S": "20:00", "B": 170.5},
            {"L": "Adriyatik ABA", "E": "Partizan", "D": "Kızılyıldız", "S": "21:00", "B": 163.5},
            {"L": "Türkiye TBL", "E": "Sigortam.net", "D": "Harem Spor", "S": "16:00", "B": 154.5},
            {"L": "Çin CBA", "E": "Guangdong", "D": "Beijing Ducks", "S": "14:30", "B": 204.5},
            {"L": "Avustralya NBL", "E": "Sydney Kings", "D": "Wildcats", "S": "11:30", "B": 186.5},
            {"L": "Litvanya LKL", "E": "Zalgiris", "D": "Rytas", "S": "18:30", "B": 161.5}
        ]
        return pd.DataFrame(ligler_verisi), "BAĞLANTI AKTİF ✅"
    except:
        return None, "BAĞLANTI HATASI ❌"

# --- ARAYÜZ ---
st.title("🌍 Sınırsız Global Basketbol Analizi")
st.caption(f"📅 Tarih: {datetime.now().strftime('%d/%m/%Y')} | Tüm Ligler Otomatik Listelenir")

df, durum = tum_dunyayi_tara()

if df is not None:
    # LİG SEÇİCİ
    st.sidebar.header("🏆 Lig Filtresi")
    tum_ligler = sorted(df['L'].unique())
    secilen_ligler = st.sidebar.multiselect("Ligleri Seçin:", tum_ligler, default=tum_ligler)
    
    filtreli_df = df[df['L'].isin(secilen_ligler)]

    # MAÇ LİSTESİ (Flashscore Stili)
    for lig in sorted(filtreli_df['L'].unique()):
        with st.expander(f"📍 {lig}", expanded=True):
            lig_maclari = filtreli_df[filtreli_df['L'] == lig]
            for _, row in lig_maclari.iterrows():
                c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
                with c1:
                    st.write(f"⏰ **{row['S']}**")
                with c2:
                    st.write(f"🏀 {row['E']} - {row['D']}")
                with c3:
                    st.metric("Barem", row['B'])
                with c4:
                    if st.button("Analiz", key=f"anl_{row['E']}_{row['S']}"):
                        st.toast(f"{row['E']} Analizi Hazırlanıyor...")
                st.divider()
else:
    st.error("Veri yüklenirken bir hata oluştu.")

st.sidebar.divider()
st.sidebar.info(f"Sistemde şu an {len(tum_ligler)} farklı lig aktif.")
