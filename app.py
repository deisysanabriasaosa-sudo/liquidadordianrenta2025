# --- 4. Bienes Inmuebles (Casas, apartamentos, fincas) ---
st.markdown("**4. Bienes Inmuebles (Casas, apartamentos, fincas)**")
with st.expander("Desplegar detalle de Bienes Inmuebles (hasta 5 propiedades)"):
    st.caption("Nota: Ingresa los valores y el sistema actualizará inmediatamente el valor fiscal a declarar.")
    
    val_inmuebles = 0.0
    detalle_inmuebles_editados = []
    
    for i in range(1, 6):
        st.markdown(f"**🔹 Inmueble {i}**")
        
        # 1. Identificación y Soporte
        c_ident1, c_ident2 = st.columns(2)
        nom_inm = c_ident1.text_input(f"Nombre o Identificación (Inmueble {i})", key=f"inm_nom_{i}")
        soporte_inm = c_ident2.text_input(f"Soporte Documental (Inmueble {i})", key=f"inm_soporte_{i}")
        
        # 2. Valores para el cálculo
        c_inm1, c_inm2, c_inm3 = st.columns(3)
        # Usamos 'key' estables para que Streamlit mantenga el estado del cálculo
        val_ant = c_inm1.number_input(f"Valor declarado año anterior", min_value=0.0, step=1000000.0, key=f"inm_ant_{i}")
        reajuste = c_inm2.number_input(f"% Reajuste fiscal", min_value=0.0, step=0.01, value=0.0, key=f"inm_reajuste_{i}")
        val_catastral = c_inm3.number_input(f"Avalúo Catastral 2025", min_value=0.0, step=1000000.0, key=f"inm_cat_{i}")
        
        # 3. Cálculo Inmediato
        val_ajustado = val_ant * (1 + (reajuste / 100))
        val_declarar = max(val_ajustado, val_catastral)
        
        # 4. Mostrar resultado calculado inmediatamente
        st.metric(label=f"Valor fiscal a declarar (Inmueble {i})", value=f"${val_declarar:,.0f}")
        
        if val_declarar > 0:
            val_inmuebles += val_declarar
            detalle_inmuebles_editados.append({
                "Inmueble": nom_inm if nom_inm else f"Inmueble {i}",
                "Soporte": soporte_inm if soporte_inm else "N/A",
                "Valor 2025": val_declarar
            })
            
        st.write("---")
        
    st.info(f"Total Inmuebles a declarar: ${val_inmuebles:,.0f}")
