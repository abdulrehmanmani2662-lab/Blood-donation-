import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸")

# --- CSS: Ultra Stylist & Professional ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    .main-box {
        background: linear-gradient(135deg, #8B0000 0%, #D32F2F 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }

    /* Stylish Blood Red Fonts */
    .blood-header {
        color: #B22222;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        border-bottom: 3px solid #B22222;
        padding-bottom: 10px;
        font-size: 24px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 50px; /* Rounded pill shape buttons */
        background-color: #B22222;
        color: white;
        font-weight: bold;
        border: 2px solid white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: white;
        color: #B22222;
        border: 2px solid #B22222;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="main-box">
        <h1 style='margin:0; font-size: 24px;'>🩸 PUNJAB BLOOD PORTAL</h1>
        <p style='margin:5px 0; font-size: 14px;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 10px; opacity: 0.8;'>By Mani Rajput</p>
    </div>
    """, unsafe_allow_html=True)

# --- Connection ---
url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Navigation ---
col1, col2 = st.columns(2)
if col1.button("🔍 SEARCH"): st.session_state.page = "S"
if col2.button("📝 JOIN US"): st.session_state.page = "R"

if 'page' not in st.session_state: st.session_state.page = "S"

# --- Pages ---
if st.session_state.page == "R":
    st.markdown("<h2 class='blood-header'>📝 Register</h2>", unsafe_allow_html=True)
    with st.form("reg", clear_on_submit=True):
        n = st.text_input("Name")
        b = st.selectbox("Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        p = st.text_input("Phone")
        if st.form_submit_button("SUBMIT"):
            if n and p:
                try:
                    df = conn.read(spreadsheet=url, ttl=0)
                    new = pd.DataFrame([{"Name": n, "Blood Group": b, "City": "Pindi Amolak", "Contact": p}])
                    final = pd.concat([df, new], ignore_index=True)
                    conn.update(spreadsheet=url, data=final)
                    st.success("Saved!")
                    st.balloons()
                except:
                    st.error("Error: Please check Secrets and Sheet Permissions.")
else:
    st.markdown("<h2 class='blood-header'>🔍 Directory</h2>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=url, ttl=0)
        if not data.empty:
            for i, row in data.iterrows():
                st.info(f"🩸 {row['Blood Group']} | {row['Name']} | 📞 {row['Contact']}")
        else:
            st.write("No data found.")
    except:
        st.write("Waiting for data...")
