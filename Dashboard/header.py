import streamlit as st

def tampilkan_header():

    st.markdown("""
<div class="hero">

<div class="hero-title">
Analisis Potensi Coffee Shop Kota Depok
</div>

<div class="hero-subtitle">
Dashboard Analisis Spasial untuk menentukan lokasi potensial
pengembangan coffee shop menggunakan pendekatan Geospatial
Information Technology.
</div>

<div class="hero-info">

<div class="hero-box">
📍<br>
<b>Kota Depok</b>
</div>

<div class="hero-box">
📅<br>
<b>Tahun 2025</b>
</div>

<div class="hero-box">
🧠<br>
<b>Random Forest</b>
</div>

<div class="hero-box">
🗺️<br>
<b>11 Kecamatan</b>
</div>

</div>

</div>
""", unsafe_allow_html=True)