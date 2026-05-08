import streamlit as st
import pandas as pd
import requests
import time

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Clean & Professional ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu { display: none !important; }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 25px; border-radius: 20px; text-align: center; color: white; margin-bottom: 20px;
    }
    .donor-card {
        background: white; padding: 15px; border-radius: 12px; 
        border-left: 10px solid #990000; margin-bottom: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: black;
    }
    .number-display {
        font-size: 22px; font-weight: bold; color: #990000; 
        text-align: center; margin: 10px 0; letter-spacing: 1px;
    }
    .call-btn {
        background-color: #28a745; color: white !important; 
        padding: 12px; border-radius: 10px; display: block; 
        text-align: center; text-decoration: none; font-weight: bold;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div class="header-box"><h1>PUNJAB BLOOD DONATION</h1><p>Welfare Committee Pindi Amolak</p></div>', unsafe_allow_html=True)

# --- CONFIG (Links Sahi Hain) ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwQpVR9WP3Ek_YHBmQkGijcBbaL7wmY6_tgPHtFVQEDt6Qs4Be0U0zIS6psCh2i1cJU/exec"
SHEET_ID = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=2137978586"

# Page Management
if 'page' not in st.session_state:
    st.session_state.page = "S"

# Navigation
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"):
    st.session_state.page = "S"
    st.rerun()
if c2.button("📝 REGISTER ME"):
    st.session_state.page = "R"
    st.rerun()

# --- REGISTRATION ---
if st.session_state.page == "R":
    st.markdown("<h3 style='color:#990000;'>📝 Join Now</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Name")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("City", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                try:
                    # Request bhejna
                    requests.post(WEB_APP_URL, json={"name": name, "bg": bg, "city": city, "phone": phone}, timeout=15)
                    st.success("Mubarak! Data Save ho gaya.")
                    time.sleep(1.5) # User ko msg dikhane ke liye wait
                    st.session_state.page = "S" # Seedha list page par switch
                    st.rerun()
                except:
                    # Sirf tab error dikhaye agar internet ya link ka masla ho
                    st.error("Technical Error! Check your connection.")
            else:
                st.warning("Please fill all details.")

# --- DONOR LIST ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Donors List</h3>", unsafe_allow_html=True)
    st.cache_data.clear() # Memory saaf takay naya banda foran nazar aaye
    
    try:
        df = pd.read_csv(f"{CSV_URL}&v={int(time.time())}")
        if not df.empty:
            blood_choice = st.selectbox("Filter Blood", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            # Filtering
            if blood_choice != "All":
                f_df = df[df.iloc[:, 2].astype(str).str.strip() == blood_choice]
            else:
                f_df = df

            if not f_df.empty:
                for i, row in f_df[::-1].iterrows():
                    d_name = row.iloc[1]
                    d_blood = row.iloc[2]
                    d_city = row.iloc[3]
                    d_phone = str(row.iloc[4])
                    
                    st.markdown(f"""
                    <div class="donor-card">
                        <h3 style="margin:0; color:#990000;">{d_name}</h3>
                        <p style="margin:5px 0;">🩸 <b>{d_blood}</b> | 📍 {d_city}</p>
                        <div class="number-display">{d_phone}</div>
                        <a href="tel:{d_phone}" class="call-btn">📞 CALL ME</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"Currently no donors available for {blood_choice}.")
        else:
            st.warning("No donors found in the record.")
    except:
        st.info("Refreshing donors directory...")
