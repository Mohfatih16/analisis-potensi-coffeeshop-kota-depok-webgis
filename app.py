import streamlit as st

from Dashboard.loader import load_data
from Dashboard.style import load_css
from Dashboard.sidebar import sidebar_filter
from Dashboard.cards import tampilkan_cards
from Dashboard.map_view import tampilkan_peta
from Dashboard.ranking import tampilkan_ranking
#from Dashboard.insight import tampilkan_insight
from Dashboard.charts import tampilkan_chart
from Dashboard.header import tampilkan_header

st.set_page_config(
    page_title="WebGIS Coffee Shop",
    layout="wide"
)

load_css()

gdf, adm, df_penduduk = load_data()

gdf_tampil, kecamatan_pilih, kategori_peta = sidebar_filter(gdf)

tampilkan_header()

# ===============================
# CARD
# ===============================
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
tampilkan_cards(gdf_tampil)
st.markdown("<div style='height:55px'></div>", unsafe_allow_html=True)
# ===============================
# MENU HORIZONTAL
# ===============================
# Pakai st.button native (bukan streamlit-option-menu) supaya tampilannya
# bisa dikontrol penuh lewat CSS di style.py (termasuk full width, tanpa
# celah kosong di kanan) dan tidak terkendala iframe komponen pihak ketiga.

if "menu_aktif" not in st.session_state:
    st.session_state.menu_aktif = "Peta"

menu_items = [
    ("Peta", "🗺️"),
    ("Statistik", "📊"),
    ("Ranking", "🏆")
]

with st.container(key="menu_bar"):

    c1, c2, c3 = st.columns(3)

    for col, (label, icon) in zip([c1, c2, c3], menu_items):

        with col:

            aktif = st.session_state.menu_aktif == label

            if st.button(
                f"{icon}  {label}",
                key=f"menu_{label}",
                type="primary" if aktif else "secondary",
                width="stretch"
            ):
                st.session_state.menu_aktif = label
                st.rerun()

selected = st.session_state.menu_aktif

# ===============================
# KONTEN
# ===============================

if selected == "Peta":

    tampilkan_peta(
        gdf_tampil,
        kategori_peta,
        adm
    )

elif selected == "Statistik":

    tampilkan_chart(
        gdf_tampil,
        df_penduduk,
        kecamatan_pilih
    )

elif selected == "Ranking":

    tampilkan_ranking(
        gdf_tampil
    )

# ===============================
# INSIGHT
# ===============================

#tampilkan_insight(
#   gdf_tampil,
#   kecamatan_pilih
#)