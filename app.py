import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium Blood Theme (No Clots) ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"], .stStatusWidget {
        display: none !important;
        visibility: hidden !important;
    }

    .header-box {
        background: linear-gradient(135deg, #800000 0%, #b30000 50%, #800000 100%);
        padding: 35px;
        border-radius: 30px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(128,0,0,0.3);
    }

    .blood-drop {
        font-size: 50px;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
        margin-bottom: 10px;
    }

    .stButton>button {
        width: 100%;
        background: #b30000;
        color: white;
        border-radius: 12px;
        height: 3.8em;
        font-weight: bold;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background: #e60000;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Stylish Header ---
st.markdown("""
    <div class="header-box">
        <div class="blood-drop">🩸</div>
        <h1 style='margin:0; font-size: 26px; font-weight: 800;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 16px; opacity: 0.9;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 11px; margin-top:10px;'>Developed with ❤️ by Mani Rajput</p>
    </div>
    """, unsafe_allow_html=True)

# --- Connection Logic ---
url = "hhttps://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=drivesdk"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Navigation ---
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- Logic ---
if st.session_state.page == "R":
    st.subheader("📝 Naya Donor Shamil Karein")
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar", "Pindi Amolak")
        phone = st.text_input("WhatsApp Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    # Direct update using the connection
                    df = conn.read(spreadsheet=url, ttl=0)
                    new_entry = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_entry], ignore_index=True)
                    conn.update(spreadsheet=url, data=updated_df)
                    st.success("Mubarak! Data save ho gaya.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Permission Error! App Settings mein Secrets check karein.")
            else:
                st.warning("Naam aur Number likhna lazmi hai.")
else:
    st.subheader("🔍 Donors Directory")
    try:
        data = conn.read(spreadsheet=url, ttl=0)
        if not data.empty:
            choice = st.selectbox("Filter", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filt = data if choice == "All" else data[data["Blood Group"] == choice]
            for i, row in filt.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:10px; border-left:10px solid #b30000; margin-bottom:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:#b30000;">{row['Name']}</h4>
                        <p style="margin:5px 0;">🩸 {row['Blood Group']} | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="color:white; background:#28a745; padding:8px; text-decoration:none; border-radius:5px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else: st.info("Koi donor nahi mila.")
    except: st.info("Directory khali hai.")
