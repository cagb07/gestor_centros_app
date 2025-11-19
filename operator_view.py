import streamlit as st
import pandas as pd
import database
import config
import json
from streamlit_folium import st_folium
from streamlit_drawable_canvas import st_canvas

# --- LÓGICA DE PRE-LLENADO ---
# Mapeo de columnas CSV a etiquetas de formulario ESPERADAS
CSV_TO_FORM_MAP = config.CSV_TO_FORM_MAP

def _render_form_from_structure(structure):
    """Función interna para dibujar el formulario dinámico."""
    form_data = {}
    
    # --- LÓGICA DE PRE-LLENADO ---
    prefill_data = {}
    if "centro_adjunto" in st.session_state and st.session_state.centro_adjunto:
        # Invertir el mapa para buscar fácilmente por la etiqueta del formulario
        FORM_TO_CSV_MAP = {v: k for k, v in CSV_TO_FORM_MAP.items()}
        
        for form_label, csv_col in FORM_TO_CSV_MAP.items():
            if csv_col in st.session_state.centro_adjunto:
                prefill_data[form_label] = st.session_state.centro_adjunto[csv_col]
    # --- FIN LÓGICA PRE-LLENADO ---

    for field in structure:
        label = field["Etiqueta del Campo"]
        field_type = field["Tipo de Campo"]
        required = field["Requerido"]
        
        field_key = f"form_field_{label.replace(' ', '_')}" # Clave única
        
        # Obtener el valor por defecto del diccionario prefill_data
        default_value = prefill_data.get(label, None)
        
        # Add a visual indicator for required fields
        display_label = f"{label}*" if required else label

        if field_type == "Texto":
            value = st.text_input(display_label, value=default_value or "", key=field_key)
            form_data[label] = value.strip() if value else ""
        elif field_type == "Área de Texto":
            value = st.text_area(display_label, value=default_value or "", key=field_key)
            form_data[label] = value.strip() if value else ""
        elif field_type == "Fecha":
            form_data[label] = st.date_input(display_label, key=field_key)
        
        elif field_type == "Tabla Dinámica":
            st.subheader(display_label)
            df_editor = pd.DataFrame([{"Columna 1": "", "Columna 2": ""}])
            form_data[label] = st.data_editor(
                df_editor, 
                num_rows="dynamic", 
                key=field_key
            ).to_dict('records')
            
        elif field_type == "Geolocalización":
            st.subheader(display_label)
            map_center = config.DEFAULT_MAP_CENTER
            map_data = st_folium(center=map_center, zoom=config.DEFAULT_MAP_ZOOM, key=field_key, width=700, height=400)
            
            coords = None
            if map_data and map_data.get("last_clicked"):
                coords = map_data["last_clicked"]
                st.write(f"Coordenadas: {coords['lat']:.6f}, {coords['lng']:.6f}")
            form_data[label] = coords
            
        elif field_type == "Firma":
            st.subheader(display_label)
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=3,
                stroke_color="#000000",
                background_color="#FFFFFF",
                width=700,
                height=200,
                drawing_mode="freedraw",
                key=field_key
            )
            if canvas_result.image_data is not None:
                form_data[label] = canvas_result.image_data.tolist() 
            else:
                form_data[label] = None
        
        elif field_type == "Carga de Imagen":
            st.subheader(display_label)
            uploaded_file = st.file_uploader(display_label, type=["png", "jpg", "jpeg"], key=field_key)
            if uploaded_file:
                form_data[label] = uploaded_file.name
            else:
                form_data[label] = None
                
    return form_data

def _validate_form(form_data, structure):
    """Checks if all required fields are filled."""
    for field in structure:
        if field["Requerido"]:
            label = field["Etiqueta del Campo"]
            value = form_data.get(label)
            
            # Verificar si el valor está vacío
            if value is None:
                return False, f"El campo '{label}' es requerido."
            
            # Para strings, verificar que no esté solo whitespace
            if isinstance(value, str):
                if not value.strip():
                    return False, f"El campo '{label}' es requerido."
            
            # Para listas (tabla dinámica), verificar que no esté vacía
            if isinstance(value, list):
                if len(value) == 0 or all(not str(item).strip() for item in value):
                    return False, f"El campo '{label}' es requerido."
    
    return True, ""


