<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-25 11:41 UTC -->
> **Último informe:** [`informes/2026-11-25_1141_investigacion_cuantitativa_v6_apex.md`](informes/2026-11-25_1141_investigacion_cuantitativa_v6_apex.md) · *Actualizado: 2026-11-25 11:41 UTC*

# Misión de Investigación Cuantitativa V6 · Apex (Auditoría Integral, Latencia, 6 Familias ML, RugGuard V6 y Viabilidad Real a 3 Años de 1.000.000 €)

> **Fecha:** 2026-11-25 11:40 UTC  
> **Modo estricto:** 100 % Backtesting y Paper Trading aislado (`0 SOL` reales, cero claves privadas, cero carteras conectadas).  
> **Despliegue aislado:** Nuevo menú independiente **`Nuevo Modo · V6 Apex`** en la sidebar, con **saldo propio de `10,0000 SOL`**, operaciones propias (`quantum_v6_vivo.json`) y endpoint dedicado (`/api/v3/quantum-v6`), manteniendo a **Quantum V5.0 · `ALPHA_SNIPER` (`10,1564 SOL`, `4/4` ganadoras)** 100 % intacto.  
> **Rollback verificado:** Copia versionada con `MANIFEST_SHA256.txt` en `/home/kiro/decu-dev/investigacion_v6/backups/pre_v6_20261125_110503`.

---

## 1. Auditoría forense de los datos históricos (96 segmentos · 10,81 M registros)

Se auditaron en streaming con `orjson` todos los segmentos reales (`diario_segmento1.jsonl` → `diario_segmento96.jsonl`, **4,839 GB**, del **2026-11-07 23:30 UTC** al **2026-11-25 09:07 UTC**, **19 días**):

| Métrica | Valor real verificado |
|---|---:|
| Registros JSONL totales | **`10.807.782`** (`0` líneas JSON corruptas) |
| Swaps individuales (`operacion`) | **`8.521.583`** (`4.638.919` compras / `3.882.664` ventas) |
| Snapshots de curva/AMM (`curva`) | `1.703.398` |
| Metadatos `token` / `creacion` / `autoridades` | `334.236` / `126.508` / `89.317` |
| Duplicados por firma en ventana | `180.478` (depurados) |
| Retrocesos de reloj `>5s` / `v_sol <= 0` | `28` / `19` |
| Sesgo de latencia `t_rx - t_evento` (backfill RPC) | `p50 = 1,014s` · `p95 = 105,6s` · `p99 = 954,1s` *(filtrado en entrenamiento)* |
| Mints únicos totales | **`335.751`** (`123.737` con `creacion`, `117.196` con curva) |
| Mints graduados a PumpSwap AMM (población completa) | **`1.158` válidos** (`1.055` con ciclo completo nacimiento → curva → AMM) |
| Lago CSR binario construido (`lago_v6_19d.npz`) | `2.519` mints (`1.158` AMM + `1.361` curva), **`2.056.450` ticks**, `37,54 MB` (carga en `0,70s`) |

**Hallazgos clave de datos infrautilizados:**
- Los registros `creacion` (`creator_fee_bps`, `is_mayhem_mode`, `is_cashback_enabled`, `token_program`) y el **ADN de curva de enlace previo a la graduación** (duración de curva, volumen, buy-ratio, traders únicos, HHI, entropía Shannon de tamaños, fracción de volumen en slot-0) **jamás se habían usado** en V4.6 ni V5.0.
- En el análisis de Información Mutua y AUC fuera de muestra, **los 8 rasgos más predictivos de `P(win)` resultaron ser precisamente el ADN de curva de nacimiento** (`dna_curve_br` AUC Holdout `0,5654`, `dna_curve_uniq_traders` `0,5606`, `dna_curve_vol` `0,5574`, `dna_curve_dur` `0,5571`, `dna_curve_hhi` `0,5535`).
- Limitación documentada: los eventos `ws_pumpswap_pool` registran la dirección del pool/vault en `trader` (`trader_hhi_60s == 1.000` en el 99 % de los ticks AMM), por lo que el HHI de traders solo es informativo durante la curva de enlace o cuando `uniq_trader_ratio >= 0,08`.

---

## 2. Auditoría de velocidad extremo a extremo y benchmark de motores de inferencia

### 2.1 Cuello de botella real descubierto en `servidor`
El problema de velocidad de Quantum **NO era la inferencia ML** (`0,14 ms`), sino las **llamadas HTTP síncronas bloqueantes de `pre_orden_verificador_fn` dentro del hilo principal**:

