import streamlit as st
import pandas as pd

# --- 1. CONSTANTES TRIBUTARIAS AG 2025 ---
UVT_2025 = 49799

# Cálculos de topes legales en pesos (COP)
TOPE_VIVIENDA = 1200 * UVT_2025
TOPE_MEDICINA = 192 * UVT_2025
TOPE_DEP_TRADICIONAL = 384 * UVT_2025
TOPE_1_DEP = 72 * UVT_2025
TOPE_DEP_ADICIONAL = 288 * UVT_2025
TOPE_ICETEX = 100 * UVT_2025
TOPE_AFC_PENSIONES = 3800 * UVT_2025
TOPE_FACTURA_ELEC = 240 * UVT_2025
TOPE_25_EXENTO = 790 * UVT_2025
TOPE_GLOBAL_1340 = 1340 * UVT_2025

def calcular_impuesto_241(base_uvt):
    if base_uvt <= 1090: return 0
    elif base_uvt <= 1700: return (base_uvt - 1090) * 0.19
    elif base_uvt <= 4100: return (base_uvt - 1700) * 0.28 + 116
    elif base_uvt <= 8670: return (base_uvt - 4100) * 0.33 + 788
    elif base_uvt <= 18970: return (base_uvt - 8670) * 0.35 + 2296
    elif base_uvt <= 31000: return (base_uvt - 18970) * 0.37 + 5901
    else: return (base_uvt - 31000) * 0.39 + 10352

st.set_page_config(page_title="Liquidador DIAN 2025", layout="wide")
st.title("Liquidador Renta Personas Naturales - AG 2025")

# --- 2. DATOS DEL CONTRIBUYENTE ---
st.header("1. Datos del Contribuyente")
col_a, col_b, col_c = st.columns(3)
with col_a: nombre = st.text_input("Nombre Completo", value="Deisy Carolina Sanabria Saosa")
with col_b: nit = st.text_input("Cédula / NIT", value="1098665319")
with col_c: 
    es_independiente = st.checkbox("¿Es usted trabajador independiente?")
    actividad_economica = st.selectbox("Actividad Económica (CIIU)", ["0010 - Asalariados", "6910 - Actividades jurídicas", "7020 - Actividades de consultoría", "Otras"])

# --- 3. PATRIMONIO ---
st.header("2. Liquidación de Patrimonio")
# (El código del patrimonio se mantiene igual que en la versión anterior para no borrar nada)
# [Se asume el mismo código de patrimonio de la versión anterior]
# ...

# --- 4. INGRESOS Y OPTIMIZACIÓN INDEPENDIENTE ---
st.header("3. Ingresos Cédula General y Optimización Fiscal")

col_ing1, col_ing2 = st.columns(2)
with col_ing1: ing_brutos = st.number_input("Ingresos Brutos Totales", min_value=0.0, step=1000000.0)
with col_ing2: incrngo = st.number_input("INCRNGO (Seguridad Social)", min_value=0.0, step=100000.0)

ingreso_neto = max(0, ing_brutos - incrngo)

costos_procedentes = 0.0
if es_independiente:
    st.info("Modo Independiente activado. El sistema comparará Costos vs Renta Exenta 25%.")
    costos_procedentes = st.number_input("Costos y Gastos Procedentes (Soportados)", min_value=0.0, step=100000.0)

# Cálculo de la Renta Exenta 25% (Base limpia)
base_25 = max(0, ingreso_neto - costos_procedentes)
renta_exenta_25 = min(base_25 * 0.25, TOPE_25_EXENTO)

# --- DECISIÓN DE OPTIMIZACIÓN ---
if es_independiente:
    if costos_procedentes > renta_exenta_25:
        st.success(f"✅ El sistema ha elegido **COSTOS PROCEDENTES** (${costos_procedentes:,.0f}) por ser más beneficioso que la Renta Exenta del 25% (${renta_exenta_25:,.0f}).")
        beneficio_seleccionado = costos_procedentes
    else:
        st.success(f"✅ El sistema ha elegido **RENTA EXENTA 25%** (${renta_exenta_25:,.0f}) por ser más beneficioso que los Costos (${costos_procedentes:,.0f}).")
        beneficio_seleccionado = renta_exenta_25
else:
    beneficio_seleccionado = renta_exenta_25

# --- LÍMITE GLOBAL 40% Y LIQUIDACIÓN FINAL ---
# [Se mantiene el resto de la lógica de límites globales y liquidación del impuesto...]
# (Debes integrar este nuevo bloque de ingresos con el resto del código existente)

st.write("---")
st.caption("Nota: El liquidador aplica automáticamente la opción más favorable para tu base gravable.")
