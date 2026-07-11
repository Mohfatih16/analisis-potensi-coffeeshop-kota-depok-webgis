import streamlit as st
import pandas as pd
import plotly.express as px


def tampilkan_chart(gdf_tampil, df_penduduk, kecamatan_pilih="Semua"):

    st.subheader("📊 Statistik")

    st.markdown("### 📈 Visualisasi Statistik")

    tab1, tab2, tab3 = st.tabs([
        "👥 Jumlah Penduduk",
        "🏙️ Kepadatan",
        "⭐ Skor Potensi"
    ])

# ==========================================================
# TOP 5 SKOR POTENSI
# ==========================================================

    top_n = 5

    top_skor = (
        gdf_tampil
        .groupby("Kecamatan")["skor_potensi"]
        .mean()
        .reset_index()
        .sort_values(
            by="skor_potensi",
            ascending=False
        )
        .head(top_n)
    )

    # ==========================================================
    # MENGIKUTI FILTER SIDEBAR
    # ==========================================================

    top_n = 5

    kec_filter = sorted(
        gdf_tampil["Kecamatan"].unique()
    )
    # ==========================================================
    # DATA PENDUDUK
    # ==========================================================

    st.markdown("### 👥 Data Kependudukan Kota Depok")

    st.caption("Sumber : Badan Pusat Statistik (BPS)")

    df_penduduk_tampil = df_penduduk[

        df_penduduk["Kecamatan"].isin(kec_filter)

    ]

    df_penduduk_tampil = df_penduduk_tampil.sort_values(

        by="Penduduk (Jiwa)",

        ascending=False

    )
# ==========================================================
# VISUALISASI STATISTIK
# ==========================================================

    with tab1:

        st.markdown("#### 👥 Jumlah Penduduk per Kecamatan")

        fig_penduduk = px.bar(

            df_penduduk_tampil.sort_values(
                by="Penduduk (Jiwa)"
            ),

            x="Penduduk (Jiwa)",

            y="Kecamatan",

            orientation="h",

            color="Penduduk (Jiwa)",

            color_continuous_scale="Blues",

            text="Penduduk (Jiwa)"

        )

        fig_penduduk.update_traces(

            texttemplate="%{text:,.0f}",

            textposition="outside",

            hovertemplate=
            "<b>%{y}</b><br>" +
            "Jumlah Penduduk : %{x:,.0f} Jiwa<extra></extra>"

        )

        fig_penduduk.update_layout(

            title="Distribusi Jumlah Penduduk",

            coloraxis_showscale=False,

            height=500,

            plot_bgcolor="white",

            paper_bgcolor="white",

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )

        )

        st.plotly_chart(
            fig_penduduk,
            use_container_width=True
        )

# ==========================================================
# TAB 2 - KEPADATAN PENDUDUK
# ==========================================================

    with tab2:

        st.markdown("#### 🏙️ Kepadatan Penduduk per Kecamatan")

        fig_kepadatan = px.bar(

            df_penduduk_tampil.sort_values(
                by="Kepadatan Penduduk (Jiwa/km²)"
            ),

            x="Kepadatan Penduduk (Jiwa/km²)",

            y="Kecamatan",

            orientation="h",

            color="Kepadatan Penduduk (Jiwa/km²)",

            color_continuous_scale="YlOrRd",

            text="Kepadatan Penduduk (Jiwa/km²)"

        )

        fig_kepadatan.update_traces(

            texttemplate="%{text:,.0f}",

            textposition="outside",

            hovertemplate=
            "<b>%{y}</b><br>" +
            "Kepadatan : %{x:,.0f} Jiwa/km²<extra></extra>"

        )

        fig_kepadatan.update_layout(

            title="Distribusi Kepadatan Penduduk",

            coloraxis_showscale=False,

            height=500,

            plot_bgcolor="white",

            paper_bgcolor="white",

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )

        )

        st.plotly_chart(
            fig_kepadatan,
            use_container_width=True
        )

# ==========================================================
# TAB 3 - SKOR POTENSI
# ==========================================================

    with tab3:

        st.markdown("#### ⭐ Top 5 Kecamatan Berdasarkan Skor Potensi")

        fig_potensi = px.bar(

        top_skor,

            x="skor_potensi",

            y="Kecamatan",

            orientation="h",

            color="skor_potensi",

            color_continuous_scale="YlOrRd",

            text="skor_potensi"

        )

        fig_potensi.update_traces(

            texttemplate="%{text:.3f}",

            textposition="outside",

            hovertemplate=
            "<b>%{y}</b><br>" +
            "Skor Potensi : %{x:.3f}<extra></extra>"

        )

        fig_potensi.update_layout(

            title="Top 5 Kecamatan Berdasarkan Skor Potensi",

            coloraxis_showscale=False,

            yaxis=dict(
                autorange="reversed"
            ),

            plot_bgcolor="white",

            paper_bgcolor="white",

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            ),

            height=500

        )

        st.plotly_chart(
            fig_potensi,
            use_container_width=True
        )

    # ==========================================================
    # TABEL
    # ==========================================================

    st.dataframe(

        df_penduduk_tampil,

        width="stretch",

        hide_index=True

    )