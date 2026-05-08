import streamlit as st
import pandas as pd
import requests
import time

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Mani Rajput Special ---
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
    .manual-link {
        text-align: center; padding: 10px; background: #fff3cd; 
        border-radius: 10px; color: #856404; font-size: 13px; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown(f"""
    <div class="header-box">
        <h1 style='margin:0; font-size: 26px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 12px; margin-top:10px;'>Created by: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- REGISTRATION ---
if st.session_state.page == "R":
    st.markdown("<h3 style='color:#990000;'>📝 Register</h3>", unsafe_allow_html=True)
    
    # Direct Form Link for Backup
    direct_form = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/viewform"
    
    with st.form("reg_form", clear_on_submit=True):
        n = st.text_input("Name")
        b = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        c = st.text_input("City", "Pindi Amolak")
        p = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if n and p:
                f_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
                payload = {"entry.1491566373": n, "entry.1741517409": b, "entry.1945112345": c, "entry.1235116789": p}
                try:
                    res = requests.post(f_url, data=payload, timeout=10)
                    if res.status_code == 200 or res.status_code == 302:
                        st.success("Mubarak! Save ho gaya.")
                        time.sleep(1)
                        st.session_state.page = "S"
                        st.rerun()
                    else:
                        st.error("Form error! Niche wale link se register karein.")
                except:
                    st.error("Network issue! Niche wala link use karein.")
            else:
                st.warning("Pura form bharein.")
    
    st.markdown(f"""<div class="manual-link">Agar upar wala button kaam na kare toh <a href="{direct_form}" target="_blank">Yahan Click Karke</a> register karein.</div>""", unsafe_allow_html=True)

# --- LIST ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Donors List</h3>", unsafe_allow_html=True)
    sheet_id = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
    gid = "2137978586"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}&cache={int(time.time())}"
    
    try:
        df = pd.read_csv(csv_url)
        if not df.empty:
            choice = st.selectbox("Filter", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
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
            st.info("No donors found.")
    except:
        st.info("Loading list...")
