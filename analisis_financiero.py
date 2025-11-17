import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# =================================================================
# CONFIGURACIÓN DE PANDAS PARA EVITAR NOTACIÓN CIENTÍFICA
# =================================================================
# Estas opciones aseguran que los números se muestren en formato decimal
pd.options.display.float_format = '{:.2f}'.format  # Formato con 2 decimales
pd.set_option('display.float_format', lambda x: '%.2f' % x)  # Alternativa más robusta

# =================================================================
# 1) DEFINICIÓN DE RUTAS Y ARCHIVOS
# =================================================================

# Usamos los nombres exactos de tus archivos
FIN_PATH = "Detallado W - Facturación consumos Septiembre 2025 1.xlsx"
COM_PATH = "TABLA PYTHON.xlsx"
MAESTRO_PATH = "Fronteras Vigentes oct_2025.xlsx"


# =================================================================
# 2) CARGAR Y NORMALIZAR ENCABEZADOS
# =================================================================

try:
    df_fin = pd.read_excel(FIN_PATH, sheet_name="Sheet1")
    df_com = pd.read_excel(COM_PATH)
    df_maestro = pd.read_excel(MAESTRO_PATH) 
except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar un archivo. Asegúrate de que los tres archivos están en la misma carpeta. Detalle: {e}")
    exit()

# Normaliza encabezados: Quita espacios y pone en mayúsculas
df_fin.columns = df_fin.columns.str.strip().str.upper()
df_com.columns = df_com.columns.str.strip().str.upper()
df_maestro.columns = df_maestro.columns.str.strip().str.upper()


# =================================================================
# 3) UNIFICAR LAS TRES TABLAS (El paso más crucial)
# =================================================================

# 3.1) Renombrar la clave de unión en las tres tablas para usar un nombre común
# Asumimos que "INT. COMERCIAL" y "BP" son el mismo identificador.
CLAVE_UNICA = "BP_CLAVE_UNICA"

df_fin.rename(columns={"INT. COMERCIAL": CLAVE_UNICA}, inplace=True)
df_com.rename(columns={"BP": CLAVE_UNICA}, inplace=True) 
df_maestro.rename(columns={"INTERLOCUTOR COMERCIAL (BP)": CLAVE_UNICA}, inplace=True)

# 3.2) Unir el Detalle W (df_fin) con la información de Cuentas (df_com)
df_merged_1 = pd.merge(
    df_fin,
    df_com,
    on=CLAVE_UNICA,
    how="left" # Mantenemos todos los movimientos del detalle W
)

# 3.3) Unir el resultado (df_merged_1) con la nueva tabla de Maestro de Clientes (df_maestro)
df_merged_2 = pd.merge(
    df_merged_1,
    df_maestro,
    on=CLAVE_UNICA,
    how="left",
    suffixes=('_CUENTA', '_MAESTRO') # Sufijos para diferenciar columnas con el mismo nombre
)

# =================================================================
# 4) LIMPIEZA Y PREPARACIÓN DE DATOS
# =================================================================

cols_keep = [
    CLAVE_UNICA, 'CLIENTE', 'SECTOR_CUENTA', 'AÑO',
    'ACTIVOS CORRIENTES', 'PASIVOS CORRIENTES', 'INVENTARIO',
    'DEUDA TOTAL', 'PATRIMONIO NETO', 'ACTIVOS TOTALES',
    'EBIT', 'GASTOS POR INTERESES', 'CFO', 'EBITDA',
    'INGRESOS OPERACIONALES', 'UTILIDAD NETA',
    'TOTAL FACTURA', 'CONSUMO ACTIVA',
    # Variables contextuales del nuevo Maestro (Fronteras Vigentes)
    'CIUDAD', 'DEPARTAMENTO', 'NIVEL TENSIÓN', 'TENSION OPERACIÓN',
    'SECTOR COMERCIAL INDICADO EN XM'
]

df_clean = df_merged_2.filter(items=cols_keep).copy()

# Convierte las columnas que deben ser numéricas
num_cols = [
    'ACTIVOS CORRIENTES', 'PASIVOS CORRIENTES', 'INVENTARIO',
    'DEUDA TOTAL', 'PATRIMONIO NETO', 'ACTIVOS TOTALES',
    'EBIT', 'GASTOS POR INTERESES', 'CFO', 'EBITDA',
    'INGRESOS OPERACIONALES', 'UTILIDAD NETA',
    'TOTAL FACTURA', 'CONSUMO ACTIVA'
]
df_clean[num_cols] = df_clean[num_cols].apply(pd.to_numeric, errors='coerce')


