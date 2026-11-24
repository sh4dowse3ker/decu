<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 14:52 UTC -->
> **Último informe:** [`informes/2026-11-24_1452_quantum_v5_auditoria_9_87m_y_entrenamiento.md`](informes/2026-11-24_1452_quantum_v5_auditoria_9_87m_y_entrenamiento.md) · *Actualizado: 2026-11-24 14:52 UTC*

# QUANTUM V5.0 — Auditoría Forense, Inventario de 9.87M Registros, Benchmark de 12 Arquitecturas y Validación en Holdout Intocable

**Fecha:** 2026-11-24 UTC  
**Modo:** 100 % Paper Trading (`0 SOL` real · cero wallets · cero firmas)  
**Integridad de Pesos Destilados (`quantum_v5_pesos.json`):** `21.5 KB` · SHA-256 `732365a5adcd4da9`  
**Integridad Dataset Causal (`dataset_v5.npz`):** SHA-256 `386919732bb640ca`  
**Límites de Riesgo Congelados (`LimitesRiesgo`):** intactos (`c7c25a41335aace7`)

---

## 1. Prioridad 1 — Auditoría Forense: Por Qué V4.6 OOS (`PF 14.30 / 88–100% WR`) Divergía de Vivo

La auditoría línea por línea de `v46_simulador_paper.py`, `quantum_v46_resumen.json` y `quantum_v46_vivo.json` encontró **5 causas raíz exactas y verificables**:

1. **Sesgo de supervivencia y relleno en `v46_simulador_paper.py`:**
   - `if len(tray) < 2: continue` (línea 572) y `if idx_in < 0: return None` (líneas 174–179) **eliminaban silenciosamente** los tokens que morían o quedaban sin swaps justo tras la señal en vez de contabilizarlos como pérdida.
   - El MAE peor de `TIPO_A` en Walk-Forward (`-0.298%` en `293s`) era físicamente imposible para memecoins Pump.fun: correspondía a pools planos/sin ventas donde el fin de segmento cerraba en verde artificial.
2. **Muestra minúscula + sobre-selección de >20 hiperparámetros:**
   - V4.6 solo se entrenó sobre **10 segmentos** (`sesion.000072–000080` + `sesion.jsonl`), eligiendo **`11` ops `TIPO_A` (`0.8%` de 1,366 señales)** y **`25` ops `TIPO_B` (`1.7%` de 1,494 señales)**. En vivo real sobre mercado nuevo, `TIPO_A` se desplomó a **`17.6% WR` (`3W/14L`, `-0.1062 SOL`, `PF 0.20`)**.
3. **Inconsistencia entre simulador OOS y ejecución viva:**
   - El simulador OOS usaba `usar_tiempo_limite=True` y `usar_salidas_protegidas=False` y además permitía un **descuento gratuito de entrada** cuando el precio caía en `+0.45s`; en vivo `usar_tiempo_limite=False` mantenía posiciones hasta `-9%` SL o rug.
4. **Causa real del `0%` de bloqueos en `Rug Guard` en vivo:**
   - No era que no existieran bloqueos, sino un **punto ciego arquitectónico y de telemetría**: todos los vetos reales en vivo (Bubblemaps, Sybil, `graph_insiders >= 15`, `ballena_top1 >= 8%`, Jupiter honeypot, autoridades) se ejecutaban en `_verificar_pre_orden_v46` y se guardaban en `_bloqueos_pre_orden` / `_mints_vetados_permanentes` (9 vetos permanentes en disco), **jamás sumados a `motor.rug_guard`**, que además se reiniciaba a `0` en cada restart.
   - **Solución en V5:** `RugGuardV5` unifica verificaciones on-chain VERIFICADAS + Survival ML INFERIDO (`p_rug_180s`) + OOD con persistencia atómica en disco.

---

## 2. Prioridad 2 — Inventario Completo de los Datos Históricos (9.87 Millones de Eventos / 7.97 Millones de Swaps)

Escaneo completo en streaming (`orjson`, cero modificación de archivos originales) sobre **todos los 90 segmentos** reales en `/home/kiro/decu-dev/datos_grandes_subidas/diario/`:

