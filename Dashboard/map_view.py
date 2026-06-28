import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import (
    MiniMap,
    MousePosition
)

def tampilkan_peta(gdf_tampil, kategori_peta, adm):

    # =====================================
    # PILIH KOLOM
    # =====================================

    if kategori_peta == "Skor Potensi":
        kolom = "skor_potensi"

    elif kategori_peta == "Kepadatan Penduduk":
        kolom = "Kepadatan Penduduk (Jiwa/km²)"

    elif kategori_peta == "Fasilitas Pendidikan":
        kolom = "jumlah_pendidikan_700m"

    elif kategori_peta == "Kompetitor Coffee Shop":
        kolom = "jumlah_kompetitor_700m"

    st.subheader(f"🗺️ Peta {kategori_peta}")

    # =====================================
    # MEMBUAT PETA
    # =====================================

    m = folium.Map(
        location=[-6.39, 106.82],
        zoom_start=11,
        tiles=None
    )



# =====================================
# ZOOM OTOMATIS
# =====================================

    xmin, ymin, xmax, ymax = gdf_tampil.total_bounds

    m.fit_bounds(
    [
        [ymin, xmin],
        [ymax, xmax]
    ]
)

    # =====================================
    # BASEMAP
    # =====================================

    folium.TileLayer(
        "OpenStreetMap",
        name="OpenStreetMap"
    ).add_to(m)

    folium.TileLayer(
        "CartoDB positron",
        name="Light"
    ).add_to(m)

    folium.TileLayer(
        "CartoDB dark_matter",
        name="Dark"
    ).add_to(m)

    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Satellite",
        overlay=False,
        control=True
    ).add_to(m)

 # =====================================
# BATAS ADMINISTRASI
# =====================================

    folium.GeoJson(

    adm,

    name="Batas Administrasi",

    style_function=lambda feature: {
        "fillColor": "transparent",
        "color": "#2C3E50",
        "weight": 3,
        "opacity": 1,
        "fillOpacity": 0
    },

    highlight_function=lambda feature: {
        "color": "#E74C3C",
        "weight": 5,
        "fillOpacity": 0.1
    },

    tooltip=folium.GeoJsonTooltip(

        fields=["NAMOBJ"],

        aliases=["🏘 Kecamatan"],

        sticky=False,

        labels=True

    )

).add_to(m)

    # =====================================
    # CHOROPLETH
    # =====================================

    folium.Choropleth(

    geo_data=gdf_tampil,

    data=gdf_tampil,

    columns=["h3_polyfill", kolom],

    key_on="feature.properties.h3_polyfill",

    fill_color="YlOrRd",

    fill_opacity=0.8,

    line_opacity=0.2,

    legend_name=None

    ).add_to(m)

    # =====================================
    # TOOLTIP HEXAGON
    # =====================================

    folium.GeoJson(

        gdf_tampil,

        style_function=lambda feature: {
            "fillOpacity": 0,
            "color": "transparent",
            "weight": 0
        },

        highlight_function=lambda feature: {
            "fillColor": "#3498DB",
            "color": "#000000",
            "weight": 2,
            "fillOpacity": 0.5
        },

        tooltip=folium.GeoJsonTooltip(

            fields=[
                "Kecamatan",
                "skor_potensi",
                "Kepadatan Penduduk (Jiwa/km²)",
                "jumlah_pendidikan_700m",
                "jumlah_kompetitor_700m"
            ],

            aliases=[
                "🏘 Kecamatan",
                "⭐ Skor Potensi",
                "👥 Kepadatan Penduduk",
                "🏫 Fasilitas Pendidikan",
                "☕ Kompetitor"
            ],

            localize=True,
            sticky=False
        )

    ).add_to(m)

# =====================================
# MINI MAP
# =====================================

    MiniMap(

    toggle_display=True,

    position="bottomright",

    width=150,

    height=150,

    zoom_level_offset=-5

    ).add_to(m)

# =====================================
# MOUSE POSITION
# =====================================

    MousePosition(

    position="bottomleft",

    prefix="📍 Koordinat",

    separator=" | ",

    num_digits=5,

    lng_first=False

    ).add_to(m)

    # =====================================
    # LAYER CONTROL
    # =====================================

    folium.LayerControl(
        collapsed=False
    ).add_to(m)


    st_folium(
        m,
        width=None,
        height=650
    )