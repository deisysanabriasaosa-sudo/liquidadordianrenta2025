import streamlit as st
import pandas as pd
import tempfile

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
            "7020 - Actividades de consultoría",
            "8620 - Práctica médica y odontológica",
            "4711 - Comercio al por menor",
            "6201 - Desarrollo de sistemas informáticos",
            "Otras actividades"
        ]
    )

# --- 3. LIQUIDACIÓN DE PATRIMONIO (Tabla Interactiva) ---
st.header("2. Liquidación de Patrimonio (Bienes y Deudas)")
st.caption("Relaciona tus activos y pasivos a 31 de diciembre de 2025. El sistema calculará tu Patrimonio Líquido y lo enviará al módulo de comparación patrimonial.")
st.markdown("---")

# Fila 1: Efectivo
c1, c2, c3 = st.columns([2, 1.5, 3])
c1.write("**1. Efectivo y saldos en cuentas bancarias**")
val_efectivo = c2.number_input("Efectivo", min_value=0.0, step=1000000.0, label_visibility="collapsed")
c3.caption("Art. 268 E.T.: Valor exacto del saldo a 31 de diciembre.")

# Fila 2: Inversiones y CDTs
st.markdown("**2. Inversiones, acciones y aportes (CDTs)**")
with st.expander("Desplegar detalle de CDTs e Inversiones (hasta 15 registros)"):
    st.caption("Identifica cada inversión o CDT y registra su valor a declarar a 31 de diciembre.")
    val_inversiones_cdts = 0.0
    
    for i in range(1, 16):
        col_inv1, col_inv2 = st.columns(2)
        nom_inv = col_inv1.text_input(f"Identificación (CDT/Inversión {i})", key=f"inv_nom_{i}", placeholder="Ej: CDT Bancolombia, Acciones Ecopetrol...")
        val_inv = col_inv2.number_input(f"Valor a declarar (Inversión {i})", min_value=0.0, step=1000000.0, key=f"inv_val_{i}")
        val_inversiones_cdts += val_inv
        
    st.markdown("---")
    val_otras_inv = st.number_input("Otras inversiones / Acciones (Consolidado adicional)", min_value=0.0, step=1000000.0)
    val_inversiones = val_inversiones_cdts + val_otras_inv
    st.info(f"Total Inversiones (Art. 272 E.T.): ${val_inversiones:,.0f}")

# Fila 3: Cuentas por cobrar
c1, c2, c3 = st.columns([2, 1.5, 3])
c1.write("**3. Cuentas por cobrar (Préstamos a terceros)**")
val_cxc = c2.number_input("CxC", min_value=0.0, step=1000000.0, label_visibility="collapsed")
c3.caption("Art. 270 E.T.: Valor nominal del crédito o deuda a tu favor.")

# Fila 4: Bienes Inmuebles
st.markdown("**4. Bienes Inmuebles (Casas, apartamentos, fincas)**")
with st.expander("Desplegar detalle de Bienes Inmuebles (hasta 5 propiedades)"):
    st.caption("Nota: Identifica el inmueble, ingresa su soporte y valores. El sistema liquida automáticamente el mayor valor a declarar (Art. 277 E.T.).")
    
    val_inmuebles = 0.0
    detalle_inmuebles_editados = []
    
    for i in range(1, 6):
        st.markdown(f"**🔹 Inmueble {i}**")
        c_ident1, c_ident2 = st.columns(2)
        nom_inm = c_ident1.text_input(f"Nombre o Identificación (Inmueble {i})", key=f"inm_nom_{i}", placeholder="Ej: Apto 101, Finca El Recuerdo...")
        soporte_inm = c_ident2.text_input(f"Soporte Documental (Inmueble {i})", key=f"inm_soporte_{i}", placeholder="Ej: Escritura Pública 123, Declaración 2024...")
        
        c_inm1, c_inm2, c_inm3 = st.columns(3)
        val_ant = c_inm1.number_input(f"Valor declarado año anterior", min_value=0.0, step=1000000.0, key=f"inm_ant_{i}")
        reajuste = c_inm2.number_input(f"% Reajuste fiscal", min_value=0.0, step=0.01, value=0.0, key=f"inm_reajuste_{i}")
        val_catastral = c_inm3.number_input(f"Avalúo Catastral 2025", min_value=0.0, step=1000000.0, key=f"inm_cat_{i}")
        
        val_ajustado = val_ant * (1 + (reajuste / 100))
        val_declarar = max(val_ajustado, val_catastral)
        
        st.metric(label=f"Valor fiscal a declarar (Inmueble {i})", value=f"${val_declarar:,.0f}")
        
        if val_declarar > 0:
            val_inmuebles += val_declarar
            detalle_inmuebles_editados.append({"Inmueble": nom_inm if nom_inm else f"Inmueble {i}", "Soporte": soporte_inm if soporte_inm else "Sin soporte", "Valor 2025": val_declarar})
        st.write("---")
        
    st.info(f"Total Inmuebles a declarar: ${val_inmuebles:,.0f}")

