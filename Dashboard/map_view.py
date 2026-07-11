import streamlit as st
import folium
from folium.plugins import (
    Fullscreen,
    LocateControl,
    MiniMap,
    MousePosition,
)
from streamlit_folium import st_folium
from branca.element import MacroElement, Template


# ==========================================================
# CONTROL: PERBAIKAN & GAYA UI PETA
# ==========================================================
# 1) Memastikan seluruh kontrol kustom (legend, north arrow,
#    panel layer, attribution) TETAP tampil di atas peta saat
#    peta dibuka mode Full Screen (baik lewat tombol plugin
#    Fullscreen maupun Fullscreen API bawaan browser).
# 2) Menaruh gaya (CSS) bersama untuk semua kontrol kustom di
#    satu tempat, supaya tampilannya konsisten seperti panel
#    pada ArcGIS Online / QGIS Web (kartu putih, rounded,
#    shadow lembut, warna brand kopi).

class MapUIEnhancements(MacroElement):
    _template = Template("""
    {% macro header(this, kwargs) %}
    <style>
        /* ---- Kontrol tetap di atas walau Full Screen aktif ---- */
        .leaflet-control-container,
        .leaflet-top, .leaflet-bottom{
            z-index:999997 !important;
        }
        .north-arrow-control,
        .map-legend-control,
        .gis-layer-panel-control,
        .gis-attribution-control{
            z-index:999998 !important;
        }
        .leaflet-container:fullscreen,
        .leaflet-container:-webkit-full-screen,
        .leaflet-container:-ms-fullscreen{
            width:100% !important;
            height:100% !important;
        }
        .leaflet-container:fullscreen .leaflet-control-container,
        .leaflet-container:-webkit-full-screen .leaflet-control-container{
            display:block !important;
            visibility:visible !important;
        }

        /* ---- Kartu kontrol kustom (gaya seragam) ---- */
        .north-arrow-control, .map-legend-control,
        .gis-layer-panel-control, .gis-attribution-control{
            font-family:Arial, sans-serif;
        }

        /* ---- Panel Layer (ArcGIS / QGIS Web style) ---- */
        .gis-layer-panel-control{
            display:flex;
            flex-direction:column;
            align-items:flex-end;
        }
        .gis-layer-toggle-btn{
            width:38px;height:38px;
            border-radius:8px;
            border:1px solid rgba(0,0,0,0.15);
            background:#8B5E3C;
            color:#fff;
            font-size:18px;
            cursor:pointer;
            box-shadow:0 2px 8px rgba(0,0,0,0.25);
        }
        .gis-layer-toggle-btn:hover{ background:#7B4F2B; }
        .gis-layer-panel-body{
            display:none;
            margin-top:8px;
            width:250px;
            max-height:60vh;
            overflow-y:auto;
            background:rgba(255,255,255,0.97);
            border-radius:12px;
            box-shadow:0 2px 10px rgba(0,0,0,0.25);
            padding:14px;
        }
        .gis-panel-title{
            font-weight:700; font-size:14px; color:#5B3A29;
            margin-bottom:10px; padding-bottom:8px;
            border-bottom:2px solid #EFE6DD;
        }
        .gis-panel-section{ margin-bottom:14px; }
        .gis-panel-section:last-child{ margin-bottom:0; }
        .gis-panel-section-title{
            font-weight:700; font-size:11px; letter-spacing:.03em;
            text-transform:uppercase; color:#8B5E3C; margin-bottom:6px;
        }
        .gis-radio-row, .gis-checkbox-row{
            display:flex; align-items:center; gap:8px;
            font-size:12.5px; color:#333; margin-bottom:6px; cursor:pointer;
        }
        .gis-overlay-row{ margin-bottom:10px; }
        .gis-overlay-row:last-child{ margin-bottom:0; }
        .gis-opacity-slider{
            width:100%; margin-top:2px; accent-color:#8B5E3C; cursor:pointer;
        }

        /* ---- Legend collapsible ---- */
        .gis-legend-head{ user-select:none; }
        .gis-legend-caret{ user-select:none; }

        /* ---- Attribution / credit box ---- */
        .gis-attribution-control{
            background:rgba(255,255,255,0.9);
            padding:6px 10px;
            border-radius:8px;
            box-shadow:0 1px 6px rgba(0,0,0,0.2);
            font-size:10.5px;
            color:#5B3A29;
            max-width:260px;
            line-height:1.4;
        }

        /* ---- Mouse position (koordinat) ---- */
        .leaflet-control-mouseposition{
            background:rgba(255,255,255,0.9);
            padding:4px 8px;
            border-radius:8px;
            box-shadow:0 1px 6px rgba(0,0,0,0.2);
            font-size:11px;
            color:#5B3A29;
            font-family:Arial, sans-serif;
        }

        /* ---- Skala batang (scale bar) - diperbesar & diberi gaya kartu senada ---- */
        .leaflet-control-scale{
            background:rgba(255,255,255,0.9);
            padding:6px 10px;
            border-radius:8px;
            box-shadow:0 1px 6px rgba(0,0,0,0.2);
            font-family:Arial, sans-serif;
        }
        .leaflet-control-scale-line{
            border:3px solid #5B3A29 !important;
            border-top:none !important;
            color:#5B3A29 !important;
            font-size:14px !important;
            font-weight:700 !important;
            background:transparent !important;
            padding:0 4px 2px !important;
            height:16px !important;
        }

        /* ---- Urutan kontrol pojok kanan atas ----
           Panel Layers di atas, kompas (arah mata angin) di bawahnya. */
        .leaflet-top.leaflet-right{
            display:flex;
            flex-direction:column;
            align-items:flex-end;
            gap:10px;
        }
        .leaflet-top.leaflet-right .gis-layer-panel-control{ order:1; margin-top:0 !important; }
        .leaflet-top.leaflet-right .north-arrow-control{ order:2; margin-top:0 !important; }

        /* ---- Urutan kontrol pojok kiri bawah ----
           Legenda paling atas, lalu skala batang, lalu kotak koordinat paling bawah. */
        .leaflet-bottom.leaflet-left{
            display:flex;
            flex-direction:column;
            align-items:flex-start;
            gap:8px;
        }
        .leaflet-bottom.leaflet-left .map-legend-control{ order:1; margin-bottom:0 !important; }
        .leaflet-bottom.leaflet-left .leaflet-control-scale{ order:2; margin-bottom:0 !important; }
        .leaflet-bottom.leaflet-left .leaflet-control-mouseposition{ order:3; margin-bottom:0 !important; }
    </style>
    {% endmacro %}

    {% macro script(this, kwargs) %}
        {{ this._parent.get_name() }}.whenReady(function () {
            var peta_{{ this.get_name() }} = {{ this._parent.get_name() }};

            peta_{{ this.get_name() }}.on('enterFullscreen', function () {
                document.querySelectorAll(
                    '.north-arrow-control, .map-legend-control, .gis-layer-panel-control, .gis-attribution-control'
                ).forEach(function (el) {
                    el.style.display = '';
                    el.style.visibility = 'visible';
                    el.style.zIndex = 999999;
                });
                setTimeout(function () {
                    peta_{{ this.get_name() }}.invalidateSize();
                }, 250);
            });

            peta_{{ this.get_name() }}.on('exitFullscreen', function () {
                setTimeout(function () {
                    peta_{{ this.get_name() }}.invalidateSize();
                }, 250);
            });
        });
    {% endmacro %}
    """)


