# Valor real de las millas

Cuánto vale, en dólares, cada milla o punto de los programas de fidelidad — con el cálculo a la vista y la fuente de cada número. Argentina primero; cualquier mercado después.

**Sitio:** https://leopiccioli.github.io/valor-millas
**Datos:** [`data/`](data/) (un JSON por programa) · índice calculado: [`data/index.json`](data/index.json)
**Método:** [METODO.md](METODO.md)

## Por qué existe

Las valuaciones conocidas (The Points Guy y similares) publican un número por programa sin mostrar rutas, fechas ni precios, y miden el *mejor* canje posible. Acá se mide el canje que la gente *hace*, con precio real de mercado, tasas restadas, fecha, fuente y autor. Y nadie cubre los programas argentinos (SuperClub+, Jumbo Más, Shell Box, Aerolíneas Plus).

## Cómo proponer una medición

Tres caminos, el primero no requiere saber nada de GitHub:

1. **[Abrir un issue con el formulario](../../issues/new?template=medicion.yml)** — programa, canje, precio cash, puntos, tasas, fecha, fuente. Se revisa y se incorpora.
2. **Pull request** editando el JSON del programa en `data/<mercado>/`. El CI valida el formato; al aprobarse se regenera el índice y el sitio.
3. **Vía MCP** (próximamente): una herramienta `propose` que abre el issue del punto 1 desde cualquier asistente de IA.

Lo que necesita toda medición: `date`, `cash` (monto, moneda, fuente), `points`, `fees` (monto, moneda; `estimated: true` si es aproximado), `fx` (cotización MEP y fecha), `author`. Ver un ejemplo en [`data/ar/aadvantage.json`](data/ar/aadvantage.json).

## Agregar un programa nuevo

Copiá cualquier archivo de `data/ar/`, cambiá `id` (= nombre del archivo), `name`, `unit` (`milla` o `punto`), `market` (código de país) y cargá al menos una alternativa con una medición. Corré `python3 scripts/build.py` para validar.

## Estructura

```
data/<mercado>/<programa>.json   mediciones crudas (lo que edita la gente)
data/index.json                  valores calculados (lo que lee el sitio y el MCP)
scripts/build.py                 valida y genera el índice
index.html                       sitio estático
METODO.md                        reglas de valuación
```

## Licencia

Datos y código: [CC0](https://creativecommons.org/publicdomain/zero/1.0/) — usalos como quieras, citar la fuente es bienvenido.