# Fila 5: Vehículos
st.markdown("**5. Vehículos y maquinaria**")
with st.expander("Desplegar detalle de Vehículos (hasta 2 vehículos)"):
    col_veh1, col_veh2 = st.columns(2)
    val_veh1 = col_veh1.number_input("[Casilla 1] Valor Vehículo 1", min_value=0.0, step=1000000.0)
    val_veh2 = col_veh2.number_input("[Casilla 2] Valor Vehículo 2", min_value=0.0, step=1000000.0)
    val_otros_veh = st.number_input("Otros vehículos / Maquinaria", min_value=0.0, step=1000000.0)
    val_vehiculos = val_veh1 + val_veh2 + val_otros_veh
    st.info(f"Total Vehículos a declarar: ${val_vehiculos:,.0f}")

# Fila 6: Activos Biológicos
c1, c2, c3 = st.columns([2, 1.5, 3])
c1.write("**6. Activos biológicos (Semovientes, ganado, cultivos)**")
val_biologicos = c2.number_input("Biologicos", min_value=0.0, step=1000000.0, label_visibility="collapsed")
c3.caption("Art. 276-2 E.T.: Costo fiscal o valor comercial según aplique contablemente.")

# Fila 7: Otros Activos
c1, c2, c3 = st.columns([2, 1.5, 3])
c1.write("**7. Otros activos (Joyas, muebles, enseres)**")
val_otros_activos = c2.number_input("Otros", min_value=0.0, step=1000000.0, label_visibility="collapsed")
c3.caption("Art. 277 y ss E.T.: Costo de adquisición o costo fiscal.")

st.markdown("---")

# Fila 8: Pasivos (Resta)
c1, c2, c3 = st.columns([2, 1.5, 3])
c1.markdown("**Menos: Pasivos (Deudas con bancos o terceros)**")
val_pasivos = c2.number_input("Pasivos", min_value=0.0, step=1000000.0, label_visibility="collapsed")
c3.caption("Art. 283 E.T.: Deudas reales y consolidadas, respaldadas con documentos idóneos (pagarés, extractos).")

# Cálculos Totales Patrimonio
patrimonio_bruto_calc = val_efectivo + val_inversiones + val_cxc + val_inmuebles + val_vehiculos + val_biologicos + val_otros_activos
patrimonio_liquido_calc = max(0, patrimonio_bruto_calc - val_pasivos)

# --- RESUMEN DE PATRIMONIO A 2025 ---
st.markdown("### 📊 Resumen de Valores a Declarar en Patrimonio (2025)")
resumen_data = []
if val_efectivo > 0: resumen_data.append(["1. Efectivo y Bancos", "Saldos bancarios y efectivo", f"${val_efectivo:,.0f}"])
if val_inversiones > 0: resumen_data.append(["2. Inversiones y CDTs", "Acciones, aportes y CDTs", f"${val_inversiones:,.0f}"])
if val_cxc > 0: resumen_data.append(["3. Cuentas por Cobrar", "Préstamos realizados a terceros", f"${val_cxc:,.0f}"])
if val_inmuebles > 0:
    for inm in detalle_inmuebles_editados:
        resumen_data.append([f"4. Inmueble: {inm['Inmueble']}", f"Soporte: {inm['Soporte']}", f"${inm['Valor 2025']:,.0f}"])
