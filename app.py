import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page configuration
st.set_page_config(page_title="Punjab Blood Donation", page_icon="🩸", layout="centered")

# --- Header Section ---
st.markdown("""
    <div style="background-color: #8b0000; padding: 25px; border-radius: 15px; text-align: center; color: white; margin-bottom: 20px; border: 2px solid #ff4b4b;">
        <h1 style='margin:0; font-size: 35px;'>🩸 PUNJAB BLOOD DONATION</h1>
        <h3 style='margin:10px 0; font-weight: normal;'>Welfare Committee Pindi Amolak</h3>
        <p style='margin:0; opacity: 0.8; font-style: italic;'>Created by: <b>Mani Rajput</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- Google Sheets Connection ---
# Aapka Diya Hua Link Yahan Set Hai
sheet_url = "https://docs.google.com/spreadsheets/d/1Okg9YfrZPDe2HcvWm8slcVlOV3-ZMianEAX-BRylRq8/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    return conn.read(spreadsheet=sheet_url, usecols=[0, 1, 2, 3])

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
menu = ["Donors Directory", "Register as Donor", "Help"]
choice = st.sidebar.radio("Select Option", menu)

all_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

# --- Registration Page ---
if choice == "Become a Donor":
    st.subheader("📝 Naya Donor Register Karein")
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("Aapka Mukammal Naam")
        bg = st.selectbox("Blood Group", all_groups)
        city = st.text_input("Shehar", value="Pindi Amolak")
        phone = st.text_input("Mobile Number (WhatsApp)")
        
        submitted = st.form_submit_button("Register Hon")
        if submitted:
            if name and phone:
                try:
                    existing_data = load_data()
                    new_row = pd.DataFrame([{"Name": name, "Blood Group": bg, "City": city, "Contact": phone}])
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    st.balloons()
                    st.success(f"Shukriya {name}! Aapka data save ho gaya hai.")
                except Exception as e:
                    st.error("Error: Meharbani karke check karein ke Google Sheet 'Editor' mode par share hai.")
            else:
                st.error("Naam aur Number lazmi likhein.")

# --- Directory Page ---
elif choice == "Donors Directory":
    st.subheader("🔍 Blood Donors ki Directory")
    search_bg = st.selectbox("Blood Group Filter Karein", ["All"] + all_groups)
    
    try:
        df = load_data()
        if search_bg != "All":
            display_df = df[df["Blood Group"] == search_bg]
        else:
            display_df = df

        if not display_df.empty:
            for index, row in display_df.iterrows():
                # Displaying cards
                st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 10px; border-left: 10px solid #d32f2f; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h3 style="margin:0; color:#8b0000;">{row['Name']}</h3>
                        <p style="margin:5px 0;"><b>Blood Group:</b> <span style="color:red;">{row['Blood Group']}</span> | <b>City:</b> {row['City']}</p>
                        <a href="tel:{row['Contact']}" style="background-color:#2e7d32; color:white; padding:8px 20px; text-decoration:none; border-radius:5px; display:inline-block; font-weight:bold; margin-top:5px;">📞 Call: {row['Contact']}</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Abhi is group ka koi donor majood nahi hai.")
    except:
        st.warning("Data load nahi ho saka. Sheet permissions check karein.")

else:
    st.subheader("💡 Website Istemal Karne ka Tariqa")
    st.write("1. **Register Hon:** Agar aap khoon dena chahte hain, toh apni details 'Register as Donor' mein likhein.")
    st.write("2. **Talash:** Directory mein ja kar matlooba group select karein.")
    st.write("3. **Rabta:** Seedha 'Call' button daba kar donor se baat karein.")
    st.markdown("---")
    st.write("**Created for Welfare Committee Pindi Amolak by Mani Rajput**")
