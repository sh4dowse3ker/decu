<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 13:54 UTC -->
> **Último informe:** [`informes/2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md`](informes/2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md) · *Actualizado: 2026-11-24 13:54 UTC*

# Auditoría de Limpieza de Código y Deuda Técnica Actual (DECU 2.0)

**Fecha:** 2026-11-24 UTC  
**Fuente:** Medición directa en el repositorio local (`/home/kiro/decu-dev/decu2-reconstruccion`) y telemetría en vivo en `servidor` (`ps`, `free -m`, `journalctl`).

---

## 1. Radiografía Real del Código Hoy

El repositorio suma **483 archivos Python (`129,491` líneas)** + **`5,241` líneas de frontend** (`decu2-ui.js`, `index.html`, `decu2.css`), ocupando **`1.5 GB`** en `servidor` (incluyendo estado/diarios).

Sin embargo, **menos del 18 % del código Python está realmente trabajando para las dos estrategias activas (`Alpha Sniper` y `Alpha Chill`)**:

| Bloque del código | Archivos | Líneas | % del Python | Estado real hoy |
|---|---:|---:|---:|---|
| **V4.6 Activo (`Alpha Sniper` + `Alpha Chill`)** | 9 | 7,851 | **6.1 %** | 🟢 Operando en vivo (y parte de V4.6 A/B/C sigue pausada dentro) |
| **Ingesta, seguridad y servicios core** | 20 | 9,747 | **7.5 %** | 🟢 Necesario (WS, RugGuard, Bubblemaps, Jupiter, paper_servicio) |
| **API Web + Telegram** | 6 | 4,617 | **3.6 %** | 🟢 Activo (con parches para convivir con datos heredados) |
| **QUANTUM V4.5 (legado)** | 11 | **26,731** | **20.6 %** | 🟡 **Apagado para operar, pero SIGUE ejecutándose en cada tick** |
| **Estrategias V3/V4 (legado)** | 25 | **9,695** | **7.5 %** | 🔴 Desactivadas (`copy_smart`, `supertrend`, `narrativas`, `mineros`, etc.) |
| **Otros heredados (`core/` v1, exploradores, `ops/`)** | 280 | **39,952** | **30.9 %** | 🔴 Código muerto / histórico de versiones previas |
| **Tests** | 132 | 30,898 | 23.9 % | 🟢 Suite de regresión (muchos tests de módulos ya retirados) |

Archivos monolíticos más grandes:
- `static/decu2-ui.js`: **`2,925` líneas** en un solo archivo.
- `decu2/lanzamientos/motor_quant_alpha_v46.py`: **`1,869` líneas**.
- `decu2/api_plataforma.py`: **`1,844` líneas**.
- `decu2/lanzamientos/pipeline_2b.py`: **`1,543` líneas**.
- `decu2/notificaciones/telegram.py`: **`1,170` líneas**.

---

## 2. Desventajas Reales que SÍ Está Produciendo Ahora Mismo

Estas no son teorías: son costes medidos hoy en producción (`servidor`):

### A. Consumo innecesario de CPU y RAM en `decu2paper` (el mayor impacto real)
Medición real de procesos en `servidor`:
- `decu2paper`: **`30.9 %` CPU constante** · **`281 MB` RAM** (`7` hilos)
- `decu2detector` (WebSockets Solana): **`9.1 %` CPU** · **`78 MB` RAM**
- `miapi` (Web/API): `0.3 %` CPU · `50 MB` RAM
- `decu2telegram`: `0.2 %` CPU · `32 MB` RAM
- **Memoria del VPS (`free -m`):** `3,819 MB` totales · `3,018 MB` usados · **`419 MB` ya en Swap** · solo `801 MB` libres.

**¿Por qué `decu2paper` gasta 3.5× más CPU y RAM que el propio detector WebSocket si Alpha Sniper y Alpha Chill solo hacen cálculos O(1) en `0.23 ms`?**
Porque en cada tick de `sesion.jsonl` sigue calculando trabajo que luego se descarta:
1. Todo `pipeline_2b.py` (`SmartMoney` con 2,783 votos SWI, `MetaBrain`, `EntryOptimizer`, `Supertrend`, `CopySmartWallet`, `PostMig`).
2. Todo `QUANTUM V4.5` (`26,731` líneas: Hawkes, VPIN, SSM, Conformal + pesos JSON) en modo solo-lectura.
3. Todo el motor ML de `V4.6 TIPO A/B` (42 features + 7 modelos) aunque `TIPO A`, `TIPO B` y `TIPO C` están pausados y **ni Alpha Sniper ni Alpha Chill los usan**.

