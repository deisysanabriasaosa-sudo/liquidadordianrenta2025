import streamlit as st

# --- 1. CONSTANTES TRIBUTARIAS AG 2025 ---
UVT_2025 = 49799

# Cálculos de topes legales en pesos (COP)
TOPE_VIVIENDA = 1200 * UVT_2025             # $59.758.800
TOPE_MEDICINA = 192 * UVT_2025              # $9.561.408
TOPE_DEP_TRADICIONAL = 384 * UVT_2025       # $19.122.816 (32 UVT/mes)
TOPE_1_DEP = 72 * UVT_2025                  # $3.585.528 (Por cada dependiente adicional)
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

# --- MEJORA: Fila 2 (Inversiones y CDTs) ---
st.markdown("**2. Inversiones, acciones y aportes (CDTs)**")
with st.expander("Desplegar detalle de CDTs e Inversiones (hasta 5)"):
    col_cdt1, col_cdt2 = st.columns(2)
    val_cdt1 = col_cdt1.number_input("[Casilla 1] Valor CDT / Inversión 1", min_value=0.0, step=1000000.0)
    val_cdt2 = col_cdt2.number_input("[Casilla 2] Valor CDT / Inversión 2", min_value=0.0, step=1000000.0)
    val_cdt3 = col_cdt1.number_input("[Casilla 3] Valor CDT / Inversión 3", min_value=0.0, step=1000000.0)
    val_cdt4 = col_cdt2.number_input("[Casilla 4] Valor CDT / Inversión 4", min_value=0.0, step=1000000.0)
    val_cdt5 = col_cdt1.number_input("[Casilla 5] Valor CDT / Inversión 5", min_value=0.0, step=1000000.0)
    val_otras_inv = col_cdt2.number_input("Otras inversiones / Acciones", min_value=0.0, step=1000000.0)
    
    val_inversiones = val_cdt1 + val_cdt2 + val_cdt3 + val_cdt4 + val_cdt5 + val_otras_inv
    st.info(f"Total Inversiones (Art. 272 E.T.): ${val_inversiones:,.0f}")

# Fila 3: Cuentas por cobrar
c1, c2, c3 = st.columns([2, 1.5, 3])
c1.write("**3. Cuentas por cobrar (Préstamos a terceros)**")
val_cxc = c2.number_input("CxC", min_value=0.0, step=1000000.0, label_visibility="collapsed")
c3.caption("Art. 270 E.T.: Valor nominal del crédito o deuda a tu favor.")

# --- MEJORA: Fila 4 (Inmuebles y actualización patrimonial) ---
st.markdown("**4. Bienes Inmuebles (Casas, apartamentos, fincas)**")
with st.expander("Desplegar detalle de Bienes Inmuebles (hasta 5 propiedades)"):
    st.caption("Nota: Ingresa el valor del año anterior y el % de reajuste (Art. 70 E.T.) para que el activo sufra la actualización legal, o bien ingresa el avalúo catastral. El sistema liquida automáticamente el mayor valor (Art. 277 E.T.).")
    val_inmuebles = 0.0
    for i in range(1, 6):
        st.markdown(f"**Inmueble {i}**")
        c_inm1, c_inm2, c_inm3, c_inm4 = st.columns(4)
        val_ant = c_inm1.number_input(f"[Casilla {i}.1] Valor declarado año anterior", min_value=0.0, step=1000000.0, key=f"inm_ant_{i}")
        reajuste = c_inm2.number_input(f"[Casilla {i}.2] % Reajuste fiscal", min_value=0.0, step=0.01, value=0.0, key=f"inm_reajuste_{i}", help="Porcentaje de ajuste fiscal fijado por el Gobierno Nacional para el año gravable.")
        val_catastral = c_inm3.number_input(f"[Casilla {i}.3] Avalúo Catastral 2025", min_value=0.0, step=1000000.0, key=f"inm_cat_{i}")
        
        # Fórmula de liquidación automática
        val_ajustado = val_ant * (1 + (reajuste / 100))
        val_declarar = max(val_ajustado, val_catastral)
        
        c_inm4.text_input(f"[Casilla {i}.4] Valor fiscal a declarar", value=f"${val_declarar:,.0f}", disabled=True, key=f"inm_dec_{i}")
        val_inmuebles += val_declarar
    st.info(f"Total Inmuebles a declarar: ${val_inmuebles:,.0f}")

