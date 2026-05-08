import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config - GitHub icon aur menu hatane ke liye
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- Custom CSS (GitHub Icon aur फालतू cheezein hatane ke liye) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Better Design */
    .header-box {
        background: linear-gradient(135deg, #b22222 0%, #ff4b4b 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .donor-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 10px solid #b22222;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0;'>🩸 PUNJAB BLOOD DONATION</h1>
        <h2 style='margin:5px 0; font-weight: 300;'>Welfare Committee Pindi Amolak</h2>
        <hr style='border: 0.5px solid rgba(255,255,255,0.3);'>
        <p style='margin:0; font-size: 14px;'>Created by: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- Google Sheets Connection ---
sheet_url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    return conn.read(spreadsheet=sheet_url, usecols=[0, 1, 2, 3])

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
# Yahan choice ko bilkul fresh rakha hai
choice = st.sidebar.radio("Select Option", ["Register as Donor", "Donors Directory", "Help & Info"])

all_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

# --- PAGE LOGIC ---

if choice == "Register as Donor":
    st.markdown("### 📝 Naya Donor Register Karein")
    with st.form("main_registration_form", clear_on_submit=True):
        name = st.text_input("Aapka Mukammal Naam")
        bg = st.selectbox("Blood Group", all_groups)
        city = st.text_input("Shehar", value="Pindi Amolak")
        phone = st.text_input("Mobile Number (WhatsApp)")
        
        submit_btn = st.form_submit_button("List mein Shamil Hon")
        
        if submit_btn:
            if name and phone:
                try:
                    df = load_data()
                    new_entry = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([df, new_entry], ignore_index=True)
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    st.success(f"Zabardast! {name}, aapka data save ho gaya hai.")
                    st.balloons()
                except:
                    st.error("Data save nahi ho saka. Sheet permissions check karein.")
            else:
                st.warning("Meharbani karke Naam aur Number lazmi likhein.")

elif choice == "Donors Directory":
    st.markdown("### 🔍 Blood Donors Directory")
    search_bg = st.selectbox("Blood Group Select Karein", ["All"] + all_groups)
    
    try:
        df = load_data()
        filtered_df = df if search_bg == "All" else df[df["Blood Group"] == search_bg]
        
        if not filtered_df.empty:
            for i, row in filtered_df.iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h3 style="margin:0; color:#b22222;">{row['Name']}</h3>
                        <p style="margin:5px 0;">🩸 Group: <b>{row['Blood Group']}</b> | 📍 City: {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background:#28a745; color:white; padding:10px 20px; text-decoration:none; border-radius:8px; display:inline-block; font-weight:bold; margin-top:5px;">📞 Call Now</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Filhal koi donor majood nahi hai.")
    except:
        st.error("Data load karne mein masla aa raha hai.")

else:
    # HELP & INFO PAGE
    st.markdown("### 💡 Website Istemal Karne ka Tariqa")
    st.write("1. **Register Hon:** Sidebar se 'Register as Donor' select karein aur form bharein.")
    st.write("2. **Talash:** 'Donors Directory' mein ja kar blood group filter karein.")
    st.write("3. **Rabta:** Seedha Call button se donor ko phone karein.")
    st.markdown("---")
    st.info("Ye platform Mani Rajput ne Welfare Committee Pindi Amolak ke liye banaya hai.")
