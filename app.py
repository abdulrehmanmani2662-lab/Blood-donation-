import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium & Stylish Design (No Clots) ---
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Shining Blood Red Header */
    .header-box {
        background: linear-gradient(135deg, #800000 0%, #ff1a1a 50%, #800000 100%);
        background-size: 200% auto;
        animation: shine_effect 3s linear infinite;
        padding: 35px;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 12px 25px rgba(128,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.1);
    }
    @keyframes shine_effect {
        to { background-position: 200% center; }
    }

    /* Blood Fonts Style */
    .blood-font {
        color: #990000;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-bottom: 4px solid #990000;
        padding-bottom: 8px;
        margin-bottom: 20px;
        display: inline-block;
    }

    /* Stylish Buttons */
    .stButton>button {
        width: 100%;
        background-color: #990000;
        color: white;
        border-radius: 15px;
        border: none;
        height: 3.8em;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Front Header ---
st.markdown("""
    <div class="header-box">
        <div style='font-size: 45px; margin-bottom: 10px;'>🩸</div>
        <h1 style='margin:0; font-size: 26px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 16px; opacity: 0.9;'>Welfare Committee Pindi Amolak</p>
        <div style='margin-top: 15px; font-size: 11px; background: rgba(0,0,0,0.2); display: inline-block; padding: 5px 12px; border-radius: 20px;'>
            Developer: <b>Mani Rajput</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Hardcoded Database Link ---
# Is baar link code ke andar hai, secrets ki zaroorat nahi.
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Navigation ---
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- Registration Page ---
if st.session_state.page == "R":
    st.markdown("<h2 class='blood-font'>📝 Registration</h2>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar (City)", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    # Fresh read to force sync
                    df = conn.read(spreadsheet=SHEET_URL, ttl=0)
                    new_entry = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_entry], ignore_index=True)
                    # Update Spreadsheet
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    st.success("Mubarak! Aapka data save ho gaya.")
                    st.balloons()
                except Exception as e:
                    st.error("Permission Issue! Please check if the Google Sheet is set to 'Editor' mode for 'Anyone with the link'.")
            else:
                st.warning("Naam aur Number likhna lazmi hai.")

# --- Search Page ---
else:
    st.markdown("<h2 class='blood-header'>🔍 Blood Directory</h2>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=SHEET_URL, ttl=0)
        if data is not None and not data.empty:
            choice = st.selectbox("Filter by Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = data if choice == "All" else data[data["Blood Group"] == choice]
            
            for i, row in filtered.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:18px; border-radius:15px; border-left:10px solid #990000; margin-bottom:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                        <h4 style="margin:0; color:#990000; font-size: 19px;">{row['Name']}</h4>
                        <p style="margin:6px 0; color:#333;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#1e7e34; color:white; padding:10px; text-decoration:none; border-radius:8px; display:inline-block; width:100%; text-align:center; font-weight:bold; font-size: 14px;">📞 CALL DONOR</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except:
        st.error("Database connection fail. Please check Sheet Permissions.")
