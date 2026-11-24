<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 18:37 UTC -->
> **Último informe:** [`informes/2026-11-24_1837_auditoria_paper_vs_mainnet_real.md`](informes/2026-11-24_1837_auditoria_paper_vs_mainnet_real.md) · *Actualizado: 2026-11-24 18:37 UTC*

# Auditoría Forense: Paper Trading vs Capital Real en Solana Mainnet (`60–80 €`)

**Fecha:** 2026-11-24  
**Objetivo:** Responder con datos reales si los beneficios del simulador Paper se mantienen al pasar a capital real (`60–80 €` ≈ `1.0–1.25 SOL`, órdenes de `0.14 SOL` ≈ `9 €`), inyectando las fricciones reales de Solana Mainnet tick a tick sobre **313 operaciones históricas reales (15 días, 92 segmentos)** y las **44 operaciones reales en vivo** de producción.

---

## 1. Conclusión Brutalmente Honesta

**No: con dinero real NO ganas lo mismo que en Paper.**  
Dependiendo de la calidad de tu ejecución y la congestión de la red Solana, en Mainnet retienes aproximadamente:

- **Escenario Mainnet realista** (`+1.5s` latencia real + Jito tip + reverts reales + `0.5%` MEV + cierre automático ATA): **`~69% – 88%`** del beneficio del Paper.
- **Escenario Mainnet estricto ("Ley de Murphy")** (nunca te favorece la latencia + `0.5%` MEV + reverts): **`~26% – 39%`** del beneficio del Paper.
- **Escenario congestión brutal** (`+2.5s` adverso + `1.0%` MEV + tips 2×): **V4.6 clásica y Alpha Chill entran en pérdidas**; **solo Quantum V5.0 Runner sobrevive en positivo (`PF 1.13x`)**.

> **Veredicto práctico:** Alpha Sniper (**V5.0 Runner** y **V4.6+Escudo**) **SÍ mantienen ventaja positiva en dinero real**, siempre que se ejecuten con **Jito + cierre automático de ATA + órdenes de `0.12–0.14 SOL`**. En cambio, **Alpha Chill (`TIPO_E`) NO tiene suficiente margen por operación** para sobrevivir a fricción estricta de Mainnet (`PF 0.91x`) y **no debería usarse con capital real**.

---

## 2. Qué cobra el Paper actual vs qué te cobra Solana Mainnet

| Fricción | Paper actual (producción) | Solana Mainnet real (`0.14 SOL/op`) |
|---|---|---|
| **Gas + Priority + Jito** | `0.00015 SOL/tx` (`0.0003/op`) | `0.00070 SOL/tx` (`0.0014–0.0021/op`, **5×–7× más**) |
| **Fee AMM PumpSwap** | `0.25%` por lado | `0.30%` por lado (`0.25%` LP + `0.05%` protocol) |
| **Latencia de inclusión** | `0.0s` (precio exacto de señal) | `+1.0s` a `+1.5s` normal (`+2.5s` en congestión) |
| **Reverts en compra** | `0` | **`16% – 19%`** de señales se escapan `> +3.5%` (pierdes priority fee y pierdes la entrada) |
| **Reverts en venta SL/Rug** | `0` | **`28 – 40`** reintentos en 15d (`+1.5s` extra cayendo + gas doble) |
| **MEV / Sandwich** | `0%` | `+0.5%` a `+1.0%` por lado si no usas Jito privado |
| **Alquiler cuenta ATA** | `0 SOL` | **`-0.002039 SOL` por token** si no cierras la cuenta al vender el 100% |

---

## 3. Simulación Tick a Tick en 15 Días Reales (`80 € = 1.25 SOL`, orden `0.14 SOL`)

Tipo de cambio de referencia: `1 SOL ≈ 64 €`.

### A) V4.6 Alpha Sniper + Escudo ML V5 (`143` ops · salida clásica)

