# Campaña de Descubrimiento Autónomo (7 Rondas · >16.130 Hipótesis): ¿Existe Otra Estrategia Rentable en Solana Mainnet Aparte de `Alpha Sniper`?

**Fecha:** 2026-11-24  
**Datos:** 15 días completos (`92` segmentos reales, `39,321` snapshots causales × `54` variables, ticks reales PumpSwap).  
**Disciplina anti-overfitting:** `TRAIN 60%` → `VAL 20%` → **Holdout Temporal Ciego `20%` sellado** + evaluación final tick a tick con fricciones reales de Solana Mainnet (`+1.5s`, reverts `>3.5%`, Jito `0.0007 SOL/tx`, PumpSwap `0.30%`, `0.5%` MEV, `0.14 SOL`).

---

## 1. Veredicto Honesto

Tras **7 rondas y más de `16.130` hipótesis distintas** (reglas humanas, evolución genética, árboles interpretables, LightGBM regularizado, estrategias anti-fricción y pre-graduación en curva):

1. **NO existe hoy en nuestros 15 días de datos on-chain otra estrategia diferente a `Alpha Sniper` que sobreviva a Solana Mainnet Real (`+1.5s`, Jito, MEV, reverts) y al Holdout Ciego (`20%`).**
2. **Por qué casi todas las demás mueren en Mainnet aunque ganen en Paper:**
   - **Perseguir momentum / rupturas (`S1–S4`)** ganaba `+0.58` a `+1.61 SOL` en Paper (`0s`), pero al inyectar `+1.5s` reales de bloque + `0.5%` MEV + gas Jito, el `WR` se desploma 10–12 puntos y todas entran en pérdidas o fallan en Holdout.
   - **Bonding curve / pre-graduación (`28,347` filas, `3,008` reglas):** incluso en `v_sol >= 65–70 SOL` la tasa de rug en 180s es del **`50%–58%`** y **`PF = 0.37x–0.53x`** (`0` supervivientes).
   - **LightGBM fuera de `Alpha Sniper`:** sacó `PF 2.44x–3.43x` en TRAIN y se hundió a **`PF 0.35x–0.65x`** en VAL (ruido puro).
3. **El gran hallazgo real de la campaña (dentro del núcleo que SÍ tiene ventaja estructural):**
   Combinar las **entradas de `V4.6 Alpha Sniper + Escudo ML` (`143` ops, sin recortar ganadores con `p_win >= 0.50`)** con la **salida `Runner 50% / 4h`** de V5.0 dispara el beneficio real en Mainnet **sin añadir complejidad ni sobreajuste**:
   - **Mainnet Realista:** **`+3.702 SOL (+237 €)`**, `PF 2.93x` (`nb 1.91x`), `p = 0.0155`, **Holdout Ciego `PF 4.52x` (`+2.450 SOL`)**.
   - **Mainnet Estricto (Ley de Murphy):** **`+2.137 SOL (+137 €)`**, `PF 1.97x` (`nb 1.08x`), **Holdout Ciego `PF 3.60x` (`+2.119 SOL`)** (**+117%** más que V4.6 clásica y **4.5×** más que V5.0).

---

## 2. Resumen de las 7 Rondas Ejecutadas

| Ronda | Universo y método | Hipótesis probadas | Supervivientes Mainnet + Holdout |
|---|---|---:|---:|
| **R1** | 10 familias humanas ortogonales en AMM (`PostMig`, `ATH Breakout`, `Squeeze`, `Phoenix`, `LiqGrowth`, `NonPump`, `Mature`, `LowTox`, `WhaleAbs`) | 120 | **0** |
| **R2** | Árbol interpretable (`depth=3`) + LightGBM regularizado en universo `0%` Alpha Sniper (`4,104` TR / `1,716` VA) | ML + 7 umbrales | **0** (`VAL PF 0.35x–0.65x`) |
| **R3–R4** | Búsqueda evolutiva (`2–4` condiciones limpias) + refinamiento de `Mature Trend Survivor` en `0%` Alpha Sniper | 13,000+ | **4** pasaron TR+VA (estrés 2×) → pasan a R5 |
| **R5** | **Examen Final tick a tick en Mainnet (`+1.5s`, Jito, MEV, reverts) + Holdout Ciego** sobre las 4 finalistas | 4 × 2 salidas × 4 escenarios | **0** aprobadas (`S1–S4` fallan en Mainnet/Holdout) |
| **R6** | 13 estrategias estructurales **anti-fricción** (dips/absorción sin perseguir velas verdes) directo en ticks reales `+1.5s` | 13 × 2 salidas | **0** aprobadas (`FE2` solo gana donde solapa 54% con Sniper) |
| **R7** | Bonding Curve / Pre-graduación (`es_amm=0`, `v_sol` 35–70) + Whale Pool `0%` Sniper | 3,008+ | **0** (`rug 50%–58%`, `PF 0.37x–0.53x`) |

