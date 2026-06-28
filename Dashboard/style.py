import streamlit as st


def load_css():

    st.markdown("""
    <style>

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

height:185px;

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

padding:30px;

border-radius:20px;

margin-bottom:30px;

box-shadow:0 8px 25px rgba(0,0,0,.15);

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

    </style>
    """, unsafe_allow_html=True)