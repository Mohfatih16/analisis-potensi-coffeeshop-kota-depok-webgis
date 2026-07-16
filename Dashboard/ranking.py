import streamlit as st
import plotly.express as px

# ==================================================
# WARNA KATEGORI (dipakai di bar chart & donut chart)
# ==================================================

WARNA_KATEGORI = {
    "🔴 Sangat Potensial": "#C0392B",
    "🟠 Potensial": "#E67E22",
    "🟡 Sedang": "#F1C40F",
    "⚪ Rendah": "#BDC3C7"
}


def tampilkan_ranking(gdf_tampil):

    st.subheader("🏆 Ranking Kecamatan")

    # ==================================================
    # FILTER
    # ==================================================

    OPSI_TAMPILAN = [
        "Diagram Batang",
        "Diagram Donut",
        "Tabel Data"
    ]

    col1, col2 = st.columns([2, 1])

    with col1:

        tampilan_dipilih = st.selectbox(
            "Urutkan Tampilan",
            OPSI_TAMPILAN,
            key="ranking_tampilan_filter"
        )

    with col2:

        ranking_pilih = st.selectbox(
            "Urutkan Berdasarkan",
            (
                "Skor Potensi",
                "Kepadatan Penduduk",
                "Fasilitas Pendidikan",
                "Kompetitor Coffee Shop"
            )
        )

    daftar_kecamatan = sorted(gdf_tampil["Kecamatan"].unique())

    if "ranking_kecamatan_filter" not in st.session_state:

        st.session_state.ranking_kecamatan_filter = daftar_kecamatan

    else:

        # Jaga-jaga kalau filter sidebar mengubah daftar kecamatan yang
        # tersedia, supaya value yang tersimpan tidak jadi tidak valid.
        st.session_state.ranking_kecamatan_filter = [
            k for k in st.session_state.ranking_kecamatan_filter
            if k in daftar_kecamatan
        ]

    jumlah_dipilih = len(st.session_state.ranking_kecamatan_filter)
    jumlah_total = len(daftar_kecamatan)

    with st.expander(
        f" Filter Kecamatan ({jumlah_dipilih}/{jumlah_total})",
        expanded=False
    ):

        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:

            if st.button("Pilih Semua", use_container_width=True):

                st.session_state.ranking_kecamatan_filter = daftar_kecamatan
                st.rerun()

        with btn_col2:

            if st.button("Hapus Semua", use_container_width=True):

                st.session_state.ranking_kecamatan_filter = []
                st.rerun()

        kecamatan_dipilih = st.multiselect(
            "Pilih Kecamatan",
            options=daftar_kecamatan,
            key="ranking_kecamatan_filter",
            label_visibility="collapsed"
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
    # MEMBUAT RANKING SEMUA KECAMATAN
    # ==================================================

    ranking = (
        gdf_tampil
        .groupby("Kecamatan", as_index=False)[kolom]
        .mean()
        .sort_values(
            by=kolom,
            ascending=False
        )
        .reset_index(drop=True)
    )

    # ==================================================
    # MEMBUAT KATEGORI (SEBELUM SEARCH)
    # ==================================================

    q1 = ranking[kolom].quantile(0.25)
    q2 = ranking[kolom].quantile(0.50)
    q3 = ranking[kolom].quantile(0.75)

    kategori = []

    for nilai in ranking[kolom]:

        if nilai >= q3:

            kategori.append("🔴 Sangat Potensial")

        elif nilai >= q2:

            kategori.append("🟠 Potensial")

        elif nilai >= q1:

            kategori.append("🟡 Sedang")

        else:

            kategori.append("⚪ Rendah")

    ranking["Kategori"] = kategori

    # ==================================================
    # FILTER KECAMATAN
    # ==================================================
    # Filter ini berlaku untuk bar chart, donut chart, dan tabel
    # sekaligus, supaya ketiganya selalu konsisten menampilkan
    # kecamatan yang sama.

    if kecamatan_dipilih:

        ranking = ranking[
            ranking["Kecamatan"].isin(kecamatan_dipilih)
        ].reset_index(drop=True)

    else:

        ranking = ranking.iloc[0:0].reset_index(drop=True)

    # Donut chart mengikuti hasil filter yang sama dengan bar chart & tabel
    ranking_full = ranking.copy()

    if ranking.empty:

        st.warning("⚠️ Pilih minimal satu kecamatan pada filter untuk menampilkan data.")

        return

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
    # FILTER TAMPILAN (Tabel / Diagram Batang / Diagram Donut)
    # ==================================================
    # Filter ini menentukan komponen mana saja yang ditampilkan,
    # supaya tampilan tidak penuh sesak kalau ketiganya sekaligus
    # tidak diperlukan.

    tampil_bar = tampilan_dipilih == "Diagram Batang"
    tampil_donut = tampilan_dipilih == "Diagram Donut"
    tampil_tabel = tampilan_dipilih == "Tabel Data"

    # ==================================================
    # DIAGRAM RANKING & DISTRIBUSI KATEGORI
    # ==================================================

    if tampil_bar or tampil_donut:

        st.markdown("###  Visualisasi Ranking")

        col_bar = st.container() if tampil_bar else None
        col_donut = st.container() if tampil_donut else None

        # ---------- BAR CHART RANKING ----------
        if tampil_bar:

            with col_bar:

                st.markdown(f"##### Ranking Kecamatan Berdasarkan {nama_kolom}")

                fig_bar = px.bar(
                    ranking.sort_values(by=nama_kolom),
                    x=nama_kolom,
                    y="Kecamatan",
                    orientation="h",
                    color="Kategori",
                    color_discrete_map=WARNA_KATEGORI,
                    text=nama_kolom
                )

                fig_bar.update_traces(
                    texttemplate="%{text:,.2f}" if kolom == "skor_potensi" else "%{text:,.0f}",
                    textposition="outside",
                    hovertemplate=
                    "<b>%{y}</b><br>" +
                    f"{nama_kolom} : " + "%{x:,.2f}<extra></extra>"
                )

                fig_bar.update_layout(
                    height=max(350, 38 * len(ranking)),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    legend_title_text="Kategori",
                    margin=dict(l=20, r=20, t=20, b=20)
                )

                st.plotly_chart(fig_bar, use_container_width=True)

        # ---------- DONUT CHART PER KECAMATAN ----------
        if tampil_donut:

            with col_donut:

                st.markdown(f"##### Kontribusi {nama_kolom} per Kecamatan")

                donut_data = ranking_full.sort_values(
                    by=kolom,
                    ascending=False
                )

                fig_donut = px.pie(
                    donut_data,
                    names="Kecamatan",
                    values=kolom,
                    hole=0.55,
                    color="Kategori",
                    color_discrete_map=WARNA_KATEGORI
                )

                fig_donut.update_traces(
                    textinfo="label+percent",
                    textposition="outside",
                    hovertemplate=
                    "<b>%{label}</b><br>" +
                    f"{nama_kolom} : " + "%{value:,.2f}<br>Persentase : %{percent}<extra></extra>"
                )

                fig_donut.update_layout(
                    showlegend=False,
                    height=max(420, 38 * len(ranking)),
                    margin=dict(l=40, r=40, t=20, b=60),
                    annotations=[dict(
                        text=f"{len(ranking_full)}<br>Kecamatan",
                        x=0.5, y=0.5,
                        font_size=16,
                        showarrow=False
                    )]
                )

                st.plotly_chart(fig_donut, use_container_width=True)

    # ==================================================
    # TABEL
    # ==================================================

    if tampil_tabel:

        st.markdown("Tabel Data Ranking")

        tinggi_tabel = min(38 * (len(ranking) + 1) + 3, 600)

        st.dataframe(
            ranking,
            use_container_width=True,
            hide_index=True,
            height=tinggi_tabel,
            column_config={
                "Rank": st.column_config.Column(width="small"),
                "Kecamatan": st.column_config.Column(width="medium"),
                nama_kolom: st.column_config.Column(width="small"),
                "Kategori": st.column_config.Column(width="medium"),
            }
        )

    # ==================================================
    # DOWNLOAD
    # ==================================================

    csv = ranking.to_csv(index=False)

    st.download_button(
        "Download Ranking",
        csv,
        "Ranking_Kecamatan.csv",
        "text/csv",
        use_container_width=True
    )