# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

ZMK firmware configuration for a **beekeeb pre-soldered Chocofi** — a 36-key (3×10 + 3 thumbs per side) low-profile Kailh Choc split keyboard on `nice_nano` v2 controllers with `nice_view` Sharp-memory displays. Despite the repo name and shield selection, the physical keyboard is Chocofi, *not* Corne; the Corne shield definition is reused because the nice_nano pin/matrix wiring is compatible. The outer-column `&none` bindings in every layer correspond to Corne keys that do not exist on the Chocofi — do not replace them with real keycodes.

This is a *user config* repo consumed by upstream ZMK — it provides only the keymap, Kconfig overrides, and west manifest. Firmware source lives in `zmkfirmware/zmk` (pulled via `config/west.yml`, revision `main`).

## Build

CI is the canonical build path. `.github/workflows/build.yml` delegates to the reusable `zmkfirmware/zmk/.github/workflows/build-user-config.yml@main`, which reads `build.yaml`. The matrix currently produces `corne_left`, `corne_right`, and `settings_reset` on `nice_nano_v2` with `nice_view_adapter nice_view`. Keep `build.yaml` in sync when adding shields or snippets.

Local builds run from a West workspace (the checked-in `zmk-workspace/` is gitignored; bootstrap with `west init -l config && west update` if missing):

```sh
cd zmk-workspace
west build -p -s zmk/app -b nice_nano_v2 -- -DSHIELD="corne_left nice_view_adapter nice_view"  -DZMK_CONFIG=../config
west build -p -s zmk/app -b nice_nano_v2 -- -DSHIELD="corne_right nice_view_adapter nice_view" -DZMK_CONFIG=../config
```

No unit tests — a successful `west build` of both halves is the verification step. Flash by copying the resulting `zephyr.uf2` to each half in bootloader mode.

## Keymap architecture (`config/corne.keymap`)

Single devicetree source. Layer order is load-bearing — indices are referenced numerically by `&lt`, `&tog_on`, `&tog_off`, and combos:

| idx | label | role |
|-----|-------|------|
| 0 | Base  | alphas with homerow mods |
| 1 | Num   | numbers/brackets (layer-lockable via combo) |
| 2 | Sym   | symbols |
| 3 | Nav   | arrows, mouse (`mmv`/`msc`/`mkp`), app macros |
| 4 | Media | transport, BT select/clear, `sys_reset` |
| 5 | Fun   | F-keys, BT profile select, `bootloader` |

Reordering layers silently breaks every `&lt N`, combo, and `tog_on/off` reference. If you move layers, grep numeric layer refs and update them together.

Custom behaviors:
- `hm` — homerow mod (hold-tap, `tap-preferred`, `tapping-term-ms=220`, `quick-tap-ms=175`, `require-prior-idle-ms=160`, `hold-trigger-on-release`). Used on inner Base keys.
- `tog_on` / `tog_off` — one-way toggle-layer variants. Combo at `key-positions <38 39>` locks Num on; `<38 37>` unlocks.

Macros wrap Windows-flavored OS shortcuts (`win_lock = LG(L)`, `task_manager = LS(LC(ESC))`, Chrome/Fusion/Proton bindings). Keep macro `label` values short uppercase to match style.

Pointing is enabled (`CONFIG_ZMK_POINTING=y`); move/scroll defaults are overridden via `ZMK_POINTING_DEFAULT_MOVE_VAL` / `ZMK_POINTING_DEFAULT_SCRL_VAL` `#define`d *before* the pointing header is included.

## Kconfig (`config/corne.conf`)

Power management is intentionally tuned: `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000` (15 min), BLE peripheral preferred latency/timeout raised for cleaner wake-from-idle reconnects, TX power bumped via `CONFIG_BT_CTLR_TX_PWR_PLUS_4=y`. Tuning sleep/BLE is the recurring experiment on the current branch.

## Documentation images

`keymaps/my_keymap_*.png` are manual reference renders, not build output. Update them by hand when user-facing layer changes ship.

## Layout

- `config/` — edit these: `corne.keymap`, `corne.conf`, `west.yml`.
- `build.yaml` — CI build matrix.
- `boards/shields/` — reserved for custom shields; `zephyr/module.yml` sets `board_root: .` so additions here are discoverable.
- `zmk-workspace/`, `.venv/` — gitignored local scaffolding.
