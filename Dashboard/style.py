import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /*=============================*/
    /* GOOGLE FONT                 */
    /*=============================*/

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stApp, p, span, div, li, label{
        font-family:'Inter', sans-serif;
    }

    h1,h2,h3,
    .hero-title,
    .metric-value,
    .metric-header{
        font-family:'Poppins', sans-serif !important;
    }

    /*=============================*/
    /* FULL WIDTH LAYOUT           */
    /*=============================*/
    /* Streamlit tetap membatasi lebar maksimum kontainer utama walau
       sudah pakai layout="wide". Selector class-nya sering berubah
       antar versi Streamlit, jadi di sini beberapa selector sekaligus
       ditarget (nama class lama + data-testid versi baru) supaya
       pasti kena versi Streamlit yang mana pun. */

    .block-container,
    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid*="MainBlockContainer"],
    [data-testid*="AppViewBlockContainer"],
    [class*="block-container"],
    section[data-testid="stMain"] > div{
        max-width:100% !important;
        width:100% !important;
        padding-left:0.6rem !important;
        padding-right:0.6rem !important;
        padding-top:1.5rem !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section[data-testid="stMain"],
    [data-testid*="AppViewContainer"]{
        max-width:100% !important;
        width:100% !important;
    }

    [data-testid="element-container"],
    [data-testid="stElementContainer"],
    [data-testid="stIFrame"],
    [data-testid="stCustomComponentV1"],
    iframe{
        width:100% !important;
        max-width:100% !important;
    }

    .stApp{
        background:#F8F5F2;
    }

    section[data-testid="stSidebar"]{
        background:#EFE6DD;
    }

   h1,h2,h3{
    color:#5B3A29;
}

.hero h1,
.hero h2,
.hero h3,
.hero-title,
.hero-subtitle,
.hero-info{
    color:white !important;
}   

/*=============================*/
/* KPI CARD */
/*=============================*/

.metric-card{

background:white;

padding:22px;

border-radius:18px;

box-shadow:0 8px 18px rgba(0,0,0,.08);

border:1px solid #EAEAEA;

transition:.3s;

min-height:185px;

margin-bottom:10px;

}

.metric-card:hover{

transform:translateY(-6px);

box-shadow:0 12px 25px rgba(0,0,0,.15);

}

.metric-header{

display:flex;

align-items:center;

gap:12px;

font-size:22px;

font-weight:bold;

color:#5B3A29;

}

.metric-icon{

font-size:32px;

}

.metric-divider{

height:3px;

width:100%;

background:#8B5E3C;

margin-top:15px;

margin-bottom:18px;

border-radius:30px;

}

.metric-value{

font-size:42px;

font-weight:700;

color:#8B5E3C;

text-align:center;

}

.metric-subtitle{

text-align:center;

margin-top:8px;

font-size:15px;

color:#777;

}

/* ========================= */
/* HERO */
/* ========================= */

.hero{

background:linear-gradient(135deg,#7B4F2B,#A97142);

background-image:
    radial-gradient(circle at 92% 15%, rgba(255,255,255,.10) 0, rgba(255,255,255,.10) 60px, transparent 61px),
    radial-gradient(circle at 98% 55%, rgba(255,255,255,.08) 0, rgba(255,255,255,.08) 90px, transparent 91px),
    radial-gradient(circle at 80% 90%, rgba(255,255,255,.06) 0, rgba(255,255,255,.06) 50px, transparent 51px),
    linear-gradient(135deg,#7B4F2B,#A97142);

background-repeat:no-repeat;
background-size:cover;

padding:34px 36px;

border-radius:20px;

margin-bottom:30px;

box-shadow:0 8px 25px rgba(0,0,0,.15);

position:relative;
overflow:hidden;

}

.hero::after{
    content:"☕";
    position:absolute;
    right:-10px;
    bottom:-35px;
    font-size:150px;
    opacity:.08;
    transform:rotate(-15deg);
    pointer-events:none;
}

.hero-title{

font-size:34px;

font-weight:700;

color:white;

margin-bottom:10px;

}

.hero-subtitle{

font-size:17px;

color:white;

opacity:.9;

margin-bottom:25px;

line-height:1.5;

}

.hero-info{

display:flex;

gap:20px;

flex-wrap:wrap;

}

.hero-box{

background:rgba(255,255,255,.12);

padding:15px 25px;

border-radius:12px;

color:white;

text-align:center;

backdrop-filter:blur(5px);

min-width:150px;

transition:.3s;

}

.hero-box:hover{

background:rgba(255,255,255,.22);

transform:translateY(-4px);

}

/* ========================= */
/* MENU HORIZONTAL (native st.button) */
/* ========================= */

.st-key-menu_bar{
    background:#F3ECE5;
    padding:14px 12px;
    border-radius:12px;
    margin:15px 0px 25px 0px;
}

.st-key-menu_bar .stButton > button{
    width:100%;
    background:transparent;
    border:none;
    color:#5B3A29;
    font-weight:600;
    font-size:17px;
    border-radius:10px;
    padding:10px 18px;
    transition:.2s;
    box-shadow:none;
}

.st-key-menu_bar .stButton > button:hover{
    background:rgba(139,94,60,0.15);
    color:#5B3A29;
    border:none;
}

.st-key-menu_bar .stButton > button:focus:not(:active){
    color:#5B3A29;
    border:none;
    box-shadow:none;
}

.st-key-menu_bar .stButton > button[kind="primary"]{
    background:#8B5E3C !important;
    color:white !important;
    border:none !important;
}

.st-key-menu_bar .stButton > button[kind="primary"]:hover{
    background:#7B4F2B !important;
    color:white !important;
}

/* ========================= */
/* FADE-IN ANIMATION         */
/* ========================= */

@keyframes fadeInUp{
    from{
        opacity:0;
        transform:translateY(14px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

.hero,
.metric-card,
[data-testid="stTabs"],
[data-testid="stDataFrame"],
.footer-app{
    animation:fadeInUp .5s ease-out;
}

/* ========================= */
/* SIDEBAR STYLING           */
/* ========================= */

section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] [data-baseweb="select"] > div{
    background:white !important;
    border-radius:10px !important;
    border:1px solid #E0D2C3 !important;
}

section[data-testid="stSidebar"] [data-testid="stMetric"]{
    background:white;
    padding:12px 14px;
    border-radius:12px;
    border:1px solid #E0D2C3;
    margin-bottom:8px;
}

section[data-testid="stSidebar"] [data-testid="stMetricValue"]{
    color:#8B5E3C;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#5B3A29 !important;
}

section[data-testid="stSidebar"] [data-testid="stAlert"]{
    background:rgba(139,94,60,.08);
    border-radius:12px;
    border:1px solid #E0D2C3;
}

/* ========================= */
/* FOOTER                    */
/* ========================= */

.footer-app{
    margin-top:45px;
    padding:26px 30px;
    background:linear-gradient(135deg,#5B3A29,#7B4F2B);
    border-radius:18px;
    color:white;
    text-align:center;
    box-shadow:0 8px 20px rgba(0,0,0,.12);
}

.footer-app .footer-title{
    font-family:'Poppins', sans-serif;
    font-weight:700;
    font-size:18px;
    margin-bottom:6px;
}

.footer-app .footer-sub{
    opacity:.85;
    font-size:14px;
    margin-bottom:14px;
}

.footer-app .footer-divider{
    width:60px;
    height:3px;
    background:rgba(255,255,255,.4);
    margin:0 auto 14px auto;
    border-radius:10px;
}

.footer-app .footer-tags{
    display:flex;
    justify-content:center;
    gap:10px;
    flex-wrap:wrap;
    margin-bottom:14px;
}

.footer-app .footer-tag{
    background:rgba(255,255,255,.12);
    padding:6px 14px;
    border-radius:20px;
    font-size:13px;
}

.footer-app .footer-copy{
    font-size:12.5px;
    opacity:.7;
}

/* ========================= */
/* HALAMAN TENTANG           */
/* ========================= */

.tentang-card{
    background:white;
    padding:22px;
    border-radius:16px;
    box-shadow:0 6px 16px rgba(0,0,0,.06);
    border:1px solid #EAEAEA;
    height:100%;
    transition:.3s;
}

.tentang-card:hover{
    transform:translateY(-4px);
    box-shadow:0 12px 22px rgba(0,0,0,.12);
}

.tentang-card .icon{
    font-size:30px;
    margin-bottom:10px;
}

.tentang-card h4{
    color:#5B3A29;
    margin-bottom:8px;
    font-family:'Poppins', sans-serif;
}

.tentang-card p{
    color:#555;
    font-size:14.5px;
    line-height:1.55;
}

/* ========================= */
/* EXPANDER FILTER KECAMATAN */
/* ========================= */

[data-testid="stExpander"]{
    background:white;
    border-radius:12px !important;
    border:1px solid #E0D2C3 !important;
    overflow:visible !important;
}

[data-testid="stExpander"] summary{
    border-radius:12px !important;
    font-weight:600;
    color:#5B3A29;
}

/* Dropdown listbox multiselect (portal BaseWeb) supaya tidak
   terpotong dan cukup tinggi saat menampilkan banyak pilihan. */
[data-baseweb="popover"] [role="listbox"]{
    max-height:320px !important;
}

    </style>
    """, unsafe_allow_html=True)