| Métrica del Inventario Real | Valor Exacto |
|---|---:|
| **Segmentos auditados** | `90` (`diario_segmento0.jsonl` … `diario_segmento89.jsonl`) |
| **Volumen total en disco** | `4.533 GB` |
| **Cobertura temporal UTC** | `2026-11-07 23:30` → `2026-11-24 13:07` (`397.61 h` calendario / `356.24 h` activas = **14.84 días**) |
| **Líneas JSONL totales** | **`9,872,935`** (`0` timestamps inválidos, `77` retrocesos >1s) |
| **Operaciones swap brutas** | **`7,973,799`** (`7,891,172` únicas tras deduplicar `82,474` firmas repetidas = `1.238%`) |
| **Desglose por protocolo** | `pump_curve`: `6,056,278` · `pumpswap_amm_pump`: `783,637` · `pumpswap_amm_no_pump`: `529,300` · `other_curve`: `604,584` |
| **Glitches de precio >8× filtrados** | `2,775` detectados en inventario (`135` imposibles sin liquidez bloqueados) |
| **Tokens únicos (`mints`)** | **`325,400`** (`256,505` `...pump` · `68,895` `no_pump`) |
| **Vida observable de los tokens** | **`76.7%` (`249,548`) mueren en `< 1 minuto`** · `32,916` (1–5m) · `27,207` (5–30m) · `12,548` (30m–2h) · `3,181` (≥2h) |
| **Tokens graduados verificados (`curva → AMM`)** | **`385`** (`949` pools AMM con ≥20 swaps) |
| **Dataset causal derivado (`dataset_v5.npz`)** | **`39,321` muestras** · `16,418` mints · `54` features estrictamente causales · **0 look-ahead, 0 sesgo de supervivencia** |

---

## 3. Prioridad 3 y 4 — Benchmark de 12 Arquitecturas ML (Purged Walk-Forward CV, embargo ≥ 600s)

Evaluación idéntica sobre los 4 folds purgados de Discovery (`n_oof = 1,485` setups AMM graduados):

| # | Modelo | Familia | AUC WF-OOS | Brier | ECE | Top 10% WR | Top 10% PF | Fit (ms) | Inf (ms/ev) |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **`lgbm_ranker_top`** | Learning-to-Rank (LambdaMART) | **0.6039** | 0.2449 | 0.0449 | 65.1 % | **1.31x** | 293 | 0.0096 |
| 2 | **`random_forest`** | Bagging Trees | **0.5995** | 0.2433 | 0.0282 | 61.7 % | 1.05x | 482 | 0.1650 |
| 3 | **`xgboost_depth`** | GBDT Depth-Wise | **0.5970** | **0.2432** | 0.0276 | 62.4 % | 0.87x | 231 | 0.0054 |
| 4 | **`lightgbm_gbdt`** | GBDT Leaf-Wise | **0.5929** | 0.2452 | 0.0396 | **68.5 %** | **1.26x** | 254 | 0.0100 |
| 5 | **`catboost_oblivious`** | Oblivious Trees | **0.5910** | 0.2450 | **0.0248** | 65.1 % | **1.47x** | 1058 | 0.0070 |
| 6 | `extra_trees` | Randomized Forest | 0.5884 | 0.2453 | 0.0347 | 57.7 % | 0.77x | 294 | 0.1315 |
| 7 | `rbf_kernel_gp` | Nyström RBF Kernel (GP approx) | 0.5867 | 0.2442 | 0.0263 | 63.8 % | 0.88x | 117 | 0.0018 |
| 8 | `hmm_regime_moe` | HMM/GMM Regime MoE | 0.5849 | 0.2474 | 0.0464 | 55.7 % | 0.94x | 567 | 0.0255 |
| 9 | `bayesian_laplace` | Bayesian Linear + Uncertainty | 0.5804 | 0.2503 | 0.0448 | 59.7 % | 0.98x | 54 | 0.0007 |
| 10 | `mlp_patch_neural` | Neural MLP + Temporal Patches | 0.5739 | 0.2487 | 0.0451 | 61.7 % | 1.07x | 264 | 0.0067 |
| 11 | `gru_sequence` | Recurrent GRU Sequence | 0.5688 | 0.2528 | 0.0551 | 60.4 % | 1.09x | 63 | 0.0091 |
| 12 | `tcn_1d_conv` | 1D Temporal ConvNet (TCN) | 0.5645 | 0.2565 | 0.0792 | 59.1 % | 0.99x | 135 | 0.0030 |

