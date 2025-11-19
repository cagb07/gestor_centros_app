#!/bin/bash
cd /workspaces/gestor_centros_app
/workspaces/gestor_centros_app/.venv/bin/python -m streamlit run app.py --server.port=8501 --logger.level=debug
