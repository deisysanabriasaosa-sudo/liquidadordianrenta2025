import streamlit as st
import pandas as pd

# --- 1. CONSTANTES TRIBUTARIAS AG 2025 ---
UVT_2025 = 49799

# Cálculos de topes legales en pesos (COP)
TOPE_VIVIENDA = 1200 * UVT_2025             # $59.758.800
TOPE_MEDICINA = 192 * UVT_2025              # $9.561.408
TOPE_DEP_TRADICIONAL = 384 * UVT_2025       # $19.122.816 (32 UVT/mes)
TOPE_1_DEP = 72 * UVT_2025                  # $3.585.528 (Por cada dependiente adicional)
TOPE_DEP_ADICIONAL = 288 * UVT_2025         # $14.342.112 (72 UVT * máx 4)
TOPE_ICETEX = 100 * UVT_2025                # $4.979.900 (Límite intereses ICETEX)
TOPE_AFC_PENSIONES = 3800 * UVT_2025        # $189.236.200 (Y limitado al 30% del ingreso)
TOPE_FACTURA_ELEC = 240 * UVT_2025          # $11.951.760
TOPE_25_EXENTO = 790 * UVT_2025             # $39.341.210
TOPE_GLOBAL_1340 = 1340 * UVT_2025          # $66.730.660

def calcular_impuesto_241(base_uvt):
    """Calcula el impuesto de renta según la tabla del Art. 241 del Estatuto Tributario."""
    if base_uvt <= 1090: return 0
    elif base_uvt <= 1700: return (base_uvt - 1090) * 0.19
    elif base_uvt <= 4100: return (base_uvt - 1700) * 0.28 + 116
    elif base_uvt <= 8670: return (base_uvt - 4100) * 0.33 + 788
    elif base_uvt <= 18970: return (base_uvt - 8670) * 0.35 + 2296
    elif base_uvt <= 31000: return (base_uvt - 18970) * 0.37 + 5901
    else: return (base_uvt - 31000) * 0.39 + 10352

# Configuración de página
st.set_page_config(page_title="Liquidador DIAN 2025", layout="wide")
st.title("Liquidador Renta Personas Naturales - AG 2025")
st.write(f"**Valor UVT 2025:** ${UVT_2025:,.0f} COP")

# --- 2. DATOS DEL CONTRIBUYENTE ---
st.header("1. Datos del Contribuyente")
col_a, col_b, col_c = st.columns(3)
with col_a:
    nombre = st.text_input("Nombre Completo", value="Deisy Carolina Sanabria Saosa")
with col_b:
    nit = st.text_input("Cédula / NIT", value="1098665319")
with col_c:
    actividad_economica = st.selectbox(
        "Actividad Económica Principal (CIIU)",
        [
            "0010 - Asalariados",
            "0090 - Pensionados",
            "0081 - Personas naturales sin actividad",
            "6910 - Actividades jurídicas",
            "6920 - Actividades de contabilidad y auditoría",
            "70
