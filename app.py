import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium Design ---
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
    }
    .donor-card {
        background: white; padding: 18px; border-radius: 15px; 
        border-left: 10px solid #990000; margin-bottom: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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
        name = st.text_input("Full Name")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("City", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                # Google Form Link
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
                payload = {
                    "entry.1491566373": name,
                    "entry.1741517409": bg,
                    "entry.1945112345": city,
                    "entry.1235116789": phone
                }
                try:
                    requests.post(form_url, data=payload)
                    st.success("Mubarak! Data save ho gaya. Ek baar Search page check karein.")
                    st.balloons()
                except:
                    st.error("Connection issue. Try again.")
            else:
                st.warning("Naam aur Number likhna lazmi hai.")

# --- Search Page ---
else:
    st.subheader("🔍 Donors Directory")
    sheet_id = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
    # gid=0 means first tab, gid=1957618236 might be for Form Responses
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1957618236"
    
    try:
        df = pd.read_csv(csv_url)
        
        if not df.empty:
            choice = st.selectbox("Filter by Blood Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            # Aapki sheet ke columns ke mutabiq:
            # Column 0 (A) = Timestamp (agar form se aa raha hai)
            # Column 1 (B) = Name
            # Column 2 (C) = Blood Group
            # Column 3 (D) = City
            # Column 4 (E) = Number
            
            if choice != "All":
                # Column index 2 is Blood Group
                filtered_df = df[df.iloc[:, 2] == choice]
            else:
                filtered_df = df

            for i, row in filtered_df[::-1].iterrows():
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