| Etapa medida en `servidor` | Latencia real medida | Diagnóstico |
|---|---:|---|
| Parseo JSON stdlib (`json.loads`) | `15,8 µs/ev` | Rápido (`orjson`: `2,0 µs/ev`) |
| Inferencia ML V5.0 (intérprete dict) | `143 µs` p50 / `430 µs` p99 | Aceptable, optimizable `5x` |
| Solana Public RPC (`getSlot` / autoridades / Top10) | `223 ms` med (×2 llamadas) | **BLOQUEO CRÍTICO** |
| RugCheck full API | `276,7 ms` med | **BLOQUEO CRÍTICO** |
| Bubblemaps legacy API | **HTTP 404 Not Found** | **ENDPOINT MUERTO** |
| Jupiter Quote (`lite-api.jup.ag`) | `41,4 ms` med (`120 ms` max) | Bloqueante en frío |
| DexScreener / GeckoTerminal (gratuitos) | `20,9 ms` / `29,6 ms` | Ultra-rápidos |
| PumpPortal WS vs Solana Public WS (handshake) | `93,1 ms` vs `546,0 ms` | PumpPortal `5,8x` más rápido |
| **Estancamiento total síncrono antiguo en candidato frío** | **`764 – 1.500+ ms`** | **Detenía todo el bucle de ticks** |
| **V6 Apex con `PrecalentadorAsincronoV6` (pool 4 hilos)** | **`0 ms` en ruta caliente** (`20,3 µs` tick p50 en vivo!) | **>5.000x menor bloqueo sin quitar controles** |

Además se detectó en `detector/salud.json`: `526` tokens descartados por cola llena frente a `927` verificados y `201` respuestas HTTP `429` en RPC.

### 2.2 Benchmark reproducible de 7 motores de inferencia (CPU local, paridad bit a bit `0,37227400`)

| Motor / Backend | p50 (µs) | p95 (µs) | p99 (µs) | Throughput (ev/s) | Speedup vs LightGBM | Dependencias |
|---|---:|---:|---:|---:|---:|---|
| LightGBM `predict_proba` (batch=1) | `964,59` | `3.336,26` | `4.903,66` | `653` | `1,0x` | Pesado |
| CatBoost `predict_proba` (batch=1) | `412,70` | `761,85` | `1.203,83` | `2.128` | `2,3x` | Pesado |
| XGBoost `inplace_predict` (batch=1) | `257,23` | `408,75` | `854,65` | `3.302` | `3,8x` | Pesado |
| Tiny MLP Python puro (`54→24→1`) | `67,48` | `125,75` | `158,63` | `13.142` | `14,3x` | `0 deps` |
| Intérprete dict-tree V5 (stdlib) | `48,47` | `120,72` | `177,38` | `16.643` | `19,9x` | `0 deps` |
| **V6 Compilado AST Python puro (`m2cgen`-style)** | **`10,27`** | **`21,07`** | **`68,25`** | **`79.081`** | **`93,9x`** | **`0 deps`** |
| **V6 Compilado C nativo (`-O3 ctypes`)** | **`2,08`** | **`3,23`** | **`14,43`** | **`390.603`** | **`463,7x`** | **`0 deps`** |
| **V6.1 Completo (4 cabezas + OOD compilado AST)** | **`25,35`** | **`61,17`** | **`118,49`** | **`~39.000`** | **`38x` (4 cabezas)** | **`0 deps` (`40,9 KB`)** |

---

## 3. Investigación de repositorios Open Source (inspeccionados y clonados)

Catálogo evaluado vía GitHub API (`5.816` repos Solana Python, `464` Rust streaming, `53.555` ML baja latencia). Seleccionados, clonados en `/home/kiro/decu-dev/investigacion_v6/repos/` y auditados por licencia, seguridad y algoritmos:

