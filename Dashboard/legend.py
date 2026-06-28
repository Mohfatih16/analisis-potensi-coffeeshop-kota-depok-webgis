import streamlit as st


def tampilkan_legend():

    st.markdown("## ☕ Legenda")

    st.markdown("""
    <div style="
    background:#C62828;
    padding:15px;
    border-radius:10px;
    color:white;
    text-align:center;
    margin-bottom:10px;
    ">
    <b>🟥 Sangat Potensial</b><br>
    0.60 - 1.00
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:#EF6C00;
    padding:15px;
    border-radius:10px;
    color:white;
    text-align:center;
    margin-bottom:10px;
    ">
    <b>🟧 Potensial</b><br>
    0.45 - 0.60
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:#FBC02D;
    padding:15px;
    border-radius:10px;
    color:black;
    text-align:center;
    margin-bottom:10px;
    ">
    <b>🟨 Cukup Potensial</b><br>
    0.30 - 0.45
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:#ECECEC;
    padding:15px;
    border-radius:10px;
    color:black;
    text-align:center;
    margin-bottom:10px;
    ">
    <b>⬜ Rendah</b><br>
    0.00 - 0.30
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.info("""
📌 **Interpretasi**

Semakin merah warna grid,
semakin tinggi potensi
lokasi coffee shop.
""")