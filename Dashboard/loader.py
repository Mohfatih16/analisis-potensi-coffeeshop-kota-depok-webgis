import geopandas as gpd
import pandas as pd
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

    # ==========================
    # DATA KEPENDUDUKAN (BPS)
    # ==========================

    df_penduduk = pd.read_csv(
        "Data/Data_Kepadatan_Depok.csv",
        encoding="utf-8-sig"
    )

    return gdf, adm, df_penduduk
