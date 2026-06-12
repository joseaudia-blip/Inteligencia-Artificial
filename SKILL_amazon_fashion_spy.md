---
name: amazon-fashion-spy
description: >
  Skill para buscar productos ganadores de moda (dropshipping) en Amazon Europa
  navegando con Claude en Chrome. Úsala cuando el usuario quiera espiar productos
  de moda en Amazon de Europa (Francia, Alemania, Reino Unido, Italia), encontrar
  productos trending con alto BSR/ventas estimadas, analizar competidores en
  ecommerce de moda, o construir un listado de productos ganadores para Amazon o
  tienda propia. Activa esta skill siempre que el usuario mencione: "buscar productos
  amazon", "productos ganadores amazon", "amazon spy moda", "BSR moda",
  "dropshipping amazon europa", "mejores vendidos amazon ropa", o quiera analizar
  ventas/rankings de productos de moda en Amazon.
compatibility:
  requires:
    - Claude in Chrome (extensión activa en el navegador)
    - Extensión "Helium 10" instalada y activa en Chrome (plan gratuito suficiente)
      (Chrome Web Store: buscar "Helium 10 Chrome Extension")
    - Acceso a amazon.co.uk · amazon.fr · amazon.de · amazon.it
  alternativa_sin_extension:
    - Sin Helium 10, usar directamente los datos de BSR visibles en cada listing
    - Acceder a "Movers & Shakers" y "Best Sellers" nativos de Amazon
  notas_extension:
    - Helium 10 X-Ray muestra ventas estimadas mensuales, revenue, BSR e historial
    - El plan gratuito permite un número limitado de usos por día
    - Xray se activa desde el popup de la extensión en cualquier página de búsqueda
    - También funciona directamente en la página de producto individual
---

# Amazon Fashion Spy

Skill para detectar productos ganadores de moda en Amazon Europa,
enfocada en dropshipping / marca propia (FR, DE, UK, IT), con filtros de
BSR y ventas estimadas para validar que el producto tiene tracción real.

---

## CONTEXTO DEL NEGOCIO

- **Nicho**: Ecommerce de moda, principalmente mujer
- **Modelo**: Dropshipping o marca propia con proveedor externo
- **Mercados objetivo**: Francia, Alemania, Reino Unido, Italia
- **Productos de interés**: Vestidos, jerseys, pantalones, zapatos, bolsos,
  conjuntos de 2 piezas, ropa mujer en general

---

## CRITERIOS DE PRODUCTO GANADOR

Un producto es **ganador** si cumple los siguientes umbrales:

### Por BSR (Best Seller Rank) — Categoría principal de Ropa/Fashion
| BSR en categoría principal | Señal               |
|----------------------------|---------------------|
| < 500                      | Producto muy caliente |
| 500 – 2.000                | Producto ganador    |
| 2.001 – 5.000              | Producto interesante |
| > 5.000                    | Ignorar             |

### Por ventas estimadas mensuales (con Helium 10 X-Ray)
| Ventas/mes estimadas | Señal               |
|----------------------|---------------------|
| > 300 unidades/mes   | Producto ganador    |
| 100 – 300 unidades   | Producto interesante |
| < 100 unidades       | Ignorar             |

### Por reseñas (indicador secundario)
- Producto con < 200 reseñas y BSR < 2.000 → **oportunidad de mercado** (poco competido)
- Producto con > 1.000 reseñas y BSR < 500 → mercado validado pero competido

> Si no hay extensión activa, usar solo el BSR visible en el listing como
> criterio principal.

---

## MARCAS A IGNORAR — LISTA NEGRA

Antes de analizar cualquier producto, verificar que el vendedor/marca
**no** es una marca grande o marketplace conocido. Si lo es, saltar al siguiente.

**Ignorar siempre estos vendedores y similares:**
Amazon Essentials · Levi's · Calvin Klein · Tommy Hilfiger · Nike · Adidas
New Balance · Skechers · Puma · Under Armour · Columbia · The North Face
Zara · H&M · Mango · ASOS · Boohoo · Shein · Temu · PrettyLittleThing
Guess · Versace · Armani · Ralph Lauren · Hugo Boss · Michael Kors

**Señales de marca grande aunque no esté en la lista:**
- Marca con más de 50.000 reseñas totales en Amazon
- Nombre de marca reconocible internacionalmente
- Vendido directamente **por Amazon** (Fulfilled AND Sold by Amazon, no solo FBA)
- Listings con imágenes de producción muy alta y vídeo de marca elaborado
- Presencia masiva en toda la categoría con decenas de variantes

