import streamlit as st

# --- 1. CONSTANTES TRIBUTARIAS AG 2025 ---
UVT_2025 = 49799

# Cálculos de topes legales en pesos (COP)
TOPE_VIVIENDA = 1200 * UVT_2025             # $59.758.800
TOPE_MEDICINA = 192 * UVT_2025              # $9.561.408
TOPE_DEP_TRADICIONAL = 384 * UVT_2025       # $19.122.816 (32 UVT/mes)
TOPE_DEP_ADICIONAL = 288 * UVT_2025         # $14.342.112 (72 UVT * máx 4)
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
    nombre = st.text_input("Nombre Completo")
with col_b:
    nit = st.text_input("Cédula / NIT")
with col_c:
    actividad_economica = st.selectbox(
        "Actividad Económica Principal (CIIU)",
        [
            "0010 - Asalariados",
            "0090 - Pensionados",
            "0081 - Personas naturales sin actividad",
            "6910 - Actividades jurídicas",
            "6920 - Actividades de contabilidad y auditoría",
            "7020 - Actividades de consultoría",
            "8620 - Práctica médica y odontológica",
            "4711 - Comercio al por menor",
            "6201 - Desarrollo de sistemas informáticos",
            "Otras actividades"
        ]
    )

# --- 3. INGRESOS CÉDULA GENERAL ---
st.header("2. Ingresos Cédula General (Trabajo, Capital, No Laboral)")
col_ing1, col_ing2 = st.columns(2)
with col_ing1:
    ingresos_brutos = st.number_input("Ingresos Brutos Totales", min_value=0.0, step=1000000.0)
with col_ing2:
    incrngo = st.number_input("Ingresos No Constitutivos de Renta (Salud, Pensión, FSP obligatorios)", min_value=0.0, step=100000.0, help="Aportes obligatorios que la ley permite restar de entrada para hallar el ingreso neto.")

ingreso_neto = max(0, ingresos_brutos - incrngo)

# --- 4. DEDUCCIONES IMPUTABLES (Con límites en COP) ---
st.header("3. Deducciones Imputables")
st.caption("Nota: El sistema no te permitirá ingresar un valor superior al tope legal anual aplicable para 2025.")
col_d1, col_d2 = st.columns(2)

with col_d1:
    ded_vivienda = st.number_input(
        f"Intereses de Vivienda (Máx ${TOPE_VIVIENDA:,.0f})", 
        min_value=0.0, max_value=float(TOPE_VIVIENDA), step=100000.0,
        help="Intereses pagados por préstamos para adquisición de vivienda del contribuyente (Art. 119 ET). Límite legal: 100 UVT mensuales."
    )
    ded_medicina = st.number_input(
        f"Medicina Prepagada (Máx ${TOPE_MEDICINA:,.0f})", 
        min_value=0.0, max_value=float(TOPE_MEDICINA), step=100000.0,
        help="Pagos por salud, medicina prepagada o seguros de salud para el contribuyente y beneficiarios. Límite legal: 16 UVT mensuales."
    )
    
with col_d2:
    ded_dep_tradicional = st.number_input(
        f"Dependientes Económicos 10% (Máx ${TOPE_DEP_TRADICIONAL:,.0f})", 
        min_value=0.0, max_value=float(TOPE_DEP_TRADICIONAL), step=100000.0,
        help="Deducción del 10% de los ingresos brutos por tener hijos, cónyuge o padres dependientes. Límite legal: 32 UVT mensuales."
    )
    ded_dep_adicional = st.number_input(
        f"Adicional por Dependientes Ley 2277 (Máx ${TOPE_DEP_ADICIONAL:,.0f})", 
        min_value=0.0, max_value=float(TOPE_DEP_ADICIONAL), step=100000.0,
        help="Nueva deducción de 72 UVT por cada dependiente, hasta máximo 4 dependientes. Se puede sumar a la deducción tradicional."
    )
    ded_gmf = st.number_input(
        "Deducción 50% GMF (4x1000)", 
        min_value=0.0, step=10000.0,
        help="Puedes deducir el 50% del Gravamen a los Movimientos Financieros certificado por los bancos."
    )

total_deducciones_limitadas = ded_vivienda + ded_medicina + ded_dep_tradicional + ded_dep_adicional + ded_gmf

# --- 5. RENTAS EXENTAS (Con límites en COP) ---
st.header("4. Rentas Exentas")
col_re1, col_re2 = st.columns(2)

with col_re1:
    re_afc_pensiones = st.number_input(
        f"Aportes Voluntarios Pensión y AFC (Máx ${TOPE_AFC_PENSIONES:,.0f})", 
        min_value=0.0, max_value=float(TOPE_AFC_PENSIONES), step=100000.0,
        help="Aportes a cuentas AFC o fondos voluntarios. Limitado al 30% del ingreso laboral o tributario del año, sin exceder 3.800 UVT."
    )
    # Ajuste automático del tope del 30% para AFC/Voluntarias según la ley
    limite_30_ingreso = ingresos_brutos * 0.30
    re_afc_pensiones_aplicable = min(re_afc_pensiones, limite_30_ingreso)

