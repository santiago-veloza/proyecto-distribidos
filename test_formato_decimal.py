"""
Test script to verify that pandas display options prevent scientific notation
"""
import pandas as pd
import numpy as np

# Configure pandas to avoid scientific notation
pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# Create test data with large numbers that would normally show in scientific notation
test_data = {
    'Categoria': ['A', 'B', 'C', 'D'],
    'Valor': [1234567.89, 9876543.21, 5555555.55, 123456789.12]
}

df = pd.DataFrame(test_data)

print("=== Test de formato decimal (sin notación científica) ===\n")
print("DataFrame con valores grandes:")
print(df)
print("\n")

# Test groupby and aggregation (similar to the main script)
df_agrupado = df.groupby('Categoria')['Valor'].mean().reset_index()
df_agrupado.columns = ['Categoria', 'Promedio']

print("Datos agrupados:")
print(df_agrupado.to_string(index=False))
print("\n")

# Verify that no scientific notation appears in string representation
df_string = df.to_string()
has_scientific = 'e+' in df_string or 'E+' in df_string or 'e-' in df_string or 'E-' in df_string

if has_scientific:
    print("❌ FAIL: Se detectó notación científica en la salida")
    exit(1)
else:
    print("✅ PASS: No se detectó notación científica - Los números se muestran en formato decimal")
    exit(0)
