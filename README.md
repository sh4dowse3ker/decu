<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-25 14:39 UTC -->
> **Último informe:** [`informes/2026-11-25_1439_seguimiento_mainnet_v5_v6.md`](informes/2026-11-25_1439_seguimiento_mainnet_v5_v6.md) · *Actualizado: 2026-11-25 14:39 UTC*

# Seguimiento Mainnet Real (12h) · Quantum V5.0 + Quantum V6 Apex

- **Fecha UTC:** 2026-11-25 14:39 UTC
- **Modo:** 100 % Paper Trading con fricción real de Solana Mainnet (`0 SOL` real; cero carteras ni claves)

## 1. Salud de Infraestructura (`servidor`)

| Servicio | Estado | Notas |
|---|---|---|
| `decu2detector.service` | `active` | Uptime continuo desde `2026-11-24 18:04 UTC`, ingesta en vivo Pump.fun + PumpSwap |
| `decu2paper.service` | `active` | Reiniciado `14:38 UTC` tras fix V6 Apex (`bundle_slot0_curva`) + alertas Telegram V6 |
| `miapi.service` | `active` | Sirviendo `/api/v3/quantum-v6` y UI rediseñada (`/decu2-ui.js?v=65`) |
| `decu2telegram.service` | `active` | Alertas separadas V5.0 y V6 Apex verificadas (sin errores críticos en `journalctl`) |

## 2. Quantum V5.0 · `ALPHA_SNIPER` (Libro Principal)

| Métrica | Valor |
|---|---|
| Estrategias activas | `['ALPHA_SNIPER']` (`V4.6` apagada · `ALPHA_CHILL` apagada) |
| Capital inicial | `10.000000 SOL` |
| **Saldo actual** | **`10.117227 SOL`** (`+0.117227 SOL` / `+1.17%`) |
| Operaciones cerradas | `5` (`4W / 1L` · **WR `80.0%`**) |
| Profit Factor | **`3.989x`** |
| Max Drawdown | **`0.39%`** |
| Posiciones abiertas | `0` |
| RugGuard V5 | `10,671` evals · `10,648` bloqueadas · `52` mints en blacklist permanente |

## 3. Quantum V6 · Apex (Nuevo Modo · Saldo 100 % Aparte)

| Métrica | Valor |
|---|---|
| Modelo cargado | `V6.1` parsimonioso (`sha256=02572bf8fae9564e`) |
| Capital inicial separado | `10.000000 SOL` |
| **Saldo V6 actual** | **`10.000000 SOL`** (`+0.000000 SOL`) |
| Operaciones cerradas / abiertas | `0` cerradas / `0` abiertas |
| Latencia tick en vivo | `p50 = 21.46 µs` · `p95 = 55.42 µs` · `p99 = 97.85 µs` |
| Precalentador RugGuard V6 | `2` tareas lanzadas en 2º plano · `0 ms` de bloqueo en ruta caliente |

### Incidencia detectada y corregida en V6 Apex (`14:38 UTC`)
- **Motivo de 0 operaciones previas:** `bundle_slot0_curva(100%)` bloqueó `314 / 348` (`90.2%`) señales porque, tras reiniciar `decu2paper` con replay parcial de curva (`1–3` ticks), todo el volumen observado caía dentro de `<= 3s` (`slot0_frac = 1.0`).
- **Corrección desplegada:** exigir curva suficiente (`dna_curve_n >= 15` y `dur >= 15s`) para activar `slot0_frac`, relajar umbrales microestructurales para dips normales de Alpha Sniper (`max_sell_to_vsol 0.14→0.24`, `max_hawkes_blowup 0.16→0.40`), añadir cooldown anti-spam por mint y conectar las alertas de compra / TP1 / cierre de V6 Apex a Telegram con etiqueta propia `[Saldo Aparte]`.
- **Verificación offline en `sesion.jsonl` vivo (`56,099` eventos):** tras el parche, `0` falsos positivos `bundle_slot0_curva`, `16 / 21` candidatos aprobados, y notificaciones `entrada`, `parcial` y `cierre` disparadas correctamente.

---

## Historial de informes

- [`2026-11-25_1439_seguimiento_mainnet_v5_v6.md`](informes/2026-11-25_1439_seguimiento_mainnet_v5_v6.md) — Seguimiento Mainnet Real (12h) · Quantum V5.0 + Quantum V6 Apex
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
