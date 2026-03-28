import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="Global Basketbol Radarı", layout="wide", page_icon="🌎")

# --- GLOBAL VERİ MOTORU (KITALAR VE TÜM LİGLER) ---
@st.cache_data(ttl=1800)
def tum_dunyayi_tara():
    # Dünyadaki tüm liglerin kategorize edilmiş listesi
    try:
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
            {"Kıta": "Asya/Pasifik", "Lig": "Japonya B.League", "Ev": "Chiba Jets", "Dep": "Alvark Tokyo", "Saat": "13:00", "B
