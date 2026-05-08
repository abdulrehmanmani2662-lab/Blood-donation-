import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Blood Theme & Strict Icon Hide ---
st.markdown("""
    <style>
    /* Sab Streamlit icons aur extra buttons ko khatam karne ke liye */
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"], .stStatusWidget {
        display: none !important;
        visibility: hidden !important;
    }

    /* Shining Blood Red Header */
    .header-box {
        background: linear-gradient(135deg, #660000 0%, #cc0000 50%, #660000 100%);
        background-size: 200% auto;
        animation: shine 3s linear infinite;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(102, 0, 0, 0.5);
    }
    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Blood Fonts Style */
    .blood-font {
        color: #990000;
        font-weight: 900;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        border-bottom: 3px solid #990000;
        padding-bottom: 5px;
    }

    /* Button Colors */
    .stButton>button {
        background-color: #990000;
        color: white;
        border-radius: 8px;
        border: none;
        height: 3.5em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 22px; letter-spacing: 1px;'>🩸 PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 16px; opacity: 0.9;'>Welfare Committee Pindi Amolak</p>
        <p style='margin:0; font-size: 10px; font-weight: bold;'>Developer: Mani Rajput</p>
    </div>
    """, unsafe_allow_html=True)

# --- Database ---
url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Navigation ---
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 FIND DONOR"): st.session_state.p = "S"
with c2:
    if st.button("📝 REGISTER ME"): st.session_state.p = "R"

if 'p' not in st.session_state: st.session_state.p = "S"

# --- Registration ---
if st.session_state.p == "R":
    st.markdown("<h3 class='blood-font'>📝 Register as Donor</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar", "Pindi Amolak")
        phone = st.text_input("Mobile Number")
        
        if st.form_submit_button("SAVE TO DIRECTORY"):
            if name and phone:
                try:
                    # Fresh read to avoid conflict
                    df = conn.read(spreadsheet=url, ttl=0)
                    new_data = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    conn.update(spreadsheet=url, data=updated_df)
                    st.success("Data Save Ho Gaya! Shukriya.")
                    st.balloons()
                except Exception as e:
                    st.error("Sheet Error: App Reboot karein ya permission check karein.")
            else:
                st.warning("Naam aur Number likhna lazmi hai.")

# --- Directory ---
else:
    st.markdown("<h3 class='blood-font'>🔍 Donors Directory</h3>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=url, ttl=0)
        if not data.empty:
            choice = st.selectbox("Search by Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = data if choice == "All" else data[data["Blood Group"] == choice]
            
            for i, row in filtered.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:10px; border-left:10px solid #990000; margin-bottom:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:#990000;">{row['Name']}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#1e7e34; color:white; padding:10px; text-decoration:none; border-radius:5px; display:inline-block; width:100%; text-align:center; font-weight:bold;">📞 CALL DONOR</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Filhal koi donor register nahi hai.")
    except:
        st.info("Data load nahi ho raha. Pehla donor register karein.")
