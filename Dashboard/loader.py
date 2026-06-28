import geopandas as gpd
import streamlit as st


@st.cache_data
def load_data():
    """
    Membaca seluruh data yang digunakan pada WebGIS.
    """

    # ==========================
    # DATA ANALISIS
    # ==========================

    gdf = gpd.read_file(
        "Data/Analisis_Potensial_Coffe_Shop_Depok.geojson"
    )

    # ==========================
    # BATAS ADMINISTRASI
    # ==========================

    adm = gpd.read_file(
        "Data/Adm_Kota_Depok.geojson"
    )

    return gdf, adm