# --- APÉNDICE DE RECOMENDACIÓN INMUEBLES ---
with st.expander("💡 Apéndice de Consulta Legal: Recomendaciones sobre Avalúo Comercial y Repercusiones Futuras en Inmuebles"):
    st.markdown("""
    **Normatividad aplicable: Artículos 70, 72, 73 y 277 del Estatuto Tributario.**
    
    Al momento de declarar un bien inmueble, la ley tributaria exige que el valor patrimonial sea **el mayor** entre:
    1. El costo de adquisición o costo fiscal declarado el año anterior.
    2. El avalúo catastral (o autoavalúo) del año gravable en curso.
    3. El costo fiscal ajustado por el porcentaje de reajuste anual decretado por el Gobierno Nacional (Art. 70 E.T.).
    
    **⚠️ Recomendación Estratégica:**
    Cuando dista significativamente el avalúo catastral del **valor comercial o posible valor de venta**, se recomienda ir actualizando el costo fiscal del inmueble en cada declaración. Para ello, utiliza la casilla del porcentaje de reajuste para que el activo "sufra" la actualización sobre el mismo valor del año anterior, o bien aplica los múltiplos del Art. 73 E.T.
    
    **Repercusiones Futuras (Impuesto de Ganancia Ocasional):**
    Si decides vender el inmueble y mantienes registrado únicamente el avalúo catastral (que en Colombia suele ser muy inferior a los precios del mercado real), al momento de la venta la utilidad generada (Precio de Venta - Costo Fiscal) será gigantesca. Esto te obligará a pagar un **Impuesto de Ganancia Ocasional del 15%** sobre una base muy alta. Al actualizar paulatinamente el costo fiscal mediante los reajustes de ley (registrando el mismo valor del año anterior y sumándole el ajuste porcentual), incrementas de forma legal el valor fiscal del inmueble, reduciendo de manera radical el impacto tributario futuro al momento de realizar la venta.
    """)

# --- MEJORA: Fila 5 (Vehículos) ---
st.markdown("**5. Vehículos y maquinaria**")
with st.expander("Desplegar detalle de Vehículos (hasta 2 vehículos)"):
    col_veh1, col_veh2 = st.columns(2)
    val_veh1 = col_veh1.number_input("[Casilla 1] Valor Vehículo 1", min_value=0.0, step=1000000.0, help="Art. 276 E.T. Costo de adquisición o avalúo comercial fijado por MinTransporte.")
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

st.success(f"**Total Patrimonio Bruto:** ${patrimonio_bruto_calc:,.0f} | **Total Patrimonio Líquido Calculado:** ${patrimonio_liquido_calc:,.0f}")

# --- 4. INGRESOS CÉDULA GENERAL (Depuración por naturaleza) ---
st.header("3. Ingresos Cédula General (Trabajo, Capital, No Laboral)")
st.caption("Diligencia cada pestaña según la naturaleza de tus ingresos, tal como aparece en el Formulario 210.")

tab_trabajo, tab_capital, tab_nolaboral = st.tabs(["💼 Rentas de Trabajo", "🏢 Rentas de Capital", "🏪 Rentas No Laborales"])

with tab_trabajo:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        ing_trabajo = st.number_input("Ingresos Brutos (Salarios, honorarios, comisiones)", min_value=0.0, step=1000000.0)
    with col_t2:
        incrngo_trabajo = st.number_input("INCRNGO Trabajo (Salud, Pensión, FSP)", min_value=0.0, step=100000.0, key="inc_t")

with tab_capital:
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        ing_capital = st.number_input("Ingresos Brutos (Intereses, rendimientos, arriendos)", min_value=0.0, step=1000000.0)
    with col_c2:
        incrngo_capital = st.number_input("INCRNGO Capital", min_value=0.0, step=100000.0, key="inc_c")
    with col_c3:
        costos_capital = st.number_input("Costos y Gastos procedentes (Capital)", min_value=0.0, step=100000.0, key="cost_c")

with tab_nolaboral:
    col_nl1, col_nl2, col_nl3 = st.columns(3)
    with col_nl1:
        ing_nolaboral = st.number_input("Ingresos Brutos (Comercio, otros no clasificados)", min_value=0.0, step=1000000.0)
    with col_nl2:
        incrngo_nolaboral = st.number_input("INCRNGO No Laboral", min_value=0.0, step=100000.0, key="inc_nl")
    with col_nl3:
        costos_nolaboral = st.number_input("Costos y Gastos procedentes (No Laboral)", min_value=0.0, step=100000.0, key="cost_nl")