# ==========================================================
# CONTROL: ARAH MATA ANGIN (NORTH ARROW / COMPASS)
# ==========================================================
# Dibuat sebagai Leaflet Control (bukan Marker), sehingga posisinya
# tetap menempel di pojok peta walaupun peta di-pan / di-zoom /
# dibuka Full Screen (lihat MapUIEnhancements di atas).

class NorthArrow(MacroElement):
    _template = Template("""
    {% macro script(this, kwargs) %}
        var northArrow_{{ this.get_name() }} = L.control({position: 'topright'});

        northArrow_{{ this.get_name() }}.onAdd = function (map) {
            var div = L.DomUtil.create('div', 'north-arrow-control');
            div.innerHTML = `
                <div style="
                    background:rgba(255,255,255,0.92);
                    border:2px solid #8B5E3C;
                    border-radius:50%;
                    width:50px;
                    height:50px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    box-shadow:0 2px 8px rgba(0,0,0,0.25);
                ">
                    <svg width="32" height="32" viewBox="0 0 100 100">
                        <polygon points="50,8 62,50 50,38 38,50" fill="#C62828"/>
                        <polygon points="50,92 62,50 50,62 38,50" fill="#5B3A29"/>
                        <text x="50" y="22" text-anchor="middle" font-size="18"
                              font-weight="700" fill="#2C3E50" font-family="Arial">N</text>
                    </svg>
                </div>
            `;
            L.DomEvent.disableClickPropagation(div);
            return div;
        };

        northArrow_{{ this.get_name() }}.addTo({{ this._parent.get_name() }});
    {% endmacro %}
    """)


