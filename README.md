<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 13:43 UTC -->
> **Último informe:** [`informes/2026-11-24_1343_evaluacion_estructura_bot_decu.md`](informes/2026-11-24_1343_evaluacion_estructura_bot_decu.md) · *Actualizado: 2026-11-24 13:43 UTC*

# Auditoría y Nota Global de la Estructura Actual de DECU 2.0 (V4.6)

**Fecha:** 2026-11-24 UTC  
**Alcance:** Infraestructura (`servidor`), ingesta de datos, seguridad anti-rug, motor cuantitativo V4.6 (**Alpha Sniper** + **Alpha Chill**), observabilidad y preparación para dinero real.

---

## Nota Global Honesta

- **Como sistema actual de Paper Trading e I+D cuantitativo:** **8.4 / 10**
- **Como sistema listo para operar dinero real HOY:** **7.6 / 10** *(sube a ~9.0/10 en cuanto se completen las 100 ops en vivo por estrategia, se valide la ejecución real con micro-capital vía Jito y se pode el código legado inactivo).*

---

## Desglose por Pilares

| Pilar | Nota | Puntos fuertes actuales | Qué falta para un 9.5–10 |
|---|---:|---|---|
| **1. Ingesta y Arquitectura en Vivo** | **8.5 / 10** | 4 servicios `systemd` desacoplados (`detector`, `paper`, `miapi`, `telegram`), diario append-only `sesion.jsonl`, multi-fuente (Helius WS con rotación automática + PumpPortal + Radar), filtro anti-glitch y `prioridad.json` para posiciones abiertas. | En dinero real, sustituir RPC gratuitos/compartidos por RPC dedicado o gRPC/Yellowstone para eliminar picos de latencia y 429 en momentos calientes. |
| **2. Seguridad y Escudo Anti-Rug** | **8.8 / 10** | Muy superior al bot promedio de Pump.fun: autoridades nulas + Token-2022, Bubblemaps + Sybil/insiders (`>=15`), antiballenas `top1 externo < 8%` y `top10 < 50%`, **fail-closed** si cae RugCheck/Bubblemaps, **blacklist permanente en disco**, Jupiter anti-honeypot y `EARLY_EXIT_RUG` por drenaje de liquidez. | En dinero real, asegurar venta de emergencia con Jito bundle + priority fee dinámico y slippage de emergencia para que el `EARLY_EXIT_RUG` entre en el primer bloque disponible. |
| **3. Estrategias y Rigor Cuantitativo** | **8.0 / 10** | Disciplina real: se descartaron >15 estrategias con EV negativo sin sesgo de confirmación. Costes realistas + pruebas de estrés 2x + bloques cronológicos. Hoy operan 2 estrategias complementarias e **independientes**: **Alpha Sniper V2** (`36` ops en vivo, `+0.2853 SOL`, `PF 1.55`) y **Alpha Chill** (recién desplegada). | Completar la muestra mínima de **100 operaciones en vivo** para cada estrategia por separado y confirmar que el edge sobrevive al cambio de régimen de mercado (días lentos vs días calientes). |
| **4. Motor V4.6 y Simulación Paper** | **7.8 / 10** | 100 % stdlib puro (AST auditado), latencia sub-milisegundo (`p50 ~0.23 ms`), persistencia atómica JSON, libros `libro_d` y `libro_e` 100 % separados, huella congelada de `LimitesRiesgo` (`c7c25a41335aace7`) y `96/96` tests pasando. | Falta probar en fuego real el puente de ejecución on-chain (confirmación de tx, retries, fills parciales, slippage real vs simulado y reconciliación estricta del balance de la wallet). |
| **5. Limpieza del Código / Deuda Técnica** | **6.5 / 10** | El punto más mejorable: el repositorio conserva mucho código legado de V3/V4/V4.5 (copy-trade, supertrend, narrativas, pesca continua) que hoy corre en solo-lectura o desactivado con `DECU2_SOLO_V46=1`, añadiendo peso cognitivo y consumo base de RAM/CPU. | Tras validar Alpha Sniper y Alpha Chill en 100 ops, aislar/archivar el motor heredado para dejar un binario/servicio ultraligero exclusivo de V4.6. |
| **6. Observabilidad, Web, Telegram y GitHub** | **8.5 / 10** | Panel web en tiempo real con velas limpias (sin señales fantasma), tarjetas independientes para Alpha Sniper y Alpha Chill, cartera Phantom sincronizada en servidor, auditoría `X/100` desglosada, bot de Telegram con watchdog crítico y archivo automático de informes en GitHub cada 4h. | Añadir telemetría de slippage real vs estimado (fase dinero real) y panel de latencia de confirmación on-chain. |

---

## Diagnóstico Directo: ¿Qué es lo mejor y qué es lo único que frena el salto a real?

### Lo mejor del bot hoy
1. **No opera por intuición ni ruido:** solo quedan encendidas las dos únicas estrategias que pasaron el filtro duro de costes + bloques temporales, separadas entre sí.
2. **Escudo pre-orden a prueba de trampas conocidas:** ya demostró en vivo bloquear clusters Sybil, ballenas `>= 8%` y tokens con `>= 15` insiders (como el primer candidato de Alpha Chill `$PI`, bloqueado al instante).
3. **Resiliencia operativa:** 4 servicios aislados, reinicio limpio con persistencia de historial/vetos y monitorización 24/7 sin intervención manual.

### Los 3 pasos exactos para llevarlo de `7.6` a `9.0+` (listo para dinero real)
1. **Completar validación en vivo (`100 ops` en Alpha Sniper y `100 ops` en Alpha Chill)** sin tocar reglas en mitad de la prueba.
2. **Limpiar la deuda técnica heredada:** desacoplar el motor antiguo V4.5/V3 del bucle de `decu2paper` para bajar RAM, latencia y complejidad.
3. **Piloto en dinero real con micro-capital (`0.02 – 0.05 SOL/op`)** durante 30–50 ops solo para medir el **slippage real vs paper**, la tasa de fills de Jito y la reconciliación on-chain antes de escalar tamaño.

---

## Historial de informes

- [`2026-11-24_1343_evaluacion_estructura_bot_decu.md`](informes/2026-11-24_1343_evaluacion_estructura_bot_decu.md) — Auditoría y Nota Global de la Estructura Actual de DECU 2.0 (V4.6)
- [`2026-11-24_1252_integracion_alpha_chill.md`](informes/2026-11-24_1252_integracion_alpha_chill.md) — Integración en Producción (Paper): Alpha Chill (`TIPO_E`)
- [`2026-11-24_1227_examen_alpha_absorption_15.md`](informes/2026-11-24_1227_examen_alpha_absorption_15.md) — Examen en Datos Reales · «Alpha Absorption 15» (`+14%–15%` bruto · 23 sesiones reales)
- [`2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) — Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)
- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
