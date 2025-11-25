import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Dataset (10 rows) consistent and realistic for server/data processing context
data = pd.DataFrame({
    "Server_Location": ["Jakarta Data Hub", "Bandung AI Center", "Surabaya Compute", 
                        "Bali Cloud Node", "Medan Storage Unit", "Makassar Edge Server", 
                        "Yogyakarta AI Lab", "Semarang Processing", "Balikpapan Backup", 
                        "Pontianak Mini Server"],
    "Data_Processed_TB":[220, 180, 260, 140, 110, 160, 95, 150, 70, 125],
    "Downtime_Hours":[4, 6, 3, 5, 8, 4, 7, 6, 9, 5],
    "Efficiency_%":[92, 88, 95, 85, 80, 90, 83, 87, 75, 86],
    "lat": [-6.2, -6.9, -7.2, -8.6, 3.5, -5.1, -7.8, -6.9, -1.2, -0.02],
    "lon": [106.8, 107.6, 112.7, 115.2, 98.6, 119.4, 110.4, 110.4, 116.8, 109.3]
})


st.subheader("Data")
st.dataframe(data)

# Dropdown 
tipe = st.selectbox("Pilih jenis grafik:", ["Bar", "Pie", "Line", "Area", "Map"])

if tipe == "Bar":
    st.bar_chart(data.set_index("Server_Location"))

elif tipe == "Line":
    st.line_chart(data.set_index("Server_Location"))

elif tipe == "Area":
    st.area_chart(data.set_index("Server_Location"))

elif tipe == "Pie":
    fig, ax = plt.subplots()
    ax.pie(
        data["Data_Processed_TB"], 
        labels=data["Server_Location"], 
        autopct="%1.1f%%"
    )
    st.pyplot(fig)

elif tipe == "Map":
    data_map = data[['lat', 'lon']]
    st.map(data_map)    
