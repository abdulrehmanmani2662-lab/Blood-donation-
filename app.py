import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Mani Rajput Design ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 30px; border-radius: 20px; text-align: center; color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; background-color: #990000; color: white;
        border-radius: 12px; height: 3.5em; font-weight: bold; border: none;
    }
    .donor-card {
        background: white; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #990000; margin-bottom: 10px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown(f"""
    <div class="header-box">
        <h1 style='margin:0; font-size: 26px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 12px; margin-top:10px;'>Created by: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# Sheet Connection
# Mani bhai, ye aapka bheja hua link hai
url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

if 'page' not in st.session_state: st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- REGISTRATION ---
if st.session_state.page == "R":
    st.subheader("📝 Join Now")
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("City", "Pindi Amolak")
        phone = st.text_input("Contact Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    # Pehle purana data read karo
                    df = conn.read(spreadsheet=url, ttl=0)
                    # Naya data add karo
                    new_entry = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_entry], ignore_index=True)
                    # Sheet update karo
                    conn.update(spreadsheet=url, data=updated_df)
                    st.success("Mubarak! Data sheet mein save ho gaya.")
                    time.sleep(1.5)
                    st.session_state.page = "S"
                    st.rerun()
                except:
                    st.error("Error! Sheet ki permissions check karein (Editor mode zaroori hai).")
            else:
                st.warning("Pura form bharein.")

# --- DONOR LIST ---
else:
    st.subheader("🔍 Donors Directory")
    try:
        data = conn.read(spreadsheet=url, ttl=0)
        if not data.empty:
            choice = st.selectbox("Filter", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = data if choice == "All" else data[data["Blood Group"] == choice]
            
            for i, row in filtered[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row['Name']}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except:
        st.write("Loading list... Agar sheet bilkul khali hai toh pehla donor register karein.")