**El perfil que SÍ buscamos:**
- Vendedor con nombre genérico o poco conocido (VONDA, ANRABESS, KIRUNDO, etc.)
- Pocos productos en su tienda pero con muchas ventas en ese producto concreto
- Menos de 2.000 reseñas en el listing objetivo (o más reseñas si BSR es muy bajo)
- Precio en rango dropshipping: 15€–60€ para ropa, hasta 80€ para zapatos/bolsos
- FBA (Fulfilled by Amazon) pero vendido por tercero, no por Amazon directamente

> 🎯 El objetivo es encontrar sellers pequeños o medianos que estén escalando
> un producto con éxito en Amazon — señal de que el producto es replicable
> con proveedor en Alibaba/CJDropshipping/Zendrop.

---

## FLUJO DE TRABAJO PRINCIPAL

### PASO 1 — Elegir el punto de entrada correcto

Hay **3 estrategias de búsqueda** principales. Usarlas en este orden:

#### Estrategia A — Best Sellers por categoría (más directo)
Navegar directamente a la sección de más vendidos de moda del país objetivo:

```
🇬🇧 https://www.amazon.co.uk/Best-Sellers-Fashion/zgbs/fashion/
🇫🇷 https://www.amazon.fr/gp/bestsellers/fashion/
🇩🇪 https://www.amazon.de/gp/bestsellers/fashion/
🇮🇹 https://www.amazon.it/gp/bestsellers/fashion/
```

Navegar por subcategorías específicas para afinar:
- Women's Dresses / Robes Femme / Damenkleider / Abiti Donna
- Women's Tops & Blouses
- Women's Trousers & Leggings
- Women's Shoes / Chaussures Femme
- Women's Handbags / Sacs à main

#### Estrategia B — Movers & Shakers (productos con más crecimiento repentino)
Productos que han subido más posiciones en BSR en las últimas 24 horas:

```
🇬🇧 https://www.amazon.co.uk/gp/movers-and-shakers/fashion/
🇫🇷 https://www.amazon.fr/gp/movers-and-shakers/fashion/
🇩🇪 https://www.amazon.de/gp/movers-and-shakers/fashion/
🇮🇹 https://www.amazon.it/gp/movers-and-shakers/fashion/
```

> 💡 Un producto que ha subido +500% en BSR en 24h es señal de viralidad
> o de campaña de ads activa — exactamente lo que buscamos.

#### Estrategia C — Búsqueda por keyword con filtros
Usar el buscador de Amazon con keywords de producto + ordenar por "Best Sellers":

**Formato de búsqueda:** `<KEYWORD>` → ordenar por **"Best Sellers"**

```
🇬🇧 https://www.amazon.co.uk/s?k=<KEYWORD>&sort=review-rank
🇫🇷 https://www.amazon.fr/s?k=<KEYWORD>&sort=review-rank
🇩🇪 https://www.amazon.de/s?k=<KEYWORD>&sort=review-rank
🇮🇹 https://www.amazon.it/s?k=<KEYWORD>&sort=review-rank
```

---

### PASO 2 — Activar Helium 10 X-Ray (si disponible)

Una vez en la página de resultados de búsqueda o en la subcategoría:

1. Hacer clic en el icono de Helium 10 en la barra de Chrome
2. Seleccionar **"X-Ray"** en el menú de herramientas
3. Esperar 3-5 segundos a que cargue la capa de datos sobre los resultados
4. X-Ray mostrará por cada producto:
   - **Monthly Sales** (ventas estimadas/mes)
   - **Monthly Revenue** (ingresos estimados/mes)
   - **BSR** (rank actual)
   - **Review Count** y **Rating**
   - **Price**
5. Ordenar la tabla de X-Ray por **Monthly Sales** de mayor a menor

> ⚠️ Si Helium 10 no está disponible o agotó el límite diario gratuito:
> Usar directamente el BSR visible en cada listing (ver PASO 3 alternativo).

---

### PASO 3 — Scroll inicial para cargar todos los productos

Antes de analizar nada, hacer un recorrido completo de la página:

1. Esperar **2-3 segundos** tras cargar la página
2. Desplazarse hacia abajo de forma continua:
   - Bajar en tramos de ~4-5 productos
   - Pausa de **1 segundo** en cada tramo
   - Repetir hasta haber visto aproximadamente **20-30 productos**
3. Volver al **principio de la página**
4. Solo entonces comenzar el análisis de arriba abajo

> 💡 Amazon usa carga dinámica (lazy loading). Sin este scroll previo,
> Helium 10 X-Ray no puede leer los datos de los productos que no han
> aparecido aún en pantalla.

---

### PASO 3 ALTERNATIVO — Sin Helium 10: leer BSR manualmente

Si no hay extensión activa, entrar en cada listing individualmente:

