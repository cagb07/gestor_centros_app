import streamlit as st
import pandas as pd
import database
import db_helpers
import auth
import config
import json

def show_ui(df_centros):
    st.title(f"Panel de Administrador")
    
    tab_list = [
        "📊 Dashboard",
        "🔎 Buscador de Centros",
        "🛠️ Creador de Formularios",
        "🗂️ Gestión de Áreas",
        "👤 Gestión de Usuarios",
        "📋 Revisión de Envíos"
    ]
    
    tab_dashboard, tab_buscador, tab_creator, tab_areas, tab_users, tab_review = st.tabs(tab_list)

    # --- 1. DASHBOARD ---
    with tab_dashboard:
        st.header("Dashboard de Operaciones")
        
        try:
            total_envios = database.get_total_submission_count()
            envios_area = database.get_submission_count_by_area()
            envios_usuario = database.get_submission_count_by_user()
            
            # Mostrar métricas principales en fila
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📋 Total de Envíos", total_envios)
            with col2:
                try:
                    areas_count = len(database.get_all_areas())
                    st.metric("🗂️ Áreas Creadas", areas_count)
                except:
                    st.metric("🗂️ Áreas Creadas", 0)
            with col3:
                try:
                    users_count = len(database.get_all_users())
                    st.metric("👥 Usuarios", users_count)
                except:
                    st.metric("👥 Usuarios", 0)
            
            st.divider()
            
            # Gráficos y tablas
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Envíos por Área")
                if not envios_area.empty:
                    st.bar_chart(envios_area.set_index("area_name")["submission_count"])
                else:
                    st.info("Aún no hay envíos.")
            
            with col2:
                st.subheader("👥 Actividad por Usuario")
                if not envios_usuario.empty:
                    st.dataframe(envios_usuario, use_container_width=True, hide_index=True)
                else:
                    st.info("Aún no hay envíos.")
            
            # Últimos envíos
            st.divider()
            st.subheader("📋 Últimos Envíos Recibidos")
            try:
                last_submissions = database.get_all_submissions_with_details()
                if not last_submissions.empty:
                    st.dataframe(last_submissions.head(10), use_container_width=True, hide_index=True)
                else:
                    st.info("No hay envíos todavía.")
            except Exception as e:
                st.warning(f"No se pueden cargar los últimos envíos: {str(e)[:50]}")
                    
        except Exception as e:
            st.error(f"❌ Error cargando el dashboard: {str(e)[:100]}")

    # --- 2. BUSCADOR DE CENTROS (CON LÓGICA DE ADJUNTAR) ---
    with tab_buscador:
        st.header("🔎 Consulta de Centros Educativos")
        
        # Filtros de búsqueda
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Buscar por nombre:", placeholder="Ej: Científico")
        with col2:
            provincia_filter = st.selectbox("📍 Filtrar por provincia:", 
                                           ["Todas"] + sorted(df_centros['PROVINCIA'].unique().tolist()))
        with col3:
            tipo_institucion = st.selectbox("🏢 Filtrar por tipo:",
                                          ["Todos"] + sorted(df_centros['TIPO_INSTITUCION'].unique().tolist()))
        
        # Aplicar filtros
        df_filtered = df_centros.copy()
        
        if search_term:
            df_filtered = df_filtered[
                df_filtered['CENTRO_EDUCATIVO'].str.contains(search_term, case=False, na=False)
            ]
        
        if provincia_filter != "Todas":
            df_filtered = df_filtered[df_filtered['PROVINCIA'] == provincia_filter]
        
        if tipo_institucion != "Todos":
            df_filtered = df_filtered[df_filtered['TIPO_INSTITUCION'] == tipo_institucion]
        
        # Mostrar resultados
        st.info(f"📊 Mostrando {len(df_filtered)} de {len(df_centros)} centros")
        st.dataframe(df_filtered, use_container_width=True, height=300)
        
        st.divider()
        st.subheader("📎 Adjuntar Centro a un Formulario")
        st.write("Seleccione un centro para pre-llenar sus datos en un nuevo formulario.")

        lista_nombres_centros = sorted(df_centros['CENTRO_EDUCATIVO'].unique().tolist())

        centro_para_adjuntar = st.selectbox(
            "Seleccione el centro que desea adjuntar:",
            options=lista_nombres_centros,
            index=None,
            placeholder="Escriba o seleccione un centro...",
            key="admin_attach_selectbox"
        )

        if st.button("✅ Adjuntar Centro Seleccionado", key="btn_adjuntar_admin"):
            if centro_para_adjuntar:
                datos_centro_seleccionado = df_centros[
                    df_centros['CENTRO_EDUCATIVO'] == centro_para_adjuntar
                ].iloc[0]
                
                st.session_state.centro_adjunto = datos_centro_seleccionado.to_dict()
                
                st.success(f"✅ ¡Centro '{centro_para_adjuntar}' adjuntado!")
                st.info("💡 Los datos se pre-llenarán automáticamente en el formulario.")
                
                # Mostrar datos del centro
                with st.expander("Ver datos del centro adjunto"):
                    for col in datos_centro_seleccionado.index:
                        st.write(f"**{col}**: {datos_centro_seleccionado[col]}")
            else:
                st.warning("⚠️ Por favor, seleccione un centro de la lista.")

    # --- 3. CREADOR DE FORMULARIOS ---
    with tab_creator:
        st.header("Creador de Plantillas de Formularios")
        
        with st.form("new_template_form"):
            st.subheader("Detalles de la Plantilla")
            
            area_options = {}  # Initialize to an empty dictionary
            try:
                areas_list = database.get_all_areas()
                area_options = {area['id']: area['name'] for area in areas_list}
                if not area_options:
                    st.warning("No hay áreas creadas. Vaya a 'Gestión de Áreas' primero.")
                    st.stop()
            except Exception as e:
                st.error(f"Error cargando áreas: {e}")
                st.stop()
            
            template_name = st.text_input("Nombre de la Plantilla", placeholder="Ej: Reporte de Visita Técnica")
            # Usar lista explícita de keys para evitar comportamientos inesperados
            template_area_id = st.selectbox(
                "Asignar al Área:", 
                options=list(area_options.keys()), 
                format_func=lambda x: area_options.get(x, "<Área desconocida>")
            )
            
            st.subheader("Constructor de Campos")
            st.write("Defina los campos que tendrá este formulario.")
            
            if 'template_fields' not in st.session_state:
                st.session_state.template_fields = pd.DataFrame(
                    [
                        {"Etiqueta del Campo": "Nombre del Visitante", "Tipo de Campo": "Texto", "Requerido": True},
                        {"Etiqueta del Campo": "Nombre del Centro", "Tipo de Campo": "Texto", "Requerido": False},
                        {"Etiqueta del Campo": "Provincia", "Tipo de Campo": "Texto", "Requerido": False},
                    ]
                )
            
            st.session_state.template_fields = st.data_editor(
                st.session_state.template_fields,
                num_rows="dynamic",
                column_config={
                    "Etiqueta del Campo": st.column_config.TextColumn(required=True),
                    "Tipo de Campo": st.column_config.SelectboxColumn(options=config.FIELD_TYPES, required=True),
                    "Requerido": st.column_config.CheckboxColumn(default=False)
                },
                use_container_width=True,
                height=300
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("✅ Guardar Plantilla")
            with col2:
                clear_form = st.form_submit_button("🔄 Limpiar Formulario")
            
            if submitted:
                if not template_name or not template_name.strip():
                    st.error("El nombre de la plantilla es requerido.")
                elif len(template_name.strip()) > config.MAX_TEMPLATE_NAME_LENGTH:
                    st.error(f"El nombre no puede exceder {config.MAX_TEMPLATE_NAME_LENGTH} caracteres.")
                else:
                    # Normalizar estructura desde la sesión (DataFrame o lista)
                    raw_fields = st.session_state.get('template_fields')
                    structure = None

                    if raw_fields is None:
                        st.error("Debe agregar al menos un campo.")
                    else:
                        try:
                            if hasattr(raw_fields, 'to_dict'):
                                structure = raw_fields.to_dict('records')
                            elif isinstance(raw_fields, list):
                                structure = raw_fields
                            else:
                                # Intentar convertir a lista de registros
                                structure = list(raw_fields)
                        except Exception:
                            structure = None

                    if not structure or len(structure) == 0:
                        st.error("Debe agregar al menos un campo válido.")
                    else:
                        # Validaciones por campo
                        invalid = False
                        for i, f in enumerate(structure):
                            label = f.get('Etiqueta del Campo') if isinstance(f, dict) else None
                            ftype = f.get('Tipo de Campo') if isinstance(f, dict) else None
                            req = f.get('Requerido') if isinstance(f, dict) else False

                            if not label or not str(label).strip():
                                st.error(f"Campo #{i+1}: la etiqueta es requerida.")
                                invalid = True
                                break
                            if len(str(label).strip()) > config.MAX_FIELD_LABEL_LENGTH:
                                st.error(f"Campo '{label}': la etiqueta excede {config.MAX_FIELD_LABEL_LENGTH} caracteres.")
                                invalid = True
                                break
                            if ftype not in config.FIELD_TYPES:
                                st.error(f"Campo '{label}': tipo de campo inválido.")
                                invalid = True
                                break

                        if not invalid:
                            try:
                                database.save_form_template(
                                    template_name.strip(),
                                    structure,
                                    st.session_state.get("user_id"),
                                    template_area_id
                                )
                                st.success(f"¡Plantilla '{template_name.strip()}' guardada!")
                                if 'template_fields' in st.session_state:
                                    del st.session_state['template_fields']
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al guardar: {e}")
            
            if clear_form:
                st.session_state.template_fields = pd.DataFrame(
                    [
                        {"Etiqueta del Campo": "", "Tipo de Campo": "Texto", "Requerido": False},
                    ]
                )
                st.rerun()

    # --- 4. GESTIÓN DE ÁREAS ---
    with tab_areas:
        st.header("Gestión de Áreas de Formularios")
        
        with st.form("new_area_form", clear_on_submit=True):
            st.subheader("Crear Nueva Área")
            area_name = st.text_input("Nombre del Área")
            area_desc = st.text_area("Descripción")
            if st.form_submit_button("Crear Área"):
                if not area_name or not area_name.strip():
                    st.error("El nombre del área es requerido.")
                elif len(area_name.strip()) > config.MAX_AREA_NAME_LENGTH:
                    st.error(f"El nombre del área no puede exceder {config.MAX_AREA_NAME_LENGTH} caracteres.")
                else:
                    success, message = database.create_area(area_name.strip(), area_desc.strip())
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        
        st.divider()
        st.subheader("Áreas Existentes")
        try:
            areas = database.get_all_areas()
            areas_df = pd.DataFrame(areas)
            if not areas_df.empty:
                st.dataframe(areas_df.drop(columns=["description"]), use_container_width=True)

                # Editar / Eliminar área
                st.subheader("Editar / Eliminar Área")
                area_ids = areas_df['id'].tolist()
                selected_area = st.selectbox(
                    "Selecciona un área:",
                    options=area_ids,
                    format_func=lambda x: areas_df[areas_df['id']==x]['name'].values[0]
                )
                area_row = next((a for a in areas if a['id'] == selected_area), None)
                if area_row:
                    new_name = st.text_input("Nombre del Área", value=area_row['name'], key="edit_area_name")
                    new_desc = st.text_area("Descripción", value=area_row['description'] or "", key="edit_area_desc")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Actualizar Área"):
                            success, msg = db_helpers.update_area(selected_area, new_name.strip(), new_desc.strip())
                            if success:
                                st.success(msg)
                                st.experimental_rerun()
                            else:
                                st.error(msg)
                    with col2:
                        confirm_key = f"confirm_delete_area_{selected_area}"
                        st.checkbox("Confirmar eliminación (irreversible)", key=confirm_key)
                        if st.button("Eliminar Área Definitivamente"):
                            if st.session_state.get(confirm_key):
                                success, msg = db_helpers.delete_area(selected_area)
                                if success:
                                    st.success(msg)
                                    st.experimental_rerun()
                                else:
                                    st.error(msg)
                            else:
                                st.warning("Por favor confirma la eliminación marcando la casilla.")
            else:
                st.info("No hay áreas aún.")
        except Exception as e:
            st.error(f"Error al cargar áreas: {e}")

    # --- 5. GESTIÓN DE USUARIOS ---
    with tab_users:
        st.header("Gestión de Usuarios")
        
        with st.form("new_user_form", clear_on_submit=True):
            st.subheader("Crear Nuevo Usuario")
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Nombre Completo")
                username = st.text_input("Nombre de Usuario (para login)")
            with col2:
                role = st.selectbox("Rol", config.ALLOWED_ROLES)
                password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Crear Usuario"):
                # Validar nombre completo
                is_valid, error_msg = auth.validate_full_name(full_name)
                if not is_valid:
                    st.error(error_msg)
                else:
                    # Validar nombre de usuario
                    is_valid, error_msg = auth.validate_username(username)
                    if not is_valid:
                        st.error(error_msg)
                    else:
                        # Validar contraseña
                        is_valid, error_msg = auth.validate_password(password)
                        if not is_valid:
                            st.error(error_msg)
                        else:
                            success, message = database.create_user(username.strip(), password, role, full_name.strip())
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
        
        st.divider()
        st.subheader("Usuarios Existentes")
        try:
            users_df = database.get_all_users()
            st.dataframe(users_df, use_container_width=True)
            if not users_df.empty:
                st.subheader("Editar / Eliminar Usuario")
                user_ids = users_df['id'].tolist()
                selected_user = st.selectbox(
                    "Selecciona un usuario:",
                    options=user_ids,
                    format_func=lambda x: f"{users_df[users_df['id']==x]['full_name'].values[0]} ({users_df[users_df['id']==x]['username'].values[0]})"
                )
                user_row = db_helpers.get_user_by_id(selected_user)
                if user_row:
                    new_full_name = st.text_input("Nombre completo", value=user_row.get('full_name',''), key='edit_user_fullname')
                    try:
                        current_index = list(config.ALLOWED_ROLES).index(user_row.get('role')) if user_row.get('role') in config.ALLOWED_ROLES else 0
                    except Exception:
                        current_index = 0
                    new_role = st.selectbox("Rol", config.ALLOWED_ROLES, index=current_index, key='edit_user_role')
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Actualizar Usuario"):
                            success, msg = db_helpers.update_user(selected_user, role=new_role, full_name=new_full_name.strip())
                            if success:
                                st.success(msg)
                                st.experimental_rerun()
                            else:
                                st.error(msg)
                    with col2:
                        confirm_key = f"confirm_delete_user_{selected_user}"
                        st.checkbox("Confirmar eliminación (irreversible)", key=confirm_key)
                        if st.button("Eliminar Usuario Definitivamente"):
                            if st.session_state.get(confirm_key):
                                # Prevent deleting yourself
                                if selected_user == st.session_state.get('user_id'):
                                    st.error("No puedes eliminar el usuario con el que estás autenticado.")
                                else:
                                    success, msg = db_helpers.delete_user(selected_user)
                                    if success:
                                        st.success(msg)
                                        st.experimental_rerun()
                                    else:
                                        st.error(msg)
                            else:
                                st.warning("Por favor confirma la eliminación marcando la casilla.")
        except Exception as e:
            st.error(f"Error al cargar usuarios: {e}")

    # --- 6. REVISIÓN DE ENVÍOS ---
    with tab_review:
        st.header("📋 Revisión de Todos los Envíos")
        
        try:
            all_submissions_df = db_helpers.get_all_submissions_with_details()
            
            if all_submissions_df.empty:
                st.info("ℹ️ Aún no se han realizado envíos de formularios.")
            else:
                # Estadísticas rápidas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📝 Total de Envíos", len(all_submissions_df))
                with col2:
                    st.metric("📅 Últimos 24h", 
                             len(all_submissions_df[all_submissions_df['created_at'] > pd.Timestamp.now() - pd.Timedelta(days=1)]))
                with col3:
                    st.metric("🏢 Áreas Activas", all_submissions_df['area_name'].nunique())
                
                st.divider()
                
                # Filtros
                col1, col2 = st.columns(2)
                with col1:
                    area_filter = st.multiselect(
                        "Filtrar por Área:",
                        all_submissions_df['area_name'].unique(),
                        default=all_submissions_df['area_name'].unique()
                    )
                with col2:
                    user_filter = st.multiselect(
                        "Filtrar por Usuario:",
                        all_submissions_df['user_name'].unique(),
                        default=all_submissions_df['user_name'].unique()
                    )
                
                # Aplicar filtros
                df_filtered = all_submissions_df[
                    (all_submissions_df['area_name'].isin(area_filter)) &
                    (all_submissions_df['user_name'].isin(user_filter))
                ]
                
                # Mostrar tabla
                st.subheader(f"Mostrando {len(df_filtered)} envíos")
                st.dataframe(df_filtered, use_container_width=True, hide_index=True, height=400)
                
                # Opción de descargar
                csv_download = df_filtered.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar como CSV",
                    data=csv_download,
                    file_name="envios_formularios.csv",
                    mime="text/csv"
                )
                # Ver detalles de un envío individual
                st.subheader("👁️ Ver Detalles de un Envío")
                if len(df_filtered) > 0:
                    selected_id = st.selectbox(
                        "Selecciona un envío:",
                        df_filtered['id'].unique(),
                        format_func=lambda x: f"Envío {x} - {df_filtered[df_filtered['id']==x]['template_name'].values[0]}"
                    )

                    submission_data = df_filtered[df_filtered['id'] == selected_id]['data'].iloc[0]

                    with st.expander("📄 Mostrar todos los datos del envío"):
                        try:
                            if isinstance(submission_data, str):
                                import json as _json
                                parsed = _json.loads(submission_data)
                            else:
                                parsed = submission_data

                            if isinstance(parsed, dict):
                                for key, value in parsed.items():
                                    st.write(f"**{key}**: {value}")
                            else:
                                st.write(parsed)
                        except Exception as e:
                            st.error(f"No se pudo mostrar los datos del envío: {str(e)[:120]}")

                    # Mostrar estado de revisión y permitir marcar
                    try:
                        row = df_filtered[df_filtered['id'] == selected_id].iloc[0]
                        reviewed = bool(row.get('reviewed', False))
                        reviewed_by = row.get('reviewed_by_name')
                        reviewed_at = row.get('reviewed_at')

                        st.markdown("**Estado de Revisión:** " + ("✅ Revisado" if reviewed else "❌ Pendiente"))
                        if reviewed and reviewed_by:
                            st.write(f"Revisado por: {reviewed_by} — {reviewed_at}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if not reviewed:
                                if st.button("Marcar como Revisado", key=f"mark_reviewed_{selected_id}"):
                                    success, msg = db_helpers.mark_submission_reviewed(selected_id, st.session_state.get('user_id'), reviewed=True)
                                    if success:
                                        st.success(msg)
                                        st.experimental_rerun()
                                    else:
                                        st.error(msg)
                            else:
                                if st.button("Marcar como No Revisado", key=f"unmark_reviewed_{selected_id}"):
                                    success, msg = db_helpers.mark_submission_reviewed(selected_id, st.session_state.get('user_id'), reviewed=False)
                                    if success:
                                        st.success(msg)
                                        st.experimental_rerun()
                                    else:
                                        st.error(msg)
                    except Exception:
                        # Si algo falla al leer el estado, no romper la vista
                        pass
        except Exception as e:
            st.error(f"❌ Error al cargar envíos: {str(e)[:100]}")