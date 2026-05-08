import streamlit as st
import pandas as pd
import requests
import time

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸")

# --- CSS Mani Rajput Style ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 30px; border-radius: 25px; text-align: center; color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom: 25px;
    }
    .donor-card {
        background: white; padding: 18px; border-radius: 15px; 
        border-left: 10px solid #990000; margin-bottom: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>PUNJAB BLOOD DONATION</h1><p>Created by: Mani Rajput</p></div>', unsafe_allow_html=True)

# Navigation
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- DATABASE URL (Fresh Link) ---
SHEET_ID = "1wi_ltnwCrsTmjj0JvXTxf4EvGuayqeV4s6SV9U91pxc"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

if st.session_state.page == "R":
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Name")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("City", "Pindi Amolak")
        phone = st.text_input("Number")
        
        if st.form_submit_button("SAVE DATA"):
            # Hum Google Form use karenge kyunke ye kabhi block nahi hota
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
            payload = {"entry.1491566373": name, "entry.1741517409": bg, "entry.1945112345": city, "entry.1235116789": phone}
            try:
                requests.post(form_url, data=payload)
                st.success("Data Saved! Redirecting...")
                time.sleep(1)
                st.session_state.page = "S"
                st.rerun()
            except:
                st.error("Error saving! Try again.")

else:
    try:
        # Cache bypass ke liye timestamp
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        if not df.empty:
            for i, row in df[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row.iloc[0]}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row.iloc[1]}</b> | 📍 {row.iloc[2]}</p>
                        <a href="tel:{row.iloc[3]}" style="background:#28a745; color:white; padding:8px; text-decoration:none; border-radius:8px; display:block; text-align:center;">📞 CALL</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No donors found.")
    except:
        st.write("Loading list...")