# ==========================================================
# CONTROL: HOME BUTTON
# ==========================================================

class HomeButton(MacroElement):

    def __init__(self, bounds):
        super().__init__()
        # bounds: [[ymin, xmin], [ymax, xmax]]
        self._bounds = bounds
        self._template = Template("""
        {% macro script(this, kwargs) %}

        var home_{{ this.get_name() }} = L.control({
            position: 'topleft'
        });

        home_{{ this.get_name() }}.onAdd = function(map){

            var div = L.DomUtil.create(
                'div',
                'leaflet-bar leaflet-control'
            );

            div.innerHTML = `
            <a href="#"
               title="Kembali ke Tampilan Awal"
               style="
                    width:30px;
                    height:30px;
                    line-height:30px;
                    text-align:center;
                    font-size:18px;
                    text-decoration:none;
                    display:block;
                    background:white;
               ">
               🏠
            </a>
            `;

            div.onclick = function(){

                map.fitBounds(""" + str(self._bounds) + """);

                return false;

            };

            L.DomEvent.disableClickPropagation(div);

            return div;

        };

        home_{{ this.get_name() }}.addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)


# ==========================================================
# CONTROL: PRINT PETA
# ==========================================================
# Menggantikan tombol "Measure distances and areas" (MeasureControl)
# yang jarang dipakai, dengan tombol cetak peta. Memakai window.print()
# bawaan browser (bukan library tambahan), supaya peta yang tercetak
# adalah tampilan Leaflet apa adanya (termasuk basemap, grid warna,
# legenda, dsb) tanpa masalah CORS seperti kalau export ke gambar.

class PrintButton(MacroElement):
    _template = Template("""
    {% macro script(this, kwargs) %}

    var print_{{ this.get_name() }} = L.control({
        position: 'topleft'
    });

    print_{{ this.get_name() }}.onAdd = function(map){

        var div = L.DomUtil.create(
            'div',
            'leaflet-bar leaflet-control'
        );

        div.innerHTML = `
        <a href="#"
           title="Print Peta"
           style="
                width:30px;
                height:30px;
                display:flex;
                align-items:center;
                justify-content:center;
                text-decoration:none;
                background:white;
           ">
           <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
               <path d="M6 9V2H18V9" stroke="#5B3A29" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
               <path d="M6 18H4C3.44772 18 3 17.5523 3 17V11C3 9.89543 3.89543 9 5 9H19C20.1046 9 21 9.89543 21 11V17C21 17.5523 20.5523 18 20 18H18" stroke="#5B3A29" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
               <rect x="6" y="14" width="12" height="8" stroke="#5B3A29" stroke-width="2" stroke-linejoin="round"/>
           </svg>
        </a>
        `;

        div.onclick = function(){

            window.print();

            return false;

        };

        L.DomEvent.disableClickPropagation(div);

        return div;

    };

    print_{{ this.get_name() }}.addTo({{this._parent.get_name()}});

    {% endmacro %}
    """)


# ==========================================================
# CONTROL: SKALA BATANG (UKURAN LEBIH BESAR)
# ==========================================================
# Menggantikan control_scale bawaan folium (ukurannya kecil & tidak
# bisa diatur dari folium.Map). Di sini pakai L.control.scale() Leaflet
# langsung dengan maxWidth lebih besar, supaya batang skalanya lebih
# panjang/besar. Gaya visualnya (tebal garis, ukuran teks) diatur lewat
# CSS .leaflet-control-scale-line di MapUIEnhancements.

class ScaleBarBesar(MacroElement):
    _template = Template("""
    {% macro script(this, kwargs) %}
        L.control.scale({
            position: 'bottomleft',
            maxWidth: 160,
            metric: true,
            imperial: true
        }).addTo({{ this._parent.get_name() }});
    {% endmacro %}
    """)


# ==========================================================
# CONTROL: LEGENDA DI DALAM PETA (collapsible)
# ==========================================================
# Legenda dibuat sebagai Leaflet Control (bukan elemen Streamlit di luar peta),
# jadi ikut menempel di peta, tetap tampil saat Full Screen, dan bisa
# dilipat/dibuka (mirip widget legend ArcGIS Online / QGIS Web).

class MapLegend(MacroElement):
    def __init__(self, judul, baris_html):
        super().__init__()
        self._judul = judul
        self._baris = baris_html
        self._template = Template("""
        {% macro script(this, kwargs) %}
            var legend_{{ this.get_name() }} = L.control({position: 'bottomleft'});

            legend_{{ this.get_name() }}.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'map-legend-control');
                div.innerHTML = `
                    <div style="
                        background:rgba(255,255,255,0.97);
                        padding:14px 16px;
                        border-radius:14px;
                        border:1px solid rgba(91,58,41,0.08);
                        box-shadow:0 4px 16px rgba(0,0,0,0.18);
                        font-family:Arial, sans-serif;
                        min-width:205px;
                    ">
                        <div class="gis-legend-head" style="
                            display:flex;align-items:center;
                            justify-content:space-between;gap:10px;
                            cursor:pointer;
                            padding-bottom:8px;
                            border-bottom:2px solid #F3ECE5;
                        ">
                            <span style="font-weight:700;font-size:13.5px;color:#5B3A29;letter-spacing:.01em;">""" + self._judul + """</span>
                            <span class="gis-legend-caret" style="font-size:11px;color:#8B5E3C;">&#9660;</span>
                        </div>
                        <div class="gis-legend-body" style="margin-top:6px;">
                            """ + self._baris + """
                        </div>
                    </div>
                `;

                div.querySelector('.gis-legend-head').onclick = function () {
                    var body = div.querySelector('.gis-legend-body');
                    var caret = div.querySelector('.gis-legend-caret');
                    if (body.style.display === 'none') {
                        body.style.display = '';
                        caret.innerHTML = '&#9660;';
                    } else {
                        body.style.display = 'none';
                        caret.innerHTML = '&#9654;';
                    }
                };

                L.DomEvent.disableClickPropagation(div);
                return div;
            };

            legend_{{ this.get_name() }}.addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)