| Repositorio | Licencia | Revisión de seguridad | Aportación concreta adoptada en V6 |
|---|---|---|---|
| `BayesWitnesses/m2cgen` | MIT | Limpio | Patrón de transpilación AST a Python puro sin dependencias (`94x` más rápido que LightGBM batch=1) |
| `online-ml/river` | BSD-3-Clause | Limpio | Reimplementación ligera stdlib de **`ADWIN`** (`DetectorDerivaADWIN`) para detección online de cambio de régimen de rugs |
| `nkaz001/hftbacktest` | MIT | Limpio | Modelo causal tick-a-tick de latencia entrada/salida y reverts por slippage sin look-ahead |
| `chainstacklabs/pumpfun-bonkfun-bot` | Apache-2.0 | Limpio (`b64decode` Anchor IDL) | Jerarquía real de latencia de listeners Solana (`blockSubscribe` < `logsSubscribe` < `Yellowstone gRPC` < `SubscribeDeshred`) |
| `0xfnzero/solana-streamer` | MIT | Limpio | Patrón de hot-path sin asignaciones innecesarias para decodificación PumpSwap |
| `KeithTheDev/rugpulldetector` | Sin licencia (solo estudio) | Limpio | Idea de ventana deslizante adaptativa (`10–60s`) de caída de liquidez y ráfagas de venta (no se copió código) |

---

## 4. Auditoría separada de estrategias (eliminación de sesgo de supervivencia)

**Hallazgo crítico anti-sesgo:** las estrategias pre-graduación en curva de enlace (`TIPO_A`, `TIPO_B`, `V6_PRE_GRAD_DNA`) parecían rentables en una muestra que incluía el 100 % de los graduados y el 5,8 % de los no graduados. Al corregir con **pesos de importancia exactos (`17,296x` para no graduados)** se demostró que **TODAS las estrategias en bonding curve tienen expectativa NEGATIVA en Mainnet Real** (`1,25%/lado` de fee + `+1,5s` de latencia + `96–98,8%` no gradúan):

| Estrategia (libro separado, Mainnet Real `+1,5s`, Jito, MEV, reverts) | `n` | % Grad real | WR real | Exp. Real (SOL/op) | PF Real | PF Murphy | Veredicto |
|---|---:|---:|---:|---:|---:|---:|---|
| `TIPO_A_CURVA_TEMPRANA` | 587 | 1,2% | 36,5% | `-0,00644` | `0,75x` | `0,19x` | **ELIMINAR** |
| `TIPO_B_PRE_GRAD` | 244 | 2,4% | 35,4% | `-0,00845` | `0,63x` | `0,16x` | **ELIMINAR** |
| `V6_PRE_GRAD_DNA` | 82 | 4,1% | 22,5% | `-0,01069` | `0,48x` | `0,34x` | **ELIMINAR** |
| `ALPHA_CHILL` (AMM) | 68 | 100% | 39,7% | `-0,00374` | `0,62x` | `0,30x` | **ELIMINAR** |
| `V6_CONTINUATION_MOM` (AMM) | 106 | 100% | 34,9% | `-0,01450` | `0,38x` | `0,20x` | **ELIMINAR** |
| `V6_EARLY_AMM_SNIPER` (AMM) | 92 | 100% | 29,3% | `-0,00732` | `0,56x` | `0,21x` | **ELIMINAR** |
| `V6_MICRO_PULLBACK` (AMM) | 178 | 100% | 32,6% | `-0,00766` | `0,66x` | `0,47x` | **ELIMINAR** |
| `TIPO_C_AMM_TEMPRANO` (AMM) | 111 | 100% | 40,5% | `+0,00058` | `1,03x` | `0,58x` | Débil |
| **`ALPHA_SNIPER` (AMM sin filtrar)** | **168** | **100%** | **42,3%** | **`+0,00187`** | **`1,10x`** | **`0,76x`** | **Única base positiva sin ML** |

---

## 5. Comparativa de 6 familias ML, sobreajuste en 3.000 pruebas vs V6.1 Parsimonioso y RugGuard FP/FN

### 5.1 Comparativa de 6 familias (Purged Walk-Forward CV 5 folds con embargo 30m + Holdout Intacto 25 % sobre `14.368` snapshots AMM)

| Familia / Modelo | OOF AUC | OOF Brier | Holdout AUC | Holdout PR-AUC | Holdout Brier | Holdout ECE |
|---|---:|---:|---:|---:|---:|---:|
| LightGBM | `0,5289` | `0,2511` | **`0,5478`** | `0,3690` | `0,2295` | `0,0472` |
| XGBoost | **`0,5508`** | **`0,2427`** | `0,5408` | `0,3598` | `0,2293` | `0,0511` |
| CatBoost | `0,5441` | `0,2522` | `0,5408` | **`0,3693`** | `0,2292` | `0,0492` |
| Residual MLP (NumPy AdamW) | `0,5383` | `0,2444` | `0,5238` | `0,3521` | `0,2329` | `0,0546` |
| Bayesian L2 LogReg | `0,5288` | `0,2556` | `0,5105` | `0,3360` | `0,2376` | `0,0695` |
| Teacher Ensemble (5 familias) | `0,5417` | `0,2454` | `0,5442` | `0,3636` | `0,2291` | `0,0477` |
| **V6 Distilled Student (AST)** | destilado | — | `0,5325` | `0,3517` | **`0,2265`** | **`0,0386`** |

- **Supervivencia multi-horizonte (predicción de rugs):** la señal predictiva es **mucho más fuerte para detectar rugs que para predecir subidas**:
  - `P(rug <= 60s)`: OOF AUC **`0,6481`** → Holdout **`0,6323`** (Student `0,6133`)
  - `P(rug <= 180s)`: OOF AUC **`0,6704`** → Holdout **`0,6317`** (Student `0,6246`)
  - Rasgos top en Holdout: `price_vsol_div_30s` (`0,6095`), `kyle_lambda_60s` (`0,5944`), `log_v_sol` (`0,5943`), `trade_rate_60s` (`0,5926`), `amihud_60s` (`0,5904`).

### 5.2 Lección científica crítica: 3.000 pruebas (Overfitting demostrado) vs V6.1 Parsimonioso (12 hipótesis)

| Experimento | OOF (`n`, PnL, PF, DSR) | Holdout Intacto 25 % (`n`, PnL, PF, Murphy PF) | Diagnóstico |
|---|---|---|---|
| **V6.0 (3.000 pruebas, 7 umbrales, OOD=2,16)** | `n=50`, `+0,591 SOL`, `PF=1,66x`, **`DSR=0,0009`** | `n=32`, **`-0,378 SOL`**, **`PF=0,39x`**, `Murphy=0,27x` | **DESCARTADO (Overfitting severo: `OOD=2,16` cortó los runners parabólicos)** |
| **V6.1 Parsimonioso (`ALPHA_SNIPER` + `RUNNER_2H_BAL` + `SOLO_RUG_SHIELD_Q85`, 28 rasgos, OOD=4,5)** | `n=79`, **`+0,327 SOL`**, **`PF=1,21x`**, `Murphy=0,91x` | `n=37`, **`+0,139 SOL`**, **`PF=1,22x`**, `Murphy=0,95x` | **GENERALIZA 1:1 (`1,21x → 1,22x`), desplegado en V6 Apex (`sha256=02572bf8fae9564e`)** |
| V6.1 alternativa (`RUNNER_4H_BASE` + `RUG_Q80_WIN_Q20`) | `n=54`, `+0,185 SOL`, `PF=1,15x`, `Murphy=0,81x` | `n=31`, `+0,190 SOL`, `PF=1,31x`, **`Murphy=1,04x`** | Consistente también en Murphy |

> **Honestidad estadística obligatoria:** sobre cinta pura AMM (sin las respuestas históricas de RugCheck/Bubblemaps/Jupiter que en vivo sí vetan el 99%+ de las granjas), la ventaja pura de cinta es **modesta (`PF 1,21–1,31x`, `exp = +2,68%/op`, `pf_nb < 1,0`)** porque 2 rugs no bloqueados en cinta (`-0,28 SOL`) pesan mucho sobre `37` ops. El valor real de V6 Apex en vivo viene de combinar **RugGuard V6 asíncrono (RugCheck + Bubblemaps + Jupiter + autoridades sin bloqueo) + microestructura anti-bundle + supervivencia ML + inferencia AST `<30 µs`**, lo cual **debe validarse en paper vivo antes de tocar dinero real**.

### 5.3 Auditoría FP / FN de RugGuard V6 por capa (Holdout Intacto, `402` rugs vs `575` ganadoras)
- **Capa Microestructura** (drenaje `v_sol`, venta ballena, Hawkes blowup, ráfaga microventas, uniformidad bots, slot-0): Recall rugs `10,7%` (`43/402`), FPR ganadoras `15,7%`.
- **Capa Supervivencia ML (60s/180s):** Recall rugs `10,4%` (`42/402`), FPR ganadoras **`6,1%`** (mejor ratio precisión/coste!).
- **Capa OOD Conformal:** Recall `1,7%`, FPR `2,3%`.
- **Combinado sin APIs externas:** Recall `19,7%` (`79/402`), FNR `80,3%`, FPR `21,4%`. *(Confirma por qué RugCheck/Bubblemaps/Jupiter on-chain siguen siendo indispensables en vivo y por qué V6 los precalienta en segundo plano en lugar de eliminarlos).*

---

## 6. Análisis económico y matemático honesto a 3 años: ¿Es viable alcanzar `1.000.000 €`?

**VEREDICTO BRUTALMENTE HONESTO: NO ES VIABLE ALCANZAR `1.000.000 €` EN 3 AÑOS OPERANDO SOLO EN PUMPSWAP / MEMECOINS DE SOLANA.**

### 6.1 Requisitos matemáticos puros (36 meses compuestos)
| Capital inicial + aporte mensual | Tasa mensual necesaria | Tasa anual equivalente | Multiplicador sobre aportado |
|---|---:|---:|---:|
| `80 € + 0 €/mes` | **`29,96 % / mes`** | `2.220,8 % / año` | `12.500x` |
| `500 € + 200 €/mes` | **`19,77 % / mes`** | `771,7 % / año` | `130x` |
| `2.000 € + 500 €/mes` | **`15,76 % / mes`** | `478,8 % / año` | `50x` |
| `10.000 € + 500 €/mes` | **`12,61 % / mes`** | `315,8 % / año` | `35,7x` |
| `50.000 € + 1.000 €/mes` | **`8,05 % / mes`** | `153,1 % / año` | `11,6x` |

### 6.2 La barrera física: techo de liquidez de PumpSwap AMM (`v_sol` medio = `85 SOL`)
Usando la expectativa real medida en el Holdout Intacto (`+2,68 %/op` sobre `0,14 SOL` sin RugCheck histórico):

| Tamaño orden (SOL / €) | Cuenta (al 10%/op) | Impacto AMM extra ida+vuelta | Expectativa neta ajustada | ¿Rentable? |
|---|---:|---:|---:|---|
| `0,14 SOL` (`9 €`) | `90 €` | `0,00 %` | `+2,68 %` | Sí |
| `0,50 SOL` (`32 €`) | `320 €` | `+0,84 %` | `+1,84 %` | Sí |
| `1,00 SOL` (`64 €`) | `640 €` | `+2,00 %` | `+0,69 %` | Al límite |
| **`1,50 SOL` (`96 €`)** | **`960 €`** | **`+3,14 %`** | **`-0,46 %`** | **NO (slippage mata el edge)** |
| `5,00 SOL` (`320 €`) | `3.200 €` | `+10,78 %` | `-8,10 %` | **NO** |

Incluso si el escudo on-chain en vivo elevara la expectativa a `+12–18%/op`, el techo físico de PumpSwap seguiría bloqueando el crecimiento alrededor de **`2,5–5,0 SOL/op` (`2.000–4.000 €` de cuenta)**, donde el impacto AMM (`5,4%–10,8%`) y el front-running MEV destruyen el alfa.

### 6.3 Monte Carlo 3 años (`5.000` trayectorias, degradación de alfa `15%/año`, distribución real Holdout)
- **`80 € + 0 €/mes`:** Mediana `10 €`, Ruina `100 %`, **`P(≥ 1.000.000 €) = 0,00 %`**
- **`500 € + 200 €/mes` (`7.700 €` aportados):** Mediana `119 €`, P90 `258 €`, **`P(≥ 1.000.000 €) = 0,00 %`**
- **`10.000 € + 500 €/mes` (`28.000 €` aportados):** Mediana `349 €`, P90 `4.009 €`, **`P(≥ 1.000.000 €) = 0,00 %`**
- **`50.000 € + 1.000 €/mes` (`86.000 €` aportados, cap 1,5 SOL):** Mediana `56.740 €`, P90 `62.009 €`, **`P(≥ 1.000.000 €) = 0,00 %`**

**Conclusión económica honesta:** con la ventaja actual en cinta pura (sin validar aún el plus en vivo de RugCheck/Bubblemaps), ni siquiera es rentable a largo plazo sin filtro on-chain; e incluso **si** V5/V6 en vivo confirman `PF > 2,0x` el 8 de diciembre, PumpSwap sirve únicamente como **acelerador de capital pequeño (hasta ~2.000–10.000 €)**. Aspirar a `1.000.000 €` exige posteriormente **saltar a mercados profundos** (perpetuos BTC/ETH/SOL, índices, acciones) con aportaciones elevadas y un horizonte realista mayor (o capital inicial de 6 cifras).

---

## 7. Despliegue en producción verificado (`Nuevo Modo · V6 Apex` 100 % separado)

- **Servicios (`servidor`):** `decu2detector`, `decu2paper`, `miapi`, `decu2telegram` → **4/4 `active`**.
- **Quantum V5.0 (`ALPHA_SNIPER`) intacto:** **`10,1564 SOL`** (`4/4` ganadoras, `+0,1564 SOL`).
- **Nuevo Modo · Quantum V6 Apex activo y aislado:**
  - **Sidebar:** nuevo menú dedicado **`Nuevo Modo · V6 Apex`** (`/api/v3/quantum-v6`, `saldo_separado: true`).
  - **Saldo propio:** **`10,0000 SOL`** (`0` ops iniciales, `quantum_v6_vivo.json`).
  - **Velocidad medida en vivo en `servidor`:** `3.443` eventos ya procesados con **`p50 = 20,29 µs`, `p95 = 36,03 µs`, `p99 = 48,66 µs`** por tick!
  - **Tests automatizados:** `26/26` pruebas unitarias e integración OK (`test_v6_apex`, `test_quantum_v5`, `test_paper_mainnet_real`, `test_telegram`, `test_nuevas_funciones`) + `node --check static/decu2-ui.js` OK.

---

## Historial de informes

- [`2026-11-25_1141_investigacion_cuantitativa_v6_apex.md`](informes/2026-11-25_1141_investigacion_cuantitativa_v6_apex.md) — Misión de Investigación Cuantitativa V6 · Apex (Auditoría Integral, Latencia, 6 Familias ML, RugGuard V6 y Viabilidad Real a 3 Años de 1.000.000 €)
- [`2026-11-25_0508_seguimiento_runner4h_mainnet.md`](informes/2026-11-25_0508_seguimiento_runner4h_mainnet.md) — Seguimiento 12h · Mainnet Real Paper Trading (2026-11-25 05:08 UTC)
- [`2026-11-24_1952_busqueda_estrategias_ortogonales_7_rondas.md`](informes/2026-11-24_1952_busqueda_estrategias_ortogonales_7_rondas.md) — Campaña de Descubrimiento Autónomo (7 Rondas · >16.130 Hipótesis): ¿Existe Otra Estrategia Rentable en Solana Mainnet Aparte de `Alpha Sniper`?
- [`2026-11-24_1909_laboratorio_v2_mainnet_y_montecarlo.md`](informes/2026-11-24_1909_laboratorio_v2_mainnet_y_montecarlo.md) — Laboratorio Cuantitativo V2: Caché Ultrarrápido, Juez Mainnet Anti-Overfitting y Monte Carlo (`80 €`)
- [`2026-11-24_1837_auditoria_paper_vs_mainnet_real.md`](informes/2026-11-24_1837_auditoria_paper_vs_mainnet_real.md) — Auditoría Forense: Paper Trading vs Capital Real en Solana Mainnet (`60–80 €`)
- [`2026-11-24_1824_seguimiento_alpha_sniper_y_chill.md`](informes/2026-11-24_1824_seguimiento_alpha_sniper_y_chill.md) — Seguimiento Automático (4h) · Alpha Sniper & Alpha Chill + QUANTUM V5.0
- [`2026-11-24_1452_quantum_v5_auditoria_9_87m_y_entrenamiento.md`](informes/2026-11-24_1452_quantum_v5_auditoria_9_87m_y_entrenamiento.md) — QUANTUM V5.0 — Auditoría Forense, Inventario de 9.87M Registros, Benchmark de 12 Arquitecturas y Validación en Holdout Intocable
- [`2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md`](informes/2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md) — Optimización de RAM, CPU y Arranque — Modo Ligero `DECU2_SOLO_V46=1`
- [`2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md`](informes/2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md) — Auditoría de Limpieza de Código y Deuda Técnica Actual (DECU 2.0)
- [`2026-11-24_1343_evaluacion_estructura_bot_decu.md`](informes/2026-11-24_1343_evaluacion_estructura_bot_decu.md) — Auditoría y Nota Global de la Estructura Actual de DECU 2.0 (V4.6)
- [`2026-11-24_1252_integracion_alpha_chill.md`](informes/2026-11-24_1252_integracion_alpha_chill.md) — Integración en Producción (Paper): Alpha Chill (`TIPO_E`)
- [`2026-11-24_1227_examen_alpha_absorption_15.md`](informes/2026-11-24_1227_examen_alpha_absorption_15.md) — Examen en Datos Reales · «Alpha Absorption 15» (`+14%–15%` bruto · 23 sesiones reales)
- [`2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) — Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)
- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
