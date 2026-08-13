import streamlit as st

# 1. CONSTANTES TRIBUTARIAS AG 2025
UVT_2025 = 49799

def calcular_impuesto_241(base_uvt):
    """Calcula el impuesto de renta según la tabla del Art. 241 del Estatuto Tributario."""
    if base_uvt <= 1090: return 0
    elif base_uvt <= 1700: return (base_uvt - 1090) * 0.19
    elif base_uvt <= 4100: return (base_uvt - 1700) * 0.28 + 116
    elif base_uvt <= 8670: return (base_uvt - 4100) * 0.33 + 788
    elif base_uvt <= 18970: return (base_uvt - 8670) * 0.35 + 2296
    elif base_uvt <= 31000: return (base_uvt - 18970) * 0.37 + 5901
    else: return (base_uvt - 31000) * 0.39 + 10352

st.title("Liquidador Renta Personas Naturales - AG 2025")
st.write(f"**Valor UVT 2025:** ${UVT_2025:,.0f} COP")

# --- 2. CÉDULA GENERAL Y LÍMITES ---
st.header("1. Cédula General (Rentas de Trabajo, Capital y No Laborales)")
col1, col2 = st.columns(2)

with col1:
    ingresos_brutos = st.number_input("Ingresos Brutos Totales", min_value=0.0, step=1000000.0)
    incrngo = st.number_input("Ingresos No Constitutivos de Renta (Salud, Pensión)", min_value=0.0, step=100000.0)
    ingreso_neto = ingresos_brutos - incrngo

with col2:
    deducciones = st.number_input("Deducciones (Dependientes, Medicina Prepagada, Intereses)", min_value=0.0, step=100000.0)
    rentas_exentas = st.number_input("Otras Rentas Exentas (Aportes AFC, Cesantías)", min_value=0.0, step=100000.0)

# Motor de optimización: Cálculo Renta Exenta Laboral (25%)
renta_exenta_laboral_base = max(0, ingreso_neto - deducciones - rentas_exentas)
renta_exenta_25 = max(0, renta_exenta_laboral_base * 0.25)
limite_25_uvt = 790 * UVT_2025
renta_exenta_25 = min(renta_exenta_25, limite_25_uvt)

# Aplicación del Límite global del 40% o 1340 UVT
total_exentas_deducciones = deducciones + rentas_exentas + renta_exenta_25
limite_40 = ingreso_neto * 0.40
limite_1340_uvt = 1340 * UVT_2025
limite_final_aplicable = min(limite_40, limite_1340_uvt)

exentas_deducciones_permitidas = min(total_exentas_deducciones, limite_final_aplicable)
renta_liquida_cedula_general = max(0, ingreso_neto - exentas_deducciones_permitidas)

st.info(f"**Renta Líquida Cédula General (Base Gravable):** ${renta_liquida_cedula_general:,.0f}")

# --- 3. RENTA POR COMPARACIÓN PATRIMONIAL ---
st.header("2. Renta por Comparación Patrimonial")
patrimonio_liquido_anterior = st.number_input("Patrimonio Líquido Año 2024", min_value=0.0, step=1000000.0)
patrimonio_liquido_actual = st.number_input("Patrimonio Líquido Año 2025", min_value=0.0, step=1000000.0)
pasivos_inexistentes = st.number_input("Pasivos Inexistentes / Bienes Omitidos", min_value=0.0, step=100000.0)

diferencia_patrimonial = max(0, patrimonio_liquido_actual - patrimonio_liquido_anterior)
# Simplificación de rentas que justifican el incremento
rentas_justificadas = renta_liquida_cedula_general + incrngo + rentas_exentas 

renta_comparacion = max(0, diferencia_patrimonial - rentas_justificadas + pasivos_inexistentes)

if renta_comparacion > 0:
    st.error(f"¡Alerta! Renta gravable adicional por comparación patrimonial: ${renta_comparacion:,.0f}")
    renta_liquida_gravable = renta_liquida_cedula_general + renta_comparacion
else:
    st.success("El incremento patrimonial se encuentra debidamente justificado.")
    renta_liquida_gravable = renta_liquida_cedula_general

# --- 4. LIQUIDACIÓN DEL IMPUESTO Y ANTICIPO ---
st.header("3. Liquidación y Anticipo (Año 2026)")
base_uvt = renta_liquida_gravable / UVT_2025
impuesto_uvt = calcular_impuesto_241(base_uvt)
impuesto_pesos = impuesto_uvt * UVT_2025

descuentos_tributarios = st.number_input("Descuentos Tributarios (Donaciones, etc.)", min_value=0.0, step=100000.0)
impuesto_neto = max(0, impuesto_pesos - descuentos_tributarios)

anos_declarando = st.selectbox("Años declarando renta", ["Primer año (25%)", "Segundo año (50%)", "Tercer año o más (75%)"])
retenciones = st.number_input("Retenciones en la fuente practicadas en 2025", min_value=0.0, step=100000.0)

porcentaje_anticipo = 0.25 if "Primer" in anos_declarando else (0.50 if "Segundo" in anos_declarando else 0.75)
anticipo_calculado = (impuesto_neto * porcentaje_anticipo) - retenciones
anticipo_final = max(0, anticipo_calculado)

st.metric(label="IMPUESTO NETO A CARGO", value=f"${impuesto_neto:,.0f}")
st.metric(label="ANTICIPO RENTA 2026", value=f"${anticipo_final:,.0f}")
st.metric(label="TOTAL SALDO A PAGAR", value=f"${(impuesto_neto + anticipo_final - retenciones):,.0f}")