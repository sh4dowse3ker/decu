<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-25 05:08 UTC -->
> **Último informe:** [`informes/2026-11-25_0508_seguimiento_runner4h_mainnet.md`](informes/2026-11-25_0508_seguimiento_runner4h_mainnet.md) · *Actualizado: 2026-11-25 05:08 UTC*

# Seguimiento 12h · Mainnet Real Paper Trading (2026-11-25 05:08 UTC)

> **Modo estricto:** 100 % Paper Trading (`0 SOL` reales) · Perfil `mainnet_realista` (`+1,5s` latencia, Jito `0,0004` + Priority `0,0003` SOL/tx, PumpSwap `0,30%`, MEV `0,5%/lado`, reverts `>3,5%`, `0,14 SOL/op`).
> **Referencia de arranque limpio:** `2026-11-24 22:38 UTC` (`10,0000 SOL`, tras desactivar V4.6 a petición del usuario y dejar solo **Quantum V5.0** en vivo).

---

## 1. Salud del servidor (`servidor`)

| Componente | Estado | Detalle |
|---|---|---|
| `decu2detector.service` | `active` | 0 errores críticos (12h) · Flujo WS vivo (`2,2s` desde último evento) |
| `decu2paper.service` | `active` | 0 errores críticos (12h) · `350` tokens activos · `165.501` eventos V5 |
| `miapi.service` | `active` | 0 errores críticos (12h) |
| `decu2telegram.service` | `active` | 0 errores críticos (12h) · Parche `NoneType` + soporte V5 desplegado |

- **Inferencia ML V5.0:** `p50 = 0,138 ms`, `p95 = 0,264 ms`, `p99 = 0,443 ms` (`4.539` evaluaciones).
- **RugGuard V5.0:** `6.204` evaluaciones, `6.191` bloqueadas (`99,79%`), `26` mints en blacklist permanente, `14` vetos adicionales por ML.

---

## 2. Resultados separados desde el reset (`10,0000 SOL`)

| Modelo / Libro | Estado | Saldo actual | Ops | WR% | PnL Neto SOL | PF | MaxDD% | Abiertas |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Quantum V5.0 · `ALPHA_SNIPER`** | **ACTIVO** | **`10,1564 SOL`** | **4** (`4W/0L`) | **100,0%** | **`+0,1564 SOL`** (`~+10,0 €`) | **`99,0x`** | **`0,00%`** | `0` |
| **Quantum V5.0 · `ALPHA_CHILL`** *(control)* | ACTIVO *(solo control)* | `9,7951 SOL` | 5 (`1W/4L`) | 20,0% | `-0,2049 SOL` (`~-13,1 €`) | `0,08x` | `2,23%` | `0` |
| **V4.6 · Runner 4h (`libro_d`)** | **APAGADO** (`NINGUNO`) | `10,0000 SOL` | `0 / 100` | — | `+0,0000 SOL` | — | `0,00%` | `0` |
| **V4.6 · Alpha Chill (`libro_e`)** | **APAGADO** (`NINGUNO`) | `10,0000 SOL` | `0` | — | `+0,0000 SOL` | — | `0,00%` | `0` |

### Fricciones Mainnet Real registradas (V5.0)
- **Fills:** `9` entradas / `12` salidas (incluye tomas parciales TP1)
- **Reverts:** `1` compra / `5` venta (`gas_reverts = 0,0018 SOL`)
- **Gas tx total (Jito + Priority):** `0,0165 SOL`
- **Alquiler ATA ahorrado (cierre automático):** `0,018354 SOL` (`0,0000 SOL` perdido)
- **Drift medio de latencia en entrada (`+1,5s`):** `-1,72%`

---

## 3. Detalle de operaciones cerradas V5.0

### `ALPHA_SNIPER` (`4W / 0L` · Expectativa `+0,0391 SOL/op` · MAE peor `-3,6%`)

| Token | PnL Neto | Ret% | MFE | MAE | Salida | `p_win` / `p_rug` |
|---|---:|---:|---:|---:|---|---|
| `H9AtJUiD...` | `+0,0754 SOL` | `+53,9%` | `+252,8%` | `-1,4%` | `MOONBAG_TRAILING` | `0,60 / 0,33` |
| `$Manlet` | `+0,0449 SOL` | `+32,1%` | `+103,0%` | `-3,6%` | `MOONBAG_TRAILING` | `0,44 / 0,34` |
| `$Spurdo` | `+0,0255 SOL` | `+18,2%` | `+43,7%` | `-0,6%` | `BREAKEVEN_SL` | `0,53 / 0,34` |
| `$FUCKCANCER` | `+0,0107 SOL` | `+7,6%` | `+25,5%` | `-0,8%` | `BREAKEVEN_SL` | `0,59 / 0,33` |

### `ALPHA_CHILL` *(control · confirma predicción negativa del Lab V2 en Mainnet Real)*

| Token | PnL Neto | Ret% | MFE | MAE | Salida |
|---|---:|---:|---:|---:|---|
| `Ayp9p7nf...` | `+0,0177 SOL` | `+12,6%` | `+15,9%` | `0,0%` | `TP` |
| `$motion` | `-0,0166 SOL` | `-11,9%` | `+8,1%` | `-13,1%` | `SL` |
| `$Dlorga` | `-0,0183 SOL` | `-13,0%` | `+2,0%` | `-12,0%` | `SL` |
| `$Spurdo` | `-0,0476 SOL` | `-34,0%` | `+4,0%` | `-37,6%` | `SL` |
| `$SLITHEEN` | `-0,1401 SOL` | `-100,1%` | `0,0%` | `-99,7%` | `EARLY_EXIT_RUG` |

---

## 4. Lectura rápida
- **Señal muy positiva en `V5.0 ALPHA_SNIPER`:** `4/4` ganadoras (`+0,1564 SOL`, `0%` DD, MAE máximo de solo `-3,6%`), con dos runners que alcanzaron `+103%` y `+253%` MFE.
- **`ALPHA_CHILL` sigue confirmando lo previsto por el Laboratorio V2:** en Mainnet Real pierde dinero (`1W/4L`, `-0,2049 SOL`) y se comió un rug (`$SLITHEEN`) y una entrada tardía en `$Spurdo` donde `ALPHA_SNIPER` había ganado `+18,2%`. Como sus libros son 100 % independientes, no contamina la contabilidad de `ALPHA_SNIPER`, aunque conviene recordar que **nunca se activará con dinero real** (y si el usuario quiere apagar también `ALPHA_CHILL` en paper para ver el balance global limpio, se puede hacer en 10 segundos).
- Muestra todavía muy pequeña (`4` ops en `ALPHA_SNIPER`): seguimos dejando correr sin tocar producción hasta el veredicto del **8 de diciembre**.

---

## Historial de informes

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
