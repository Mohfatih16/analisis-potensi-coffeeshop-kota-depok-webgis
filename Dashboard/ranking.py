import streamlit as st
import pandas as pd


def tampilkan_ranking(gdf_tampil):

    st.subheader("🏆 Ranking Kecamatan")

    # ==================================================
    # FILTER
    # ==================================================

    col1, col2 = st.columns([2, 1])

    with col1:

        ranking_pilih = st.selectbox(
            "Urutkan Berdasarkan",
            (
                "Skor Potensi",
                "Kepadatan Penduduk",
                "Fasilitas Pendidikan",
                "Kompetitor Coffee Shop"
            )
        )

    with col2:

        cari = st.text_input(
            "🔍 Cari Kecamatan",
            placeholder="Contoh : Beji"
        )

    # ==================================================
    # MENENTUKAN KOLOM
    # ==================================================

    if ranking_pilih == "Skor Potensi":

        kolom = "skor_potensi"
        nama_kolom = "Skor Potensi"

    elif ranking_pilih == "Kepadatan Penduduk":

        kolom = "Kepadatan Penduduk (Jiwa/km²)"
        nama_kolom = "Kepadatan Penduduk"

    elif ranking_pilih == "Fasilitas Pendidikan":

        kolom = "jumlah_pendidikan_700m"
        nama_kolom = "Fasilitas Pendidikan"

    else:

        kolom = "jumlah_kompetitor_700m"
        nama_kolom = "Kompetitor Coffee Shop"

    # ==================================================
    # MEMBUAT RANKING
    # ==================================================

    ranking = (
        gdf_tampil
        .groupby("Kecamatan", as_index=False)[kolom]
        .mean()
        .sort_values(
            by=kolom,
            ascending=False
        )
    )

    # ==================================================
    # SEARCH
    # ==================================================

    if cari:

        ranking = ranking[
            ranking["Kecamatan"]
            .str.contains(
                cari,
                case=False,
                na=False
            )
        ]

    # ==================================================
    # MEMBUAT RANK
    # ==================================================

    rank = []

    for i in range(len(ranking)):

        if i == 0:
            rank.append("🥇")

        elif i == 1:
            rank.append("🥈")

        elif i == 2:
            rank.append("🥉")

        else:
            rank.append(i + 1)

    ranking.insert(
        0,
        "Rank",
        rank
    )

    # ==================================================
    # MEMBUAT KATEGORI
    # ==================================================

    q1 = ranking[kolom].quantile(0.25)
    q2 = ranking[kolom].quantile(0.50)
    q3 = ranking[kolom].quantile(0.75)

    kategori = []

    for nilai in ranking[kolom]:

        if nilai >= q3:

            kategori.append("🔴 Sangat Potenisial")

        elif nilai >= q2:

            kategori.append("🟠 Potensial")

        elif nilai >= q1:

            kategori.append("🟡 Sedang")

        else:

            kategori.append("⚪ Rendah")

    ranking["Kategori"] = kategori

    # ==================================================
    # FORMAT ANGKA
    # ==================================================

    if kolom == "skor_potensi":

        ranking[kolom] = ranking[kolom].round(3)

    else:

        ranking[kolom] = ranking[kolom].round(0).astype(int)

    ranking = ranking.rename(
        columns={
            kolom: nama_kolom
        }
    )

    # ==================================================
    # DOWNLOAD
    # ==================================================

    csv = ranking.to_csv(index=False)

    st.download_button(
        "📥 Download Ranking",
        csv,
        "Ranking_Kecamatan.csv",
        "text/csv"
    )

    # ==================================================
    # TABEL
    # ==================================================

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )