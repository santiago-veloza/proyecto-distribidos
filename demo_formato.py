"""
Demostración visual de la diferencia entre notación científica y formato decimal
"""
import pandas as pd
import numpy as np

print("="*70)
print("DEMOSTRACIÓN: NOTACIÓN CIENTÍFICA vs. FORMATO DECIMAL")
print("="*70)

# Crear datos de ejemplo
datos = {
    'Sector': ['Industrial', 'Comercial', 'Residencial'],
    'Consumo_kWh': [1234567890.5, 987654321.3, 456789123.7],
    'Factura_COP': [5432109876.2, 3210987654.9, 1987654321.5]
}

df = pd.DataFrame(datos)

print("\n1. SIN CONFIGURACIÓN (Notación Científica por defecto):")
print("-" * 70)
# Resetear configuración para mostrar comportamiento por defecto
pd.reset_option('display.float_format')
print(df)
print("\nObserva que los números grandes se muestran como 1.234568e+09")

print("\n" + "="*70)
print("\n2. CON CONFIGURACIÓN (Formato Decimal):")
print("-" * 70)
# Aplicar la configuración del script
pd.options.display.float_format = '{:.2f}'.format
print(df)
print("\nAhora los números se muestran como 1234567890.50")

print("\n" + "="*70)
print("\n3. EJEMPLO CON AGRUPACIÓN (como en el script principal):")
print("-" * 70)
df_resumen = df.groupby('Sector')[['Consumo_kWh', 'Factura_COP']].mean().reset_index()
print(df_resumen.to_string(index=False))

print("\n" + "="*70)
print("✅ CONCLUSIÓN:")
print("   La configuración evita la notación científica en:")
print("   - DataFrames impresos con print()")
print("   - Operaciones de agrupación (groupby)")
print("   - Salida de to_string()")
print("="*70)