# Consolidación Cédula General
ingresos_brutos = ing_trabajo + ing_capital + ing_nolaboral
incrngo = incrngo_trabajo + incrngo_capital + incrngo_nolaboral
costos_procedentes = costos_capital + costos_nolaboral

ingreso_neto = max(0, ingresos_brutos - incrngo)
ingreso_neto_trabajo = max(0, ing_trabajo - incrngo_trabajo)
renta_liquida_antes_beneficios = max(0, ingreso_neto - costos_procedentes)

st.write(f"**Resumen Consolidado:** Ingresos Brutos Totales: ${ingresos_brutos:,.0f} | Ingreso Neto: ${ingreso_neto:,.0f}")

# --- 5. DEDUCCIONES IMPUTABLES (Con límites en COP) ---
st.header("4. Deducciones Imputables")
st.caption("Nota: El sistema no te permitirá ingresar un valor superior al tope legal anual aplicable para 2025.")
col_d1, col_d2 = st.columns(2)

with col_d1:
    ded_vivienda = st.number_input(
        f"Intereses de Vivienda (Máx ${TOPE_VIVIENDA:,.0f})", 
        min_value=0.0, max_value=float(TOPE_VIVIENDA), step=100000.0,
        help=f"Norma: Art. 119 E.T. Forma de liquidación: Se deduce el 100% de los intereses pagados en el año por créditos hipotecarios o leasing habitacional, con un límite legal de 100 UVT mensuales. Esto equivale a un tope anual máximo de 1.200 UVT, es decir, ${TOPE_VIVIENDA:,.0f} COP."
    )
    ded_medicina = st.number_input(
        f"Medicina Prepagada (Máx ${TOPE_MEDICINA:,.0f})", 
        min_value=0.0, max_value=float(TOPE_MEDICINA), step=100000.0,
        help=f"Norma: Art. 387 E.T. Forma de liquidación: Se deduce el valor de los pagos a empresas de medicina prepagada o seguros de salud para el contribuyente, cónyuge o dependientes. Límite legal: 16 UVT mensuales, lo que equivale a un tope anual máximo de 192 UVT, es decir, ${TOPE_MEDICINA:,.0f} COP."
    )
    
    ded_gmf = st.number_input(
        "Deducción 50% GMF (4x1000)", 
        min_value=0.0, step=10000.0,
        help="Norma: Art. 115 E.T. Forma de liquidación: Se deduce el 50% del Gravamen a los Movimientos Financieros (4x1000) que haya sido efectivamente pagado y certificado por la entidad financiera. No tiene un límite en UVT, el límite es exactamente la mitad de lo certificado."
    )
    
with col_d2:
    st.markdown("**Deducción Tradicional por Dependiente (Art. 387 E.T.)**")
    
    # Límite del 10% vs Tope UVT
    limite_10_ingresos = ingresos_brutos * 0.10
    tope_dep_tradicional_aplicable = min(limite_10_ingresos, TOPE_DEP_TRADICIONAL)
    max_limit = float(tope_dep_tradicional_aplicable)
    
    if max_limit == 0:
        ded_dep_tradicional = st.number_input("Dependiente 10% (Ingresa ingresos primero)", value=0.0, disabled=True)
    else:
        ded_dep_tradicional = st.number_input(
            f"Dependiente 10% (Tope Dinámico: ${max_limit:,.0f})", 
            min_value=0.0, max_value=max_limit, step=100000.0,
            help=f"Norma: Art. 387 E.T. Forma de liquidación: Se calcula permitiendo deducir hasta el 10% de los ingresos brutos reportados. Este valor no puede exceder el límite legal de 32 UVT mensuales, equivalente a 384 UVT anuales (${TOPE_DEP_TRADICIONAL:,.0f} COP). El sistema aplica automáticamente el menor de estos dos valores."
        )
    
    st.markdown("**Dependientes Adicionales Ley 2277 (Art. 336 E.T.)**")
    st.caption(f"Norma: Art. 336 E.T. Forma de liquidación: Se permite deducir 72 UVT anuales (${TOPE_1_DEP:,.0f} COP) por cada dependiente, hasta un máximo de 4 dependientes. El límite global anual es de 288 UVT (${TOPE_DEP_ADICIONAL:,.0f} COP).")
    
    dep_1 = st.number_input(f"Dependiente Adicional 1 (Máx ${TOPE_1_DEP:,.0f})", min_value=0.0, max_value=float(TOPE_1_DEP), step=100000.0, help=f"Deducción fija de 72 UVT (${TOPE_1_DEP:,.0f} COP) por dependiente.")
    dep_2 = st.number_input(f"Dependiente Adicional 2 (Máx ${TOPE_1_DEP:,.0f})", min_value=0.0, max_value=float(TOPE_1_DEP), step=100000.0, help=f"Deducción fija de 72 UVT (${TOPE_1_DEP:,.0f} COP) por dependiente.")
    dep_3 = st.number_input(f"Dependiente Adicional 3 (Máx ${TOPE_1_DEP:,.0f})", min_value=0.0, max_value=float(TOPE_1_DEP), step=100000.0, help=f"Deducción fija de 72 UVT (${TOPE_1_DEP:,.0f} COP) por dependiente.")
    dep_4 = st.number_input(f"Dependiente Adicional 4 (Máx ${TOPE_1_DEP:,.0f})", min_value=0.0, max_value=float(TOPE_1_DEP), step=100000.0, help=f"Deducción fija de 72 UVT (${TOPE_1_DEP:,.0f} COP) por dependiente.")
    
    ded_dep_adicional = dep_1 + dep_2 + dep_3 + dep_4
    st.info(f"**Suma Adicionales:** ${ded_dep_adicional:,.0f} (Límite Global Adicionales: ${TOPE_DEP_ADICIONAL:,.0f})")

