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
        border-left: 10px solid #990000; margin-bottom: 10px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .number-box {
        background: #f8f9fa; border: 1px dashed #990000;
        padding: 8px; border-radius: 8px; margin: 10px 0;
        font-family: monospace; font-size: 18px; text-align: center; color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>PUNJAB BLOOD DONATION</h1><p>Welfare Committee Pindi Amolak</p></div>', unsafe_allow_html=True)

# CONFIG
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwQpVR9WP3Ek_YHBmQkGijcBbaL7wmY6_tgPHtFVQEDt6Qs4Be0U0zIS6psCh2i1cJU/exec"
SHEET_ID = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=2137978586"

if 'page' not in st.session_state: st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- REGISTRATION ---
if st.session_state.page == "R":
    with st.form("reg", clear_on_submit=True):
        n = st.text_input("Name")
        b = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        c = st.text_input("City", "Pindi Amolak")
        p = st.text_input("Mobile")
        if st.form_submit_button("SAVE DATA"):
            if n and p:
                try:
                    requests.post(WEB_APP_URL, json={"name": n, "bg": b, "city": c, "phone": p}, allow_redirects=True)
                    st.success("Save ho gaya!")
                    time.sleep(1)
                    st.session_state.page = "S"
                    st.rerun()
                except:
                    st.error("Error saving.")

# --- LIST PAGE ---
else:
    st.cache_data.clear()
    try:
        df = pd.read_csv(f"{CSV_URL}&v={int(time.time())}")
        if not df.empty:
            choice = st.selectbox("Filter Blood Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            f_df = df if choice == "All" else df[df.iloc[:, 2].astype(str).str.strip() == choice]

            for i, row in f_df[::-1].iterrows():
                name = row.iloc[1]
                blood = row.iloc[2]
                city = row.iloc[3]
                phone = str(row.iloc[4]) # Phone number as string
                
                st.markdown(f"""
                <div class="donor-card">
                    <h4 style="margin:0; color:#990000;">{name}</h4>
                    <p style="margin:5px 0;">🩸 <b>{blood}</b> | 📍 {city}</p>
                    
                    <div class="number-box">
                        📞 {phone}
                    </div>

                    <div style="display: flex; gap: 10px;">
                        <a href="tel:{phone}" style="flex: 1; background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; text-align:center; font-weight:bold;">CALL</a>
                        <button onclick="navigator.clipboard.writeText('{phone}')" style="flex: 1; background:#007bff; color:white; padding:10px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">COPY</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No donors found.")
    except:
        st.info("Refreshing list...")
