import streamlit as st
import pandas as pd
import requests
import time

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Mani Rajput Premium Design ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 30px; border-radius: 20px; text-align: center; color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; background-color: #990000; color: white;
        border-radius: 12px; height: 3.5em; font-weight: bold; border: none;
    }
    .donor-card {
        background: white; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #990000; margin-bottom: 10px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown(f"""
    <div class="header-box">
        <h1 style='margin:0; font-size: 26px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 12px; margin-top:10px;'>Created by: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- CONFIG: Naya Google Script URL ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwQpVR9WP3Ek_YHBmQkGijcBbaL7wmY6_tgPHtFVQEDt6Qs4Be0U0zIS6psCh2i1cJU/exec"
SHEET_CSV = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/export?format=csv&gid=0"

if 'page' not in st.session_state: st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- REGISTRATION PAGE ---
if st.session_state.page == "R":
    st.markdown("<h3 style='color:#990000;'>📝 Join as a Donor</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    # 'allow_redirects=True' Google Script ke liye lazmi hai
                    requests.post(WEB_APP_URL, json={"name": name, "bg": bg, "city": city, "phone": phone}, allow_redirects=True)
                    st.success("Mubarak! Data Save ho gaya.")
                    time.sleep(2)
                    st.session_state.page = "S"
                    st.rerun()
                except Exception as e:
                    st.error("Technical Error! Check internet or Script deployment.")
            else:
                st.warning("Naam aur Number lazmi likhein.")

# --- DONOR LIST PAGE ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Donors Directory</h3>", unsafe_allow_html=True)
    try:
        # Cache bypass using timestamp
        df = pd.read_csv(f"{SHEET_CSV}&t={int(time.time())}")
        if not df.empty:
            choice = st.selectbox("Filter by Blood", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            # Index-based data fetch (1=Name, 2=Blood Group, 3=City, 4=Contact)
            f_df = df if choice == "All" else df[df.iloc[:, 2].astype(str).str.strip() == choice]

            for i, row in f_df[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                        <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor registered nahi hai.")
    except:
        st.info("Loading donors list... Please wait.")