total_deducciones_limitadas = ded_vivienda + ded_medicina + ded_dep_tradicional + ded_dep_adicional + ded_gmf

# --- APÉNDICE DE CONSULTA ---
with st.expander("📖 Apéndice de Consulta Legal: Límite Deducción por Dependientes (Art. 387 E.T.)"):
    st.markdown(f"""
    **Referencia: Estatuto Tributario y doctrina DIAN**
    
    Para efectos de la deducción tradicional por dependientes, el **Artículo 387 del Estatuto Tributario** establece dos condiciones simultáneas:
    1. **Condición porcentual:** Se podrá deducir hasta el diez por ciento (10%) del total de los ingresos brutos.
    2. **Condición de techo absoluto:** Esta deducción no podrá exceder de treinta y dos (32) UVT mensuales, lo que se traduce en un máximo de 384 UVT anuales (**${TOPE_DEP_TRADICIONAL:,.0f} COP**).
    
    **Aplicación normativa en este liquidador:**
    Para garantizar que la declaración se ajuste a derecho y evitar rechazos o glosas por parte de la DIAN, el sistema evalúa ambos parámetros en tiempo real y restringe automáticamente la casilla para que **solo permita tomar el menor valor resultante** entre el 10% de sus ingresos brutos y el tope de las 384 UVT.
    """)

# --- 6. RENTAS EXENTAS (Con límites en COP) ---
st.header("5. Rentas Exentas")
col_re1, col_re2 = st.columns(2)

with col_re1:
    re_afc_pensiones = st.number_input(
        f"Aportes Voluntarios Pensión y AFC (Máx ${TOPE_AFC_PENSIONES:,.0f})", 
        min_value=0.0, max_value=float(TOPE_AFC_PENSIONES), step=100000.0,
        help=f"Norma: Art. 126-1 y 126-4 E.T. Forma de liquidación: Se suma el valor aportado a fondos voluntarios de pensiones y cuentas AFC. El beneficio está limitado al 30% del ingreso laboral o tributario del año, y en ningún caso puede exceder el límite absoluto de 3.800 UVT anuales (${TOPE_AFC_PENSIONES:,.0f} COP)."
    )
    # Ajuste automático del tope del 30%
    limite_30_ingreso = ingresos_brutos * 0.30
    re_afc_pensiones_aplicable = min(re_afc_pensiones, limite_30_ingreso)

with col_re2:
    re_cesantias = st.number_input(
        "Cesantías e Intereses de Cesantías", 
        min_value=0.0, step=100000.0,
        help="Norma: Art. 206 Numeral 4 E.T. Forma de liquidación: Renta exenta aplicable al ingreso reconocido por cesantías e intereses. Su cálculo oficial depende del salario promedio de los últimos 6 meses del contribuyente (tabla de exención escalonada con tope de 350 UVT mensuales). Se debe ingresar aquí el valor exento final ya depurado."
    )

