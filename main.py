import pandas as pd
import streamlit as st

# Cargar el dataset
df = pd.read_csv("data/invoices_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Configurar el título del dashboard
st.title("Dashboard Interactivo de Facturas 📊")

# Filtrado por rango de fechas
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input("Fecha de inicio", value=df["Date"].min())
end_date = st.sidebar.date_input("Fecha de fin", value=df["Date"].max())
# Filtro por método de pago
payment_method = st.sidebar.multiselect("Métodos de Pago", options=df["PaymentMethod"].unique(), default=df["PaymentMethod"].unique())

# Validar rango de fechas
if start_date > end_date:
    st.sidebar.error("La fecha de inicio no puede ser posterior a la fecha de fin.")

# Filtrar el dataframe según las fechas seleccionadas
filtered_data = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
filtered_data = filtered_data[filtered_data["PaymentMethod"].isin(payment_method)]

# Mostrar los datos filtrados
st.subheader(f"Facturas entre {start_date} y {end_date}")
st.dataframe(filtered_data)

# Resumen de métricas
st.subheader("Resumen de métricas")
total_revenue = filtered_data["Total"].sum()
num_invoices = filtered_data.shape[0]
st.metric(label="Total Ingresos ($)", value=f"{total_revenue:,.2f}")
st.metric(label="Número de Facturas", value=num_invoices)

import altair as alt

# Gráfico de ingresos por fecha
revenue_chart = (
    alt.Chart(filtered_data)
    .mark_line()
    .encode(
        x="Date:T",
        y="Total:Q",
        tooltip=["Date", "Total"]
    )
    .interactive()
)

st.subheader("Ingresos por Fecha")
st.altair_chart(revenue_chart, use_container_width=True)
