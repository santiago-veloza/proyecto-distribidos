# Análisis Financiero - Solución al Problema de Notación Científica

## Problema
El script de análisis financiero mostraba números en notación científica (por ejemplo: `1.23e+06`) en lugar de formato decimal (por ejemplo: `1,230,000`).

## Solución Implementada

Se han agregado las siguientes configuraciones al inicio del script para evitar la notación científica:

```python
# Configuración de pandas para evitar notación científica
pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.float_format', lambda x: '%.2f' % x)
```

También se agregó formateo específico para el eje Y del gráfico:

```python
# Formatear los valores del eje Y para evitar notación científica
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
```

## Cambios Realizados

1. **Configuración Global de Pandas**: Al inicio del script, se configuró pandas para mostrar todos los números con formato decimal con 2 decimales.

2. **Formato del Gráfico**: Se agregó un formateador personalizado para el eje Y que muestra números con separadores de miles y sin decimales.

3. **Impresión de Resultados**: Se agregó `print(df_exploracion.to_string(index=False))` para mostrar los resultados en la consola con formato decimal.

## Instalación de Dependencias

Antes de ejecutar el script, instala las dependencias requeridas:

```bash
pip install -r requirements_analisis.txt
```

O instala los paquetes individualmente:

```bash
pip install pandas numpy seaborn matplotlib openpyxl
```

## Uso

1. Asegúrate de que los archivos de Excel estén en el mismo directorio que el script:
   - `Detallado W - Facturación consumos Septiembre 2025 1.xlsx`
   - `TABLA PYTHON.xlsx`
   - `Fronteras Vigentes oct_2025.xlsx`

2. Ejecuta el script:

```bash
python analisis_financiero.py
```

Ahora todos los números se mostrarán en formato decimal legible, tanto en la consola como en los gráficos generados.

## Verificación

Para verificar que el formato decimal funciona correctamente, puedes ejecutar el script de prueba:

```bash
python test_formato_decimal.py
```

## Personalización

Si deseas cambiar el número de decimales mostrados, modifica esta línea:

```python
pd.options.display.float_format = '{:.2f}'.format  # Cambia .2f por .0f para sin decimales, .3f para 3 decimales, etc.
```

Para el formato del gráfico, puedes ajustar:

```python
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))  # .0f = sin decimales, .2f = 2 decimales
```