if val_vehiculos > 0: resumen_data.append(["5. Vehículos", "Vehículos y Maquinaria", f"${val_vehiculos:,.0f}"])
if val_biologicos > 0: resumen_data.append(["6. Activos Biológicos", "Semovientes y cultivos", f"${val_biologicos:,.0f}"])
if val_otros_activos > 0: resumen_data.append(["7. Otros Activos", "Muebles, enseres, joyas", f"${val_otros_activos:,.0f}"])

if resumen_data:
    df_resumen = pd.DataFrame(resumen_data, columns=["Concepto Patrimonial", "Detalle / Soporte", "Valor a Declarar 2025"])
    st.table(df_resumen)
    col_tot1, col_tot2 = st.columns(2)
    col_tot1.info(f"**SUMA PATRIMONIO BRUTO:** ${patrimonio_bruto_calc:,.0f}")
    if val_pasivos > 0: col_tot2.warning(f"**MENOS PASIVOS DECLARADOS:** -${val_pasivos:,.0f}")
    st.success(f"**PATRIMONIO LÍQUIDO FINAL 2025:** ${patrimonio_liquido_calc:,.0f}")
else:
    st.warning("No se han ingresado valores en el patrimonio aún.")
st.markdown("---")

# --- 4. INGRESOS CÉDULA GENERAL (Con Optimización Independientes) ---
st.header("3. Ingresos Cédula General (Trabajo, Capital, No Laboral)")

es_independiente = st.checkbox("👤 ¿Es usted trabajador independiente? (Activa la optimización automática entre Costos Procedentes y Renta Exenta del 25%)")

tab_trabajo, tab_capital, tab_nolaboral = st.tabs(["💼 Rentas de Trabajo", "🏢 Rentas de Capital", "🏪 Rentas No Laborales"])

with tab_trabajo:
    with st.expander("💡 Guía Normativa: ¿Qué incluir en Rentas de Trabajo? (Art. 103 E.T.)"):
        st.markdown("""
        **Tipos de Ingreso a reportar:**
        - Salarios, comisiones, prestaciones sociales, viáticos, gastos de representación.
        - Honorarios y compensaciones por servicios personales.
        """)
        
    col_t1, col_t2 = st.columns(2)
    with col_t1: ing_trabajo = st.number_input("Ingresos Brutos Laborales / Honorarios", min_value=0.0, step=1000000.0)
    with col_t2: incrngo_trabajo = st.number_input("INCRNGO Trabajo (Aportes a Salud y Pensión)", min_value=0.0, step=100000.0)
    
    costos_trabajo = 0.0
    if es_independiente:
        costos_trabajo = st.number_input("Costos y Gastos Procedentes (Rentas de Trabajo)", min_value=0.0, step=100000.0, key="cost_t_indep")

with tab_capital:
    with st.expander("💡 Guía Normativa: ¿Qué incluir en Rentas de Capital? (Art. 106 E.T.)"):
        st.markdown("""
        **Tipos de Ingreso a reportar:**
        - Arrendamientos, intereses, rendimientos financieros y regalías.
        """)
        
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1: ing_capital = st.number_input("Ingresos Brutos (Intereses, arriendos, regalías)", min_value=0.0, step=1000000.0)
    with col_c2: incrngo_capital = st.number_input("INCRNGO Capital (Salud, Pensión s/ independientes)", min_value=0.0, step=100000.0)
    with col_c3: costos_capital = st.number_input("Costos procedentes (Capital)", min_value=0.0, step=100000.0)

with tab_nolaboral:
    with st.expander("💡 Guía Normativa: ¿Qué incluir en Rentas No Laborales? (Art. 107 y ss E.T.)"):
        st.markdown("""
        **Tipos de Ingreso a reportar:**
        - Comercio, ventas < 2 años.
        """)
        
    col_nl1, col_nl2, col_nl3 = st.columns(3)
    with col_nl1: ing_nolaboral = st.number_input("Ingresos Brutos (Comercio, ventas < 2 años, etc)", min_value=0.0, step=1000000.0)
    with col_nl2: incrngo_nolaboral = st.number_input("INCRNGO No Laboral (Aportes seguridad social)", min_value=0.0, step=100000.0)
    with col_nl3: costos_nolaboral = st.number_input("Costos procedentes (No Laboral)", min_value=0.0, step=100000.0)

