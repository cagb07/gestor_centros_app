#!/usr/bin/env python3
"""
Script de prueba para verificar que el CSV se carga correctamente
"""
import pandas as pd
import sys

def test_csv_loading():
    """Prueba la carga del archivo CSV con diferentes codificaciones"""
    file_path = "datos_centros.csv"
    encodings = ['utf-8', 'cp1252', 'iso-8859-1', 'latin-1']
    
    print("🔍 Probando carga de CSV...")
    print("-" * 60)
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"✅ Codificación {encoding}: ÉXITO")
            print(f"   - Filas: {len(df)}")
            print(f"   - Columnas: {len(df.columns)}")
            print(f"   - Columnas: {list(df.columns)[:5]}...")
            return True, encoding, df
        except UnicodeDecodeError:
            print(f"❌ Codificación {encoding}: Error de decodificación")
        except Exception as e:
            print(f"❌ Codificación {encoding}: {type(e).__name__}")
    
    return False, None, None

if __name__ == "__main__":
    success, encoding, df = test_csv_loading()
    print("-" * 60)
    
    if success:
        print(f"\n✅ CSV cargado exitosamente con codificación: {encoding}")
        print(f"\nPrimeras filas:")
        print(df.head(3))
        sys.exit(0)
    else:
        print("\n❌ No se pudo cargar el CSV con ninguna codificación")
        sys.exit(1)