def show_ui(df_centros):
    st.title(f"Panel de Operador - {st.session_state.get('full_name', 'Usuario')}")
    
    tab_buscador, tab_fill_form, tab_my_submissions = st.tabs([
        "🔎 Buscador de Centros",
        "📝 Llenar Formulario",
        "📋 Mis Envíos"
    ])
    
    # --- 1. BUSCADOR DE CENTROS (CON LÓGICA DE ADJUNTAR) ---
    with tab_buscador:
        st.header("🔎 Consulta de Centros Educativos")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Buscar centro:", placeholder="Ej: Científico")
        with col2:
            provincia_filter = st.selectbox("📍 Provincia:", 
                                           ["Todas"] + sorted(df_centros['PROVINCIA'].unique().tolist()),
                                           key="op_prov")
        with col3:
            tipo_filter = st.selectbox("🏢 Tipo:",
                                      ["Todos"] + sorted(df_centros['TIPO_INSTITUCION'].unique().tolist()),
                                      key="op_tipo")
        
        # Aplicar filtros
        df_filtered = df_centros.copy()
        
        if search_term:
            df_filtered = df_filtered[
                df_filtered['CENTRO_EDUCATIVO'].str.contains(search_term, case=False, na=False)
            ]
        
        if provincia_filter != "Todas":
            df_filtered = df_filtered[df_filtered['PROVINCIA'] == provincia_filter]
        
        if tipo_filter != "Todos":
            df_filtered = df_filtered[df_filtered['TIPO_INSTITUCION'] == tipo_filter]
        
        st.info(f"📊 Resultados: {len(df_filtered)} de {len(df_centros)} centros")
        st.dataframe(df_filtered, use_container_width=True, height=300)
        
        st.divider()
        st.subheader("📎 Adjuntar Centro a mi Formulario")
        st.write("Seleccione un centro para pre-llenar sus datos automáticamente.")

        lista_nombres_centros = sorted(df_centros['CENTRO_EDUCATIVO'].unique().tolist())

        centro_para_adjuntar = st.selectbox(
            "Seleccione el centro que desea usar:",
            options=lista_nombres_centros,
            index=None,
            placeholder="Escriba o seleccione un centro...",
            key="operator_attach_selectbox"
        )

        if st.button("✅ Adjuntar Centro", key="btn_adjuntar_operator"):
            if centro_para_adjuntar:
                datos_centro_seleccionado = df_centros[
                    df_centros['CENTRO_EDUCATIVO'] == centro_para_adjuntar
                ].iloc[0]
                
                st.session_state.centro_adjunto = datos_centro_seleccionado.to_dict()
                
                st.success(f"✅ Centro '{centro_para_adjuntar}' adjuntado exitosamente!")
                st.info("💡 Los datos aparecerán pre-llenados en el siguiente formulario.")
                
                with st.expander("👁️ Ver detalles del centro"):
                    cols_to_show = ['CENTRO_EDUCATIVO', 'PROVINCIA', 'CANTON', 'DISTRITO', 'DIRECCION', 'CODSABER']
                    for col in cols_to_show:
                        if col in datos_centro_seleccionado.index:
                            st.write(f"**{col}**: {datos_centro_seleccionado[col]}")
            else:
                st.warning("⚠️ Por favor, seleccione un centro.")

    # --- 2. LLENAR FORMULARIO ---
    with tab_fill_form:
        st.header("📝 Llenar Nuevo Formulario")
        
        # Mostrar si hay un centro adjunto
        if "centro_adjunto" in st.session_state and st.session_state.centro_adjunto:
            col1, col2 = st.columns([4, 1])
            with col1:
                centro_nombre = st.session_state.centro_adjunto['CENTRO_EDUCATIVO']
                st.info(f"✅ Centro Adjunto: **{centro_nombre}**")
                st.write("*Los datos se pre-llenarán automáticamente en los campos correspondientes.*")
            with col2:
                if st.button("❌ Quitar", key="remove_centro"):
                    st.session_state.centro_adjunto = None
                    st.rerun()
            st.divider()
        
        try:
            # Paso 1: Seleccionar Área
            st.subheader("Paso 1️⃣: Selecciona el Área")
            areas_list = database.get_all_areas()
            area_options = {area['id']: area['name'] for area in areas_list}
            
            if not area_options:
                st.warning("⚠️ No hay formularios disponibles. Contacta al administrador.")
                st.stop()
            
            selected_area_id = st.selectbox(
                "Selecciona un área:",
                options=area_options.keys(),
                format_func=lambda x: area_options[x],
                key="area_select"
            )
            
            # Paso 2: Seleccionar Plantilla
            st.subheader("Paso 2️⃣: Selecciona el Formulario")
            template_list = database.get_templates_by_area(selected_area_id)
            template_options = {t['id']: t['name'] for t in template_list}
            
            if not template_options:
                st.info("ℹ️ No hay formularios disponibles en esta área.")
                st.stop()
            
            selected_template_id = st.selectbox(
                "Selecciona un formulario:",
                options=template_options.keys(),
                format_func=lambda x: template_options[x],
                key="template_select"
            )
            
            # Paso 3: Renderizar el formulario
            st.divider()
            st.subheader("Paso 3️⃣: Completa el Formulario")
            
            form_structure = database.get_template_structure(selected_template_id)
            if not form_structure:
                st.error("❌ No se pudo cargar la estructura de este formulario.")
                st.stop()
            
            # Mostrar información del formulario
            with st.expander("📋 Ver información del formulario", expanded=False):
                st.write(f"**Nombre**: {template_options[selected_template_id]}")
                st.write(f"**Área**: {area_options[selected_area_id]}")
                st.write(f"**Campos**: {len(form_structure)}")
                for i, field in enumerate(form_structure, 1):
                    req = "✅ Requerido" if field.get("Requerido", False) else "⭕ Opcional"
                    st.write(f"{i}. {field['Etiqueta del Campo']} ({field['Tipo de Campo']}) - {req}")
                
            with st.form("dynamic_form", clear_on_submit=True):
                # Renderizar todos los campos
                form_data = _render_form_from_structure(form_structure)
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("✅ Enviar Formulario", use_container_width=True)
                with col2:
                    st.form_submit_button("🔄 Limpiar Formulario", use_container_width=True)
                
                if submitted:
                    is_valid, error_message = _validate_form(form_data, form_structure)
                    if is_valid:
                        try:
                            database.save_submission(
                                selected_template_id,
                                st.session_state["user_id"],
                                form_data
                            )
                            st.success("✅ ¡Formulario enviado con éxito!")
                            st.balloons()
                            
                            # Limpiar el centro adjunto después de un envío exitoso
                            if "centro_adjunto" in st.session_state:
                                st.session_state.centro_adjunto = None
                            
                            # Mostrar resumen
                            with st.expander("📋 Ver resumen del envío"):
                                st.write(f"**Formulario**: {template_options[selected_template_id]}")
                                st.write(f"**Área**: {area_options[selected_area_id]}")
                                st.write(f"**Hora**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
                                st.write("**Datos enviados:**")
                                for key, value in form_data.items():
                                    if value and str(value) != '[]':
                                        st.write(f"- {key}: {str(value)[:100]}")
                            
                            st.info("💡 Puedes seguir completando más formularios o ir a 'Mis Envíos' para ver tu historial.")
                        except Exception as e:
                            st.error(f"❌ Error al guardar el envío: {str(e)[:100]}")
                    else:
                        st.error(f"❌ {error_message}")

        except Exception as e:
            st.error(f"❌ Error cargando formularios: {str(e)[:100]}")

    # --- 3. MIS ENVÍOS ---
    with tab_my_submissions:
        st.header("📋 Historial de Mis Envíos")
        
        try:
            my_submissions_df = database.get_submissions_by_user(st.session_state["user_id"])
            
            if my_submissions_df.empty:
                st.info("ℹ️ Aún no has enviado ningún formulario.")
                st.balloons()
                col1, col2 = st.columns(2)
                with col1:
                    st.write("👉 Para empezar:")
                    st.write("1. Ve a 'Buscador de Centros' y adjunta un centro")
                    st.write("2. Ve a 'Llenar Formulario' y completa el formulario")
                    st.write("3. Haz clic en 'Enviar Formulario'")
                with col2:
                    st.write("💡 Consejos:")
                    st.write("• Los campos marcados con * son obligatorios")
                    st.write("• Puedes adjuntar un centro para pre-llenar datos")
                    st.write("• Verifica tus datos antes de enviar")
            else:
                # Estadísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📝 Total de Envíos", len(my_submissions_df))
                with col2:
                    st.metric("📅 Últimas 24h", 
                             len(my_submissions_df[my_submissions_df['created_at'] > pd.Timestamp.now() - pd.Timedelta(days=1)]))
                with col3:
                    st.metric("📋 Formularios Diferentes", my_submissions_df['name'].nunique())
                
                st.divider()
                
                # Filtro por formulario
                form_filter = st.selectbox(
                    "Filtrar por formulario:",
                    ["Todos"] + sorted(my_submissions_df['name'].unique().tolist()),
                    key="form_filter"
                )
                
                # Aplicar filtro
                if form_filter != "Todos":
                    df_filtered = my_submissions_df[my_submissions_df['name'] == form_filter]
                else:
                    df_filtered = my_submissions_df
                
                # Mostrar tabla
                st.subheader(f"Mostrando {len(df_filtered)} envíos")
                
                # Crear vista mejorada sin la columna 'data'
                display_df = df_filtered.drop(columns=['data']).copy()
                display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)
                
                # Opción para ver detalles
                st.subheader("👁️ Ver Detalles de un Envío")
                if len(df_filtered) > 0:
                    selected_id = st.selectbox(
                        "Selecciona un envío:",
                        df_filtered['id'].unique(),
                        format_func=lambda x: f"Envío {x} - {df_filtered[df_filtered['id']==x]['name'].values[0]}"
                    )
                    
                    submission_data = df_filtered[df_filtered['id'] == selected_id]['data'].iloc[0]
                    
                    with st.expander("📄 Mostrar todos los datos del envío"):
                        if isinstance(submission_data, str):
                            import json
                            submission_data = json.loads(submission_data)
                        
                        for key, value in submission_data.items():
                            st.write(f"**{key}**: {value}")
                
                # Descargar datos
                csv_download = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar mis envíos como CSV",
                    data=csv_download,
                    file_name=f"mis_envios_{st.session_state['username']}.csv",
                    mime="text/csv"
                )
                
        except Exception as e:
            st.error(f"❌ Error al cargar tus envíos: {str(e)[:100]}")