# Consolidación Ingresos y Costos
ingresos_brutos = ing_trabajo + ing_capital + ing_nolaboral
incrngo = incrngo_trabajo + incrngo_capital + incrngo_nolaboral
costos_procedentes_totales = costos_trabajo + costos_capital + costos_nolaboral

ingreso_neto = max(0, ingresos_brutos - incrngo)
ingreso_neto_trabajo = max(0, ing_trabajo - incrngo_trabajo)
renta_liquida_antes_beneficios = max(0, ingreso_neto - costos_procedentes_totales)

st.write(f"**Resumen Consolidado:** Ingresos Brutos Totales: ${ingresos_brutos:,.0f} | Costos Totales: ${costos_procedentes_totales:,.0f} | Ingreso Neto: ${ingreso_neto:,.0f}")
st.markdown("---")

# --- 5. DEDUCCIONES IMPUTABLES COMPLETAS Y TOPETEADAS ---
st.header("4. Deducciones Imputables (Con topes legales en COP)")
col_d1, col_d2 = st.columns(2)

with col_d1:
    val_vivienda = st.number_input(f"Intereses Crédito Vivienda (Máx Legal :red[${TOPE_VIVIENDA:,.0f}])", min_value=0.0, step=100000.0)
    ded_vivienda = min(val_vivienda, float(TOPE_VIVIENDA))
    
    val_medicina = st.number_input(f"Medicina Prepagada (Máx Legal :red[${TOPE_MEDICINA:,.0f}])", min_value=0.0, step=100000.0)
    ded_medicina = min(val_medicina, float(TOPE_MEDICINA))
    
    ded_gmf = st.number_input("Deducción 50% GMF (4x1000)", min_value=0.0, step=10000.0)
    
    val_icetex = st.number_input(f"Intereses Préstamos ICETEX (Máx Legal :red[${TOPE_ICETEX:,.0f}])", min_value=0.0, step=100000.0)
    ded_icetex = min(val_icetex, float(TOPE_ICETEX))

with col_d2:
    limite_10_ingresos = ingresos_brutos * 0.10
    tope_dep_tradicional_aplicable = min(limite_10_ingresos, TOPE_DEP_TRADICIONAL)
    if tope_dep_tradicional_aplicable == 0:
        ded_dep_tradicional = st.number_input("Dependiente Económico 10% (Ingresa ingresos primero)", value=0.0, disabled=True)
    else:
        val_dep_tradicional = st.number_input(f"Dependiente Económico 10% (Tope :red[${tope_dep_tradicional_aplicable:,.0f}])", min_value=0.0, step=100000.0)
        ded_dep_tradicional = min(val_dep_tradicional, float(tope_dep_tradicional_aplicable))
    
    with st.expander("Dependientes Adicionales Ley 2277 (Hasta 4 dependientes)"):
        val_dep_1 = st.number_input(f"Dependiente 1 (Máx: :red[${TOPE_1_DEP:,.0f}])", min_value=0.0, step=10000.0)
        dep_1 = min(val_dep_1, float(TOPE_1_DEP))
        
        val_dep_2 = st.number_input(f"Dependiente 2 (Máx: :red[${TOPE_1_DEP:,.0f}])", min_value=0.0, step=10000.0)
        dep_2 = min(val_dep_2, float(TOPE_1_DEP))
        
        val_dep_3 = st.number_input(f"Dependiente 3 (Máx: :red[${TOPE_1_DEP:,.0f}])", min_value=0.0, step=10000.0)
        dep_3 = min(val_dep_3, float(TOPE_1_DEP))
        
        val_dep_4 = st.number_input(f"Dependiente 4 (Máx: :red[${TOPE_1_DEP:,.0f}])", min_value=0.0, step=10000.0)
        dep_4 = min(val_dep_4, float(TOPE_1_DEP))
        
        ded_dep_adicional = dep_1 + dep_2 + dep_3 + dep_4

total_deducciones_limitadas = ded_vivienda + ded_medicina + ded_dep_tradicional + ded_dep_adicional + ded_gmf + ded_icetex

st.markdown("---")

# --- 6. RENTAS EXENTAS COMPLETAS Y TOPETEADAS ---
st.header("5. Rentas Exentas (Con topes legales en COP)")
col_re1, col_re2 = st.columns(2)

