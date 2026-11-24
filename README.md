<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 14:03 UTC -->
> **Último informe:** [`informes/2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md`](informes/2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md) · *Actualizado: 2026-11-24 14:03 UTC*

# Optimización de RAM, CPU y Arranque — Modo Ligero `DECU2_SOLO_V46=1`

**Fecha:** 2026-11-24 UTC  
**Objetivo:** Eliminar todo lo que consumía RAM y CPU en `decu2paper` sin usarse, manteniendo 100 % operativas **Alpha Sniper (`TIPO_D`)**, **Alpha Chill (`TIPO_E`)**, la gráfica de velas en vivo, el panel web y Telegram.

---

## 1. ¿Por qué QUANTUM 4.5 no opera? (100 % normal e intencionado)

- En la auditoría sobre datos reales de `servidor`, **QUANTUM V4.5** dio **`PF 0.41`** (perdía dinero al entrar en granjas LP `no-pump`, incluyendo un rug del `-100%` en 16 segundos).
- Por eso se desactivaron sus entradas con `DECU2_SOLO_V46=1`, dejando operando únicamente las estrategias validadas de V4.6 (**Alpha Sniper** y **Alpha Chill**).
- Con esta optimización, **V4.5 ya ni siquiera se carga en RAM** ni procesa ticks en segundo plano (`0 MB` de RAM, `0 %` de CPU). Sus archivos de respaldo permanecen intactos en disco únicamente para compatibilidad de tests y rollback seguro.

---

## 2. Qué se ha desconectado de la RAM y del bucle en vivo

1. **`QUANTUM V4.5` apagado por completo en `DECU2_SOLO_V46=1`:** no carga `quantum_v45_pesos.json` ni ejecuta Hawkes / VPIN / SSM / Conformal / 450 estados.
2. **Modelos ML de `V4.6 TIPO A/B/C` saltados automáticamente** cuando solo corren `TIPO_D` y `TIPO_E`: no carga `quantum_v46_pesos.json` ni extrae 42 features + 7 modelos en cada swap (solo estado causal O(1) para `...pump` + comprobación de autoridades).
3. **`Pipeline2B` legado desconectado en cada swap (`puente_vivo.py`):** no ejecuta `MetaBrain`, `SmartMoney` (`2,783` votos SWI), `CopySmartWallet` (`cargar_elite` cada 30s), `EntryOptimizer`, `PostMig` (hilo de fondo eliminado) ni estrategias retiradas V3/V4. Solo alimenta precio/liquidez y las velas 5s del panel web.
4. **Cachés acotadas en memoria:**
   - `RegistroTokens`: `1500` → `350` tokens (`max_serie`: `1000` → `240`).
   - Velas `MotorSupertrendEstructura`: `3000` → `200` mints más activos.
   - `_alpha_sniper_estados`: `4000` → `1200` mints `...pump`.
   - `max_bytes_arranque`: `4 MB` → `2 MB` + `gc.collect()` tras warm-up.
   - `live_chart.json`: escritura cada `1.0s` en vez de `0.45s` + autofoco automático en posiciones abiertas de Alpha Sniper y Alpha Chill.

---

## 3. Resultados Reales Medidos en `servidor` (Antes vs Después)

| Métrica (`decu2paper` en `servidor`) | Antes | Después | Mejora real |
|---|---:|---:|---:|
| **RAM de `decu2paper` (RSS)** | `281 MB` | **`121 MB`** | **`-160 MB` (`-57 %`)** |
| **RAM disponible del VPS (`free -m`)** | `801 MB` | **`999 MB`** | **`+198 MB` libres** |
| **CPU de `decu2paper`** | `30.9 %` | **`14.1 %`** *(bajando tras arranque)* | **`-54 %` (y menor en régimen estable)** |
| **Hilos activos de `decu2paper`** | `7` | **`5`** | `-2` hilos muertos |
| **Tiempo de arranque (reinicio)** | `19 s` | **`3 s`** | **`6.3×` más rápido** |
| **Tests de regresión (`servidor`)** | — | **`68 / 68` OK** | `LimitesRiesgo` intacto (`c7c25a41335aace7`) |

### Verificación en vivo post-despliegue
- **Servicios:** `decu2detector`, `decu2paper`, `miapi`, `decu2telegram` — **4/4 `active`** sin errores.
- **Estrategias activas:** `['TIPO_D', 'TIPO_E']` (**Alpha Sniper** + **Alpha Chill**).
- **Alpha Sniper (`libro_d`) intacto:** `36` ops · **`+0.2853 SOL`**.
- **Alpha Chill (`libro_e`) activa:** `0` ops (vigilando en tiempo real).
- **Gráfica en vivo (`live_chart.json`):** `10` monedas activas con velas al día.

---

## Historial de informes

- [`2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md`](informes/2026-11-24_1403_optimizacion_ram_cpu_modo_ligero_v46.md) — Optimización de RAM, CPU y Arranque — Modo Ligero `DECU2_SOLO_V46=1`
- [`2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md`](informes/2026-11-24_1354_auditoria_limpieza_y_deuda_tecnica.md) — Auditoría de Limpieza de Código y Deuda Técnica Actual (DECU 2.0)
- [`2026-11-24_1343_evaluacion_estructura_bot_decu.md`](informes/2026-11-24_1343_evaluacion_estructura_bot_decu.md) — Auditoría y Nota Global de la Estructura Actual de DECU 2.0 (V4.6)
- [`2026-11-24_1252_integracion_alpha_chill.md`](informes/2026-11-24_1252_integracion_alpha_chill.md) — Integración en Producción (Paper): Alpha Chill (`TIPO_E`)
- [`2026-11-24_1227_examen_alpha_absorption_15.md`](informes/2026-11-24_1227_examen_alpha_absorption_15.md) — Examen en Datos Reales · «Alpha Absorption 15» (`+14%–15%` bruto · 23 sesiones reales)
- [`2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) — Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)
- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
