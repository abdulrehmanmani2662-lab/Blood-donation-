import streamlit as st
import pandas as pd
import requests

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium Style ---
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

st.markdown('<div class="header-box"><h1>🩸 PUNJAB BLOOD</h1><p>Welfare Committee Pindi Amolak</p></div>', unsafe_allow_html=True)

# Navigation
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- Registration Page ---
if st.session_state.page == "R":
    st.subheader("📝 Register New Donor")
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("City", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                # Google Form Link
                f_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
                payload = {
                    "entry.1491566373": name,
                    "entry.1741517409": bg,
                    "entry.1945112345": city,
                    "entry.1235116789": phone
                }
                try:
                    requests.post(f_url, data=payload)
                    st.success("Saved! List check karein.")
                    st.balloons()
                except:
                    st.error("Error saving data.")
            else:
                st.warning("Naam aur Number zaruri hai.")

# --- Search Page ---
else:
    st.subheader("🔍 Donors Directory")
    s_id = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
    
    # !!! Yahan apna GID number check kar ke sahi daalein !!!
    # Form Responses wali tab ka GID number link se dekh kar yahan likhein
    GID_NUMBER = "1957618236" 
    
    csv_url = f"https://docs.google.com/spreadsheets/d/{s_id}/export?format=csv&gid={GID_NUMBER}"
    
    try:
        df = pd.read_csv(csv_url)
        if not df.empty:
            choice = st.selectbox("Filter", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            # Google Form Sheet Columns: A=Timestamp, B=Name, C=Blood Group, D=City, E=Number
            # index starts from 0, so Name is 1, Blood Group is 2
            f_df = df if choice == "All" else df[df.iloc[:, 2] == choice]

            for i, row in f_df[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                        <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except:
        st.info("Data load ho raha hai... (Sheet mein data check karein)")