| Escenario | Ejecutadas (revB / revS) | WR | PF (sin mejor) | PnL 15d | % del Paper | Fees fijos | Max DD |
|---|---:|---:|---:|---:|---:|---:|---:|
| **0. Paper actual** (`0s`, gas `0.00015`) | 143 (0 / 0) | 50.3% | 2.79x (2.18x) | **+2.674 SOL (+171 €)** | 100.0% | 0.051 | 19.2% |
| **1. Mainnet realista** (`+1.5s` real + Jito + reverts + `0.5%` MEV + ATA ok) | 120 (23 / 40) | 46.7% | 2.42x (1.94x) | **+2.589 SOL (+166 €)** | 96.8% | 0.221 | 14.5% |
| **2. Mainnet estricto** (`+1.5s` adverso + `0.5%` MEV + ATA ok) | 120 (23 / 40) | 45.0% | 1.49x (1.07x) | **+1.019 SOL (+65 €)** | 38.1% | 0.218 | 36.3% |
| **3. Mainnet estricto SIN cerrar ATA** | 120 (23 / 40) | 43.3% | 1.35x (0.96x) | **+0.774 SOL (+50 €)** | 28.9% | 0.462 | 41.2% |
| **4. Mainnet congestión brutal** (`+2.5s` adverso + `1.0%` MEV + tip 2×) | 114 (29 / 36) | 37.7% | **0.82x** (0.70x) | **-0.418 SOL (-27 €)** | -15.6% | 0.381 | 56.4% |

### B) Quantum V5.0 Sniper Runner (`75` ops · Moonbag `50%` / `4h`)

| Escenario | Ejecutadas (revB / revS) | WR | PF (sin mejor) | PnL 15d | % del Paper | Fees fijos | Max DD |
|---|---:|---:|---:|---:|---:|---:|---:|
| **0. Paper actual** (`0s`, gas `0.00015`) | 75 (0 / 0) | 57.3% | 3.69x (3.12x) | **+1.910 SOL (+122 €)** | 100.0% | 0.027 | 4.1% |
| **1. Mainnet realista** (`+1.5s` real + Jito + reverts + `0.5%` MEV + ATA ok) | 61 (14 / 28) | 50.8% | 2.58x (1.99x) | **+1.676 SOL (+107 €)** | 87.8% | 0.117 | 7.6% |
| **2. Mainnet estricto** (`+1.5s` adverso + `0.5%` MEV + ATA ok) | 61 (14 / 28) | 50.8% | 1.45x (1.11x) | **+0.490 SOL (+31 €)** | 25.6% | 0.115 | 20.9% |
| **3. Mainnet estricto SIN cerrar ATA** | 61 (14 / 28) | 47.5% | 1.31x (1.00x) | **+0.365 SOL (+23 €)** | 19.1% | 0.240 | 24.5% |
| **4. Mainnet congestión brutal** (`+2.5s` adverso + `1.0%` MEV + tip 2×) | 61 (14 / 25) | 44.3% | **1.13x** (0.84x) | **+0.157 SOL (+10 €)** | 8.2% | 0.211 | 27.7% |

> **Por qué V5.0 resiste mejor que V4.6 en dinero real:** hace la mitad de operaciones (`75` vs `143`), paga la mitad de gas/reverts (`0.117` vs `0.221 SOL`), tiene un **Drawdown casi a la mitad** (`7.6%–20.9%` vs `14.5%–36.3%`) y es la **única que aguanta en positivo en congestión extrema**.

### C) Alpha Chill (`TIPO_E`, `95` ops · entrada tranquila) — NO APTA PARA REAL

| Escenario | Ejecutadas | WR | PF (sin mejor) | PnL 15d | % del Paper | Max DD |
|---|---:|---:|---:|---:|---:|---:|
| **0. Paper actual** | 95 | 44.2% | 1.66x (1.23x) | +0.630 SOL (+40 €) | 100.0% | 13.2% |
| **1. Mainnet exacto** (`+1.5s` real + Jito) | 84 | 39.3% | 1.40x (1.02x) | +0.421 SOL (+27 €) | 66.8% | 22.7% |
| **2. Mainnet estricto** (`+1.5s` adverso + `0.5%` MEV) | 84 | 29.8% | **0.91x** (0.60x) | **-0.106 SOL (-7 €)** | -16.9% | 42.2% |
| **3. Mainnet estricto SIN cerrar ATA** | 84 | 28.6% | **0.80x** (0.51x) | **-0.278 SOL (-18 €)** | -44.0% | 52.7% |

