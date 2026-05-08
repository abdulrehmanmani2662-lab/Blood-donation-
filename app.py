import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Shining Design & Icon Hide ---
st.markdown("""
    <style>
    /* Sab faltu Streamlit icons aur footer hide karo */
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Shining Animated Header */
    .header-box {
        background: linear-gradient(-45deg, #4a0000, #8b0000, #ff0000, #4a0000);
        background-size: 400% 400%;
        animation: shine_effect 4s ease infinite;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(139, 0, 0, 0.5);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    @keyframes shine_effect {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Blood Red Title Font */
    .blood-title {
        color: #8b0000;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 3px solid #8b0000;
        display: inline-block;
        margin-bottom: 15px;
    }

    /* Buttons Style */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        background-color: #8b0000;
        color: white;
        border: none;
        padding: 10px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        box-shadow: 0 0 15px #ff0000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Shining Header ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 26px; letter-spacing: 2px;'>🩸 PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 18px; font-weight: 300;'>Welfare Committee Pindi Amolak</p>
        <div style='font-size: 11px; opacity: 0.8; margin-top: 10px;'>Developer: <b>Mani Rajput</b></div>
    </div>
    """, unsafe_allow_html=True)

# --- Connection ---
url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Navigation ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 FIND DONOR"): st.session_state.p = "S"
with col2:
    if st.button("📝 REGISTER ME"): st.session_state.p = "R"

if 'p' not in st.session_state: st.session_state.p = "S"

# --- Registration Page ---
if st.session_state.p == "R":
    st.markdown("<h3 class='blood-title'>📝 Register New Donor</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        n = st.text_input("Full Name")
        b = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        c = st.text_input("City", "Pindi Amolak")
        p = st.text_input("WhatsApp Number")
        
        if st.form_submit_button("SAVE DATA"):
            if n and p:
                try:
                    df = conn.read(spreadsheet=url)
                    new = pd.DataFrame([{"Name": n, "Blood Group": b, "City": c, "Contact": p}])
                    final = pd.concat([df, new], ignore_index=True)
                    conn.update(spreadsheet=url, data=final)
                    st.success("Mubarak! Data sheet mein save ho gaya.")
                    st.balloons()
                except:
                    st.error("Sheet permission masla! Please check Google Sheet Editor settings.")
            else:
                st.warning("Naam aur number lazmi likhein.")

# --- Search Page ---
else:
    st.markdown("<h3 class='blood-title'>🔍 Donors Directory</h3>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=url)
        if data is not None and not data.empty:
            grp = st.selectbox("Blood Group Select Karein", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filt = data if grp == "All" else data[data["Blood Group"] == grp]
            
            for i, row in filt.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:15px; border-left:12px solid #8b0000; margin-bottom:15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:#8b0000;">{row['Name']}</h4>
                        <p style="margin:5px 0; color:#333;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:10px 20px; text-decoration:none; border-radius:10px; font-weight:bold; display:inline-block; margin-top:5px; width:100%; text-align:center;">📞 CALL DONOR</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi tak koi donor register nahi hua.")
    except:
        st.info("Directory khali hai. Pehla data register karein!")
