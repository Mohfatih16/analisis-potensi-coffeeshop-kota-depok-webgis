import streamlit as st


def tampilkan_cards(gdf):

    total_grid = len(gdf)
    total_kecamatan = gdf["Kecamatan"].nunique()
    skor_max = gdf["skor_potensi"].max()
    skor_avg = gdf["skor_potensi"].mean()

    cards = [

        {
            "icon":"📍",
            "title":"Jumlah Grid",
            "value":f"{total_grid:,}",
            "subtitle":"Total Grid Analisis"
        },

        {
            "icon":"🏘️",
            "title":"Kecamatan",
            "value":total_kecamatan,
            "subtitle":"Wilayah Analisis"
        },

        {
            "icon":"⭐",
            "title":"Skor Maksimum",
            "value":f"{skor_max:.3f}",
            "subtitle":"Potensi Tertinggi"
        },

        {
            "icon":"📈",
            "title":"Rata-rata Skor",
            "value":f"{skor_avg:.3f}",
            "subtitle":"Nilai Potensi"
        }

    ]

    cols = st.columns(4)

    for col, card in zip(cols, cards):

        with col:

            st.markdown(f"""
<div class="metric-card">

<div class="metric-header">

<span class="metric-icon">
{card['icon']}
</span>

<span class="metric-title">
{card['title']}
</span>

</div>

<div class="metric-divider"></div>

<div class="metric-value">

{card['value']}

</div>

<div class="metric-subtitle">

{card['subtitle']}

</div>

</div>
""", unsafe_allow_html=True)