with col_re2:
    re_cesantias = st.number_input(
        "Cesantías e Intereses de Cesantías", 
        min_value=0.0, step=100000.0,
        help="El valor del ingreso reconocido por cesantías e intereses a las cesantías, que entra como ingreso bruto pero se resta como exento según los límites del Art 206."
    )

# --- 6. CÁLCULO DE LÍMITES Y RENTA EXENTA LABORAL ---
st.header("5. Liquidación Cédula General")

# Motor de cálculo: Renta Exenta Laboral (25%)
renta_exenta_laboral_base = max(0, ingreso_neto - total_deducciones_limitadas - re_afc_pensiones_aplicable - re_cesantias)
renta_exenta_25 = max(0, renta_exenta_laboral_base * 0.25)
renta_exenta_25_aplicable = min(renta_exenta_25, TOPE_25_EXENTO)

# Aplicación del Límite Global (40% o 1.340 UVT)
total_beneficios_sometidos = total_deducciones_limitadas + re_afc_pensiones_aplicable + re_cesantias + renta_exenta_25_aplicable
limite_40 = ingreso_neto * 0.40
limite_final_aplicable = min(limite_40, TOPE_GLOBAL_1340)

beneficios_permitidos = min(total_beneficios_sometidos, limite_final_aplicable)

# Deducción especial: 1% compras factura electrónica (SIN LÍMITE DEL 40%)
st.subheader("Beneficio Adicional (Sin límite del 40%)")
ded_factura_elec = st.number_input(
    f"1% de Compras con Factura Electrónica (Máx ${TOPE_FACTURA_ELEC:,.0f})", 
    min_value=0.0, max_value=float(TOPE_FACTURA_ELEC), step=10000.0,
    help="El 1% del valor de tus compras sustentadas con factura electrónica de venta, sin exceder 240 UVT. No se somete al límite del 40%."
)

renta_liquida_cedula_general = max(0, ingreso_neto - beneficios_permitidos - ded_factura_elec)

# --- PANEL DE RESUMEN ---
st.info(f"**Renta Líquida Gravable Cédula General:** ${renta_liquida_cedula_general:,.0f}")
with st.expander("Ver detalles del límite del 40%"):
    st.write(f"- Total Deducciones y Exentas ingresadas: ${total_beneficios_sometidos:,.0f}")
    st.write(f"- Límite del 40% del Ingreso Neto: ${limite_40:,.0f}")
    st.write(f"- Límite en UVT (1340 UVT): ${TOPE_GLOBAL_1340:,.0f}")
    st.write(f"- **Beneficios finalmente tomados (El menor):** ${beneficios_permitidos:,.0f}")
    st.write(f"- *Nota: La deducción por factura electrónica (${ded_factura_elec:,.0f}) se restó de forma independiente.*")

# --- 7. RENTA POR COMPARACIÓN PATRIMONIAL ---
st.header("6. Renta por Comparación Patrimonial")
col_pat1, col_pat2, col_pat3 = st.columns(3)
with col_pat1:
    patrimonio_liquido_anterior = st.number_input("Patrimonio Líquido Año 2024", min_value=0.0, step=1000000.0)
with col_pat2:
    patrimonio_liquido_actual = st.number_input("Patrimonio Líquido Año 2025", min_value=0.0, step=1000000.0)
with col_pat3:
    pasivos_inexistentes = st.number_input("Pasivos Inexistentes / Bienes Omitidos", min_value=0.0, step=100000.0)

diferencia_patrimonial = max(0, patrimonio_liquido_actual - patrimonio_liquido_anterior)
rentas_justificadas = renta_liquida_cedula_general + incrngo + beneficios_permitidos + ded_factura_elec
renta_comparacion = max(0, diferencia_patrimonial - rentas_justificadas + pasivos_inexistentes)

renta_liquida_definitiva = renta_liquida_cedula_general
if renta_comparacion > 0:
    st.error(f"¡Alerta! Tienes una Renta Líquida por Comparación Patrimonial de: ${renta_comparacion:,.0f}. Revisa tus rentas exentas omitidas o ganancias ocasionales para justificar el patrimonio.")
    renta_liquida_definitiva += renta_comparacion

# --- 8. LIQUIDACIÓN DEL IMPUESTO Y ANTICIPO ---
st.header("7. Liquidación de Impuestos y Saldo a Pagar")
base_uvt = renta_liquida_definitiva / UVT_2025
impuesto_uvt = calcular_impuesto_241(base_uvt)
impuesto_pesos = impuesto_uvt * UVT_2025