# ==========================================================
# CONTROL: ATTRIBUTION / SUMBER DATA (pojok kanan bawah)
# ==========================================================
# Mirip kotak "credit"/attribution kecil pada ArcGIS Online
# dan hasil ekspor QGIS2Web.

class AttributionPanel(MacroElement):
    def __init__(self, teks_html):
        super().__init__()
        self._teks = teks_html
        self._template = Template("""
        {% macro script(this, kwargs) %}
            var attr_{{ this.get_name() }} = L.control({position: 'bottomright'});

            attr_{{ this.get_name() }}.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'gis-attribution-control');
                div.innerHTML = `""" + self._teks + """`;
                L.DomEvent.disableClickPropagation(div);
                return div;
            };

            attr_{{ this.get_name() }}.addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)


# ==========================================================
# CONTROL: PANEL LAYER (Basemap + Overlay & Opacity)
# ==========================================================
# Panel tunggal, collapsible, gaya "Layer List" seperti ArcGIS
# Online / QGIS Web: pilih basemap (radio) + nyalakan/matikan
# overlay (checkbox) + atur transparansi overlay (slider),
# semua diproses langsung di sisi client (JS) tanpa perlu
# reload/rerun Streamlit, sehingga terasa real-time.

def _baris_basemap(label, nama_layer_js, semua_layer_js, checked):

    matikan_lain = ""
    for lyr in semua_layer_js:
        if lyr != nama_layer_js:
            matikan_lain += "{{ this._parent.get_name() }}.removeLayer(" + lyr + "); "

    onchange = matikan_lain + "{{ this._parent.get_name() }}.addLayer(" + nama_layer_js + ");"

    html = """
    <label class="gis-radio-row">
        <input type="radio" name="gis-basemap-radio" """ + ("checked" if checked else "") + """
            onchange='""" + onchange + """'>
        <span>""" + label + """</span>
    </label>
    """
    return html


def _baris_overlay(label, nama_layer_js, tipe, opacity_awal, terlihat_awal):
    """
    tipe:
      'fill'   -> layer isian/poligon berkelompok (mis. grid choropleth,
                  berupa FeatureGroup) -> pakai eachLayer + setStyle(fillOpacity)
      'line'   -> layer garis tunggal (mis. batas administrasi, GeoJson
                  tunggal) -> pakai setStyle(opacity) langsung
      'marker' -> kumpulan marker/label (FeatureGroup) -> pakai
                  eachLayer + setOpacity
    """

    checked = "checked" if terlihat_awal else ""

    if tipe == "fill":
        js_opacity = nama_layer_js + ".eachLayer(function(l){ l.setStyle({fillOpacity: v}); });"
    elif tipe == "line":
        js_opacity = nama_layer_js + ".setStyle({opacity: v});"
    else:
        js_opacity = nama_layer_js + ".eachLayer(function(l){ l.setOpacity(v); });"

    js_toggle = (
        "if(this.checked){ {{ this._parent.get_name() }}.addLayer(" + nama_layer_js + "); } "
        "else { {{ this._parent.get_name() }}.removeLayer(" + nama_layer_js + "); }"
    )

    html = """
    <div class="gis-overlay-row">
        <label class="gis-checkbox-row">
            <input type="checkbox" """ + checked + """
                onclick='""" + js_toggle + """'>
            <span>""" + label + """</span>
        </label>
        <input type="range" min="0" max="100" value=\"""" + str(int(round(opacity_awal * 100))) + """\"
            class="gis-opacity-slider" title="Opacity"
            oninput='var v=this.value/100; """ + js_opacity + """'>
    </div>
    """
    return html


class LayerControlPanel(MacroElement):
    def __init__(self, basemap_html, overlay_html):
        super().__init__()
        self._basemap_html = basemap_html
        self._overlay_html = overlay_html
        self._template = Template("""
        {% macro script(this, kwargs) %}
            var panel_{{ this.get_name() }} = L.control({position: 'topright'});

            panel_{{ this.get_name() }}.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'gis-layer-panel-control');

                div.innerHTML = `
                    <button class="gis-layer-toggle-btn" title="Layers">&#128450;</button>
                    <div class="gis-layer-panel-body">
                        <div class="gis-panel-title">Layers</div>

                        <div class="gis-panel-section">
                            <div class="gis-panel-section-title">Basemap</div>
                            """ + self._basemap_html + """
                        </div>

                        <div class="gis-panel-section">
                            <div class="gis-panel-section-title">Overlay &amp; Opacity</div>
                            """ + self._overlay_html + """
                        </div>
                    </div>
                `;

                div.querySelector('.gis-layer-toggle-btn').onclick = function () {
                    var body = div.querySelector('.gis-layer-panel-body');
                    body.style.display = (body.style.display === 'block') ? 'none' : 'block';
                };

                L.DomEvent.disableClickPropagation(div);
                L.DomEvent.disableScrollPropagation(div);

                return div;
            };

            panel_{{ this.get_name() }}.addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)


