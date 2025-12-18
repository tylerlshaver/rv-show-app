# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. LIST OF OUTFITTERS ---
OUTFITTERS = ["Select...", "John Smith", "Sarah Jones", "Mike Miller", "Taylor Reed", "Chris Wilson"]

st.set_page_config(page_title="RV Show Digital Guide", page_icon="🚐", layout="wide")

@st.cache_data
def load_data():
    try:
        # We use latin1 encoding here as backup for CSVs exported from Excel
        df = pd.read_csv('LANSING SHOW 26.csv', encoding='latin1')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

df = load_data()

if 'lead_list' not in st.session_state:
    st.session_state.lead_list = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🚐 Welcome to the RV Show!")
    st.markdown("### Sign in to access inventory and floorplans.")
    
    with st.form("login_form"):
        st.subheader("Customer Information")
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        outfitter = st.selectbox("Who is your Outfitter today?", OUTFITTERS)
        submit = st.form_submit_button("Access Digital Guide")
        
        if submit:
            if name and phone and outfitter != "Select...":
                st.session_state.lead_list.append({
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Name": name, "Phone": phone, "Outfitter": outfitter
                })
                st.session_state.user_name = name
                st.session_state.outfitter = outfitter
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Please fill out all fields.")

else:
    if df is not None:
        st.sidebar.title("Filters")
        mfr_list = sorted(df['MANUFACTORER'].unique().tolist())
        selected_mfr = st.sidebar.multiselect("Manufacturer", options=mfr_list)
        
        filtered_df = df.copy()
        if selected_mfr:
            filtered_df = filtered_df[filtered_df['MANUFACTORER'].isin(selected_mfr)]

        st.title(f"📍 Welcome, {st.session_state.user_name}")
        st.info(f"Your Outfitter: **{st.session_state.outfitter}**")
        
        for _, row in filtered_df.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"### {row['YEAR']} {row['MANUFACTORER']} {row['MAKE']}")
                    st.caption(f"Model: {row['MODEL']}")
                with col2:
                    st.write(f"📏 {row['LENGTH(FT)']} ft | ⚖️ {row['WEIGHT(LBS)']} lbs")
                with col3:
                    st.subheader(f"{row['SALE PRICE']}")
                    st.link_button("View Floorplan 🔗", row['FLOORPLAN URL'])

    st.divider()
    with st.expander("Admin & Lead Export"):
        if st.session_state.lead_list:
            leads_df = pd.DataFrame(st.session_state.lead_list)
            st.dataframe(leads_df)
            csv_data = leads_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Leads CSV", csv_data, "leads.csv", "text/csv")
        else:
            st.write("No leads recorded yet.")

    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. LIST OF OUTFITTERS ---
OUTFITTERS = ["Select...", "John Smith", "Sarah Jones", "Mike Miller", "Taylor Reed", "Chris Wilson"]

st.set_page_config(page_title="RV Show Digital Guide", page_icon="🚐", layout="wide")

@st.cache_data
def load_data():
    try:
        # We use latin1 encoding here as backup for CSVs exported from Excel
        df = pd.read_csv('LANSING SHOW 26.csv', encoding='latin1')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

df = load_data()

if 'lead_list' not in st.session_state:
    st.session_state.lead_list = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🚐 Welcome to the RV Show!")
    st.markdown("### Sign in to access inventory and floorplans.")
    
    with st.form("login_form"):
        st.subheader("Customer Information")
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        outfitter = st.selectbox("Who is your Outfitter today?", OUTFITTERS)
        submit = st.form_submit_button("Access Digital Guide")
        
        if submit:
            if name and phone and outfitter != "Select...":
                st.session_state.lead_list.append({
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Name": name, "Phone": phone, "Outfitter": outfitter
                })
                st.session_state.user_name = name
                st.session_state.outfitter = outfitter
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Please fill out all fields.")

else:
    if df is not None:
        st.sidebar.title("Filters")
        mfr_list = sorted(df['MANUFACTORER'].unique().tolist())
        selected_mfr = st.sidebar.multiselect("Manufacturer", options=mfr_list)
        
        filtered_df = df.copy()
        if selected_mfr:
            filtered_df = filtered_df[filtered_df['MANUFACTORER'].isin(selected_mfr)]

        st.title(f"📍 Welcome, {st.session_state.user_name}")
        st.info(f"Your Outfitter: **{st.session_state.outfitter}**")
        
        for _, row in filtered_df.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"### {row['YEAR']} {row['MANUFACTORER']} {row['MAKE']}")
                    st.caption(f"Model: {row['MODEL']}")
                with col2:
                    st.write(f"📏 {row['LENGTH(FT)']} ft | ⚖️ {row['WEIGHT(LBS)']} lbs")
                with col3:
                    st.subheader(f"{row['SALE PRICE']}")
                    st.link_button("View Floorplan 🔗", row['FLOORPLAN URL'])

    st.divider()
    with st.expander("Admin & Lead Export"):
        if st.session_state.lead_list:
            leads_df = pd.DataFrame(st.session_state.lead_list)
            st.dataframe(leads_df)
            csv_data = leads_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Leads CSV", csv_data, "leads.csv", "text/csv")
        else:
            st.write("No leads recorded yet.")

    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()
