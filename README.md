<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 12:03 UTC -->
> **Último informe:** [`informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) · *Actualizado: 2026-11-24 12:03 UTC*

# Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`

> **Modo:** 100 % Paper Trading (dinero ficticio) · **Repositorio de informes:** [`sh4dowse3ker/decu`](https://github.com/sh4dowse3ker/decu)

---

## 1. Idea A — Consolidación fuerte / Entrada temprana AMM (`30–145 s`, VWAP reclaim)

Evaluada sobre las **23 sesiones reales de PumpSwap (`38.9 h` · `2,55M` operaciones)** con latencia `+0.45 s` en entrada y salida, comisiones reales `0.25%` por lado, slippage `x·y=k` + estrés `2×`, 100 % rugs reales y `TP +16%` bruto (`~+13–14%` neto):

| Variante | Ops | WR | Retorno | PF | PF (2× slip) | p-value | Bloques `Q12 / Q34 / NEW` |
|---|---:|---:|---:|---:|---:|---:|---|
| `A1` Pullback suave (`-12..-4%`, `vSOL ≥ 90`) | 89 | 52.8% | **-267%** | 0.65 | 0.62 | 0.893 | `1.52 / 0.82 / 0.46` |
| `A2` Temprana `30–145 s` (`vSOL ≥ 75`) | 50 | 52.0% | +22% | 1.08 | 1.02 | 0.429 | `1.18 / 1.19 / 0.94` |
| `A3` Temprana `30–145 s` (`vSOL ≥ 90`) | 27 | 40.7% | **-119%** | 0.38 | 0.36 | 0.975 | `0.59 / 0.75 / 0.10` |
| `A4` VWAP reclaim (`vSOL ≥ 100`) | 63 | 41.3% | **-229%** | 0.61 | 0.58 | 0.943 | `0.41 / 0.50 / 0.88` |
| `A5` Consolidación `vSOL ≥ 120` | 105 | 38.1% | **-380%** | 0.53 | 0.51 | 0.995 | `0.29 / 0.89 / 0.39` |

- **Veredicto Idea A:** ❌ **Descartada.** 4 de 5 pierden fuerte y `A2` (`PF 1.08`, `p = 0.43`, `PF sin mejor 0.91`) es ruido estadístico.

---

## 2. Idea B — Supervivientes maduros AMM (`edad ≥ 5–15 min`, `vSOL ≥ 90–150`, `had_cur=0`)

Evaluada sobre las **23 sesiones reales** con fills de TP capados honestamente (sin inflación por saltos anómalos):

| Variante | Ops | WR | Retorno | PF | PF (2× slip) | PF sin mejor | p-value | Bloques `Q12 / Q34 / NEW` |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `B3` Maduros `had_cur=0` (`vSOL ≥ 90`, `TP 17%`) | 73 | 49.3% | +22% | 1.05 | 1.02 | 1.00 | 0.425 | `0.80 / 1.33 / 1.13` |
| `B5` Superviviente `≥5m`, `vSOL ≥ 120`, `dd60 ≤ -10%` | 87 | 56.3% | +106% | 1.23 | 1.20 | 1.19 | 0.200 | `1.61 / 1.23 / 1.00` |
| `B5b` Igual pero `vSOL ≥ 100` | 109 | 50.5% | **-6%** | 0.99 | 0.95 | 0.96 | 0.519 | `0.96 / 0.86 / 1.29` |
| `B5e` Igual pero `vSOL ≥ 150` | 65 | 50.8% | **-55%** | 0.86 | 0.84 | 0.81 | 0.698 | `0.70 / 1.44 / 0.40` |
| `B1b` Superviviente `≥10m`, `vSOL ≥ 100` | 98 | 52.0% | **-148%** | 0.80 | 0.78 | 0.77 | 0.756 | `1.85 / 0.70 / 0.56` |

- **Veredicto Idea B:** ❌ **Descartada.** No existe meseta robusta (`B5` cae a `PF 0.99` en `vSOL ≥ 100` y a `0.86` en `vSOL ≥ 150`, `p ≥ 0.20`).

---

## 3. Idea C — 11 monedas consolidadas reales de Solana (`0%` rugs · velas 1h · hasta 167 días)

Datos reales de Binance (`WIF`, `BONK`, `JUP`, `RAY`, `BOME`, `RENDER`, `ORCA`, `PNUT`, `ACT`, `FIDA`, `TNSR`; 9 de 11 cayeron `-10%` a `-46%` en el periodo). Entrada en apertura de la vela siguiente (cero lookahead), costes reales CEX `0.3%` / DEX `0.7%`:

| Estrategia (`+11% a +15%` neto objetivo) | Ops (ops/día) | WR | Retorno | PF (CEX) | PF (DEX) | MaxDD | p-value | Bloques `T1 / T2 / T3` |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`C1` Tendencia `>EMA200` + `RSI ≤ 35` (`TP 13.5% / SL 8%`)** | **30** (`0.18/d`) | **70.0%** | **+70%** | **2.05** | **1.82** | **25%** | `0.0527` | `0.18(5) / 13.4(17) / 0.60(8)` |
| `C4` Tendencia `EMA50>200` + Bollinger + `RSI ≤ 35` | 62 (`0.37/d`) | 59.7% | +72% | 1.43 | 1.26 | 61% | `0.1287` | `0.09 / 5.49 / 0.84` |
| `C5` Flush 48h `-12%` + rebote + volumen | 35 (`0.21/d`) | 60.0% | +10% | 1.08 | 0.96 | 41% | `0.4413` | `0.37 / 1.13 / 1.92` |
| `C3` Bollinger sobreventa en cualquier régimen | 116 (`0.70/d`) | 45.7% | **-151%** | 0.69 | 0.62 | 259% | `0.9633` | `1.04 / 2.41 / 0.40` |
| `C7` Ruptura 48h con volumen | 59 (`0.35/d`) | 42.4% | **-66%** | 0.75 | 0.68 | 145% | `0.8333` | `0.00 / 2.95 / 0.24` |
| `C12` Pullback a EMA50 en tendencia | 81 (`0.49/d`) | 43.2% | **-83%** | 0.74 | 0.66 | 145% | `0.8960` | `0.59 / 1.34 / 0.25` |

- **Veredicto Idea C:** ⚠️ **Solo rentable en fases alcistas y muy baja frecuencia (`~1 op cada 5 días`).**

---

## 4. Referencia validada — `Alpha Sniper V2` (Runner vs Modo "Poco a Poco" 65.1% WR)

Sobre la única entrada validada estadísticamente en las 23 sesiones (`...pump` graduado real `had_cur=1`, `vSOL ≥ 65`, `AMM ≥ 150s`, `dd ≤ -15%`, `reb ≥ +6%`, `vol60 ≥ 8`, `br60 ≤ 0.85` + escudo permanente Bubblemaps/Sybil y `top1 externo < 8%`):

| Perfil | Objetivo | Ops | WR | Retorno acum. | PF | PF sin mejor | MaxDD | p-value | Bloques `Q12 / Q34 / NEW` *(sin Bubblemaps)* |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Perfil A · Runner (ACTIVO HOY)** | `TP1 +40% · TP2 +160% · Moonbag -24% · BE +20%→+8%` | 126 | 48.4% | **+800%** | 1.58 | 1.39 | 361% | `0.0420` | `2.87 / 2.39 / 0.74` *(en vivo con Bubblemaps: `PF 1.39–1.68`)* |
| **Perfil B · Poco a Poco (`+17%` neto)** | `TP +20% · BE +10%→+5% · SL -12%` | 126 | **65.1%** | +404% | **1.61** | **1.53** | **109%** | **`0.0280`** | **`1.31 / 1.75 / 1.62` (3/3 verde)** |

## 5. Conclusión operativa
- **NO añadir Idea A ni Idea B** (carecen de ventaja estadística real).
- **Motor activo actual:** `Alpha Sniper V2` en paper hacia **`100 / 100`** operaciones reales (`33 / 100`, `+0.2003 SOL`, `PF 1.39`) con candado **`top1 externo < 8%`** y veto permanente de sybils/rugs.
- **Alternativas sólidas si se desea una 2.ª línea:** activar el **Perfil B ("Poco a Poco" `65.1%` WR · `TP +20%`)** en libro aparte para compararlo en vivo frente al Runner, o desarrollar en el futuro un módulo independiente de swing alcista (`C1`) en criptos grandes (`0%` rugs).

---

## Historial de informes

- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
