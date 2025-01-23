import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("dark_background")

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

graph_columns = st.columns(3)

with graph_columns[0]:

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

    # Calcular ingresos por método de pago
    payment_distribution = df.groupby("PaymentMethod")["Total"].sum()

    # Boceto del gráfico
    st.subheader("Distribución de Ingresos por Métodos de Pago")
    fig, ax = plt.subplots()
    ax.pie(payment_distribution, labels=payment_distribution.index, autopct="%1.1f%%", startangle=140, colors=["#FF9999", "#66B2FF", "#99FF99", "#FFCC99"])
    ax.set_title("Métodos de Pago")
    st.pyplot(fig)

    

with graph_columns[1]:
    # Calcular facturas por cliente
    top_customers = df["CustomerName"].value_counts().head(10)
    # Boceto del gráfico
    st.subheader("Top 10 Clientes con Más Facturas")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_customers.index, top_customers.values, color="coral")
    ax.set_title("Top Clientes por Número de Facturas", fontsize=16)
    ax.set_xlabel("Número de Facturas", fontsize=12)
    ax.set_ylabel("Cliente", fontsize=12)
    plt.gca().invert_yaxis()  # Invertir el orden para mostrar el más alto primero
    st.pyplot(fig)


    # Calcular ingresos por mes
    monthly_revenue = df.groupby("Date")["Total"].sum().reset_index()

    # Boceto del gráfico
    st.subheader("Ingresos Totales por Mes")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(monthly_revenue["Date"].astype(str), monthly_revenue["Total"], color="skyblue")
    ax.set_title("Ingresos Totales por Mes", fontsize=16)
    ax.set_xlabel("Mes", fontsize=12)
    ax.set_ylabel("Ingresos Totales ($)", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with graph_columns[2]:
    
    # Calcular ingresos por producto/servicio
    product_revenue = df.groupby("Product")["Total"].sum().sort_values(ascending=False)

    # Boceto del gráfico
    st.subheader("Ingresos por Producto/Servicio")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(product_revenue.index, product_revenue.values, color="lightgreen")
    ax.set_title("Ingresos por Producto/Servicio", fontsize=16)
    ax.set_xlabel("Producto/Servicio", fontsize=12)
    ax.set_ylabel("Ingresos Totales ($)", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)


    # Contar facturas por estado
    invoice_status = df["Status"].value_counts()

    # Boceto del gráfico
    st.subheader("Estado de Facturas")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(invoice_status.index, invoice_status.values, color="gold")
    ax.set_title("Facturas por Estado", fontsize=16)
    ax.set_xlabel("Número de Facturas", fontsize=12)
    ax.set_ylabel("Estado", fontsize=12)
    st.pyplot(fig)
