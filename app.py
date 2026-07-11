import streamlit as st

from streamlit_option_menu import option_menu

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

gdf, adm = load_data()

gdf_tampil, kecamatan_pilih, kategori_peta = sidebar_filter(gdf)

tampilkan_header()

# ===============================
# CARD
# ===============================
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
tampilkan_cards(gdf_tampil)
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
# ===============================
# MENU HORIZONTAL
# ===============================

selected = option_menu(
    menu_title=None,

    options=[
        "Peta",
        "Statistik",
        "Ranking"
    ],

    icons=[
        "map",
        "bar-chart",
        "trophy"
    ],

    default_index=0,

    orientation="horizontal",

    styles={

        "container":{

        "padding":"12px",

        "margin":"15px 0px 25px 0px",

        "background-color":"#F3ECE5",

        "border-radius":"12px"

    },

        "nav-link":{
            "font-size":"18px",
            "font-weight":"600",
            "text-align":"center",
            "color":"#5B3A29"
        },

        "nav-link-selected":{
            "background-color":"#8B5E3C",
            "color":"white",
            "border-radius":"10px"
        }

    }
)

# ===============================
# KONTEN
# ===============================

if selected == "Peta":
    tampilkan_peta(gdf_tampil, kategori_peta, adm)

# ===============================
# INSIGHT
# ===============================

#tampilkan_insight(
#   gdf_tampil,
#   kecamatan_pilih
#)