with col_re1:
    tope_afc_dinamico = min(float(TOPE_AFC_PENSIONES), ingresos_brutos * 0.30)
    val_afc_pensiones = st.number_input(f"Aportes Vol. Pensión y AFC (Máx: :red[${tope_afc_dinamico:,.0f}])", min_value=0.0, step=100000.0)
    re_afc_pensiones_aplicable = min(val_afc_pensiones, tope_afc_dinamico)
    
    re_indemnizaciones = st.number_input("Indemnizaciones (Seguros, enfermedad, maternidad)", min_value=0.0, step=100000.0)

with col_re2:
    re_cesantias = st.number_input("Cesantías e Intereses de Cesantías (Valor exento)", min_value=0.0, step=100000.0)
    re_gastos_rep = st.number_input("Gastos de Representación", min_value=0.0, step=100000.0)

st.markdown("---")

# --- 7. PANEL DE OPTIMIZACIÓN INDEPENDIENTE Y CÁLCULO 25% / 40% ---
st.header("6. Liquidación Cédula General y Límites")

base_25_porciento = max(0, ingreso_neto_trabajo - costos_trabajo - total_deducciones_limitadas - re_afc_pensiones_aplicable - re_cesantias - re_indemnizaciones - re_gastos_rep)
calculo_25_bruto = base_25_porciento * 0.25
renta_exenta_25_teorica = min(calculo_25_bruto, TOPE_25_EXENTO)

if es_independiente:
    beneficio_trabajo_aplicado = max(costos_trabajo, renta_exenta_25_teorica)
else:
    beneficio_trabajo_aplicado = renta_exenta_25_teorica

st.markdown("### 🔹 Paso 2: Aplicación del Límite Global del 40%")
total_beneficios_sometidos = total_deducciones_limitadas + re_afc_pensiones_aplicable + re_cesantias + re_indemnizaciones + re_gastos_rep + beneficio_trabajo_aplicado
limite_40 = ingreso_neto * 0.40
limite_uvt_1340 = TOPE_GLOBAL_1340

limite_final_aplicable = min(limite_40, limite_uvt_1340)
beneficios_permitidos = min(total_beneficios_sometidos, limite_final_aplicable)

st.subheader("Beneficio Adicional: Factura Electrónica (1%)")
col_fe1, col_fe2 = st.columns(2)
with col_fe1:
    val_compras_factura = st.number_input("Valor Total Compras con Factura Electrónica", min_value=0.0, step=100000.0)
with col_fe2:
    calculo_1_porciento = val_compras_factura * 0.01
    ded_factura_elec = min(calculo_1_porciento, float(TOPE_FACTURA_ELEC))

renta_liquida_cedula_general = max(0, renta_liquida_antes_beneficios - beneficios_permitidos - ded_factura_elec)

st.markdown("---")

# --- 8. RENTA POR COMPARACIÓN PATRIMONIAL ---
st.header("7. Renta por Comparación Patrimonial")
col_pat1, col_pat2, col_pat3 = st.columns(3)
with col_pat1:
    patrimonio_liquido_anterior = st.number_input("[Casilla 1] Patrimonio Líquido Año 2024", min_value=0.0, step=1000000.0)
with col_pat2:
    patrimonio_liquido_actual = st.number_input("[Casilla 2] Patrimonio Líquido Año 2025", value=float(patrimonio_liquido_calc), min_value=0.0, step=1000000.0)
with col_pat3:
    pasivos_inexistentes = st.number_input("[Casilla 3] Pasivos Inexistentes / Bienes Omitidos", min_value=0.0, step=100000.0)

diferencia_patrimonial_bruta = max(0, patrimonio_liquido_actual - patrimonio_liquido_anterior)
rentas_justificadas = renta_liquida_cedula_general + incrngo + beneficios_permitidos + ded_factura_elec
renta_comparacion = max(0, diferencia_patrimonial_bruta - rentas_justificadas + pasivos_inexistentes)

renta_liquida_definitiva = renta_liquida_cedula_general
if renta_comparacion > 0:
    st.error(f"¡Alerta! Renta Líquida por Comparación Patrimonial: ${renta_comparacion:,.0f}.")
    renta_liquida_definitiva += renta_comparacion

st.markdown("---")

