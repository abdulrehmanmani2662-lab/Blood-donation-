import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Stylish & Clean ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"] {
        display: none !important;
    }
    .header-box {
        background: linear-gradient(135deg, #8B0000 0%, #FF0000 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }
    .blood-header {
        color: #B22222;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        border-bottom: 3px solid #B22222;
        padding-bottom: 10px;
        font-size: 22px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #B22222;
        color: white;
        font-weight: bold;
        border: none;
        height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 24px;'>🩸 PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 14px;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 10px; opacity: 0.8;'>Dev: Mani Rajput</p>
    </div>
    """, unsafe_allow_html=True)

# --- Connection ---
url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

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
                    df = conn.read(spreadsheet=url, ttl=0)
                    new_row = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(spreadsheet=url, data=updated_df)
                    st.success("Data Save Ho Gaya!")
                    st.balloons()
                except Exception as e:
                    st.error("Permission Issue! Please check if Sheet is set to 'Editor' mode.")
            else:
                st.warning("Naam aur Number likhna lazmi hai.")

# --- Search Page ---
else:
    st.markdown("<h2 class='blood-header'>🔍 Donors List</h2>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=url, ttl=0)
        if data is not None and not data.empty:
            group = st.selectbox("Blood Group Filter", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filt = data if group == "All" else data[data["Blood Group"] == group]
            
            for i, row in filt.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:10px; border-left:10px solid #B22222; margin-bottom:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:#B22222;">{row['Name']}</h4>
                        <p style="margin:5px 0;">🩸 {row['Blood Group']} | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:8px 15px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block; width:100%; text-align:center;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except:
        st.error("Database connection error.")
