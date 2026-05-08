import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium & Clean Look ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"] {
        display: none !important;
    }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .blood-header {
        color: #990000;
        font-weight: 800;
        text-transform: uppercase;
        border-bottom: 3px solid #990000;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #990000;
        color: white;
        border-radius: 12px;
        height: 3.8em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-box">
        <div style='font-size: 40px;'>🩸</div>
        <h1 style='margin:0; font-size: 24px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 15px; opacity: 0.9;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 10px; margin-top:10px;'>Dev: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- Hardcoded Link ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"

# --- Force Refresh Connection ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Connection setup mein masla hai: {e}")

# --- Navigation ---
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- Registration Page ---
if st.session_state.page == "R":
    st.markdown("<h2 class='blood-header'>📝 Registration</h2>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar (City)", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    # ttl=0 is used to get fresh data
                    df = conn.read(spreadsheet=SHEET_URL, ttl=0)
                    new_entry = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_entry], ignore_index=True)
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    st.success("Data Save Ho Gaya!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}. Please ensure Sheet is 'Editor' and App is Rebooted.")
            else:
                st.warning("Naam aur Number likhna lazmi hai.")

# --- Search Page ---
else:
    st.markdown("<h2 class='blood-header'>🔍 Blood Directory</h2>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=SHEET_URL, ttl=0)
        if data is not None and not data.empty:
            choice = st.selectbox("Filter", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = data if choice == "All" else data[data["Blood Group"] == choice]
            
            for i, row in filtered.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:10px; border-left:10px solid #990000; margin-bottom:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <h4 style="margin:0; color:#990000;">{row['Name']}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:8px; text-decoration:none; border-radius:5px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except:
        st.info("Wait... loading data.")
