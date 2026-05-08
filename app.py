import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Shining Header & Hide Icons ---
st.markdown("""
    <style>
    /* Hide Everything Faltu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {display:none;}
    [data-testid="stDecoration"] {display:none;}
    div[data-testid="stStatusWidget"] {display:none;}
    
    /* Shining Animated Header */
    .header-box {
        background: linear-gradient(-45deg, #8b0000, #ff4b4b, #d32f2f, #8b0000);
        background-size: 400% 400%;
        animation: gradient 5s ease infinite;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4);
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Mobile Menu Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Shining Header ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 24px;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:0; font-size: 16px;'>Welfare Committee Pindi Amolak</p>
        <p style='margin:0; font-size: 10px; opacity:0.7;'>By: Mani Rajput</p>
    </div>
    """, unsafe_allow_html=True)

# --- Database Connection ---
url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Navigation (Buttons Instead of Sidebar) ---
col1, col2 = st.columns(2)
with col1:
    btn_search = st.button("🔍 Find Donor")
with col2:
    btn_reg = st.button("📝 Register Me")

# Session State for Menu
if 'page' not in st.session_state:
    st.session_state.page = "Search"

if btn_search: st.session_state.page = "Search"
if btn_reg: st.session_state.page = "Register"

# --- Page Logic ---

if st.session_state.page == "Register":
    st.markdown("### 📝 Register as Donor")
    with st.form("my_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar", "Pindi Amolak")
        phone = st.text_input("Phone/WhatsApp")
        
        if st.form_submit_button("Save Data"):
            if name and phone:
                try:
                    df = conn.read(spreadsheet=url, usecols=[0,1,2,3])
                    new_row = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    df_final = pd.concat([df, new_row], ignore_index=True)
                    conn.update(spreadsheet=url, data=df_final)
                    st.success("Mubarak! Data Save Ho Gaya.")
                    st.balloons()
                except Exception as e:
                    st.error("Error: Please check Google Sheet permissions.")
            else:
                st.warning("Naam aur Number likhein.")

else:
    st.markdown("### 🔍 Donors Directory")
    try:
        data = conn.read(spreadsheet=url, usecols=[0,1,2,3])
        search = st.selectbox("Filter by Blood Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        
        filtered = data if search == "All" else data[data["Blood Group"] == search]
        
        if not filtered.empty:
            for i, row in filtered.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:10px; border-left:8px solid #d32f2f; margin-bottom:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:#8b0000;">{row['Name']}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:8px 15px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">📞 Call Now</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Koi donor nahi mila.")
    except:
        st.error("Abhi tak koi data nahi hai ya link sahi nahi hai.")