---

## 3. Examen Final Tick a Tick en Solana Mainnet (`0.14 SOL/op`, 15 días + Holdout Ciego)

| Estrategia | Overlap Sniper | Paper (15d) | Mainnet Realista (`+1.5s`, Jito, `0.5%` MEV) | Mainnet Estricto (Ley de Murphy) | Holdout Ciego (20%) Realista | Veredicto |
|---|---:|---|---|---|---|---|
| **REF: V4.6 Sniper+Escudo (salida clásica)** | 100% | `+2.674 SOL` (PF 2.79x) | **`+2.589 SOL (+166 €)`** (PF `2.42x`, nb `1.94x`) | `+0.983 SOL (+63 €)` (PF `1.47x`) | **`+1.512 SOL` (PF `3.33x`)** | **APROBADA** |
| **HALLAZGO: V4.6 Sniper+Escudo + Salida Runner 4h** | 100% | `+4.224 SOL` (PF 3.83x) | **`+3.702 SOL (+237 €)`** (PF **`2.93x`**, nb `1.91x`) | **`+2.137 SOL (+137 €)`** (PF **`1.97x`**) | **`+2.450 SOL` (PF `4.52x`)** | **APROBADA (MEJOR)** |
| `S1_MATURE_SURVIVOR` (`age>=600, v_pk>=0.85, ret300>=15%`) | 38.3% | `+1.261 SOL` (PF 1.32x) | `-0.559 SOL (-36 €)` (PF `0.89x`) | `-1.735 SOL (-111 €)` (PF `0.66x`) | `-0.795 SOL` (PF `0.47x`) | **RECHAZADA** |
| `S2_MATURE_MIDCAP_WAKE` (`age>=600, v<=250, ret60>=4%`) | 50.7% | `+0.955 SOL` (PF 1.34x) | `-0.939 SOL (-60 €)` (PF `0.77x`) | `-1.956 SOL (-125 €)` (PF `0.54x`) | `-0.906 SOL` (PF `0.44x`) | **RECHAZADA** |
| `S3_CLEAN_TREND_REBOUND` (`ret300>=20%, reb>=6%, rug<0.30`) | 57.2% | `+1.609 SOL` (PF 1.64x) | `+0.945 SOL (+60 €)` (PF `1.36x`, `p=0.18`) | `-0.112 SOL (-7 €)` (PF `0.96x`) | `-0.191 SOL` (PF `0.71x`) | **RECHAZADA** |
| `S4_NON_PUMP_KING` (`!is_pump, age>=450, v_pk>=0.92`) | 0.0% | `+0.576 SOL` (PF 1.44x) | `+0.161 SOL (+10 €)` (PF `1.11x`, `p=0.39`) | `+0.089 SOL (+6 €)` (PF `1.07x`) | `-0.246 SOL` (PF `0.25x`) | **RECHAZADA** |

---

## 4. Conclusión Práctica

- **No merece la pena forzar una segunda estrategia artificial:** en memecoins de Solana con los datos on-chain actuales, la única ineficiencia que paga de sobra el peaje real de Mainnet (`+1.5s`, Jito, MEV, reverts) es el **rebote estructural post-graduación con Escudo ML (`Alpha Sniper`)**.
- **Para encontrar una segunda estrategia genuinamente distinta** haría falta una **fuente de información distinta** (por ejemplo: *tracking de carteras "smart money" históricamente rentables en Solana* — copy-alpha filtrado por Escudo ML — que no depende del patrón de precio de `Alpha Sniper`).
- Mientras tanto, **no tocamos producción durante las 2 semanas**; al finalizarlas, el hallazgo **`V4.6 Sniper+Escudo + Salida Runner 4h`** será el candidato nº 1 a validar para la siguiente versión.