1. Abrir el producto en nueva pestaña
2. Bajar hasta la sección **"Product details"** / **"Informations sur le produit"** /
   **"Produktinformation"** / **"Informazioni sul prodotto"**
3. Localizar el campo:

| País | Texto a buscar              | Ejemplo                              |
|------|-----------------------------|--------------------------------------|
| 🇬🇧  | **Best Sellers Rank**       | `#342 in Women's Dresses`            |
| 🇫🇷  | **Classement des meilleures ventes** | `#342 en Robes Femme`    |
| 🇩🇪  | **Amazon Bestseller-Rang**  | `Nr. 342 in Damenkleider`            |
| 🇮🇹  | **Posizione nella classifica** | `#342 in Abiti Donna`            |

4. Usar el BSR de la **subcategoría más específica** (siempre más bajo y relevante)
5. Aplicar umbrales de la tabla de criterios

---

### PASO 4 — Escanear y filtrar

Para cada producto visible:
1. Leer nombre del vendedor / marca
2. Leer título del producto
3. Leer BSR y/o ventas estimadas (de X-Ray o manualmente)
4. Verificar si el producto es moda mujer (prioridad)
5. Verificar que no está en la lista negra de marcas
6. Aplicar umbrales: si NO cumple → ignorar · si SÍ cumple → PASO 5

---

### PASO 5 — Extraer datos del ganador

Entrar en el listing del producto y recoger:

1. URL completa del listing de Amazon
2. Nombre exacto del producto (título del listing)
3. Nombre del vendedor/marca (ver sección "Sold by" / "Vendu par")
4. Precio actual y precio tachado (si hay descuento)
5. BSR en categoría principal y en subcategoría
6. Número de reseñas y valoración media (estrellas)
7. Variantes disponibles (colores, tallas)
8. Fecha de primera disponibilidad (en "Product details" → "Date First Available")
9. Si Helium 10 activo: ventas estimadas/mes y revenue estimado/mes

---

### PASO 6 — Investigar al competidor (opcional pero recomendado)

1. Hacer clic en el nombre del vendedor → ver su tienda en Amazon
2. Revisar cuántos productos tiene activos
3. Identificar si tiene más productos de moda con buen BSR
4. Buscar el producto en Alibaba / CJDropshipping para validar margen

> 💡 Un seller con 3-5 productos y todos con BSR < 2.000 es señal de
> dropshipping activo bien optimizado — explorar su catálogo completo.

---

### PASO 7 — Reportar al usuario

Formato de reporte por cada producto ganador encontrado:

```
✅ PRODUCTO GANADOR

🔗 Link: [URL del listing en Amazon]
🏷️ Producto: [nombre/descripción]
📦 BSR: #[número] en [subcategoría] · #[número] en [categoría principal]
📈 Ventas estimadas: [N] unidades/mes · [revenue €/mes] (si Helium 10 activo)
⭐ Reseñas: [N reseñas] · [X.X estrellas]
💰 Precio: [precio] (original: [precio tachado si aplica])
🌍 País: [bandera + nombre]
🏪 Vendedor: [nombre del seller]
📅 En Amazon desde: [fecha si visible]
📂 Categoría: [Vestido / Bolso / Pantalón / Zapatos / Conjunto / Otro]
🔍 Oportunidad: [Alta / Media — breve justificación, ej: "pocas reseñas, BSR bajo"]

---
```

**Continuar automáticamente** con la siguiente keyword/subcategoría sin esperar confirmación.

---

## BANCOS DE PALABRAS CLAVE

### 🇬🇧 Reino Unido (amazon.co.uk)

**Productos directos:** Women dress · Summer dress · Midi dress · Wrap dress
Palazzo trousers · Wide leg trousers · Jumpsuit women · Bodycon dress
Women blouse · Oversized blazer · Women cardigan · Knit dress

**Con modificadores de tendencia:** Trending women fashion · Bestselling dress
Women fashion 2025 · Viral dress · Women outfit · Elegant dress

### 🇫🇷 Francia (amazon.fr)

**Productos directos:** Robe femme · Robe d'été · Robe midi · Combinaison femme
Pantalon palazzo · Chemisier femme · Veste femme · Pull femme · Robe longue

**Con modificadores de tendencia:** Robe tendance · Mode femme 2025
Robe élégante · Tenue femme chic · Robe casual

### 🇩🇪 Alemania (amazon.de)

**Productos directos:** Damen Kleid · Sommerkleid · Midi Kleid · Overall Damen
Palazzo Hose · Damen Bluse · Damen Strickjacke · Wickelkleid · Jumpsuit Damen

**Con modificadores de tendencia:** Trendiges Damen Outfit · Bestseller Kleid
Mode Damen 2025 · Elegantes Kleid · Casual Damen Kleid

