import streamlit as st


def sidebar_filter(gdf):

    # =====================================
    # HEADER
    # =====================================

    st.sidebar.markdown("Dashboard")
    st.sidebar.caption("Sistem Informasi Geografis Analisis Potensi Coffee Shop Kota Depok")

    st.sidebar.divider()

    # =====================================
    # FILTER
    # =====================================

    st.sidebar.subheader("📍 Filter")

    kecamatan = ["Semua"] + sorted(gdf["Kecamatan"].unique())

    kecamatan_pilih = st.sidebar.selectbox(
        "Pilih Kecamatan",
        kecamatan
    )

    kategori_peta = st.sidebar.selectbox(
        "Kategori Peta",
        [
            "Skor Potensi",
            "Kepadatan Penduduk",
            "Fasilitas Pendidikan",
            "Kompetitor Coffee Shop"
        ]
    )

    # =====================================
    # FILTER DATA
    # =====================================

    if kecamatan_pilih == "Semua":
        gdf_tampil = gdf.copy()
    else:
        gdf_tampil = gdf[gdf["Kecamatan"] == kecamatan_pilih]

    # =====================================
    # INFORMASI DATA
    # =====================================

    st.sidebar.divider()

    st.sidebar.subheader("📊 Informasi")

    st.sidebar.metric(
        "Jumlah Grid",
        len(gdf_tampil)
    )

    st.sidebar.metric(
        "Jumlah Kecamatan",
        gdf_tampil["Kecamatan"].nunique()
    )

    # =====================================
    # TENTANG DASHBOARD
    # =====================================

    st.sidebar.divider()

    st.sidebar.info(
        """
Dashboard ini digunakan untuk
menganalisis potensi lokasi
Coffee Shop di Kota Depok
menggunakan analisis spasial.
"""
    )

    st.sidebar.divider()

    st.sidebar.caption("© 2026")
    st.sidebar.caption("Universitas Ibn Khaldun")

    return (
        gdf_tampil,
        kecamatan_pilih,
        kategori_peta
    )