import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium Design (Clean & Professional) ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 30px; border-radius: 25px; text-align: center; color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; background-color: #990000; color: white;
        border-radius: 12px; height: 3.5em; font-weight: bold; border: none;
    }
    .donor-card {
        background: white; padding: 18px; border-radius: 15px; 
        border-left: 10px solid #990000; margin-bottom: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div class="header-box">
        <div style='font-size: 45px; margin-bottom: 10px;'>🩸</div>
        <h1 style='margin:0; font-size: 24px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 16px; opacity: 0.9;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 11px; margin-top:10px; background:rgba(0,0,0,0.2); display:inline-block; padding:2px 12px; border-radius:10px;'>Created by: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- Hardcoded Normal Sheet Link ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1wi_ltnwCrsTmjj0JvXTxf4EvGuayqeV4s6SV9U91pxc/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Navigation
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- Registration Page ---
if st.session_state.page == "R":
    st.markdown("<h3 style='color:#990000;'>📝 Join as a Donor</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar (City)", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    # Reading current data
                    df = conn.read(spreadsheet=SHEET_URL, ttl=0)
                    new_data = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    # Updating the normal sheet
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    st.success("Mubarak! Aapka data save ho gaya.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Permission issue! Sheet ko 'Editor' mode par set karein.")
            else:
                st.warning("Naam aur Number lazmi likhein.")

# --- Search Page ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Donors Directory</h3>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=SHEET_URL, ttl=0)
        if data is not None and not data.empty:
            choice = st.selectbox("Filter by Blood Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = data if choice == "All" else data[data["Blood Group"] == choice]

            for i, row in filtered[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row['Name']}</h4>
                        <p style="margin:5px 0; color:#333;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:inline-block; width:100%; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except:
        st.info("Loading donors list...")