### 🇮🇹 Italia (amazon.it)

**Productos directos:** Vestito donna · Abito donna · Vestito estivo · Tuta donna
Pantaloni palazzo · Camicetta donna · Maglione donna · Vestito lungo

**Con modificadores de tendencia:** Abito tendenza · Moda donna 2025
Vestito elegante · Outfit donna · Vestito casual

---

## ESTRATEGIA DE BÚSQUEDA RECOMENDADA

**Orden de países por sesión estándar:**
1. 🇬🇧 Reino Unido — Best Sellers directos (mayor volumen, datos más claros)
2. 🇫🇷 Francia — Movers & Shakers (detectar tendencias emergentes)
3. 🇩🇪 Alemania — Keywords de productos directos
4. 🇮🇹 Italia — Best Sellers por subcategoría

**Rotación dentro de cada país:**
- Primero Best Sellers → luego Movers & Shakers → luego keyword search
- Si una subcategoría no da resultados con BSR suficiente, pasar a la siguiente
- Explorar siempre al menos 3 subcategorías por país antes de cambiar de país

---

## TROUBLESHOOTING

**Si Helium 10 no muestra datos:**
- Verificar que el icono aparece activo en la barra de Chrome
- Refrescar la página y esperar 4-5 segundos
- Comprobar si se agotaron los créditos gratuitos del día
- Si se agotaron: usar BSR manual (PASO 3 ALTERNATIVO)

**Si Amazon redirige o muestra CAPTCHA:**
- Pausar y notificar: "Amazon está mostrando verificación de seguridad.
  Por favor, completa el CAPTCHA manualmente y avísame para continuar."

**Si los resultados de Best Sellers no muestran moda mujer:**
- Navegar a subcategorías más específicas desde el menú lateral izquierdo
- Buscar "Women" / "Femme" / "Damen" / "Donna" en el filtro de departamento

**Si el BSR de un producto interesante no aparece en el listing:**
- Bajar más en la página de detalles — a veces está tras las descripciones largas
- Buscar en la sección "Additional Information" / "Informations complémentaires"

**Cómo identificar dropshippers en Amazon:**
- Vendedor con nombre extraño (siglas, palabras inventadas tipo "ANRABESS", "KIRUNDO")
- Pocos productos en su tienda pero con muchas reseñas en ese producto concreto
- Imágenes con fondo blanco o lifestyle genérico sin logo de marca visible
- Sin página de marca oficial (Brand Store de Amazon) o con Brand Store muy básico
- Precio con descuento marcado desde un precio alto (táctica de percepción de valor)

---

## VALIDACIÓN DE MARGEN (paso opcional tras encontrar ganador)

Para verificar que el producto es rentable antes de reportarlo como ganador:

1. Copiar imagen o descripción del producto de Amazon
2. Buscar en **Alibaba** (`alibaba.com`) o **CJDropshipping** (`cjdropshipping.com`)
3. Margen mínimo aceptable: precio Amazon × 0.30 ≥ coste proveedor + FBA fees
4. Estimar FBA fees: usar la calculadora `amazon.co.uk/fba` (o equivalente por país)

> 💡 Regla rápida: si el producto se vende en Amazon a 30€ y en Alibaba
> sale a menos de 8€/ud, el margen es viable para FBA o dropshipping.

---

## RESUMEN FINAL DE SESIÓN

Al terminar (o cuando el usuario lo pida), generar:

```
📊 RESUMEN DE SESIÓN — Amazon Fashion Spy
==========================================
🔍 Categorías/keywords analizadas: [N]
🌍 Países cubiertos: [lista]
✅ Productos ganadores encontrados: [N]

TOP PRODUCTOS:
1. [Producto] — BSR #[N] — [Ventas/mes si disponible] — [País] — [Link]
2. [Producto] — BSR #[N] — [Ventas/mes si disponible] — [País] — [Link]
...

💡 OBSERVACIONES:
- [Tendencias de producto detectadas]
- [Patrones de precio que funcionan]
- [Vendedores con más potencial de replicar]
- [Subcategorías más rentables encontradas]
```

---

## PRINCIPIOS DE COMPORTAMIENTO

- **Proactivo**: No esperar confirmación entre productos. Reportar y continuar.
- **Selectivo**: Solo reportar lo que supera umbrales de BSR o ventas. Sin inflación.
- **Preciso**: Siempre incluir link directo al listing. Sin link, el dato no tiene valor.
- **Priorizar mujer**: Si hay duda sobre categoría, anotar como "verificar categoría".
- **Sin duplicados**: Mismo vendedor + mismo producto = reportar solo una vez.
- **Margen primero**: Si el producto no parece replicable con margen, ignorarlo.
