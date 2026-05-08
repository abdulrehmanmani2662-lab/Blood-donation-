import streamlit as st
import pandas as pd
import requests
import time

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Mani Rajput Design ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 25px; border-radius: 20px; text-align: center; color: white; margin-bottom: 20px;
    }
    .donor-card {
        background: white; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #990000; margin-bottom: 10px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>PUNJAB BLOOD DONATION</h1><p>Welfare Committee Pindi Amolak</p></div>', unsafe_allow_html=True)

# CONFIG
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwQpVR9WP3Ek_YHBmQkGijcBbaL7wmY6_tgPHtFVQEDt6Qs4Be0U0zIS6psCh2i1cJU/exec"
SHEET_ID = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
# Direct Export Link with forced CSV
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

if 'page' not in st.session_state: st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- REGISTRATION ---
if st.session_state.page == "R":
    with st.form("final_reg", clear_on_submit=True):
        n = st.text_input("Name")
        b = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        c = st.text_input("City", "Pindi Amolak")
        p = st.text_input("Mobile")
        if st.form_submit_button("SAVE DATA"):
            if n and p:
                try:
                    requests.post(WEB_APP_URL, json={"name": n, "bg": b, "city": c, "phone": p}, timeout=10)
                    st.success("Saving to Sheet... Please wait.")
                    time.sleep(2)
                    st.session_state.page = "S"
                    st.rerun()
                except:
                    st.error("Submission error - but check sheet.")

# --- LIST PAGE (Super Simplified) ---
else:
    st.cache_data.clear()
    try:
        # Fetching fresh data
        raw_data = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        
        if not raw_data.empty:
            # We skip filtering for a second just to see if ANY data shows up
            st.write(f"Total Donors Found: {len(raw_data)}")
            
            for i, row in raw_data[::-1].iterrows():
                # Displaying whatever is in the columns 1, 2, 3, 4
                try:
                    st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                        <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    continue
        else:
            st.warning("No data found in sheet yet.")
    except Exception as e:
        st.info("Refreshing donors list... wait 5 seconds.")