# --- 7. CÁLCULO DE LÍMITES Y RENTA EXENTA LABORAL ---
st.header("6. Liquidación Cédula General")

# Motor de cálculo: Renta Exenta Laboral (25%)
renta_exenta_laboral_base = max(0, ingreso_neto_trabajo - total_deducciones_limitadas - re_afc_pensiones_aplicable - re_cesantias)
renta_exenta_25 = max(0, renta_exenta_laboral_base * 0.25)
renta_exenta_25_aplicable = min(renta_exenta_25, TOPE_25_EXENTO)

# Aplicación del Límite Global (40% o 1.340 UVT)
total_beneficios_sometidos = total_deducciones_limitadas + re_afc_pensiones_aplicable + re_cesantias + renta_exenta_25_aplicable
limite_40 = ingreso_neto * 0.40
limite_final_aplicable = min(limite_40, TOPE_GLOBAL_1340)

beneficios_permitidos = min(total_beneficios_sometidos, limite_final_aplicable)

# Deducción especial 1% compras factura electrónica
st.subheader("Beneficio Adicional (Sin límite del 40%)")
col_fe1, col_fe2 = st.columns(2)

with col_fe1:
    total_compras_factura_elec = st.number_input(
        "Valor Total Compras con Factura Electrónica", 
        min_value=0.0, step=100000.0,
        help="Ingresa el valor TOTAL de tus compras pagadas por medios electrónicos y soportadas con factura electrónica de venta."
    )

with col_fe2:
    calculo_1_porciento = total_compras_factura_elec * 0.01
    ded_factura_elec = min(calculo_1_porciento, TOPE_FACTURA_ELEC)
    
    st.text_input(
        f"Valor a Deducir (1% Aplicado - Máx ${TOPE_FACTURA_ELEC:,.0f})", 
        value=f"${ded_factura_elec:,.0f}", 
        disabled=True,
        help=f"Norma: Art. 336 Numeral 5 E.T. Forma de liquidación: Se calcula el 1% del valor total de las compras sustentadas. El valor a restar no puede exceder las 240 UVT anuales (${TOPE_FACTURA_ELEC:,.0f} COP). Esta deducción NO se somete al límite global del 40%."
    )
    if calculo_1_porciento > TOPE_FACTURA_ELEC:
        st.caption(f"⚠️ El 1% de tus compras (${calculo_1_porciento:,.0f}) supera el tope. Se aplicará el máximo legal permitido de 240 UVT (${TOPE_FACTURA_ELEC:,.0f}).")

renta_liquida_cedula_general = max(0, renta_liquida_antes_beneficios - beneficios_permitidos - ded_factura_elec)

# --- PANEL DE RESUMEN ---
st.info(f"**Renta Líquida Gravable Cédula General:** ${renta_liquida_cedula_general:,.0f}")
with st.expander("Ver detalles de los Límites Legales (Renta Exenta 25% y Límite Global 40%)"):
    st.markdown(f"""
    **1. Renta Exenta Laboral (Art. 206 Numeral 10 E.T.)**
    *   **Forma de liquidación:** Se calcula tomando el ingreso neto laboral y restando las deducciones y rentas exentas imputables a dicha renta. Al subtotal se le aplica el 25%.
    *   **Límite Legal:** El resultado no puede exceder las 790 UVT anuales (**${TOPE_25_EXENTO:,.0f} COP**).
    
    **2. Límite Global de Beneficios (Art. 336 E.T.)**
    *   **Forma de liquidación:** Se suman todas las deducciones imputables y rentas exentas (incluida la exenta del 25%). La suma de estos beneficios no puede superar el 40% del total del Ingreso Neto de la Cédula General.
    *   **Límite Legal Adicional:** Dicho 40% tiene a su vez un tope máximo absoluto de 1.340 UVT anuales (**${TOPE_GLOBAL_1340:,.0f} COP**). El liquidador aplica la limitante más estricta.
    """)
    st.write("---")
    st.write(f"- Total Deducciones y Exentas ingresadas: ${total_beneficios_sometidos:,.0f}")
    st.write(f"- Límite del 40% del Ingreso Neto: ${limite_40:,.0f}")
    st.write(f"- Límite en UVT (1.340 UVT): ${TOPE_GLOBAL_1340:,.0f}")
    st.write(f"- **Beneficios finalmente tomados (El menor valor permitido):** ${beneficios_permitidos:,.0f}")
    st.write(f"- *Nota: La deducción por factura electrónica (${ded_factura_elec:,.0f}) se restó de forma independiente a los límites anteriores.*")

