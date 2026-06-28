import streamlit as st
import plotly.express as px


def tampilkan_chart(gdf_tampil):

    st.subheader("📊 Statistik")

    # ==========================
    # TOP 5
    # ==========================

    top5 = (
        gdf_tampil
        .groupby("Kecamatan")["skor_potensi"]
        .mean()
        .reset_index()
        .sort_values(
            by="skor_potensi",
            ascending=False
        )
        .head(5)
    )

    fig = px.bar(

        top5,

        x="skor_potensi",

        y="Kecamatan",

        orientation="h",

        color="skor_potensi",

        color_continuous_scale="YlOrRd"

    )

    fig.update_layout(

        title="Top 5 Kecamatan",

        yaxis=dict(
            categoryorder="total ascending"
        ),

        height=450

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )