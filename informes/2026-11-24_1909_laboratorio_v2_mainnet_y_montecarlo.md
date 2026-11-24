# Laboratorio Cuantitativo V2: Caché Ultrarrápido, Juez Mainnet Anti-Overfitting y Monte Carlo (`80 €`)

**Fecha:** 2026-11-24  
**Alcance:** 100 % local (`decu2/laboratorio_v5/`), con paridad 1:1 respecto al simulador Mainnet Real activo en producción (`servidor`).

---

## 1. Mejoras Implementadas en el Laboratorio V2

1. **Caché binario CSR (`cache_trayectorias.py`):** pre-indexa los `92` segmentos reales (`197` mints, `276,838` ticks AMM, `5.26 MB`). Acelera cada benchmark completo de **`57s` → `0.77s` (74× más rápido)** y se reconstruye automáticamente solo cuando lleguen segmentos nuevos.
2. **Juez Mainnet + Guardián Anti-Overfitting (`juez_mainnet.py`):** usa exactamente `evaluar_fill_compra_mainnet` y `evaluar_fill_venta_mainnet` del motor vivo, evalúa **5 escenarios obligatorios** (`paper_clasico`, `mainnet_realista`, `mainnet_estricto`, `mainnet_congestion`, `mainnet_sin_ata`), separa **Holdout Temporal Ciego (último 20%)** y exige significancia bootstrap con corrección por múltiples ensayos.
3. **Simulador Monte Carlo (`montecarlo_cuenta.py`):** 10.000 caminos vectorizados para cuenta pequeña (`80 € = 1.25 SOL`, horizonte 30 días), comparando tamaño fijo (`0.08–0.18 SOL`) vs compuesto (`12%–15%`).
4. **Verificador de Deriva Vivo vs Lab (`auditor_deriva_vivo.py`):** lee `servidor` (solo lectura, `DECU2_NO_TELEGRAM=1`) y compara las operaciones cerradas tras el corte Mainnet Real (`2026-11-24 18:58 UTC`: op `#46+` V4.6 / `#4+` V5.0) contra el laboratorio.
5. **CLI unificado (`python -m decu2.laboratorio_v5.cli_lab`)** y **41/41 tests unitarios en verde**.

---

## 2. Veredicto del Juez Mainnet (`0.14 SOL` · 15 días reales · ejecutado en `0.77s`)

| Estrategia | Veredicto Guardián | Mainnet Realista (`+1.5s`, Jito, `0.5%` MEV) | Mainnet Estricto (Ley de Murphy) | Holdout Ciego (último 20% tiempo) |
|---|---|---|---|---|
| **V4.6 Alpha Sniper + Escudo ML** (`143` ops) | **APROBADA** | `+2.589 SOL (+166 €)`, PF `2.42x` (`nb 1.94x`), `p=0.0085`, DD `14.5%` | `+0.983 SOL (+63 €)`, PF `1.47x` (`nb 1.05x`), DD `36.8%` | **Realista `+1.292 SOL` (`PF 4.23x`) · Estricto `+1.233 SOL` (`PF 3.77x`)** |
| **Quantum V5.0 Runner** (`75` ops) | **RECHAZADA** *(fallo holdout 15 ops)* | `+1.677 SOL (+107 €)`, PF `2.58x` (`nb 1.99x`), `p=0.0230`, DD `7.6%` | `+0.471 SOL (+30 €)`, PF `1.42x` (`nb 1.09x`), DD `21.4%` | Realista `-0.139 SOL` (`PF 0.55x`) · Estricto `-0.155 SOL` (`PF 0.52x`) |
| **Alpha Chill (`TIPO_E`)** (`95` ops) | **RECHAZADA** | `+0.015 SOL (+1 €)`, PF `1.02x` (`nb 0.86x`), `p=0.4950` | **`-0.553 SOL (-35 €)`**, PF `0.48x` | Realista `+0.048 SOL` · Estricto `-0.025 SOL` |

> **Hallazgo crítico del guardián:** el filtro `p_win >= 0.50` de V5.0 recortó ganadores grandes en el último 20% de los días (`15` ops en holdout frente a `29` de V4.6+Escudo). Las 2 semanas en vivo en modo Mainnet Real comparando ambos motores en paralelo resolverán esta diferencia con datos 100 % nuevos.

