# Examen en Datos Reales · «Alpha Absorption 15» (`+14%–15%` bruto · 23 sesiones reales)

> **Dataset:** 23 sesiones completas de PumpSwap (`38.11 h` = `1.59 días` · `2,55M` operaciones).
> **Reglas del examen:** latencia `+0.45 s` entrada y salida, fees reales `0.25%` por lado, slippage `x·y=k` + estrés `2×`, fills de TP capados (`≤ TP+3%`, cero inflación por glitches), 100 % rugs reales y 3 bloques cronológicos `Q12 / Q34 / NEW`.

---

## 1. Primera prueba (Propuesta original `P0` vs ajustes clave)

| Variante | Ops (`ops/día`) | WR | Gan. media | Pérd. media | Retorno | PF | PF (2×) | PF sin mejor | MaxDD | Dur. media | p-value | Bloques `Q12 / Q34 / NEW` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `P0` Propuesta original (`age ≥ 60s`, `v90`, `vol45`, `ofi ≥ 0.25`) | 34 (`21.4/d`) | 52.9% | +10.8% | -15.1% | **-47%** | 0.81 | 0.77 | 0.74 | 119% | 42 s | 0.614 | `0.31 / 0.93 / 1.32` ❌ |
| `P4` Sin filtro `ofi_10s` (`age ≥ 150s`, `v90`, `vol35`) | 50 (`31.5/d`) | 52.0% | +11.3% | -14.1% | **-45%** | 0.87 | 0.83 | 0.82 | 148% | 37 s | 0.593 | `0.97 / 0.58 / 1.37` ❌ |
| `P6` Usando `dd_a` (como Alpha Sniper) en vez de `dd_120s` | 58 (`36.5/d`) | 55.2% | +10.6% | -14.0% | **-24%** | 0.93 | 0.89 | 0.89 | 160% | 24 s | 0.557 | `0.76 / 0.64 / 1.73` ❌ |
| **`P2` Corregida con `age ≥ 150s` + `ofi ≥ 0.20` (`v90`, `vol45`, `dd120 ≤ -18%`)** | **37 (`23.3/d`)** | **62.2%** | **+10.0%** | **-9.9%** | **+91%** | **1.65** | **1.57** | **1.53** | **65%** | **41 s** | `0.094` | **`4.52 / 1.19 / 1.79` (3/3)** ⚠️ |
| **`P3` Relajada (`age ≥ 150s`, `v85`, `vol35`, `dd120 ≤ -15%`, `ofi ≥ 0.15`)** | **53 (`33.4/d`)** | **66.0%** | **+11.8%** | **-15.4%** | **+136%** | **1.49** | **1.43** | **1.43** | **114%** | **40 s** | `0.163` | **`3.52 / 1.12 / 1.80` (3/3)** ⚠️ |

### Hallazgos mecánicos clave
1. **Entrar antes de `150 s` (`P0`, `age ≥ 60s`) mata la estrategia (`PF 0.81`):** los primeros 2.5 minutos post-graduación siguen dominados por ventas de snipers de curva.
2. **La absorción real (`ofi_10s`) y la caída corta de 2 min (`dd_120s`) SÍ aportan señal propia:** quitar `ofi_10s` (`P4`) hunde el PF de `1.65` a `0.87`; cambiar `dd_120s` por `dd_a` (`P6`) lo hunde a `0.93`.

---

## 2. Auditoría de meseta (estabilidad de parámetros) y solape con `Alpha Sniper`

Se comprobó el porcentaje de operaciones que coinciden en el mismo minuto (`sameT`) con `Alpha Sniper` y si la estrategia aguanta al mover ligeramente los umbrales:

