import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Config - Icons aur Menu Hide karne ke liye
st.set_page_config(
    page_title="Punjab Blood Donation", 
    page_icon="🩸", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS - Icons aur Footer Hatane ke liye
st.markdown("""
    <style>
    /* Sab icons aur extra buttons hatane ke liye */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {display:none !important;}
    
    /* Design Improvements */
    .header-box {
        background: linear-gradient(135deg, #8b0000 0%, #ff4b4b 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 28px;'>🩸 PUNJAB BLOOD DONATION</h1>
        <p style='margin:5px 0; font-size: 18px;'>Welfare Committee Pindi Amolak</p>
        <p style='margin:0; font-size: 12px; opacity: 0.8;'>Created by: Mani Rajput</p>
    </div>
    """, unsafe_allow_html=True)

# --- Google Sheets Connection ---
sheet_url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    return conn.read(spreadsheet=sheet_url, usecols=[0, 1, 2, 3])

# --- Sidebar Menu (Bohat Wazeh) ---
st.sidebar.header("📋 MAIN MENU")
choice = st.sidebar.selectbox(
    "Option Select Karein:", 
    ["Donors Directory", "Register as Donor", "About/Help"]
)

all_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

# --- Logical Switching ---

if choice == "Register as Donor":
    st.subheader("📝 Naya Donor Shamil Karein")
    with st.form("main_form", clear_on_submit=True):
        name = st.text_input("Naam")
        bg = st.selectbox("Blood Group", all_groups)
        city = st.text_input("Shehar", value="Pindi Amolak")
        phone = st.text_input("Mobile/WhatsApp")
        
        if st.form_submit_button("Save Karein"):
            if name and phone:
                try:
                    df = load_data()
                    new_row = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    st.success("Mubarak ho! Data save ho gaya.")
                    st.balloons()
                except:
                    st.error("Sheet Connection Error!")
            else:
                st.warning("Naam aur Number lazmi hain.")

elif choice == "Donors Directory":
    st.subheader("🔍 Donors ki Talash")
    search_bg = st.selectbox("Blood Group Filter", ["All"] + all_groups)
    
    try:
        df = load_data()
        res = df if search_bg == "All" else df[df["Blood Group"] == search_bg]
        
        if not res.empty:
            for i, row in res.iterrows():
                st.markdown(f"""
                    <div style="background:white; padding:15px; border-radius:10px; border-left:8px solid #8b0000; margin-bottom:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color:#8b0000;">{row['Name']}</h4>
                        <p style="margin:5px 0;">🩸 <b>{row['Blood Group']}</b> | 📍 {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:8px 15px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">📞 Call Now</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Koi donor nahi mila.")
    except:
        st.error("Data load nahi ho saka.")

else:
    st.subheader("💡 Website Istemal Karne ka Tariqa")
    st.write("1. Sidebar se 'Register' select karke apna naam likhein.")
    st.write("2. 'Directory' mein ja kar blood group search karein.")
    st.markdown("---")
    st.write("**Welfare Committee Pindi Amolak**")
