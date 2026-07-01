import streamlit as st
import tempfile
import os

from Dashboard.map_view import buat_peta


def tampilkan_download(gdf, adm, kategori_peta):

    st.subheader("📥 Download Hasil Analisis")

    col1, col2, col3 = st.columns(3)

    # ======================
    # CSV
    # ======================

    with col1:

        csv = gdf.drop(columns="geometry").to_csv(index=False)

        st.download_button(

            "⬇ Download CSV",

            csv,

            file_name="Analisis_CoffeeShop_Depok.csv",

            mime="text/csv",

            use_container_width=True

        )

    # ======================
    # GEOJSON
    # ======================

    with col2:

        geojson = gdf.to_json()

        st.download_button(

            "🌍 Download GeoJSON",

            geojson,

            file_name="Analisis_CoffeeShop_Depok.geojson",

            mime="application/geo+json",

            use_container_width=True

        )

    # ======================
    # HTML MAP
    # ======================

    with col3:

        m = buat_peta(

            gdf,

            kategori_peta,

            adm

        )

        html = m.get_root().render()

        st.download_button(

            "🗺 Download HTML",

            html,

            file_name="Peta_Analisis_CoffeeShop_Depok.html",

            mime="text/html",

            use_container_width=True

        )