| Variante (`age ≥ 150s`, `had_cur = 1`, `reb120 ∈ [4%,12%]`, `sol ≤ 3.0`) | Ops (`ops/día`) | Solape `sameT` | WR | Retorno | PF | PF (2×) | PF sin mejor | MaxDD | p-value | `Q12 / Q34 / NEW` | Salidas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| `G1` `v75 · vol30 · dd15 · ofi15 · TP15` | 70 (`44/d`) | 24% | **67.1%** | +197% | 1.56 | 1.49 | 1.51 | 149% | 0.088 | `∞ / 0.91 / 1.96` | `37 TP · 16 BE · 16 SL · 1 RUG` |
| **`G2` `v80 · vol35 · dd15 · ofi15 · TP15`** | **63 (`39.6/d`)** | **22%** | **69.8%** | **+209%** | **1.71** | **1.63** | **1.65** | **114%** | `0.070` | **`∞ / 1.15 / 1.75` (3/3)** | **`34 TP · 17 BE · 11 SL · 1 RUG`** |
| `G3` `v85 · vol35 · dd15 · ofi15 · TP15` | 54 (`34/d`) | 13% | **64.8%** | +123% | 1.42 | 1.37 | 1.37 | 114% | 0.178 | `3.52 / 1.12 / 1.58` (3/3) | `27 TP · 14 BE · 12 SL · 1 RUG` |
| **`G5` `v90 · vol45 · dd18 · ofi20 · TP15`** | **38 (`23.9/d`)** | **11%** | **60.5%** | **+77%** | **1.51** | **1.44** | **1.40** | **65%** | `0.136` | **`4.52 / 1.19 / 1.44` (3/3)** | **`15 TP · 13 BE · 10 SL · 0 RUG`** |
| `G7` Igual `G5` con `TP 17%` | 38 (`23.9/d`) | 11% | 57.9% | +80% | 1.45 | 1.39 | 1.35 | 80% | 0.166 | `4.81 / 1.05 / 1.53` (3/3) | `14 TP · 13 BE · 11 SL` |
| `G8` `v85 · vol35 · dd15 · ofi20 · TP16` | 52 (`32.7/d`) | 10% | 53.8% | **-90%** | **0.76** | 0.73 | 0.71 | 137% | 0.726 | `0.63 / 0.64 / 1.02` ❌ | `17 TP · 18 BE · 16 SL · 1 RUG` |
| `G10` `v90 · vol40 · dd18 · ofi25 · TP15` | 37 (`23.3/d`) | 11% | 51.4% | **-75%** | **0.74** | 0.71 | 0.68 | 140% | 0.725 | `0.31 / 0.74 / 1.16` ❌ | `14 TP · 8 BE · 14 SL · 1 RUG` |
| `G11` Incluyendo `had_cur=0` (maduros) | 73 (`45.9/d`) | 5% | 54.8% | **-13%** | **0.97** | 0.93 | 0.93 | 81% | 0.546 | `0.90 / 0.84 / 1.30` ❌ | `25 TP · 23 BE · 25 SL` |

---

## 3. Veredicto científico honesto (**APROBADA CON RESERVAS — CANDIDATA A PRUEBA EN PAPER, NO A REAL**)

### Lo bueno (muy prometedor)
- **`G2` (`ofi ≥ 0.15`, `vSOL ≥ 80`, `vol60 ≥ 35`, `dd120 ≤ -15%`, `TP +15%`, `BE +8.5%→+4.5%`, `SL -10.5%`):**
  - **`69.8%` WR** (`51` verdes vs `12` rojas), **`+11.5%` ganancia media neta**, **`PF 1.71`**, **`PF sin mejor 1.65`**, **3/3 bloques en verde**, **duración media ~40 s** y **solo 22 % de solape temporal con `Alpha Sniper`**.
- **`G5` (`vSOL ≥ 90`, `vol60 ≥ 45`, `dd120 ≤ -18%`, `ofi ≥ 0.20`, `TP +15%`):**
  - Exactamente en tu objetivo de frecuencia (**`23.9 ops/día`**), **`60.5%` WR**, **`PF 1.51`**, **`MaxDD 65%`**, **`0` rugs** y **3/3 bloques en verde**, con solo **11 %** de solape temporal con `Alpha Sniper`.

### La advertencia obligatoria (por qué exige cautela)
1. **Sensibilidad a `ofi_10s`:** si subes demasiado `ofi_10s` (`≥ 0.25`, `G10`) o combinas `ofi ≥ 0.20` con `TP 16%` (`G8`), entras tarde en el rebote y el PF cae a `0.74–0.76`. La meseta ganadora vive claramente en **`ofi_10s ≥ 0.15` (`G1 / G2 / G3`: `PF 1.42 – 1.71`, `WR 64.8% – 69.8%`)**.
2. **Significancia estadística límite (`p = 0.070` en `G2`, `p = 0.136` en `G5`):** al ser muy selectiva, en `38 h` solo acumuló `38–63` operaciones, todavía insuficiente para alcanzar `p < 0.05` con certeza total.

### Recomendación
- **NO** meterla a dinero real todavía, pero **SÍ tiene muy buena pinta para validarla en vivo en PAPER** en un libro separado (p. ej. **`G2`** o **`G5`**) junto a `Alpha Sniper`, porque:
  - El **78%–89%** de sus entradas son en momentos distintos a `Alpha Sniper`.
  - Cierra en **~40 segundos** con **`60%–70%` WR** y **`+10%–11.5%` neto** (justo antes de los rugs).
  - En ~3–4 días de paper real sumará 100+ operaciones en vivo (con Bubblemaps + `top1 < 8%` activos) y sabremos con certeza si confirma el `65%–70%` WR.
