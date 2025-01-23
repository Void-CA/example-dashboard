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

# Resumen de métricas
st.subheader("Resumen de métricas")
metrics_columns = st.columns(4)
total_revenue = filtered_data["Total"].sum()
num_invoices = filtered_data.shape[0]

with metrics_columns[0]:
    st.metric(label="Total Ingresos ($)", value=f"{total_revenue:,.2f}")
    st.metric(label="Ingresos Mínimos ($)", value=f"{filtered_data['Total'].min():,.2f}")
with metrics_columns[1]:
    st.metric(label="Ingresos Máximos ($)", value=f"{filtered_data['Total'].max():,.2f}")
    st.metric(label="Ingresos Promedio ($)", value=f"{total_revenue / num_invoices:,.2f}")
with metrics_columns[2]:
    st.metric(label="Número de Productos", value=filtered_data["Product"].nunique())
    st.metric(label="Número de Clientes", value=filtered_data["CustomerID"].nunique())
with metrics_columns[3]:
    st.metric(label="Número de Facturas", value=num_invoices)
    st.metric(label="Facturas pagadas (%)", value=f"{(filtered_data['Status'].value_counts(normalize=True).get('Paid', 0) * 100):.2f}%")

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