# --- 9. LIQUIDACIÓN DEL IMPUESTO Y ANÁLISIS DETALLADO DEL ANTICIPO ---
st.header("8. Liquidación de Impuestos y Saldo a Pagar")
base_uvt = renta_liquida_definitiva / UVT_2025
impuesto_uvt = calcular_impuesto_241(base_uvt)
impuesto_pesos = impuesto_uvt * UVT_2025

limite_legal_descuentos = impuesto_pesos * 0.25

col_liq1, col_liq2 = st.columns(2)
with col_liq1:
    val_descuentos = st.number_input(f"Descuentos Tributarios (Máx: :red[${limite_legal_descuentos:,.0f}])", min_value=0.0, step=100000.0)
    descuentos_tributarios = min(val_descuentos, limite_legal_descuentos)
    
    retenciones = st.number_input("Retenciones en la fuente practicadas en 2025", min_value=0.0, step=100000.0)
    impuesto_neto_anterior = st.number_input("Impuesto neto de renta (2024)", min_value=0.0, step=100000.0)
with col_liq2:
    anos_declarando = st.selectbox("Número de veces que ha presentado declaración", ["1 vez (25%)", "2 veces (50%)", "3 veces o más (75%)"])
    saldo_favor_anterior = st.number_input("Saldo a favor año anterior (2024)", min_value=0.0, step=100000.0)

impuesto_neto = max(0, impuesto_pesos - descuentos_tributarios)

porcentaje_anticipo = 0.25 if "1" in anos_declarando else (0.50 if "2" in anos_declarando else 0.75)
anticipo_metodo_1 = max(0, (impuesto_neto * porcentaje_anticipo) - retenciones)
promedio_impuestos = (impuesto_neto + impuesto_neto_anterior) / 2
anticipo_metodo_2 = max(0, (promedio_impuestos * porcentaje_anticipo) - retenciones)
anticipo_final = min(anticipo_metodo_1, anticipo_metodo_2)
saldo_total = (impuesto_neto + anticipo_final) - retenciones - saldo_favor_anterior

st.markdown("---")
col_res1, col_res2, col_res3 = st.columns(3)
col_res1.metric(label="IMPUESTO NETO A CARGO", value=f"${impuesto_neto:,.0f}")
col_res2.metric(label="ANTICIPO AÑO SIGUIENTE", value=f"${anticipo_final:,.0f}")

if saldo_total > 0:
    col_res3.metric(label="🔴 SALDO A PAGAR", value=f"${saldo_total:,.0f}")
else:
    col_res3.metric(label="🟢 SALDO A FAVOR", value=f"${abs(saldo_total):,.0f}")

st.markdown("---")

# ================= 10. GENERADOR DE INFORMES Y PDF FORMULARIO 210 =================
st.header("9. Generador de Informes y Borrador Formulario 210 (DIAN)")
st.caption("Visualiza el informe detallado de la liquidación y el borrador oficial listo para transcribir al portal Muisca.")

tab_inf1, tab_inf2 = st.tabs(["📄 Informe Detallado de Liquidación", "📋 Borrador Formulario 210 (PDF)"])

with tab_inf1:
    st.subheader("Informe de Campos Editados y Resultados Fiscales - AG 2025")
    st.write(f"**Patrimonio Líquido 2025:** ${patrimonio_liquido_calc:,.0f}")
    st.write(f"**Ingreso Neto:** ${ingreso_neto:,.0f}")
    st.write(f"**Renta Líquida Gravable Cédula General:** ${renta_liquida_cedula_general:,.0f}")
    st.write(f"**Impuesto Neto a Cargo:** ${impuesto_neto:,.0f}")