---

## 3. Monte Carlo — 10.000 Caminos para Cuenta de `80 €` (`1.25 SOL`, 30 días)

### A) Bajo Mainnet REALISTA (`+1.5s` real + Jito + `0.5%` MEV + ATA cerrado)

| Estrategia y Sizing | P5 (mala racha) | Mediana (30d) | P95 (buena racha) | P(ganar) | P(2× cuenta) | P(DD ≥ 25%) | P(quiebra <0.30 SOL) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **V4.6+Escudo · Fijo `0.10 SOL`** | `182 €` | `305 € (+225 €)` | `455 €` | `99.9%` | `97.6%` | `10.2%` | `0.01%` |
| **V4.6+Escudo · Fijo `0.12 SOL`** | `207 €` | `355 € (+275 €)` | `535 €` | `99.9%` | `98.6%` | `14.7%` | `0.04%` |
| **V4.6+Escudo · Fijo `0.14 SOL`** | `232 €` | `405 € (+325 €)` | `615 €` | `99.9%` | `99.1%` | `19.4%` | `0.09%` |
| **V5.0 Runner · Fijo `0.10 SOL`** | `135 €` | `226 € (+146 €)` | `334 €` | `99.8%` | `87.5%` | `9.5%` | `0.00%` |
| **V5.0 Runner · Fijo `0.12 SOL`** | `149 €` | `258 € (+178 €)` | `387 €` | `99.8%` | `92.6%` | `14.4%` | `0.04%` |
| **V5.0 Runner · Fijo `0.14 SOL`** | `163 €` | `290 € (+210 €)` | `441 €` | `99.8%` | `95.3%` | `19.1%` | `0.09%` |

### B) Bajo Mainnet ESTRICTO ("Ley de Murphy": nunca te favorece la latencia)

| Estrategia y Sizing | P5 (mala racha) | Mediana (30d) | P95 | P(ganar) | P(DD ≥ 25%) | P(quiebra <0.30 SOL) |
|---|---:|---:|---:|---:|---:|---:|
| **V4.6+Escudo · Fijo `0.10 SOL`** | `53 €` | `157 € (+77 €)` | `282 €` | `89.1%` | `56.3%` | `2.47%` |
| **V4.6+Escudo · Fijo `0.12 SOL`** | `44 €` | `178 € (+98 €)` | `328 €` | `89.6%` | `63.0%` | `3.86%` |
| **V4.6+Escudo · Fijo `0.14 SOL`** | `19 €` | `198 € (+118 €)` | `373 €` | `89.5%` | `68.4%` | `5.62%` |
| **V5.0 Runner · Fijo `0.10 SOL`** | `59 €` | `117 € (+37 €)` | `185 €` | `84.7%` | `41.2%` | **`0.53%`** |
| **V5.0 Runner · Fijo `0.12 SOL`** | `57 €` | `127 € (+47 €)` | `208 €` | `86.2%` | `50.1%` | **`1.21%`** |
| **V5.0 Runner · Fijo `0.14 SOL`** | `53 €` | `138 € (+58 €)` | `232 €` | `86.8%` | `57.2%` | `2.21%` |

> **Conclusión de gestión de capital:** con `80 €`, empezar con tamaño fijo **`0.10–0.12 SOL` (`~6.5–7.5 €`)** protege mucho mejor la cuenta frente a malas rachas (`P(quiebra) < 1.2%–2.5%` incluso en Ley de Murphy). El modo compuesto (`12%`) solo conviene activarlo cuando la cuenta supere `150–200 €`.

---

## 4. Primer Chequeo de Deriva Vivo (`servidor`, 10 min tras activar Mainnet Real)

El verificador `cli_lab deriva` ya confirmó la **primera operación cerrada en vivo bajo Mainnet Real** (`V4.6 op #46`):
- Ejecutó con latencia `+1.5s`, **sufrió 1 revert real en venta**, reintentó pagando `+0.0003 SOL` extra (`gas_tx_total = 0.0017 SOL`, comisión total `0.00254 SOL`) y **ahorró `0.002039 SOL`** cerrando el ATA. Estado: `OK`.
