# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. OUTFITTERS LIST ---
OUTFITTERS = ["Select...", "John Smith", "Sarah Jones", "Mike Miller", "Taylor Reed"]

st.set_page_config(page_title="RV Show Guide", page_icon="🚐", layout="wide")

# --- 2. DATA LOADING (UPDATED FOR UTF-8-SIG) ---
@st.cache_data
def load_data():
    try:
        # 'utf-8-sig' specifically ignores the ï»¿ characters
        df = pd.read_csv('LANSING SHOW 26.csv', encoding='utf-8-sig')
        # Standard cleaning
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Could not read the CSV file. Error: {e}")
        return None

df = load_data()

# --- 3. SESSION STATE ---
if 'leads' not in st.session_state:
    st.session_state.leads = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 4. APP LOGIC ---
if not st.session_state.logged_in:
    st.title("🚐 Welcome to the RV Show!")
    st.subheader("Sign in to view inventory")
    
    with st.form(key="unique_login_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        outfitter = st.selectbox("Outfitter", OUTFITTERS)
        if st.form_submit_button("Enter"):
            if name and phone and outfitter != "Select...":
                st.session_state.leads.append({
                    "Date": datetime.now().strftime("%m/%d %H:%M"),
                    "Name": name, "Phone": phone, "Outfitter": outfitter
                })
                st.session_state.user_name = name
                st.session_state.outfitter = outfitter
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("All fields are required.")

else:
    st.title(f"📍 Welcome, {st.session_state.user_name}")
    st.sidebar.header("Filter")
    
    if df is not None:
        # Check if YEAR exists now that we used utf-8-sig
        if 'YEAR' not in df.columns:
            st.error(f"Still can't find 'YEAR'. I see: {list(df.columns)}")
        else:
            mfrs = st.sidebar.multiselect("Brand", options=sorted(df['MANUFACTORER'].unique()))
            filtered = df[df['MANUFACTORER'].isin(mfrs)] if mfrs else df

            for _, row in filtered.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['YEAR']} {row['MANUFACTORER']} {row['MAKE']}")
                        st.write(f"**Model:** {row['MODEL']} | **Status:** {row['STOCK STATUS']}")
                    with col2:
                        st.write(f"Price: **{row['SALE PRICE']}**")
                        st.link_button("Floorplan", str(row['FLOORPLAN URL']))

    # --- ADMIN EXPORT ---
    st.divider()
    with st.expander("Admin: Export Leads"):
        if st.session_state.leads:
            ld_df = pd.DataFrame(st.session_state.leads)
            st.dataframe(ld_df)
            st.download_button("Download CSV", ld_df.to_csv(index=False).encode('utf-8'), "leads.csv")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
