import streamlit as st
import pandas as pd
import requests

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Mani Rajput Special Design ---
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
        border-radius: 12px; height: 3.8em; font-weight: bold; border: none;
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
        <h1 style='margin:0; font-size: 26px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 16px;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 12px; margin-top:10px; background:rgba(0,0,0,0.2); display:inline-block; padding:2px 12px; border-radius:10px;'>Created by: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# Navigation
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- Registration ---
if st.session_state.page == "R":
    st.markdown("<h3 style='color:#990000;'>📝 Join Now</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Name")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("City", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                # Direct Google Form Bridge (Isse data meri banayi hui sheet mein jayega)
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
                payload = {
                    "entry.1491566373": name, 
                    "entry.1741517409": bg,
                    "entry.1945112345": city, 
                    "entry.1235116789": phone
                }
                try:
                    requests.post(form_url, data=payload)
                    st.success("Saved! List check karein.")
                    st.balloons()
                except:
                    st.error("Error! Internet check karein.")
            else:
                st.warning("Please fill all fields.")

# --- Search Page ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Donors Directory</h3>", unsafe_allow_html=True)
    # Maine ye sheet public kardi hai takay list lazmi show ho
    sheet_id = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
    gid = "2137978586" 
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    try:
        df = pd.read_csv(csv_url)
        if not df.empty:
            choice = st.selectbox("Filter", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = df if choice == "All" else df[df.iloc[:, 2] == choice]

            for i, row in filtered[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                        <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No donors found yet.")
    except:
        st.info("Loading list... Ek test entry karke check karein.")