with tab_inf2:
    st.subheader("Borrador Oficial - Formulario 210 (Personas Naturales Residentes)")
    st.caption("Verifica los datos y descarga el PDF para usarlo de guía en tu declaración de la DIAN.")
    
    # Datos exactos del Formulario 210
    datos_f210 = [
        ["DATOS INICIALES", "28. Compras con factura electrónica (1%)", f"${ded_factura_elec:,.0f}"],
        ["PATRIMONIO", "30. Deudas / Pasivos", f"${val_pasivos:,.0f}"],
        ["PATRIMONIO", "31. Total patrimonio bruto", f"${patrimonio_bruto_calc:,.0f}"],
        ["PATRIMONIO", "32. Total patrimonio líquido", f"${patrimonio_liquido_calc:,.0f}"],
        ["CÉDULA GENERAL", "33. Ingresos brutos rentas de trabajo", f"${ing_trabajo:,.0f}"],
        ["CÉDULA GENERAL", "35. Ingresos no constitutivos de renta", f"${incrngo_trabajo:,.0f}"],
        ["CÉDULA GENERAL", "36. Costos y deducciones procedentes", f"${costos_trabajo:,.0f}"],
        ["CÉDULA GENERAL", "40. Total rentas exentas (Trabajo)", f"${(re_afc_pensiones_aplicable + re_cesantias + re_indemnizaciones + re_gastos_rep + beneficio_trabajo_aplicado):,.0f}"],
        ["CÉDULA GENERAL", "53. Total deducciones imputables", f"${total_deducciones_limitadas:,.0f}"],
        ["CÉDULA GENERAL", "54. Rentas exentas y/o deduc. limitadas", f"${beneficios_permitidos:,.0f}"],
        ["RENTA GRAVABLE", "91. Renta líquida ordinaria", f"${renta_liquida_antes_beneficios:,.0f}"],
        ["RENTA GRAVABLE", "95. Renta líquida gravable", f"${renta_liquida_cedula_general:,.0f}"],
        ["LIQUIDACIÓN", "126. Impuesto neto de renta", f"${impuesto_neto:,.0f}"],
        ["LIQUIDACIÓN", "131. Saldo a favor año gravable anterior", f"${saldo_favor_anterior:,.0f}"],
        ["LIQUIDACIÓN", "132. Retenciones año gravable a declarar", f"${retenciones:,.0f}"],
        ["LIQUIDACIÓN", "133. Anticipo renta para año siguiente", f"${anticipo_final:,.0f}"],
        ["LIQUIDACIÓN", "136. TOTAL SALDO A PAGAR", f"${max(0, saldo_total):,.0f}"],
        ["LIQUIDACIÓN", "137. Total saldo a favor", f"${abs(min(0, saldo_total)):,.0f}"]
    ]
    
    # Vista previa en tabla (Opcional, para visualización rápida)
    df_f210 = pd.DataFrame(datos_f210, columns=["Sección", "Concepto DIAN", "Valor COP"])
    st.table(df_f210)
    
    st.markdown("---")
    st.markdown("### 📥 Descargar tu Borrador")
    
    # Intentar generar el PDF
    try:
        from fpdf import FPDF
        
        # Helper para evitar errores de codificación en fuentes básicas de PDF
        def formatear_texto(texto):
            reemplazos = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ñ':'n', 'Á':'A', 'É':'E', 'Í':'I', 'Ó':'O', 'Ú':'U', 'Ñ':'N'}
            for busqueda, reemplazo in reemplazos.items():
                texto = texto.replace(busqueda, reemplazo)
            return texto
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt="BORRADOR OFICIAL - FORMULARIO 210 (AG 2025)", ln=True, align='C')
        
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 10, txt=formatear_texto(f"Contribuyente: {nombre} | NIT: {nit}"), ln=True, align='C')
        pdf.ln(5)
        
        # Encabezado tabla PDF
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(45, 8, "SECCION", 1, 0, 'C')
        pdf.cell(100, 8, "CONCEPTO / CASILLA", 1, 0, 'C')
        pdf.cell(45, 8, "VALOR", 1, 1, 'C')
        
        # Contenido tabla PDF
        pdf.set_font("Arial", '', 8)
        for fila in datos_f210:
            pdf.cell(45, 8, formatear_texto(fila[0]), 1, 0, 'L')
            pdf.cell(100, 8, formatear_texto(fila[1]), 1, 0, 'L')
            pdf.cell(45, 8, formatear_texto(fila[2]), 1, 1, 'R')
            
        # Generar archivo temporal para descargar
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            with open(tmp.name, "rb") as f:
                pdf_bytes = f.read()
                
        # Botón de Descarga Streamlit
        st.download_button(
            label="📄 Descargar Formulario 210 (PDF)",
            data=pdf_bytes,
            file_name=f"Borrador_Formulario_210_{nit}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
    except ImportError:
        st.error("⚠️ Falta la librería **fpdf** para generar el documento. Instálala ejecutando en tu terminal: `pip install fpdf`")