# --- 8. RENTA POR COMPARACIÓN PATRIMONIAL ---
st.header("7. Renta por Comparación Patrimonial")
st.caption("Esta sección verifica si el incremento de tu patrimonio de un año a otro está justificado matemáticamente por los ingresos reportados.")

col_pat1, col_pat2, col_pat3 = st.columns(3)
with col_pat1:
    patrimonio_liquido_anterior = st.number_input("[Casilla 1] Patrimonio Líquido Año 2024", min_value=0.0, step=1000000.0, help="Patrimonio líquido declarado en el año inmediatamente anterior.")
with col_pat2:
    patrimonio_liquido_actual = st.number_input(
        "[Casilla 2] Patrimonio Líquido Año 2025", 
        value=float(patrimonio_liquido_calc), 
        min_value=0.0, 
        step=1000000.0,
        help="Calculado automáticamente desde la Tabla de Liquidación de Patrimonio (Sección 2)."
    )
with col_pat3:
    pasivos_inexistentes = st.number_input("[Casilla 3] Pasivos Inexistentes / Bienes Omitidos", min_value=0.0, step=100000.0, help="Art. 239-1 E.T. Se suman directamente a la renta líquida por comparación.")

# Cálculos de la liquidación patrimonial
diferencia_patrimonial_bruta = max(0, patrimonio_liquido_actual - patrimonio_liquido_anterior)
rentas_justificadas = renta_liquida_cedula_general + incrngo + beneficios_permitidos + ded_factura_elec
renta_comparacion = max(0, diferencia_patrimonial_bruta - rentas_justificadas + pasivos_inexistentes)

# Mostrar en pantalla las operaciones que originan el resultado
st.markdown("**Operaciones de Liquidación (Fórmula de Comparación de Patrimonios):**")
st.code(f"""
A. Diferencia Patrimonial Bruta = [Casilla 2] - [Casilla 1]
   ${patrimonio_liquido_actual:,.0f} - ${patrimonio_liquido_anterior:,.0f} = ${patrimonio_liquido_actual - patrimonio_liquido_anterior:,.0f}
   (Base sujeta a justificar: ${diferencia_patrimonial_bruta:,.0f})

B. [Casilla 4] Rentas Justificadas = Renta Líquida Gravable + INCRNGO + Exenciones y Deducciones permitidas
   ${renta_liquida_cedula_general:,.0f} + ${incrngo:,.0f} + ${(beneficios_permitidos + ded_factura_elec):,.0f} = ${rentas_justificadas:,.0f}

C. Renta por Comparación Patrimonial = (Base a Justificar + [Casilla 3]) - [Casilla 4]
   (${diferencia_patrimonial_bruta:,.0f} + ${pasivos_inexistentes:,.0f}) - ${rentas_justificadas:,.0f} = ${renta_comparacion:,.0f}
""", language="text")

renta_liquida_definitiva = renta_liquida_cedula_general
if renta_comparacion > 0:
    st.error(f"¡Alerta! Tienes una Renta Líquida por Comparación Patrimonial de: ${renta_comparacion:,.0f}. Revisa tus rentas exentas omitidas, anticipos o ganancias ocasionales para justificar el incremento.")
    renta_liquida_definitiva += renta_comparacion
else:
    st.success("Variación patrimonial debidamente justificada. No se genera renta por comparación patrimonial.")

# --- Apéndice de Consulta Legal ---
with st.expander("📖 Apéndice de Consulta Legal: Renta por Comparación Patrimonial (Arts. 236 al 239-1 E.T.)"):
    st.markdown("""
    **Fundamento normativo aplicable al control de patrimonios de la DIAN:**
    
    1. **Renta por comparación de patrimonios (Art. 236 E.T.):** 
       Establece que, si el incremento del patrimonio líquido de un año a otro es mayor que la suma de los ingresos netos declarados (Renta Gravable + Rentas Exentas + Ganancias Ocasionales, menos los impuestos pagados), **dicha diferencia no justificada se considerará renta gravable.** Por ende, aumentará directamente el impuesto a pagar.
       
    2. **Ajuste para justificar el incremento (Art. 237 E.T.):** 
       Para depurar y justificar ese incremento, el contribuyente tiene derecho a sumar a su renta gravada todo aquello que fue un ingreso real capitalizado pero que no tributó por ser un beneficio legal. Esto incluye:
       * Los Ingresos No Constitutivos de Renta (INCRNGO).
       * Las Rentas Exentas y Deducciones (como el tope del 40% y beneficios especiales).
       * *(Nota: En declaraciones más complejas también se sumarían las Ganancias Ocasionales netas y se restarían los impuestos del año anterior).*
       
    3. **Pasivos inexistentes o activos omitidos (Art. 239-1 E.T.):**
       La inclusión de deudas falsas (para bajar el patrimonio ficticiamente) o la omisión de bienes en las declaraciones anteriores y su posterior inclusión, constituye una **renta líquida gravable de manera automática** y se suma de forma sancionatoria a la liquidación.
    """)

