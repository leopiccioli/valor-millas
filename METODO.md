# Método

*English below.*

## Un solo número por canje

```
valor por punto (USD) = (precio cash del canje − tasas que se pagan igual al canjear) ÷ puntos necesarios
```

Se expresa en **centavos de dólar por punto** (¢). Un programa puede tener varias alternativas de canje; cada una tiene su número. La alternativa marcada como *referencia* es la de **máxima rotación**: lo que la mayoría de la gente canjea de verdad, no el mejor caso.

## Reglas

1. **Precio real de mercado, no precio de lista.** El "cash" es lo que pagarías hoy con tarjeta por el mismo producto, mismas fechas, misma cabina, en el sitio del proveedor o en Google Flights. Nunca el "antes" de un catálogo ni el precio de referencia que publica el programa.
2. **Producto de máxima rotación.** Para aerolíneas: ida y vuelta en turista a la ruta más común del mercado (desde Argentina: Miami para AA y United; una ciudad argentina para Aerolíneas). Para bancos y retail: el canje más líquido (crédito, cupón), no un producto.
3. **Se restan las tasas** que igual hay que pagar al canjear (tasas aeroportuarias, cargos). Si la tasa es estimada, la medición se marca `estimated: true` y se muestra así.
4. **Ventana fija y declarada.** Aerolíneas: martes a martes, ~5 meses adelante, fuera de temporada alta. Cada medición registra su ventana para que sea comparable.
5. **Dólar MEP** para convertir pesos (fuente: dolarapi.com). Se registra la cotización y la fecha.
6. **Toda medición tiene fuente, fecha y autor.** URL pública cuando existe; si el dato está detrás de login, se describe la ruta exacta dentro del sitio o app.
7. **Vencimiento.** Una medición de más de 90 días se marca *vencida* y deja de contar para la confianza. El número sigue visible, pero avisado.
8. **Confianza** = cantidad de autores distintos con mediciones vigentes para esa alternativa.
9. **Transferencias entre programas** se registran como tasa (`from_points` → `to_points`) y permiten calcular el valor "vía otro programa": `valor_vía_B = tasa × valor_de_B`.

## Qué NO hace este método

- No estima el "techo" (business a Europa, sweet spots). Eso lo hace [The Points Guy](https://thepointsguy.com/loyalty-programs/points-miles-valuations-methodology/) con millones de búsquedas y una fórmula no publicada.
- No descuenta riesgo de devaluación del programa ni costo de oportunidad (ver la [crítica de View from the Wing](https://viewfromthewing.com/why-the-points-guy-systematically-overstates-the-value-of-miles/)). Es un piso práctico, no un valor financiero.

## Diferencia con TPG en una frase

TPG mide cuánto pasaje *pueden* comprar las millas; esto mide cuánto compran en el canje que la gente *hace*, y muestra la cuenta.

---

# Method (English)

**One number per redemption:**

```
value per point (USD) = (cash price of the redemption − fees you still pay when redeeming) ÷ points required
```

Expressed in **US cents per point**. A program can have several redemption alternatives, each with its own number. The one marked *reference* is the **highest-turnover** redemption — what most people actually redeem for, not the best case.

Rules: real market price (what you'd pay today, same dates and cabin), not list price · highest-turnover product (round-trip economy on the market's most common route; most liquid redemption for banks/retail) · fees subtracted, estimates flagged · fixed, declared window (Tuesday to Tuesday, ~5 months out, off-peak) · ARS converted at the MEP rate · every measurement has source, date and author · measurements older than 90 days are flagged stale · confidence = number of distinct authors with current measurements · program-to-program transfers recorded as rates.

This is a practical floor, not a ceiling and not a financial valuation. TPG measures how much airfare miles *could* buy; this measures what they buy in the redemption people *actually make*, and shows the math.