# =================================================================
# 5) CÁLCULO DE INDICADORES FINANCIEROS
# =================================================================

# Calcula los indicadores financieros
df_clean['RAZON_CORRIENTE'] = df_clean['ACTIVOS CORRIENTES'] / df_clean['PASIVOS CORRIENTES']
df_clean['PRUEBA_ACIDA'] = (df_clean['ACTIVOS CORRIENTES'] - df_clean['INVENTARIO']) / df_clean['PASIVOS CORRIENTES']
df_clean['DEUDA_PATRIMONIO'] = df_clean['DEUDA TOTAL'] / df_clean['PATRIMONIO NETO']
df_clean['DEUDA_ACTIVOS'] = df_clean['DEUDA TOTAL'] / df_clean['ACTIVOS TOTALES']
df_clean['ROA'] = df_clean['UTILIDAD NETA'] / df_clean['ACTIVOS TOTALES']
df_clean['ROE'] = df_clean['UTILIDAD NETA'] / df_clean['PATRIMONIO NETO']
df_clean['MARGEN_EBITDA'] = df_clean['EBITDA'] / df_clean['INGRESOS OPERACIONALES']
df_clean['DSCR'] = df_clean['CFO'] / df_clean['GASTOS POR INTERESES']

# Limpiar valores infinitos o NaN
df_clean.replace([np.inf, -np.inf], np.nan, inplace=True)

# Tabla final para el análisis
indicadores_clave = ['ROA','ROE','DEUDA_PATRIMONIO','MARGEN_EBITDA','DSCR']
df_indicadores = df_clean.dropna(subset=indicadores_clave, how='all')

print("✅ Data preparada y lista para la correlación.")

# =================================================================
# 6) CORRELACIÓN INESPERADA (CATEGÓRICA vs. NUMÉRICA)
# ❗ ESTE ES EL PASO DE EXPLORACIÓN. CAMBIA ESTAS VARIABLES PARA EXPERIMENTAR
# =================================================================

# Correlación inicial: NIVEL TENSIÓN (Contexto) vs. CONSUMO ACTIVA (Medida)
V_CONTEXTO = 'SECTOR COMERCIAL INDICADO EN XM'      
V_MEDIDA = 'CONSUMO ACTIVA'       

print(f"\n--- 🔎 Exploración de Correlación: {V_CONTEXTO} vs. {V_MEDIDA} ---")

# Agrupación y Sumarización: Promedio de la Medida por la Variable de Contexto
df_exploracion = df_indicadores.groupby(V_CONTEXTO)[V_MEDIDA].mean().reset_index()
df_exploracion.columns = [V_CONTEXTO, 'PROMEDIO_VALOR']

# Ordenar para identificar anomalías rápidamente
df_exploracion = df_exploracion.sort_values(by='PROMEDIO_VALOR', ascending=False)
df_exploracion = df_exploracion.dropna() # Eliminar nulos de la variable de contexto

# Mostrar los resultados en formato decimal (sin notación científica)
print("\nResultados del análisis:")
print(df_exploracion.to_string(index=False))

# 7) VISUALIZACIÓN
plt.figure(figsize=(12, 6))
sns.barplot(
    x=V_CONTEXTO, 
    y='PROMEDIO_VALOR', 
    data=df_exploracion,
    palette='magma' 
)

# Formatear los valores del eje Y para evitar notación científica
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

plt.title(f'Patrones Inesperados: Promedio de {V_MEDIDA} por {V_CONTEXTO}')
plt.ylabel(f'Promedio de {V_MEDIDA}')
plt.xlabel(V_CONTEXTO)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# ----------------------------------------------------
# ❗ CÓMO EXPERIMENTAR DESPUÉS:
# ----------------------------------------------------
# Para probar una nueva correlación (ej. CIUDAD vs. ROA), simplemente cambia las variables en la Sección 6:
# V_CONTEXTO = 'CIUDAD'
# V_MEDIDA = 'ROA' 
# Luego, ejecuta el script de nuevo.
