import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium & Professional Design ---
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
        border-radius: 15px; height: 3.8em; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff0000; transform: scale(1.02); }
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
                # Google Form Bridge
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
                payload = {
                    "entry.1491566373": name,
                    "entry.1741517409": bg,
                    "entry.1945112345": city,
                    "entry.1235116789": phone
                }
                try:
                    requests.post(form_url, data=payload)
                    st.success("Mubarak! Data save ho gaya. List check karein.")
                    st.balloons()
                except:
                    st.error("Technical Error! Check internet.")
            else:
                st.warning("Naam aur Number lazmi likhein.")

# --- Search Page (Using your GID for Live List) ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Donors Directory</h3>", unsafe_allow_html=True)
    sheet_id = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
    
    # Aapka nikala hua sahi GID number
    GID_NUMBER = "2137978586" 
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={GID_NUMBER}"
    
    try:
        # Fresh data fetch
        df = pd.read_csv(csv_url)
        
        if not df.empty:
            choice = st.selectbox("Filter by Blood Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            # Google Form Order: 0:Timestamp, 1:Name, 2:Blood, 3:City, 4:Number
            filtered = df if choice == "All" else df[df.iloc[:, 2] == choice]

            for i, row in filtered[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                        <p style="margin:5px 0; color:#333;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                        <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:inline-block; width:100%; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except:
        st.info("Searching for donors... (Pehla data aatay hi list show hogi)")
