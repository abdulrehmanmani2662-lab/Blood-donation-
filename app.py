import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- CSS: Premium & Clean Look (No Clots) ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu, [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    .header-box {
        background: linear-gradient(135deg, #7d0000 0%, #ff1a1a 50%, #7d0000 100%);
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .stButton>button {
        width: 100%;
        background-color: #990000;
        color: white;
        border-radius: 15px;
        height: 3.8em;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div class="header-box">
        <div style='font-size: 45px; margin-bottom: 10px;'>🩸</div>
        <h1 style='margin:0; font-size: 24px; font-weight: 900;'>PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 16px; opacity: 0.9;'>Welfare Committee Pindi Amolak</p>
        <p style='font-size: 10px; margin-top:10px;'>Dev: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- Navigation ---
if 'page' not in st.session_state: st.session_state.page = "S"
c1, c2 = st.columns(2)
if c1.button("🔍 FIND DONOR"): st.session_state.page = "S"
if c2.button("📝 REGISTER ME"): st.session_state.page = "R"

# --- Registration Page (Via Google Form Bridge) ---
if st.session_state.page == "R":
    st.markdown("<h3 style='color:#990000;'>📝 Join as a Donor</h3>", unsafe_allow_html=True)
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Aapka Naam")
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        city = st.text_input("Shehar (City)", "Pindi Amolak")
        phone = st.text_input("WhatsApp/Mobile Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                # Google Form URL
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
                
                # Entry IDs for your specific form
                payload = {
                    "entry.1491566373": name,   # Name ID
                    "entry.1741517409": bg,     # Blood Group ID
                    "entry.1945112345": city,   # City ID (Approx ID)
                    "entry.1235116789": phone   # Contact ID
                }
                
                try:
                    # Sending data to Google Form
                    requests.post(form_url, data=payload)
                    st.success("Mubarak! Aapka data save ho gaya aur directory mein shamil kar diya gaya hai.")
                    st.balloons()
                except:
                    st.error("Connection slow hai, dobara koshish karein.")
            else:
                st.warning("Naam aur Number lazmi likhein.")

# --- Search Page (Using CSV Export for Zero-Permission Issues) ---
else:
    st.markdown("<h3 style='color:#990000;'>🔍 Search Donors</h3>", unsafe_allow_html=True)
    # Aapki sheet ka public ID
    sheet_id = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    
    try:
        df = pd.read_csv(csv_url)
        if not df.empty:
            choice = st.selectbox("Filter by Blood Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            filtered = df if choice == "All" else df[df.iloc[:, 1] == choice] # Assuming Blood Group is Column 2
            
            for i, row in filtered.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:12px; border-left:10px solid #990000; margin-bottom:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                        <h4 style="margin:0; color:#990000;">{row.iloc[0]}</h4>
                        <p style="margin:5px 0; color:#333;">🩸 <b>{row.iloc[1]}</b> | 📍 {row.iloc[2]}</p>
                        <a href="tel:{row.iloc[3]}" style="background:#28a745; color:white; padding:10px; text-decoration:none; border-radius:8px; display:inline-block; width:100%; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi tak koi donor register nahi hua.")
    except:
        st.info("Searching for donors... (Pehla data enter hotay hi list show ho jayegi)")
