import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------
# Cargar datos
# ---------------------------
car_data = pd.read_csv("vehicles_us.csv")

st.set_page_config(page_title="Análisis de Vehículos", layout="wide")

# ---------------------------
# Encabezado principal
# ---------------------------
st.title("🚗 Análisis de anuncios de vehículos")
st.write("Explora los datos de anuncios de venta de autos en EE.UU. usando filtros y visualizaciones interactivas.")

# ---------------------------
# Filtros generales
# ---------------------------
st.sidebar.header("Filtros")

# Filtro por año
min_year = int(car_data['model_year'].min())
max_year = int(car_data['model_year'].max())
year_filter = st.sidebar.slider("Año mínimo", min_year, max_year, min_year)

# Filtro por combustible
fuel_options = car_data['fuel'].dropna().unique()
fuel_filter = st.sidebar.multiselect("Tipo de combustible", fuel_options, default=fuel_options)

# Filtro por rango de precios
min_price = int(car_data['price'].min())
max_price = int(car_data['price'].clip(upper=100000).max())  # límite para evitar outliers extremos
price_filter = st.sidebar.slider("Rango de precios", min_price, max_price, (min_price, max_price))

# Aplicar filtros
filtered_data = car_data[
    (car_data['model_year'] >= year_filter) &
    (car_data['fuel'].isin(fuel_filter)) &
    (car_data['price'].between(price_filter[0], price_filter[1]))
]

# ---------------------------
# Tabs de navegación
# ---------------------------
tabs = st.tabs(["📊 Datos", "📈 Histogramas", "🔍 Dispersión", "🚗 Comparación por modelo"])

# --- Tab 1: Vista de datos
with tabs[0]:
    st.subheader("Vista previa del dataset filtrado")
    st.dataframe(filtered_data.head(50))

# --- Tab 2: Histogramas
with tabs[1]:
    st.subheader("Distribución de variables")
    hist_var = st.selectbox("Selecciona la variable para el histograma:", ["price", "odometer", "model_year"])
    fig_hist = px.histogram(filtered_data, x=hist_var, nbins=30,
                            title=f"Distribución de {hist_var}")
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Tab 3: Gráfico de dispersión
with tabs[2]:
    st.subheader("Relación entre variables")
    x_var = st.selectbox("Eje X:", ["odometer", "model_year", "price"], index=0)
    y_var = st.selectbox("Eje Y:", ["price", "odometer"], index=0)
    fig_scatter = px.scatter(filtered_data, x=x_var, y=y_var, color="fuel",
                             title=f"Dispersión de {y_var} vs {x_var}")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Tab 4: Comparación por modelo
with tabs[3]:
    st.subheader("Comparación de variables por modelo")

    if "model" in filtered_data.columns:
        variable = st.selectbox("Selecciona la variable:", ["price", "odometer"])
        top_models = filtered_data['model'].value_counts().nlargest(10).index
        model_data = filtered_data[filtered_data['model'].isin(top_models)]

        col1, col2 = st.columns(2)

        # Boxplot
        with col1:
            fig_box = px.box(model_data, x="model", y=variable,
                             title=f"Distribución de {variable} según el modelo")
            st.plotly_chart(fig_box, use_container_width=True)

        # Promedio en gráfico de barras
        with col2:
            avg_data = model_data.groupby("model")[variable].mean().reset_index()
            fig_bar = px.bar(avg_data, x="model", y=variable,
                             title=f"Promedio de {variable} por modelo")
            st.plotly_chart(fig_bar, use_container_width=True)