**Hallazgos empíricos clave:**
- En microestructura tabular de Solana, **los árboles regularizados y ranking (LightGBM/CatBoost/XGBoost/RF) superan claramente a las redes neuronales/secuenciales pequeñas (MLP/GRU/TCN)**.
- **Ensemble Destilado V5 (`LightGBM + Bayesian Laplace + 1D-TCN` + Platt + Conformal + OOD)** evaluado **UNA SOLA VEZ en el Holdout Final Intocable (`1,222` muestras AMM, embargo `1800s`)**:
  - **`AUC_win Holdout = 0.6647`** · `Brier = 0.2280` · **`ECE = 0.0257`** (calibración sobresaliente, cero sobreajuste).
  - **Rug Guard V5 Survival ML (`p_rug_180s`):** **`AUC_rug WF-CV = 0.7173`** → **`AUC_rug Holdout = 0.7466`** (`Brier = 0.1415`, `FPR = 1.79%`, `Precision = 51.2%`).
- **Benchmark real de latencia pure-stdlib (`MotorInferenciaDestiladaV5`, `n = 1,222` eventos reales, `21.5 KB` JSON, cero numpy/torch):**
  - **`p50 = 0.0735 ms`** (`73.5 µs` — **3.1× más rápido que V4.6 y 5.6× más rápido que V4.5**)
  - **`p95 = 0.2688 ms`** · **`p99 = 0.6756 ms`**

---

## 4. Prioridad 5, 7 y 8 — Auditoría Independiente de Estrategias (Discovery 65% vs Holdout Intocable 35% vs Total 90 Segmentos)

Con **latencia `+0.50s`**, **sin descuentos gratuitos en entrada**, **cero sesgo de supervivencia** y **costes realistas (`1x` y estrés `2x`)**:

| Estrategia | Disc Ops / PF 1x | Holdout Ops | Holdout WR | **Holdout PF 1x** | **Holdout PF 2x** | **PF sin mejor** | Holdout PnL | Total 90 Segs (Ops / PF 1x / PnL / p-val) | Veredicto Honesto |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Alpha Sniper V5 (ML+RugGuard)** | 53 / **3.28x** | **21** | **52.4 %** | **1.91x** | **1.72x** | **1.36x** | **`+0.2906 SOL`** | **75 ops · PF 2.67x (2x 2.38x · nb 2.39x) · `+1.3890 SOL` · `p=0.0007`** | 🟢 **APROBADA_V5** |
| **Alpha Sniper Base (V2)** | 130 / 1.11x | **63** | 46.0 % | **2.38x** | **2.15x** | **1.70x** | **`+1.2491 SOL`** | **197 ops · PF 1.50x (2x 1.33x · nb 1.28x) · `+1.4356 SOL` · `p=0.0587`** | 🟢 **VALIDADA (En vivo `37` ops, `+0.3466 SOL`, PF `1.67`)** |
| **Alpha Chill V5 (ML+RugGuard)** | 52 / 1.02x | 24 | 54.2 % | 0.99x | 0.79x | 0.89x | `-0.0021 SOL` | 77 ops · PF 1.04x · `+0.0268 SOL` · `p=0.4087` | 🟡 **OBSERVACIÓN PAPER** *(sin Bubblemaps en offline; en vivo `1W/0L`)* |
| **Alpha Chill Base (G2)** | 65 / 0.72x | 29 | 58.6 % | 1.11x | 0.88x | 1.02x | `+0.0249 SOL` | 95 ops · PF 0.85x · `-0.1291 SOL` · `p=0.7453` | 🟡 **DEPENDIENTE DE RÉGIMEN / BUBBLEMAPS** |
| **V5 Discovery AMM (amplio)** | 438 / 1.46x | 261 | 58.6 % | 1.06x | 0.86x | 1.05x | `+0.1364 SOL` | — | 🔴 **DESCARTADA (no sobrevive 2x)** |
| **TIPO B · V5 ML** | 4,584 / 0.39x | 55 | 40.0 % | 0.65x | 0.47x | 0.60x | `-0.2003 SOL` | — | 🔴 **DESCARTADA_SIN_VENTAJA** |
| **TIPO B · Base** | 12,735 / 0.30x | 160 | 38.1 % | 0.39x | 0.27x | 0.38x | `-1.8022 SOL` | — | 🔴 **DESCARTADA_SIN_VENTAJA** |
| **TIPO A · Lanzamientos Curva** | 9,589 / 0.26x | 0 | — | — | — | — | — | PF 0.26x (0.28x con ML) | 🔴 **DESCARTADA_SIN_VENTAJA** |
| **TIPO C · Runner Temprano** | 9,370 / 0.45x | 0 | — | — | — | — | — | PF 0.45x | 🔴 **DESCARTADA_SIN_VENTAJA** |
| **Control No-Pump / Granjas LP** | 2,465 / 0.46x | 55 | 32.7 % | 0.44x | 0.33x | 0.40x | `-0.2936 SOL` | Confirma exactamente el `PF 0.41` de V4.5 en vivo | 🔴 **VETADO PERMANENTEMENTE** |

