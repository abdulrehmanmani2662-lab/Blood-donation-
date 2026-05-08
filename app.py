import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Professional & Stylish Blood Theme ---
st.markdown("""
    <style>
    /* Hide Streamlit Elements */
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"], .stStatusWidget {
        display: none !important;
        visibility: hidden !important;
    }

    /* Modern Shining Header (No Clots, Clean Professional Drop) */
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        background-size: 200% auto;
        animation: shine_effect 3s linear infinite;
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    @keyframes shine_effect {
        to { background-position: 200% center; }
    }

    /* Stylish Blood Fonts */
    .stylist-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #990000;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 4px solid #990000;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    /* Custom Stylish Buttons */
    .stButton>button {
        width: 100%;
        background: #990000;
        color: white;
        border-radius: 15px;
        border: none;
        height: 4em;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #ff0000;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Stylish Front Logo & Header ---
st.markdown("""
    <div class="header-box">
        <div style='font-size: 50px; margin-bottom: 10px;'>💧</div>
        <h1 style='margin:0; font-size: 28px; font-weight: 900; letter-spacing: 1px;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 18px; font-weight: 300; opacity: 0.9;'>Welfare Committee Pindi Amolak</p>
        <div style='margin-top: 15px; font-size: 12px; background: rgba(0,0,0,0.2); display: inline-block; padding: 5px 15px; border-radius: 20px;'>
            Developer: <b>Mani Rajput</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Database ---
url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Navigation ---
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 FIND A DONOR"): st.session_state.page = "S"
with c2:
    if st.button("📝 REGISTER ME"): st.session_state.page = "R"

if 'page' not in st.session_state: st.session_state.page = "S"

# --- Registration ---
if st.session_state.page == "R":
    st.markdown("<h2 class='stylist-header'>📝 Become a Hero</h2>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Shubh Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar/Gao", "Pindi Amolak")
        phone = st.text_input("Mobile/WhatsApp Number")
        
        if st.form_submit_button("SAVE TO DIRECTORY"):
            if name and phone:
                try:
                    # Fresh sync to force update
                    df = conn.read(spreadsheet=url, ttl=0)
                    new_entry = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_entry], ignore_index=True)
                    conn.update(spreadsheet=url, data=updated_df)
                    st.success("Mubarak! Aapka data save ho gaya.")
                    st.balloons()
                except Exception as e:
                    st.error("Technical Masla! Please Reboot your App from Dashboard.")
            else:
                st.warning("Naam aur Number lazmi likhein.")

# --- Directory ---
else:
    st.markdown("<h2 class='stylist-header'>🔍 Blood Directory</h2>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=url, ttl=0)
        if not data.empty:
            choice = st.selectbox("Filter by Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = data if choice == "All" else data[data["Blood Group"] == choice]
            
            for i, row in filtered.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:20px; border-radius:15px; border-left:12px solid #990000; margin-bottom:15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                        <h4 style="margin:0; color:#990000; font-size: 20px;">{row['Name']}</h4>
                        <p style="margin:8px 0; color:#444;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#1e7e34; color:white; padding:12px; text-decoration:none; border-radius:8px; display:inline-block; width:100%; text-align:center; font-weight:bold; font-size: 14px;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai. Pehle register karein.")
    except:
        st.info("Directory khali hai.")
