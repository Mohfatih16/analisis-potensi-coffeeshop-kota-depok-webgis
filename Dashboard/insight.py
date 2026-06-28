import streamlit as st


def tampilkan_insight(gdf_tampil, kecamatan_pilih):

    st.subheader("💡 Insight Analisis")

    # ==========================
    # Semua Kecamatan
    # ==========================

    if kecamatan_pilih == "Semua":

        ranking = (
            gdf_tampil
            .groupby("Kecamatan")["skor_potensi"]
            .mean()
            .sort_values(ascending=False)
        )

        terbaik = ranking.index[0]
        skor = ranking.iloc[0]

        st.success(f"""
### 🏆 Kecamatan Terbaik

**{terbaik}**

⭐ Skor Rata-rata : **{skor:.3f}**

🗺️ Jumlah Grid : **{len(gdf_tampil)}**

🏘️ Jumlah Kecamatan : **{gdf_tampil['Kecamatan'].nunique()}**
""")

        st.info(f"""
### 📌 Kesimpulan

Berdasarkan hasil analisis spasial,
**Kecamatan {terbaik}**
memiliki rata-rata skor potensi tertinggi.

Wilayah ini direkomendasikan
sebagai lokasi prioritas
pengembangan coffee shop.
""")

    # ==========================
    # Kecamatan tertentu
    # ==========================

    else:

        skor = gdf_tampil["skor_potensi"].mean()

        kepadatan = gdf_tampil[
            "Kepadatan Penduduk (Jiwa/km²)"
        ].mean()

        pendidikan = gdf_tampil[
            "jumlah_pendidikan_700m"
        ].mean()

        kompetitor = gdf_tampil[
            "jumlah_kompetitor_700m"
        ].mean()

        st.success(f"""
### 📍 Kecamatan

**{kecamatan_pilih}**

⭐ Skor Potensi : **{skor:.3f}**

👥 Kepadatan : **{kepadatan:,.0f} jiwa/km²**

🏫 Pendidikan : **{pendidikan:.0f}**

☕ Kompetitor : **{kompetitor:.0f}**
""")

        if skor >= 0.40:
            status = "Sangat Potensial"

        elif skor >= 0.33:
            status = "Potensial"

        else:
            status = "Potensi Rendah"

        st.info(f"""
### 📌 Kesimpulan

Kecamatan **{kecamatan_pilih}**
memiliki kategori **{status}**
berdasarkan hasil analisis spasial.
""")