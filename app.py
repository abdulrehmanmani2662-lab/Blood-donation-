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
        background: white; padding: 15px; border-radius: 12px; 
        border-left: 8px solid #990000; margin-bottom: 10px; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
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
        phone = st.text_input("WhatsApp Number")
        
        if st.form_submit_button("SAVE DATA"):
            if name and phone:
                # Aapke Google Form ka Link
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe-XoMAt_e9E6lR6o6YvV4DqR69N_n7XfW_R1p2Y_G-A_v8aA/formResponse"
                payload = {
                    "entry.1491566373": name,
                    "entry.1741517409": bg,
                    "entry.1945112345": city,
                    "entry.1235116789": phone
                }
                try:
                    requests.post(form_url, data=payload)
                    st.success("Data saved! Ek baar Search page refresh karein.")
                    st.balloons()
                except:
                    st.error("Error saving data.")
            else:
                st.warning("Please fill all fields.")

# --- Search Page (Fixing the List Display) ---
else:
    st.subheader("🔍 Donors Directory")
    sheet_id = "1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8"
    # Exporting as CSV for live updates
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    try:
        # data load karte waqt cache bypass karne ke liye ttl=0 ya direct URL use kar rahe hain
        df = pd.read_csv(csv_url)
        
        if not df.empty:
            # Filter bar
            choice = st.selectbox("Filter by Blood Group", ["All"] + ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            # Google Forms usually adds a Timestamp as the first column. 
            # We skip it and match columns.
            if choice != "All":
                # Blood Group Column check (usually index 2 or 3 depending on form)
                filtered_df = df[df.iloc[:, 2] == choice]
            else:
                filtered_df = df

            # Reverse the list to show newest donors on top
            for i, row in filtered_df[::-1].iterrows():
                st.markdown(f"""
                    <div class="donor-card">
                        <h4 style="margin:0; color:#990000;">{row.iloc[1]}</h4>
                        <p style="margin:5px 0; color:#333;">🩸 <b>{row.iloc[2]}</b> | 📍 {row.iloc[3]}</p>
                        <a href="tel:{row.iloc[4]}" style="background:#28a745; color:white; padding:8px; text-decoration:none; border-radius:5px; display:block; text-align:center; font-weight:bold;">📞 CALL NOW</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi koi donor register nahi hai.")
    except Exception as e:
        st.info("Searching for latest donors... Refreshing list.")