---

## 4. Auditoría de las 44 Operaciones REALES en Vivo (`servidor`)

Sobre las **44 operaciones cerradas en vivo** de V4.6 Alpha Sniper (`operaciones_d`, `0.15 SOL/op`, `WR 43.2%`, `PF 1.73x`, `PnL +0.4290 SOL`), reescaladas a tu capital (`0.14 SOL/op`):

| Escenario sobre las 44 ops vivas | PnL neto | En euros | Profit Factor | % del Paper |
|---|---:|---:|---:|---:|
| **Paper vivo** (reescalado a `0.14 SOL`) | `+0.4004 SOL` | `+26 €` | `1.73x` | 100.0% |
| **Mainnet realista** (`+0.0014` gas Jito + `1.0%` MEV/latencia) | `+0.2772 SOL` | `+18 €` | `1.45x` | **69.2%** |
| **Mainnet estricto** (`+0.0014` gas Jito + `3.0%` fricción adversa) | `+0.1540 SOL` | `+10 €` | `1.22x` | **38.5%** |
| **Mainnet realista SIN cerrar ATA** (`-0.0897 SOL` perdidos en rent) | `+0.1875 SOL` | `+12 €` | `1.28x` | **46.8%** |

---

## 5. Tamaño de Orden Óptimo para `60–80 €` (`1.0–1.25 SOL`)

Bajo **Mainnet Estricto** (`+1.5s` adverso + `0.5%` MEV + Jito + ATA cerrado):

| Tamaño por orden | Gas fijo / orden | V4.6+Escudo (15d) | V5.0 Runner (15d) | Veredicto |
|---:|---:|---|---|---|
| `0.04 SOL` (`2.6 €`) | **3.50%** | `+0.144 SOL` (`+9 €`, PF `1.21x`, nb `0.85x`) | `+0.062 SOL` (`+4 €`, PF `1.17x`, nb `0.88x`) | **NO operar** (gas se come la ventaja) |
| `0.08 SOL` (`5.1 €`) | `1.75%` | `+0.499 SOL` (`+32 €`, PF `1.40x`, nb `1.00x`) | `+0.235 SOL` (`+15 €`, PF `1.36x`, nb `1.04x`) | Mínimo viable |
| **`0.14 SOL` (`9.0 €`)** | **`1.00%`** | **`+1.019 SOL` (`+65 €`, PF `1.49x`, nb `1.07x`, DD `36%`)** | **`+0.490 SOL` (`+31 €`, PF `1.45x`, nb `1.11x`, DD `21%`)** | **Punto dulce para `60–80 €`** |
| `0.25 SOL` (`16.0 €`) | `0.56%` | `+1.932 SOL` (`+124 €`, DD **`62.5%`**) | `+0.937 SOL` (`+60 €`, DD `26.6%`) | Demasiado riesgo por trade en `80 €` |

---

## 6. Las 4 Reglas Obligatorias Antes de Poner 1 € Real

1. **Cierre automático de ATA (`ata_manager.py`):** sin esto regalas `0.002039 SOL` por moneda (`~8–16 €` cada 15 días), suficiente para matar el Profit Factor sin el mejor trade.
2. **Jito bundles privados:** evitan los sandwich bots (`0.5%–1.0%` por lado) y aceleran la inclusión de SL/Rug para evitar el escenario de congestión `+2.5s`.
3. **Tamaño fijo `0.12–0.14 SOL` (`~8–9 €`) con máximo 2 posiciones simultáneas:** nunca bajar de `0.08 SOL` ni superar `0.16 SOL` con capital de `60–80 €`.
4. **Solo Alpha Sniper (`V5.0 Runner` prioritario, `V4.6+Escudo` secundario):** NO meter capital real en `Alpha Chill` (`TIPO_E`).

---

## Historial de informes

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