# Cálculo en tiempo real del límite legal del 25% para Descuentos (Art. 258 ET)
limite_legal_descuentos = impuesto_pesos * 0.25

col_liq1, col_liq2 = st.columns(2)
with col_liq1:
    descuentos_tributarios = st.number_input(
        "Descuentos Tributarios (Donaciones, I+D+i, etc.)", 
        min_value=0.0, step=100000.0,
        help="Se restan directamente del impuesto. Despliega el panel de abajo para ver la normatividad."
    )
    
    # NUEVO: Panel explicativo de Descuentos Tributarios
    with st.expander("📚 Ver conceptos legales de Descuentos Tributarios (Art. 253 al 257 ET)"):
        st.markdown("""
        **Conceptos válidos según el Estatuto Tributario:**
        1. **Donaciones a ESAL (Art. 257):** 25% del valor donado a entidades del Régimen Tributario Especial o públicas.
        2. **Impuestos pagados en el exterior (Art. 254):** Para residentes que tributaron fuera de Colombia.
        3. **Inversiones I+D+i (Art. 256):** 25% invertido en proyectos avalados en ciencia y tecnología.
        4. **Inversiones en medio ambiente (Art. 253):** 25% de la inversión directa avalada por ANLA/CAR.
        5. **Otros (25%):** Red de Bibliotecas, Parques Naturales, Becas ICETEX, Innpulsa.
        
        ⚠️ **Regla General del Límite (Art. 258 ET):** 
        Los descuentos tributarios no pueden exceder el **25% del impuesto básico de renta**.
        """)
        st.info(f"💡 Para este caso específico, el límite legal máximo a descontar sugerido es: **${limite_legal_descuentos:,.0f}**")

    retenciones = st.number_input("Retenciones en la fuente practicadas en 2025", min_value=0.0, step=100000.0)
    impuesto_neto_anterior = st.number_input("Impuesto neto de renta del año anterior (2024)", min_value=0.0, step=100000.0, help="Obligatorio para calcular el anticipo por el Procedimiento 2 (Promedio).")
with col_liq2:
    anos_declarando = st.selectbox("Número de veces que ha presentado declaración de renta", ["1 vez (25%)", "2 veces (50%)", "3 veces o más (75%)"])
    saldo_favor_anterior = st.number_input("Saldo a favor del año anterior (2024)", min_value=0.0, step=100000.0)

impuesto_neto = max(0, impuesto_pesos - descuentos_tributarios)

# --- MOTOR DE CÁLCULO DE ANTICIPO (Art 807 ET) ---
porcentaje_anticipo = 0.25 if "1" in anos_declarando else (0.50 if "2" in anos_declarando else 0.75)

# Procedimiento 1: Impuesto del año actual
anticipo_metodo_1 = max(0, (impuesto_neto * porcentaje_anticipo) - retenciones)

# Procedimiento 2: Promedio de los dos últimos años
promedio_impuestos = (impuesto_neto + impuesto_neto_anterior) / 2
anticipo_metodo_2 = max(0, (promedio_impuestos * porcentaje_anticipo) - retenciones)

# El sistema elige el menor impuesto
anticipo_final = min(anticipo_metodo_1, anticipo_metodo_2)

saldo_total = (impuesto_neto + anticipo_final) - retenciones - saldo_favor_anterior

st.markdown("---")

# Mostrar análisis de la elección del anticipo al usuario
with st.expander("Ver análisis detallado del Anticipo de Renta (Art 807 ET)"):
    st.write(f"Según la ley, puedes elegir el procedimiento que arroje el menor valor a pagar:")
    st.write(f"- **Porcentaje aplicado:** {porcentaje_anticipo * 100}%")
    st.write(f"- **Procedimiento 1 (Basado en impuesto actual):** ${anticipo_metodo_1:,.0f}")
    st.write(f"- **Procedimiento 2 (Basado en promedio con año anterior):** ${anticipo_metodo_2:,.0f}")
    st.success(f"**El sistema seleccionó automáticamente el menor valor: ${anticipo_final:,.0f}**")

col_res1, col_res2, col_res3 = st.columns(3)
col_res1.metric(label="IMPUESTO NETO A CARGO", value=f"${impuesto_neto:,.0f}")
col_res2.metric(label="ANTICIPO AÑO SIGUIENTE", value=f"${anticipo_final:,.0f}")

if saldo_total > 0:
    col_res3.metric(label="🔴 SALDO A PAGAR", value=f"${saldo_total:,.0f}")
else:
    col_res3.metric(label="🟢 SALDO A FAVOR", value=f"${abs(saldo_total):,.0f}")

st.caption("Nota Legal: Este liquidador es una herramienta de referencia basada en la normativa vigente (incluyendo modificaciones Ley 2277/2022). Se recomienda validación profesional final.")
