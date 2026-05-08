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
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

if 'page' not in st.session_state: st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- REGISTER PAGE ---
if st.session_state.page == "R":
    st.subheader("📝 Register")
    with st.form("reg", clear_on_submit=True):
        n = st.text_input("Name")
        b = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        c = st.text_input("City", "Pindi Amolak")
        p = st.text_input("Mobile")
        submit = st.form_submit_button("SAVE DATA")
        
        if submit:
            if n and p:
                try:
                    requests.post(WEB_APP_URL, json={"name": n, "bg": b, "city": c, "phone": p}, allow_redirects=True)
                    st.success("Mubarak! Save ho gaya.")
                    time.sleep(1)
                    st.session_state.page = "S"
                    st.rerun()
                except:
                    st.error("Technical Error! Try again.")
            else:
                st.warning("Please fill all fields.")

# --- SEARCH / LIST PAGE ---
else:
    st.subheader("🔍 Donors Directory")
    try:
        # Har baar fresh data mangwane ke liye timestamp
        t = int(time.time())
        df = pd.read_csv(f"{CSV_URL}&cache={t}")
        
        if not df.empty:
            choice = st.selectbox("Filter by Blood", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            # Filtering logic using Column Index 2 (Blood Group)
            if choice != "All":
                f_df = df[df.iloc[:, 2].astype(str).str.strip() == choice]
            else:
                f_df = df

            if not f_df.empty:
                for i, row in f_df[::-1].iterrows():
                    # Safeguard: check if row has enough data
                    if len(row) >= 4:
                        st.markdown(f"""
                        <div class="donor-card">
                            <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                            <p style="margin:5px 0;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                            <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info(f"No donor found for {choice}")
        else:
            st.warning("Sheet is empty.")
    except Exception as e:
        st.error("List display error. Please check if your sheet has a header row.")
        st.info("Make sure Row 1 of your sheet has: Timestamp, Name, Blood, City, Phone")
