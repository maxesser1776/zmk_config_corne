# ZMK Config: beekeeb Chocofi (36-key split)

[![Build ZMK firmware](https://github.com/maxesser1776/zmk_config_corne/actions/workflows/build.yml/badge.svg)](https://github.com/maxesser1776/zmk_config_corne/actions/workflows/build.yml)

ZMK firmware configuration for a **beekeeb pre-soldered Chocofi**: a 36-key, low-profile (Kailh Choc) wireless split keyboard. The layout is QWERTY with home-row mods. It's tuned for prose and light programming, one-handed CAD work in Fusion 360 and Blender (right hand on the mouse), and Windows navigation.

> **Why "corne"?** The Chocofi's wiring is compatible with the Corne, so this config uses ZMK's built-in `corne_left` / `corne_right` shields with the 5-column physical layout. The board itself is a Chocofi.

## Contents

- [Hardware](#hardware)
- [Quick start](#quick-start)
- [Firmware builds](#firmware-builds)
- [Flashing](#flashing)
- [Keymap](#keymap)
- [KeyPeek overlay](#keypeek-overlay)
- [Bluetooth notes](#bluetooth-notes)
- [Building locally](#building-locally)
- [Repository layout](#repository-layout)
- [Development workflow](#development-workflow)
- [Acknowledgements](#acknowledgements)

## Hardware

| | |
|---|---|
| Keyboard | beekeeb Chocofi, 3×5 + 3 thumbs per side (36 keys) |
| Controllers | nice!nano v2 (nRF52840), one per half |
| Displays | nice!view |
| Power | Battery per half, physical power switch on each half |
| Host | Windows laptop (Intel AX201 Bluetooth) |
| Firmware | ZMK **v0.3.0** (pinned) |

The **left half is the central**: it connects to the computer, and the right half connects to it. Keymap-only changes need the left half flashed only.

## Quick start

1. Push to GitHub (or open the **Actions** tab and run the workflow by hand).
2. When the run finishes, download the firmware artifacts.
3. Flash `corne_left_keypeek` to the left half (see [Flashing](#flashing)). Flash `corne_right` to the right half only when the physical layout or `corne.conf` changes.

## Firmware builds

GitHub Actions builds every entry in [`build.yaml`](build.yaml) using ZMK's reusable `build-user-config` workflow.

| Artifact | Half | Use |
|---|---|---|
| `corne_left_keypeek` | Left | **Daily firmware.** Includes ZMK Studio and the KeyPeek modules. |
| `corne_left nice_view_adapter nice_view-nice_nano_v2-zmk` | Left | Plain build without KeyPeek or Studio. |
| `corne_right nice_view_adapter nice_view-nice_nano_v2-zmk` | Right | Right half. |
| `corne_left_debug` | Left | USB debug logging (see [Bluetooth notes](#debugging-drops)). Uses more battery; flash normal firmware afterwards. |
| `settings_reset-nice_nano_v2-zmk` | Either | Clears stored settings and Bluetooth bonds on that half. |

## Flashing

1. Put the half into bootloader mode. Either double-tap the half's reset button, or use the `&bootloader` keys on the **Fun** layer:
   - **Left half:** hold `"` (right outer thumb) for Fun, then press the left outer thumb.
   - **Right half:** hold `'` + `Tab` (left thumb combo) for Fun, then press **P** or the right inner thumb.

   `&bootloader` and `&sys_reset` act on the half where they're pressed.
2. The half mounts as a USB drive (`NICENANO`). Copy the `.uf2` onto it. It reboots when done.
3. After changing `corne.conf` or the physical layout, flash **both** halves.
4. If the halves won't pair after a flash, flash `settings_reset` to both, then normal firmware, and re-pair with the computer.

## Keymap

Source: [`config/corne.keymap`](config/corne.keymap). Reference image: [`keymaps/my_keymap.png`](keymaps/my_keymap.png).

Key positions run `0`–`35` (5 columns per side), and combos use these numbers:

```
    0  1  2  3  4   |   5  6  7  8  9
   10 11 12 13 14   |  15 16 17 18 19
   20 21 22 23 24   |  25 26 27 28 29
         30 31 32   |  33 34 35
```

### Layers

| Layer | How to reach it | Contents |
|---|---|---|
| **Base** | Default | QWERTY. Home-row mods: S/D/F = Alt/Ctrl/Shift, J/K/L = Shift/Ctrl/Alt, Z = Win. Backspace on the right pinky. |
| **CAD** | Toggle: Fun + G | Same letters, but S/D/F/Z modifiers fire instantly for one-handed chords (Blender Shift+A, Ctrl+R). |
| **Num/CAD** | Hold Tab; toggle with Tab + Enter | Numpad on the left fingers (7 8 9 / 4 5 6 / 1 2 3, 0 on Z, `.` beside 3). Ctrl/Alt on the pinky, Shift on G. Alt + digit sends numpad keys (Blender views). PgUp/PgDn on the right. |
| **Sym** | Hold left outer thumb, or hold Enter | Symbols, brackets, `::` and `../` macros. |
| **Nav** | Hold `'` (left middle thumb) | Left: mouse keys with real Alt/Shift/Ctrl/Win and an Alt+Tab key. Right: arrows, copy/paste/undo, virtual desktop left/right, Home/End, Alt+F4. |
| **Media** | Hold Space | Volume, mute, play/pause, prev/next. **U = output Bluetooth, I = output USB.** BT disconnect, BT clear (Enter-position thumb), reset. |
| **Fun** | Hold `"` (right outer thumb), or hold `'` + Tab | F1–F12, Bluetooth profiles 0–4, CAD-mode toggle, Lock, Task Manager, Explorer, bootloader. |

### Combos (Base and CAD layers)

| Combo | Action |
|---|---|
| Q + W | Esc |
| Z + X | Undo |
| X + C | Copy |
| C + V | Paste |
| X + C + V | Cut |
| F + J | Caps Word |
| `'` + Tab | Hold for Fun (any layer) |
| Tab + Enter | Toggle Num/CAD (any layer) |

Letter combos need a short pause before them (`require-prior-idle-ms`), so fast typing doesn't trigger them.

## KeyPeek overlay

[KeyPeek](https://github.com/srwi/keypeek) shows the active layer and key presses as an on-screen overlay. It needs:

- the `corne_left_keypeek` firmware, which adds [`zmk-raw-hid`](https://github.com/zzeneg/zmk-raw-hid), [`zmk-keypeek-layer-notifier`](https://github.com/srwi/zmk-keypeek-layer-notifier) and ZMK Studio (with locking off). KeyPeek reads the keymap through Studio.
- the KeyPeek desktop app, connected to **"Corne (ZMK BLE …)"** for Bluetooth, or to the USB device.

Notes:

- Studio follows the keyboard's selected output. Plugging in USB switches the output (and Studio) to USB, which ends a KeyPeek session over Bluetooth. Press **Media + U** to keep Bluetooth as the output while USB is plugged in. The choice is saved on the keyboard.
- KeyPeek can't show combos; use the combo table above.
- Recommended legend mode: **Single + live preview**.
- Both KeyPeek modules are pinned to tested commits in [`config/west.yml`](config/west.yml).

## Bluetooth notes

Settings live in [`config/corne.conf`](config/corne.conf):

- 15-minute idle sleep (`CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000`).
- Preferred connection parameters: 15 ms interval, latency 30, 5 s timeout.
- TX power +4 dBm.
- **`CONFIG_BT_CTLR_CONN_PARAM_REQ=n`**: required with this laptop (see below).

### Intel AX201 dropouts

**Symptom:** the keyboard goes dead for about 5 seconds and reconnects, often in pairs about 50 seconds apart after a reconnect. A key held at that moment may auto-repeat on the host.

**Cause:** 5 seconds after every connection, ZMK (Zephyr) asks the host to confirm connection parameters using the link-layer *Connection Parameter Request* procedure. The AX201 sometimes accepts that request but never applies it. The keyboard waits out its 40-second timeout and drops the link (reason `0x22` on the keyboard, `0x08` on the host). ZMK Studio's own latency request (when KeyPeek connects) triggered the same failure.

**Fix:**

- `CONFIG_BT_CTLR_CONN_PARAM_REQ=n` makes the keyboard send the request as an L2CAP Connection Parameter Update instead. Windows applies that itself, and it completes reliably.
- The KeyPeek build sets `CONFIG_ZMK_STUDIO_TRANSPORT_BLE_PREF_LATENCY=30`, so Studio never asks for a change.

**Don't** use `CONFIG_BT_GAP_AUTO_UPDATE_CONN_PARAMS=n` as an alternative: that build hung the left half in testing.

Also keep the Intel Bluetooth driver current: driver 23.60 (Lenovo) caused the original dropouts, and 24.70.0.4 or newer is required.

### Debugging drops

- **Keyboard side:**
  1. Flash `corne_left_debug` to the left half and plug it into USB.
  2. Optionally press Media + U to keep the output on Bluetooth.
  3. Run `python logs\capture.py COM5 <name>`. This writes a timestamped log to `logs/`, which is gitignored. Find the COM port with `python -m serial.tools.list_ports -v`.
  4. Look for `disconnected: … (reason 0x..)` and `le_param_updated`.
- **Host side:** Microsoft's Bluetooth Virtual Sniffer (from the Bluetooth Test Platform package) streams HCI traffic to Wireshark:
  - Run `btvs.exe -Mode Wireshark` from an admin prompt.
  - Leave *Full Packet Logging* and *Debug Mode* off, since they record keystrokes and keys.
  - Useful filter:

    ```
    bthci_evt.code == 0x05 || bthci_evt.le_meta_subevent == 0x03 || bthci_evt.le_meta_subevent == 0x06
    ```

Don't put `CONFIG_ZMK_USB_LOGGING=y` in `corne.conf`; use the `zmk-usb-logging` snippet build instead.

## Building locally

CI is the canonical build. For local builds, use a West workspace in `zmk-workspace/` (gitignored). If it's missing, bootstrap it with `west init -l config && west update`. Then:

```sh
cd zmk-workspace
west build -p -s zmk/app -b nice_nano_v2 -- -DSHIELD="corne_left nice_view_adapter nice_view"  -DZMK_CONFIG=../config
west build -p -s zmk/app -b nice_nano_v2 -- -DSHIELD="corne_right nice_view_adapter nice_view" -DZMK_CONFIG=../config
```

The output is `build/zephyr/zephyr.uf2`. There are no unit tests: a successful build of both halves is the check.

## Repository layout

```
.github/workflows/build.yml   CI: ZMK reusable workflow, pinned to v0.3.0
build.yaml                    Build matrix (boards, shields, snippets, cmake-args)
config/
  corne.keymap                Keymap: layers, combos, macros, custom behaviors
  corne.conf                  Kconfig: power, Bluetooth, pointing
  west.yml                    Manifest: ZMK v0.3.0 + KeyPeek modules (pinned)
  backups/                    Old keymap snapshots
keymaps/                      Reference images of the layout (manual renders)
boards/shields/               Reserved for custom shields
zephyr/module.yml             Makes this repo a Zephyr module (board_root)
CLAUDE.md                     Notes for AI coding assistants
```

## Development workflow

- ZMK and both modules are **pinned**. Tracking ZMK `main` caused left-half wake failures and poor battery. Update deliberately, and keep the `west.yml` revision and the workflow ref in sync.
- Experiments go on short-lived branches. CI builds every push, so test the artifact and merge when it's good.
- Layers are referenced by their `#define` names (`BASE`, `NUM`, …), never raw numbers. Layer order matters for `&trans` and combos.
- Update `keymaps/my_keymap.png` by hand when user-facing layout changes ship.

## Acknowledgements

- [ZMK Firmware](https://zmk.dev) and its contributors.
- [KeyPeek](https://github.com/srwi/keypeek) and [zmk-keypeek-layer-notifier](https://github.com/srwi/zmk-keypeek-layer-notifier) by srwi.
- [zmk-raw-hid](https://github.com/zzeneg/zmk-raw-hid) by zzeneg.
- [beekeeb](https://beekeeb.com) for the Chocofi.