# --- 9. LIQUIDACIÓN DEL IMPUESTO Y ANTICIPO ---
st.header("8. Liquidación de Impuestos y Saldo a Pagar")
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
        help="Se restan directamente del impuesto. Despliega el panel de abajo para ver la normatividad y el método de liquidación."
    )
    
    # Panel explicativo de Descuentos Tributarios
    with st.expander("📚 Ver conceptos legales de Descuentos Tributarios (Art. 253 al 257 E.T.)"):
        st.markdown("""
        **Norma aplicable y Forma de liquidación:**
        Los descuentos tributarios se restan directamente del impuesto de renta (no de los ingresos). Se calculan aplicando un porcentaje sobre la inversión o donación realizada:
        1. **Donaciones a ESAL (Art. 257):** Se liquida tomando el 25% del valor donado a entidades del Régimen Tributario Especial o públicas.
        2. **Impuestos pagados en el exterior (Art. 254):** Aplica para residentes fiscales colombianos, tomando el impuesto de renta pagado en el otro país sobre la renta de fuente extranjera (sometido a fórmulas de límite según el impuesto en Colombia).
        3. **Inversiones I+D+i (Art. 256):** Se liquida calculando el 25% de lo invertido en proyectos calificados de ciencia y tecnología.
        4. **Inversiones en medio ambiente (Art. 253):** Se liquida tomando el 25% de la inversión directa acreditada por autoridades ambientales (ANLA/CAR).
        
        ⚠️ **Regla General del Límite (Art. 258 E.T.):** 
        La liquidación concurrente de los descuentos tributarios mencionados (salvo excepciones precisas de ley) **no podrá exceder el 25% del impuesto sobre la renta** a cargo del contribuyente en el respectivo año gravable.
        """)
        st.info(f"💡 Para este caso específico, el límite legal máximo a descontar sugerido equivale a: **${limite_legal_descuentos:,.0f} COP**")

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
with st.expander("Ver análisis detallado del Anticipo de Renta (Art 807 E.T.)"):
    st.write(f"Norma: Art. 807 E.T. Forma de liquidación: Según la ley, el sistema liquida dos procedimientos y puedes elegir el que arroje el menor valor a pagar:")
    st.write(f"- **Porcentaje aplicado:** {porcentaje_anticipo * 100}% (según antigüedad declarando)")
    st.write(f"- **Procedimiento 1 (Basado en impuesto neto actual):** (${impuesto_neto:,.0f} * {porcentaje_anticipo}) - ${retenciones:,.0f} = ${anticipo_metodo_1:,.0f}")
    st.write(f"- **Procedimiento 2 (Basado en promedio con año anterior):** (Promedio ${promedio_impuestos:,.0f} * {porcentaje_anticipo}) - ${retenciones:,.0f} = ${anticipo_metodo_2:,.0f}")
    st.success(f"**El sistema seleccionó automáticamente el menor valor: ${anticipo_final:,.0f} COP**")

col_res1, col_res2, col_res3 = st.columns(3)
col_res1.metric(label="IMPUESTO NETO A CARGO", value=f"${impuesto_neto:,.0f}")
col_res2.metric(label="ANTICIPO AÑO SIGUIENTE", value=f"${anticipo_final:,.0f}")

if saldo_total > 0:
    col_res3.metric(label="🔴 SALDO A PAGAR", value=f"${saldo_total:,.0f}")
else:
    col_res3.metric(label="🟢 SALDO A FAVOR", value=f"${abs(saldo_total):,.0f}")

st.caption("Nota Legal: Este liquidador es una herramienta de referencia basada en la normativa vigente (incluyendo modificaciones Ley 2277/2022). Se recomienda validación profesional final.")
