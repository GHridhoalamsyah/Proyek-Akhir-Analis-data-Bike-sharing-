import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')
    
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "registered": "total_registered",
        "casual": "total_casual",
        "cnt": "total_customer"
    }, inplace=True)
    
    return daily_rentals_df

def create_monthly_rentals_df(df):
    monthly_rentals_df = df.resample(rule='M', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })
    monthly_rentals_df = monthly_rentals_df.reset_index()
    monthly_rentals_df.rename(columns={
        "registered": "total_registered",
        "casual": "total_casual",
        "cnt": "total_customer"
    }, inplace=True)
    
    return monthly_rentals_df

def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").cnt.sum().reset_index()
    byhour_df.rename(columns={
        "cnt": "total_customer"
    }, inplace=True)

    return byhour_df


all_df = pd.read_csv('data_utama1.csv')

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]


byhour_df = create_byhour_df(main_df)
daily_rentals_df = create_daily_rentals_df(main_df)
monthly_rentals_df = create_monthly_rentals_df(main_df)


st.header('Bike Sharing Dashboard')

 
col1 ,col2, col3 = st.columns(3)
 
with col1:
    total_rentals = daily_rentals_df.total_customer.sum()
    st.metric("Total Rentals", value=total_rentals)
 
with col2:
    total_registered = daily_rentals_df.total_registered.sum()
    st.metric("Total Registered Customer", value=total_registered)

with col3:
    total_casual = daily_rentals_df.total_casual.sum()
    st.metric("Total Casual Customer", value=total_casual)



fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_rentals_df["dteday"],
    monthly_rentals_df["total_registered"], 
    marker='o', 
    label='Registered Rentals')

plt.plot(
    monthly_rentals_df["dteday"], 
    monthly_rentals_df["total_casual"], 
    marker='o', 
    label='Casual Rentals')


ax.set_xlabel("Bulan")
ax.set_ylabel("Total Customers")
ax.set_title("pinjaman perbulan pelanggan yang teregistrasi dan tidak teregistrasi")
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.legend(fontsize=12)
ax.grid(True)
st.pyplot(fig)

typecust_colors = ['skyblue', 'gold']

fig, ax = plt.subplots(figsize=(14,8))
total_registered = daily_rentals_df['total_registered'].sum()
total_casual = daily_rentals_df['total_casual'].sum()
labels = ['Registered', 'Casual']
sizes = [total_registered, total_casual]
colors_typecust = ['skyblue', 'gold']

ax.pie(sizes, labels=labels, colors=typecust_colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85, textprops={'fontsize': 14})

ax.axis('equal')
plt.tight_layout() 
ax.set_title("Persentase pelanggan yang teregristrasi dan tidak teregistrasi", fontsize=20 , pad=20)
st.pyplot(fig) 