def _buat_baris_legenda(bins):
    """
    bins: list of (warna, label, rentang_nilai)
    """

    baris = ""

    for warna, label, rentang in bins:
        baris += f"""
        <div style="
            display:flex;align-items:center;gap:10px;
            padding:9px 10px;
            margin-bottom:6px;
            border-radius:8px;
            border-left:4px solid {warna};
            background:{warna}17;
        ">
            <span style="
                width:14px;height:14px;border-radius:50%;
                background:{warna};display:inline-block;
                border:1px solid rgba(0,0,0,0.15);
                box-shadow:0 1px 3px rgba(0,0,0,0.2);
                flex-shrink:0;
            "></span>
            <span style="line-height:1.4;">
                <span style="font-size:12.5px;font-weight:700;color:#3D2A1F;display:block;">{label}</span>
                <span style="font-size:11px;color:#8B7768;">{rentang}</span>
            </span>
        </div>
        """

    return baris


def _hitung_bins_legenda(gdf_tampil, kolom, kategori_peta):
    """
    Untuk 'Skor Potensi' pakai ambang tetap (0-1) supaya konsisten
    dengan interpretasi skor. Untuk kategori lain, ambang dihitung
    otomatis dari kuartil data yang sedang tampil, supaya rentang
    angkanya selalu sesuai dengan kategori yang dipilih.
    """

    if kategori_peta == "Skor Potensi":
        return [
            ("#C62828", "Sangat Potensial", "0.60 - 1.00"),
            ("#EF6C00", "Potensial", "0.45 - 0.60"),
            ("#FBC02D", "Cukup Potensial", "0.30 - 0.45"),
            ("#ECECEC", "Rendah", "0.00 - 0.30"),
        ]

    nilai = gdf_tampil[kolom]

    vmin = nilai.min()
    vmax = nilai.max()
    q1 = nilai.quantile(0.25)
    q2 = nilai.quantile(0.50)
    q3 = nilai.quantile(0.75)

    def fmt(x):
        return f"{x:,.0f}".replace(",", ".")

    return [
        ("#C62828", "Sangat Tinggi", f"{fmt(q3)} - {fmt(vmax)}"),
        ("#EF6C00", "Tinggi", f"{fmt(q2)} - {fmt(q3)}"),
        ("#FBC02D", "Sedang", f"{fmt(q1)} - {fmt(q2)}"),
        ("#ECECEC", "Rendah", f"{fmt(vmin)} - {fmt(q1)}"),
    ]