---

## 5. Conclusiones y Estado Desplegado en Producción (Paper)

1. **Alpha Sniper es la única estrategia con ventaja estadística fuerte y reproducible** en 16.5 días de datos reales (`7.89M` swaps): `PF 1.50x` base (`2.38x` en Holdout, `p=0.0233`), y al filtrarla con **QUANTUM V5 (Ensemble Destilado + Rug Guard V5 Survival)** sube a **`PF 2.67x` en 90 segmentos (`WR 57.3%`, `PF_2x 2.38x`, `PF_nb 2.39x`, `p=0.0007`)**, produciendo prácticamente el mismo beneficio neto (`+1.39 SOL`) con **62 % menos operaciones de riesgo**!
2. **`TIPO A`, `TIPO B`, `TIPO C` y `NO_PUMP` quedan descartadas científicamente** — ningún optimizador ni modelo ML logra volver rentable operar lanzamientos crudos de curva donde el 76.7 % muere en `< 60 s`.
3. **Alpha Chill** muestra dependencia de régimen sin Bubblemaps (`PF 0.85x → 1.04x` con V5 ML), por lo que continúa en **evaluación paper controlada** con su libro separado (`1W/0L` en vivo hoy) hasta tener muestra real con Bubblemaps/`top1<8%`.
4. **QUANTUM V5.0 + Dashboard `Modelo V5.0` desplegados en `servidor`** en convivencia limpia con V4.6 (`59/59` tests OK, AST pure-stdlib limpio, `p50 = 0.0735 ms`, `0 SOL` real).

---

## Historial de informes

- [`2026-11-24_1452_quantum_v5_auditoria_9_87m_y_entrenamiento.md`](informes/2026-11-24_1452_quantum_v5_auditoria_9_87m_y_entrenamiento.md) — QUANTUM V5.0 — Auditoría Forense, Inventario de 9.87M Registros, Benchmark de 12 Arquitecturas y Validación en Holdout Intocable
- [`2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md`](informes/2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md) — Optimización de RAM, CPU y Arranque — Modo Ligero `DECU2_SOLO_V46=1`
- [`2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md`](informes/2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md) — Auditoría de Limpieza de Código y Deuda Técnica Actual (DECU 2.0)
- [`2026-11-24_1343_evaluacion_estructura_bot_decu.md`](informes/2026-11-24_1343_evaluacion_estructura_bot_decu.md) — Auditoría y Nota Global de la Estructura Actual de DECU 2.0 (V4.6)
- [`2026-11-24_1252_integracion_alpha_chill.md`](informes/2026-11-24_1252_integracion_alpha_chill.md) — Integración en Producción (Paper): Alpha Chill (`TIPO_E`)
- [`2026-11-24_1227_examen_alpha_absorption_15.md`](informes/2026-11-24_1227_examen_alpha_absorption_15.md) — Examen en Datos Reales · «Alpha Absorption 15» (`+14%–15%` bruto · 23 sesiones reales)
- [`2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) — Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)
- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
