# trabajo_final_medialab

# Análisis de titulares de Andina vs La República Deportes

## Descripción del proyecto
Este proyecto busca analizar y comparar los titulares de noticias deportivas provenientes de dos medios peruanos: **Andina** y **La República Deportes**, con el objetivo de entender patrones de publicación, frecuencia y uso de palabras clave. Se presenta un **análisis visual** a través de nubes de palabras, barras de publicaciones por momento del día y tablas de titulares con su longitud.

---

## Pregunta central
¿Cómo se diferencian los titulares deportivos de Andina y La República Deportes en cuanto a frecuencia, momento de publicación y palabras más usadas?

---

## Fuente de datos
Los datos utilizados provienen de los CSV procesados con Python:

- `andina_procesado.csv` → titulares de Andina  
- `larepublica_procesado.csv` → titulares de La República Deportes  
- `top_palabras_titulares.csv` → palabras más frecuentes en todos los titulares  
- `publicaciones_por_momento_dia.csv` → número de publicaciones según el momento del día  

Todos los archivos se encuentran en la carpeta `data` del repositorio.

---

## Metodología

1. **Recolección de datos**  
   - Se extrajeron titulares deportivos de los portales de Andina y La República mediante scraping y APIs disponibles.  
   
2. **Procesamiento de los datos con Python**  
   - Limpieza de textos: eliminación de caracteres especiales y stopwords (español e inglés).  
   - Cálculo de métricas de los titulares:
     - Longitud en palabras
     - Longitud en caracteres  
   - Extracción de las **palabras más frecuentes** en los titulares.  

3. **Generación de archivos procesados**  
   - CSV combinados por medio y métricas calculadas:
     - `andina_procesado.csv`
     - `larepublica_procesado.csv`
     - `top_palabras_titulares.csv`
     - `publicaciones_por_momento_dia.csv`

4. **Visualización en HTML**  
   - Se adaptó un HTML estático para mostrar:
     - Barras de publicaciones por momento del día.  
     - Nube de palabras con tamaño proporcional a la frecuencia.  
     - Tabla combinada de titulares, con columna de medio, longitud en palabras y caracteres.  
   - Se mantiene el **modo oscuro/claro** y estilos de presentación.

---

## Principales hallazgos

- **Frecuencia de publicaciones:**  
  La mayoría de titulares se publican por la **noche** y tarde, mientras que madrugadas y mañanas tienen menos actividad.  

- **Palabras más frecuentes:**  
  Se destacan términos como *lima, alianza, peña, zambrano* y *noche*, indicando la relevancia de noticias sobre fútbol local y ciertos jugadores.  

- **Comparación entre medios:**  
  - Andina tiende a publicar titulares más cortos y objetivos.  
  - La República Deportes presenta titulares más largos, descriptivos y enfocados en detalles polémicos o de interés mediático.  

- **Tendencias visuales:**  
  La nube de palabras y barras muestran claramente la concentración temática y el momento de publicación más frecuente, permitiendo comparar de manera inmediata ambos medios.

---

### Autor
Proyecto desarrollado por Carlos Reyes para el curso de Extracción y Procesamiento de Datos, ofrecido por el MediaLab, usando Python y HTML para procesamiento y visualización de datos.