Un motor limpio dedicado únicamente a `Alpha Sniper` + `Alpha Chill` bajaría `decu2paper` de **`31 % CPU / 281 MB RAM`** a **~`3–5 % CPU / 40–60 MB RAM`**.

### B. Riesgo de latencia (`lag`) en picos de mercado
En momentos de máxima actividad en PumpSwap (cientos de swaps/segundo), gastar `31 %` de CPU en modelos muertos alarga la cola de lectura de `sesion.jsonl`. En **dinero real**, unos pocos cientos de milisegundos de retraso empeoran el precio de entrada y pueden hacer que un `EARLY_EXIT_RUG` llegue un bloque tarde.

### C. Arranques lentos (`19 segundos` ciego al reiniciar)
En el reinicio de hoy (`12:51:25 -> 12:51:44`), `decu2paper` tardó **19 segundos** en cargar `V4.5`, SWI y reproducir el historial heredado antes de quedar operativo. En un motor limpio solo V4.6 arrancaría en **~1–2 segundos**.

### D. Bugs fantasma y contaminación visual/métrica
- Ya produjo bugs reales: hoy mismo hubo que limpiar señales fantasma `COMPRA` de `V4.5` que se pintaban sobre la gráfica en vivo (`3GZ4G2`) aunque `V4.5` no estaba comprando.
- Obligó a añadir lógica especial (`auditoria_paso_real`, `DECU2_SOLO_V46=1`) para que el histórico antiguo (`eventos_paper*.jsonl`, libros `A/B/C`) no contamine los contadores de `Alpha Sniper` y `Alpha Chill`.

### E. Velocidad de desarrollo y riesgo al tocar código
Para añadir una estrategia simple como **Alpha Chill** hubo que editar **9 archivos** grandes y coordinar 4 capas (motor, servicio, API, Telegram, UI monolítica). Cuanto más código muerto convive en el mismo flujo, mayor es el riesgo de regresiones involuntarias cuando se toque algo para dinero real.

---

## 3. Qué NO Está Roto (para no sobrerreaccionar)

- **No contamina los resultados actuales:** `libro_d` (Alpha Sniper) y `libro_e` (Alpha Chill) están 100 % aislados y verificados (`96/96` tests).
- **No está tirando el servidor:** los 4 servicios llevan horas estables (`active`), sin OOM ni errores en logs.

---

## 4. Plan Recomendado (Sin Prisas y Sin Romper la Prueba Actual)

1. **Ahora (en mitad de las 100 ops de validación):** NO tocar el núcleo de `decu2paper` salvo necesidad, para mantener limpia la muestra en vivo de `Alpha Sniper` y `Alpha Chill`.
2. **Al completar la validación (o si decides hacerlo en paralelo antes de dinero real):**
   - **Fase 1 (rápida, impacto inmediato en CPU/RAM):** añadir un modo `DECU2_V46_LIGERO=1` que salte `V4.5`, `pipeline_2b` heredado y los 7 modelos `TIPO A/B` cuando solo corran `TIPO_D`/`TIPO_E` (reduce ~80 % CPU y RAM sin borrar nada todavía).
   - **Fase 2 (antes de dinero real):** archivar `core/` v1, `V4.5` y estrategias retiradas fuera del paquete activo, y modularizar `decu2-ui.js` y `motor_quant_alpha_v46.py`.

---

## Historial de informes

- [`2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md`](informes/2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md) — Auditoría de Limpieza de Código y Deuda Técnica Actual (DECU 2.0)
- [`2026-11-24_1343_evaluacion_estructura_bot_decu.md`](informes/2026-11-24_1343_evaluacion_estructura_bot_decu.md) — Auditoría y Nota Global de la Estructura Actual de DECU 2.0 (V4.6)
- [`2026-11-24_1252_integracion_alpha_chill.md`](informes/2026-11-24_1252_integracion_alpha_chill.md) — Integración en Producción (Paper): Alpha Chill (`TIPO_E`)
- [`2026-11-24_1227_examen_alpha_absorption_15.md`](informes/2026-11-24_1227_examen_alpha_absorption_15.md) — Examen en Datos Reales · «Alpha Absorption 15» (`+14%–15%` bruto · 23 sesiones reales)
- [`2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) — Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)
- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
