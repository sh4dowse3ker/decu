<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 12:19 UTC -->
> **Último informe:** [`informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) · *Actualizado: 2026-11-24 12:19 UTC*

# Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)

> **Estado:** Propuesta teórica de diseño (**NO implementada ni validada todavía**). Pendiente de aprobación del usuario para testearla en las 23 sesiones históricas reales (`38.9 h`).

---

## 1. Por qué `15–20 ops/día` cambia completamente las reglas del juego

Buscar `15–20 ops/hora` obliga a entrar en ruido y destruye el Profit Factor (`PF 0.5–0.9`). En cambio, **`15–20 ops/día` (`~0.6–0.85 ops/hora`)** es **4× más selectivo que `Alpha Sniper`** (`~80 ops/día`): permite filtrar y quedarse **solo con el Top 15 % de los mejores pools y mejores suelos del día**.

---

## 2. Diseño exacto de la estrategia («Alpha Absorption 15»)

### A. Filtro de universo (solo pools profundos y muy activos)
1. **Graduado real de Pump.fun (`...pump`, `had_cur = 1`):** cero LP-farms/escaleritas `no-pump`.
2. **Liquidez profunda (`v_sol ≥ 90–100 SOL`):** slippage mínimo (`<0.2%`) y mucha mayor resistencia a que una sola ballena rompa el precio `-40%` en un bloque.
3. **Mercado realmente caliente (`vol_60s ≥ 45–60 SOL` y `≥ 25–30` swaps/min):** si el pool no tiene compradores reales compitiendo, no hay rebote rápido de `+12%–15%`.
4. **Flujo orgánico equilibrado (`br_60s` entre `0.38` y `0.72`):** descarta tanto cascadas 100 % vendedoras como bots unidireccionales.
5. **Escudo de seguridad permanente:** Bubblemaps/RugCheck fail-closed + `top1 externo < 8%` + lista negra permanente de sybils.

### B. Disparador de entrada (absorción real de pánico corto, sin perseguir velones)
1. **Flush rápido de corto plazo (`dd_120s ≤ -18%`):** caída brusca en los últimos 2 minutos (toma de beneficios / liquidación rápida), **no** un desangrado lento de 30 minutos.
2. **Confirmación de suelo vivo (anti-cuchillo):**
   - No entra en la primera micro-compra suelta.
   - Exige **absorción real en los últimos 10 s** (`ofi_10s ≥ +0.25`, compras superando claramente a ventas) y **rebote contenido en `[+4%, +10%]`** desde el mínimo.
   - **Anti-velón:** prohíbe entrar si la vela disparadora fue una sola compra gigante (`sol > 2.5–3.0 SOL`) que ya estiró el precio `+8%` en un tick (evitando trampas tipo `Cupsey`).

### C. Gestión de salida rápida («cobra antes del rug»)
- **Take Profit completo:** **`+14% a +15%` bruto** (`~+11.5% – +13%` neto tras fees `0.5%` + slippage `<0.4%` + gas).
- **Breakeven temprano:** al tocar **`+8.5%`**, sube el suelo a **`+4.5%` bruto** (`~+2.5%` neto mínimo garantizado — evitando casos como `DUVAL`, que tocó `+10.6%` y acabó en `-16.7%`).
- **Stop Loss limpio:** **`-10%` a `-11%`** (más `EARLY_EXIT_RUG` inmediato si la liquidez cae `-20%`).
- **Salida por falta de impulso (`DEAD EXIT`):** si tras **`90 s`** en un pool caliente no superó `+4%` y sigue plano/rojo, cierra rápido en vez de esperar al SL.
- **Horizonte máximo:** **`10 minutos`** (duración media esperada: `1–4 min`).

---

## 3. Cómo la validaremos antes de tocar una sola línea de producción
Si tiene buena pinta, la someteremos en las **23 sesiones reales (`38.9 h`)** al mismo examen sin piedad:
- Latencia realista `+0.45 s` en entrada y salida + estrés `2×` slippage + 100 % rugs reales.
- Frecuencia objetivo real: `~25–35` operaciones en `38.9 h` (`~15–20 ops/día`).
- Criterios mínimos para aprobar: **`WR ≥ 62–65%`**, **`PF ≥ 1.50`**, **`PF sin mejor ≥ 1.35`**, **3/3 bloques cronológicos (`Q12 / Q34 / NEW`) en verde** y **`p-value < 0.05`**.

---

## Historial de informes

- [`2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) — Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)
- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
