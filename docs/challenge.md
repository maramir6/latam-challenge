# Justificación de la Elección del Modelo

## Justificación

Aunque la precisión y la exactitud son importantes, en este caso, el `recall` de la clase atraso (minoritaria) es crucial. El modelo XGBoost balanceado tiene un `recall` de 0.69 para la clase 1, lo que significa que de todas las instancias positivas, el 69% fueron correctamente identificadas por el modelo. En contraste, los modelos XGBoost y Regresión Logística no balanceados tienen un `recall` extremadamente bajo para la clase 1 (0.01 y 0.01, respectivamente).

El F1-score, que es la media de la precisión y el `recall`, también es significativamente más alto para el modelo XGBoost balanceado en la clase atraso (0.37) en comparación con los modelos XGBoost no balanceado (0.01) y Regresión Logística no balanceada (0.03).

En situaciones donde el desequilibrio de clases es significativo, como en este caso, el balanceo de clases puede ayudar a mejorar el rendimiento del modelo en la clase minoritaria. Aunque el modelo XGBoost balanceado tiene una precisión y exactitud más baja en comparación con los otros modelos, su capacidad para identificar correctamente un mayor porcentaje de la clase minoritaria (como se indica por el `recall` y el F1-score) lo convierte en la mejor opción para este problema específico.

## Importancia de las Características

La importancia de las características también se evaluó para cada modelo. En general, el modelo XGBoost con clases balanceadas proporcionó una mejor interpretación de las características que contribuyen más a la predicción. Esto es especialmente útil para entender qué variables son más informativas para predecir la clase minoritaria.

## Conclusión
En el caso de negocio es importante predecir los atrasos para poder tomar acciones relevantes, es por esta razón, que clasificar los atrasos se vuelve más importante que clasificar los no atrasos. Debido a la naturaleza del problema, los atrasos no están representados de la misma forma que los no atrasos, ya que tienen una probabiliad de ocurrencia menor.
Dado que el `recall` de la clase atraso es particularmente importante para este problema, y considerando la importancia de las características, el modelo XGBoost con clases balanceadas se seleccionó como el modelo final. Aunque tiene una precisión y exactitud más bajas en comparación con los otros modelos, su mayor `recall` y F1-score para la clase atraso indican que es más adecuado para este problema de clasificación específico.
