import streamlit as st
import pandas as pd
import requests
import time

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Mani Rajput Premium Design ---
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
        background: white; padding: 18px; border-radius: 15px; 
        border-left: 10px solid #990000; margin-bottom: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div class="header-box"><h1>PUNJAB BLOOD DONATION</h1><p>Welfare Committee Pindi Amolak</p><p style="font-size:12px;">Created by: <b>Mani Rajput</b></p></div>', unsafe_allow_html=True)

# --- CONFIG ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwQpVR9WP3Ek_YHBmQkGijcBbaL7wmY6_tgPHtFVQEDt6Qs4Be0U0zIS6psCh2i1cJU/exec"
SHEET_ID = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
# GID 0 is for the first sheet
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

if 'page' not in st.session_state: st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- REGISTRATION ---
if st.session_state.page == "R":
    st.markdown("<h3 style='color:#990000;'>📝 Join as a Donor</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    requests.post(WEB_APP_URL, json={"name": name, "bg": bg, "city": city, "phone": phone}, allow_redirects=True)
                    st.success("Mubarak! Save ho gaya. List check karein.")
                    time.sleep(1.5)
                    st.session_state.page = "S"
                    st.rerun()
                except:
                    st.error("Error saving data.")
            else:
                st.warning("Naam aur Number lazmi likhein.")

# --- DONOR LIST ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Donors Directory</h3>", unsafe_allow_html=True)
    try:
        # Cache bypass using timestamp
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        
        if not df.empty:
            choice = st.selectbox("Filter by Blood", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            # Agar filter laga ho (Blood group is usually at index 2 if column A is Timestamp)
            # Hum search karenge ke "choice" kisi bhi column mein mil jaye takay error na aaye
            if choice != "All":
                # Filtering based on column index 2 (Blood Group)
                f_df = df[df.iloc[:, 2].astype(str).str.strip() == choice]
            else:
                f_df = df

            if not f_df.empty:
                for i, row in f_df[::-1].iterrows():
                    # Display data by index to avoid 'Column Name' errors
                    # 1: Name, 2: Blood Group, 3: City, 4: Contact
                    st.markdown(f"""
                        <div class="donor-card">
                            <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                            <p style="margin:5px 0; color:#333;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                            <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"Filhal {choice} ka koi donor nahi mila.")
        else:
            st.warning("Abhi koi donor registered nahi hai.")
    except Exception as e:
        st.info("Loading donors list... Please wait.")