def tampilkan_peta(gdf_tampil, kategori_peta, adm):

    # ======================================================
    # MENENTUKAN KOLOM
    # ======================================================

    if kategori_peta == "Skor Potensi":
        kolom = "skor_potensi"

    elif kategori_peta == "Kepadatan Penduduk":
        kolom = "Kepadatan Penduduk (Jiwa/km²)"

    elif kategori_peta == "Fasilitas Pendidikan":
        kolom = "jumlah_pendidikan_700m"

    else:
        kolom = "jumlah_kompetitor_700m"

    st.subheader(f"🗺️ Peta Analisis Potensi Coffee Shop — {kategori_peta}")
    st.caption(
        "💡 Gunakan panel **Layers** (ikon 🗂️ di pojok kanan atas peta) untuk "
        "mengganti basemap, menyalakan/mematikan layer, dan mengatur "
        "transparansi (opacity) tiap layer secara langsung."
    )

    # ======================================================
    # MEMBUAT PETA
    # ======================================================

    m = folium.Map(
        location=[-6.39, 106.82],
        zoom_start=11,
        tiles=None,
        control_scale=False  # -> diganti ScaleBarBesar kustom di bawah (ukuran bisa diatur)
    )

    # ======================================================
    # PERBAIKAN UI GLOBAL (fullscreen-safe + gaya kontrol)
    # ======================================================

    MapUIEnhancements().add_to(m)

    # ======================================================
    # TOOLBAR KIRI ATAS: FULL SCREEN, PRINT, LOKASI, HOME
    # (dikelompokkan seperti toolbar pada ArcGIS Online / QGIS Web)
    # ======================================================

    Fullscreen(
        position="topleft",
        title="Perbesar Peta",
        title_cancel="Keluar Full Screen",
        force_separate_button=True
    ).add_to(m)

    PrintButton().add_to(m)

    ScaleBarBesar().add_to(m)

    LocateControl(
        auto_start=False,
        position="topleft",
        strings={
            "title": "Lokasi Saya"
        }
    ).add_to(m)

    xmin, ymin, xmax, ymax = adm.total_bounds
    home_bounds = [[ymin, xmin], [ymax, xmax]]

    HomeButton(home_bounds).add_to(m)

    # ======================================================
    # ZOOM OTOMATIS KE DATA YANG SEDANG TAMPIL
    # ======================================================

    gxmin, gymin, gxmax, gymax = gdf_tampil.total_bounds

    m.fit_bounds([
        [gymin, gxmin],
        [gymax, gxmax]
    ])

    # ======================================================
    # BASEMAP (hanya OpenStreetMap yang aktif di awal;
    # basemap lain dipilih lewat Panel Layer, bukan tumpang
    # tindih otomatis seperti sebelumnya)
    # ======================================================

    tile_osm = folium.TileLayer(
        "OpenStreetMap",
        name="OpenStreetMap",
        show=True,
        control=False
    ).add_to(m)

    tile_light = folium.TileLayer(
        "CartoDB positron",
        name="Light",
        show=False,
        control=False
    ).add_to(m)

    tile_dark = folium.TileLayer(
        "CartoDB dark_matter",
        name="Dark",
        show=False,
        control=False
    ).add_to(m)

    tile_sat = folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Satellite",
        overlay=False,
        show=False,
        control=False
    ).add_to(m)

    # ======================================================
    # NAMA KECAMATAN (LABEL PERMANEN DI PETA)
    # ======================================================
    # Label ditempatkan pada representative_point tiap kecamatan
    # (dijamin berada di dalam polygon, berbeda dengan centroid biasa)
    # supaya nama kecamatan langsung terbaca tanpa harus hover.

    label_kecamatan = folium.FeatureGroup(
        name="Nama Kecamatan",
        show=True,
        control=False
    )

    adm_label = adm.copy()
    adm_label["label_point"] = adm_label.geometry.representative_point()

    for _, row in adm_label.iterrows():

        titik = row["label_point"]
        nama = row["NAMOBJ"]

        # Lebar kotak label dibuat menyesuaikan panjang nama kecamatan
        # (bukan lebar tetap 150px) supaya label kecamatan yang berdekatan
        # (mis. Bojongsari & Sawangan) tidak saling menimpa.
        lebar = min(120, max(60, len(nama) * 7 + 12))

        folium.map.Marker(
            [titik.y, titik.x],

            icon=folium.DivIcon(
                icon_size=(lebar, 16),
                icon_anchor=(lebar // 2, 8),
                html=f"""
                <div style="
                    text-align:center;
                    font-size:11px;
                    font-weight:700;
                    line-height:1.1;
                    color:#1A1A1A;
                    text-shadow:
                        -1px -1px 0 #FFFFFF,
                        1px -1px 0 #FFFFFF,
                        -1px 1px 0 #FFFFFF,
                        1px 1px 0 #FFFFFF;
                    pointer-events:none;
                ">
                    {nama}
                </div>
                """
            )

        ).add_to(label_kecamatan)

    label_kecamatan.add_to(m)

    # ======================================================
    # CHOROPLETH (GRID SKOR POTENSI / KATEGORI TERPILIH)
    # ======================================================

    choropleth = folium.Choropleth(
        geo_data=gdf_tampil,
        data=gdf_tampil,
        columns=["h3_polyfill", kolom],
        key_on="feature.properties.h3_polyfill",
        fill_color="YlOrRd",
        fill_opacity=0.8,
        line_opacity=0.2,
        legend_name=None,
        name="Grid " + kategori_peta,
        control=False
    ).add_to(m)

    # folium.Choropleth otomatis menempelkan legenda gradasi warna
    # (color scale) di pojok atas peta. Legenda itu kita lepas di sini
    # karena sudah digantikan oleh legenda kategori kustom (MapLegend)
    # yang lebih mudah dibaca.
    for key in list(choropleth._children.keys()):
        if key.startswith("color_map"):
            del choropleth._children[key]

    # ======================================================
    # BATAS ADMINISTRASI (GARIS PERBATASAN KECAMATAN)
    # ======================================================
    # Layer ini sengaja ditambahkan SETELAH choropleth (bukan sebelumnya),
    # karena di Leaflet layer yang ditambahkan belakangan digambar di atas.
    # Kalau ditambahkan sebelum choropleth, garis batasnya akan tertutup
    # rapat oleh warna hexbin yang solid (itu sebabnya sebelumnya garis
    # batas kecamatan tidak kelihatan sama sekali).

    batas_admin = folium.GeoJson(
        adm,
        name="Batas Administrasi",
        show=True,
        control=False,

        style_function=lambda feature: {
            "fillColor": "transparent",
            "color": "#1A1A1A",
            "weight": 2.2,
            "opacity": 0.9,
            "fillOpacity": 0
        },

        highlight_function=lambda feature: {
            "color": "#E74C3C",
            "weight": 4
        },

        tooltip=folium.GeoJsonTooltip(
            fields=["NAMOBJ"],
            aliases=["🏘 Kecamatan"],
            sticky=False
        )

    ).add_to(m)

    # ======================================================
    # TOOLTIP (LAYER INTERAKSI, TIDAK DITAMPILKAN DI PANEL LAYER
    # KARENA HANYA UNTUK HOVER INFORMASI GRID)
    # ======================================================

    folium.GeoJson(

        gdf_tampil,

        style_function=lambda feature: {
            "fillOpacity": 0,
            "color": "transparent",
            "weight": 0
        },

        highlight_function=lambda feature: {
            "fillColor": "#3498DB",
            "color": "black",
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
                "⭐ Skor",
                "👥 Kepadatan",
                "🏫 Pendidikan",
                "☕ Kompetitor"
            ],

            sticky=False,
            localize=True

        )

    ).add_to(m)

    # ======================================================
    # POSISI KURSOR (KOORDINAT) - status bar ala ArcGIS Online
    # ======================================================

    MousePosition(
        position="bottomleft",
        separator=" | ",
        prefix="📍 Koordinat:",
        num_digits=5,
        lat_formatter="function(num) {return L.Util.formatNum(num, 5) + '° LS/LU';}",
        lng_formatter="function(num) {return L.Util.formatNum(num, 5) + '° BT/BB';}"
    ).add_to(m)

    # ======================================================
    # MINI MAP
    # ======================================================

    MiniMap(
        position="bottomright",
        toggle_display=True,
        width=120,
        height=120,
        zoom_level_offset=-5
    ).add_to(m)

    # ======================================================
    # ARAH MATA ANGIN
    # ======================================================

    NorthArrow().add_to(m)

    # ======================================================
    # LEGENDA (DI DALAM PETA, COLLAPSIBLE)
    # ======================================================

    bins_legenda = _hitung_bins_legenda(gdf_tampil, kolom, kategori_peta)

    MapLegend(
        judul=f"Legenda: {kategori_peta}",
        baris_html=_buat_baris_legenda(bins_legenda)
    ).add_to(m)

    # ======================================================
    # PANEL LAYER (BASEMAP + OVERLAY & OPACITY)
    # Menggantikan folium.LayerControl bawaan supaya kontrol
    # basemap, visibilitas layer, dan slider opacity berada
    # dalam SATU panel terpadu (seperti ArcGIS Online / QGIS Web),
    # bukan tersebar di beberapa kontrol terpisah.
    # ======================================================

    semua_basemap_js = [
        tile_osm.get_name(),
        tile_light.get_name(),
        tile_dark.get_name(),
        tile_sat.get_name()
    ]

    basemap_html = (
        _baris_basemap("OpenStreetMap", tile_osm.get_name(), semua_basemap_js, checked=True)
        + _baris_basemap("Light", tile_light.get_name(), semua_basemap_js, checked=False)
        + _baris_basemap("Dark", tile_dark.get_name(), semua_basemap_js, checked=False)
        + _baris_basemap("Satellite", tile_sat.get_name(), semua_basemap_js, checked=False)
    )

    overlay_html = (
        _baris_overlay(
            "Grid " + kategori_peta,
            choropleth.get_name(),
            tipe="fill",
            opacity_awal=0.8,
            terlihat_awal=True
        )
        + _baris_overlay(
            "Batas Administrasi",
            batas_admin.get_name(),
            tipe="line",
            opacity_awal=0.9,
            terlihat_awal=True
        )
        + _baris_overlay(
            "Nama Kecamatan",
            label_kecamatan.get_name(),
            tipe="marker",
            opacity_awal=1.0,
            terlihat_awal=True
        )
    )

    LayerControlPanel(
        basemap_html=basemap_html,
        overlay_html=overlay_html
    ).add_to(m)

    # ======================================================
    # TAMPILKAN PETA
    # ======================================================

    st_folium(
        m,
        width=None,
        height=650,
        use_container_width=True
    )
