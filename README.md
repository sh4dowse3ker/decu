<!-- AUTO-ACTUALIZADO: último informe publicado el 2026-11-24 12:52 UTC -->
> **Último informe:** [`informes/2026-11-24_1252_integracion_alpha_chill.md`](informes/2026-11-24_1252_integracion_alpha_chill.md) · *Actualizado: 2026-11-24 12:52 UTC*

# Integración en Producción (Paper): Alpha Chill (`TIPO_E`)

**Fecha:** 2026-11-24 UTC  
**Modo:** 100 % Paper Trading (`0 SOL` real)  
**Estado en `servidor`:** 🟢 Activo en paralelo con **Alpha Sniper** (`TIPO_D`), con libros y posiciones **100 % independientes**.

---

## 1. Arquitectura 100 % Separada (Cero Mezcla con Alpha Sniper)

| Componente | **Alpha Sniper (`TIPO_D`)** | **Alpha Chill (`TIPO_E`)** |
|---|---|---|
| **Libro contable** | `libro_d` (`operaciones_d`) | `libro_e` (`operaciones_e`) |
| **Posiciones abiertas** | `abiertas` (máx. 3 simultáneas) | `abiertas_e` (máx. 3 simultáneas, independientes) |
| **Memoria por token** | `_alpha_sniper_ejecutados` | `_alpha_abs_ejecutados` (1 entrada limpia por mint) |
| **Convivencia en mismo token** | Puede mantener runner hasta 45 min | Puede entrar y cerrar `+15%` en ~40s sin tocar ni bloquear a Alpha Sniper |
| **Tarjeta en Dashboard Web** | `Alpha Sniper · Post-Grad AMM` | `Alpha Chill · Rebote +15%` |
| **Notificaciones Telegram** | `🏹 QUANTUM V4.6 · Alpha Sniper` | `🧊 QUANTUM V4.6 · Alpha Chill (Rebote +15%)` |
| **Auditoría 100 ops (Paso a Real)** | Contador independiente (`35 / 100`) | Contador independiente (`0 / 100`) |

---

## 2. Reglas Activas de **Alpha Chill** (`TIPO_E`)

Validada en 23 sesiones reales de PumpSwap (`38.11 h`, 3/3 bloques cronológicos `Q12 / Q34 / NEW` positivos: `WR 69.8%`, `PF 1.71`, `PF_2x 1.63`, `PF_nb 1.65`, ritmo real estimado ~`22–28 ops / 24h` tras vetos de seguridad):

- **Entrada (solo tokens `...pump` graduados de curva a PumpSwap AMM):**
  - Edad en AMM `>= 150s`, liquidez `v_sol >= 80 SOL`, compra disparadora `<= 3.0 SOL` (anti-spike).
  - Pool vivo últimos 60s: `>= 20` swaps, volumen `>= 35 SOL`, ratio compras `0.35 <= br60 <= 0.78`.
  - Barrida de pánico de corto plazo (últimos 120s): caída `dd120 <= -15%` y rebote confirmado `4% <= reb120 <= 12%`.
  - Absorción compradora real (últimos 10s): `OFI_10s >= +0.15`.
  - Tamaño: `0.15 SOL` ficticios por operación, máx. 3 posiciones simultáneas.
- **Escudos de seguridad pre-orden (idénticos a Alpha Sniper V2):**
  - Blacklist permanente en disco (`_mints_vetados_permanentes`).
  - RugCheck / Bubblemaps en modo **fail-closed** (`sin_verificacion_rugcheck` veta).
  - Filtro antiballenas `top1 externo < 8%` y `top10 < 50%`, autoridades nulas y Jupiter anti-honeypot.
- **Gestión de salida:**
  - **Take Profit (100%):** `+15%` bruto (`~+11.5% a +13%` neto tras comisiones/slippage).
  - **Breakeven protegido:** al alcanzar `+8.5%` fija suelo en `+4.5%` bruto (cierre siempre verde neto).
  - **Stop Loss:** `-10.5%` (con gracia anti-MEV `1.5s`, o salida inmediata si `<= -22%`).
  - **Anti-Rug inmediato:** drenaje de liquidez `>= 20%` o estado `BLOCKED`.
  - **Sin impulso (`DEAD`):** `90s` si `MFE < +4%` y `ret <= +0.5%`.
  - **Horizonte máximo:** `10 minutos` (`600s`).

---

## 3. Verificación Post-Despliegue en `servidor`

- **Tests locales:** `96/96` OK (`test_quantum_v46`, `test_plataforma_v3`, `test_quantum_v45`, `test_telegram`), `node --check static/decu2-ui.js` OK, auditoría AST pure-stdlib OK, huella congelada `LimitesRiesgo` intacta (`c7c25a41335aace7`).
- **Tests remotos en `servidor`:** `55/55` OK (`DECU2_NO_TELEGRAM=1`).
- **Servicios systemd:** `decu2detector`, `decu2paper`, `miapi`, `decu2telegram` — **4/4 `active`** sin errores.
- **Estado inicial confirmado en `paper_estado.json`:**
  - `tipos_activos_entrada: ['TIPO_D', 'TIPO_E']`
  - **Alpha Sniper (`libro_d`) intacto:** `35` ops (`13W`, `WR 37.1%`, **`+0.2617 SOL`**, **`PF 1.51`**)
  - **Alpha Chill (`libro_e`) inicializado:** `0` ops (`+0.0000 SOL`), vigilando en vivo.
- **Seguimiento automático:** cron cada 4 horas actualizado para reportar ambos libros por separado hasta completar las `100` operaciones en vivo de cada estrategia.

---

## Historial de informes

- [`2026-11-24_1252_integracion_alpha_chill.md`](informes/2026-11-24_1252_integracion_alpha_chill.md) — Integración en Producción (Paper): Alpha Chill (`TIPO_E`)
- [`2026-11-24_1227_examen_alpha_absorption_15.md`](informes/2026-11-24_1227_examen_alpha_absorption_15.md) — Examen en Datos Reales · «Alpha Absorption 15» (`+14%–15%` bruto · 23 sesiones reales)
- [`2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md`](informes/2026-11-24_1219_propuesta_estrategia_15_20_ops_dia.md) — Propuesta de Estrategia · «Absorción de Pánico en Pools Calientes» (`15–20 ops/día` · `+12%–15%` bruto)
- [`2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md`](informes/2026-11-24_1203_evaluacion_3_ideas_y_alpha_sniper.md) — Informe DECU · Evaluación Exhaustiva de Estrategias (+10–15% Neto) y Estado `Alpha Sniper V2`
