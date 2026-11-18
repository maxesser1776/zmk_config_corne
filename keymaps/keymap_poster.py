#!/usr/bin/env python3
"""Render the Chocofi keymap poster (keymaps/keymap.html -> keymaps/keymap.png).

Hand-maintained: update LAYERS / COMBOS / CHEATS when config/corne.keymap changes.
Usage:  python keymaps/keymap_poster.py --png
        Writes keymaps/keymap.html and renders keymaps/keymap.png with Playwright
        (pip install playwright pillow && playwright install chromium).
        Without --png it only writes the HTML, which you can open in a browser.
"""
import html, pathlib, sys

OUT = pathlib.Path(__file__).with_name("keymap.html")

# category -> (background, border, text)
CAT = {
    "key":   ("#f7f6f3", "#d9d6cf", "#1d1d1f"),
    "mod":   ("#ecebfb", "#8f86e0", "#3d2fb0"),
    "edit":  ("#eceff4", "#b7bfcc", "#2b3440"),
    "cursor":("#e3f5f2", "#6cc3b6", "#0f6e63"),
    "mouse": ("#e8f1fc", "#8cb5ea", "#1d5fb3"),
    "media": ("#e5f5e9", "#78c38c", "#1f7a3a"),
    "win":   ("#fdf3dc", "#e7b95a", "#8a5a00"),
    "app":   ("#fde8f1", "#ec93b9", "#b02a64"),
    "sys":   ("#fde9e6", "#ec8f84", "#b42318"),
    "bt":    ("#eeeff1", "#b4b8c0", "#3a3f47"),
}
LAYER_COLOR = {"Base": "#5b6170", "CAD": "#e07b28", "Num/CAD": "#2f6db5", "Sym": "#7a4fc2",
               "Nav": "#149086", "Media": "#2e8b57", "Fun": "#d0453a"}

T = ("trans",)      # falls through
H = ("held",)       # thumb holding this layer
N = ("none",)       # does nothing

def k(t, s="", c="key", flash=False):
    return ("key", t, s, c, flash)

def thumb(t, s, layer):
    return ("thumb", t, s, layer)

# 36 positions:  0-9 top, 10-19 home, 20-29 bottom, 30-35 thumbs (left outer -> right outer)
LAYERS = [
 ("Base", "0 · Base", "Always on. Normal typing (QWERTY).", [
   k("Q"),k("W"),k("E"),k("R"),k("T"),  k("Y"),k("U"),k("I"),k("O"),k("P"),
   k("A"),k("S","Alt","key"),k("D","Ctrl"),k("F","Shift"),k("G"),  k("H"),k("J","Shift"),k("K","Ctrl"),k("L","Alt"),k("⌫","","edit"),
   k("Z","Win"),k("X"),k("C"),k("V"),k("B"),  k("N"),k("M"),k(","),k("."),k("/"),
   thumb("Sym","hold only","Sym"),thumb("'","hold: Nav","Nav"),thumb("Tab","hold: Num/CAD","Num/CAD"),
   thumb("Enter","hold: Sym","Sym"),thumb("Space","hold: Media","Media"),thumb('"',"hold: Fun","Fun")]),
 ("CAD", "1 · CAD mode", "Toggle on/off: Fun layer → G. Same letters, but S/D/F/Z become Alt/Ctrl/Shift/Win instantly (for one-handed Blender chords like Shift+A).", [
   T,T,T,T,T, T,T,T,T,T,
   T,k("S","Alt ⚡","mod"),k("D","Ctrl ⚡","mod"),k("F","Shift ⚡","mod"),T, T,T,T,T,T,
   k("Z","Win ⚡","mod"),T,T,T,T, T,T,T,T,T,
   T,T,T,T,T,T]),
 ("Num/CAD", "2 · Num / CAD", "Hold Tab (left thumb), or lock it on/off with Tab + Enter. Numpad on ring / middle / index for the left hand while the right stays on the mouse. Hold Alt + a digit = numpad key (Blender camera views).", [
   k("Ctrl","","mod"),k("7","Alt: numpad"),k("8","Alt: numpad"),k("9","Alt: numpad"),k("Enter","","edit"),
   k("`"),k("÷","numpad"),k("×","numpad"),k("+","numpad"),T,
   k("Alt","","mod"),k("4","Alt: numpad"),k("5","Alt: numpad"),k("6","Alt: numpad"),k("Shift","","mod"),
   k("Del","","edit"),T,k("PgUp","","cursor"),T,T,
   k("0","Alt: numpad"),k("1","Alt: numpad"),k("2","Alt: numpad"),k("3","Alt: numpad"),k(".","Alt: numpad"),
   T,T,k("PgDn","","cursor"),T,T,
   k("−","when locked"),k("⌫","when locked","edit"),("held","Esc when locked"),T,T,T]),
 ("Sym", "3 · Symbols", "Hold the left outer thumb or Enter. Every symbol has its own key, so no Shift needed.", [
   k("'"),k("<"),k(">"),k('"'),k("`"),  k("&"),k("::","macro","app"),k("["),k("]"),k("%"),
   k("!"),k("-"),k("+"),k("="),k("#"),  k("|"),k(":"),k("("),k(")"),k("?"),
   k("^"),k("/"),k("*"),k("\\"),k("../","macro","app"),  k("~"),k("$"),k("{"),k("}"),k("@"),
   H,k(";"),k("_"),N,T,T]),
 ("Nav", "4 · Navigation", "Hold ' (left thumb). Left hand: mouse + real modifiers. Right hand: arrows, editing, windows and desktops.", [
   k("Alt","","mod"),k("Middle click","","mouse"),k("Mouse ↑","","mouse"),k("Scroll ↑","","mouse"),k("Ctrl+Shift","","mod"),
   k("Redo","","edit"),k("Paste","","edit"),k("Copy","","edit"),k("Cut","","edit"),k("Undo","","edit"),
   k("Shift","","mod"),k("Mouse ←","","mouse"),k("Left click","","mouse"),k("Mouse →","","mouse"),k("Right click","","mouse"),
   k("Proton","mail app","app"),k("←","","cursor"),k("↑","","cursor"),k("↓","","cursor"),k("→","","cursor"),
   k("Ctrl","","mod"),k("Switch","Alt+Tab · hold","win"),k("Mouse ↓","","mouse"),k("Scroll ↓","","mouse"),k("Win","","mod"),
   k("Tab","","edit"),k("Desktop ←","","win"),k("Desktop →","","win"),k("Back","Alt+←","cursor"),k("Fwd","Alt+→","cursor"),
   T,H,T,k("Home","","cursor"),k("End","","cursor"),k("Close","Alt+F4","win")]),
 ("Media", "5 · Media", "Hold Space (right thumb). Music and volume on the left home row; output select on the right.", [
   T,k("Prev","⏮","media"),k("Next","⏭","media"),T,T,  T,k("Out BT","output","bt"),k("Out USB","output","bt"),T,T,
   k("Mute","","media"),k("Vol −","","media"),k("Vol +","","media"),k("Play / Pause","","media"),T,  T,T,T,T,T,
   k("Reset","restart half","sys"),k("BT","disconnect","bt"),T,T,k("Calc","calculator","win"),  T,T,T,T,k("Reset","restart half","sys"),
   k("Mute","","media"),k("Play / Pause","","media"),k("Stop","","media"),k("BT Clear","forget pairing","sys"),H,T]),
 ("Fun", "6 · Function & system", "Hold \" (right outer thumb), or hold ' + Tab together with the left thumb. F-keys, Bluetooth profiles, firmware flashing, CAD-mode switch.", [
   k("F12"),k("F7"),k("F8"),k("F9"),k("PrtSc"),  k("Snip","screenshot","win"),k("Explorer","","win"),k("Quake","terminal","app"),k("Task Mgr","","win"),k("Boot","flash right","sys",True),
   k("F11"),k("F4"),k("F5"),k("F6"),k("CAD mode","on / off","app"),  k("BT 0","","bt"),k("BT 1","","bt"),k("BT 2","","bt"),k("BT 3","","bt"),k("BT 4","","bt"),
   k("F10"),k("F1"),k("F2","rename"),k("F3","search"),k("Pause"),  k("Colors","Fusion","app"),k("Isolate","Fusion","app"),k("Unisolate","Fusion","app"),k("Lock","lock PC","win"),N,
   k("Boot","flash left","sys",True),T,T,k("Boot","flash right","sys",True),T,H]),
]

COMBOS = [((0,1),"Esc"),((13,16),"Caps Word"),((20,21),"Undo"),((21,22),"Copy"),((22,23),"Paste"),
          ((21,22,23),"Cut"),((31,32),"hold: Fun"),((32,33),"Num/CAD lock")]

CHEATS = [
 ("Fusion (CAD)", "#e07b28", [
   ("Extrude / Dimension / Line…", "tap E / D / L (letters on Base)"),
   ("Window / Freeform / Paint select", "<kbd>hold Tab</kbd> + 1 / 2 / 3"),
   ("Orbit", "<kbd>Tab</kbd> + <kbd>G (Shift)</kbd> + middle-drag"),
   ("Visual styles", "<kbd>Tab</kbd> + <kbd>Q (Ctrl)</kbd> + 4…9"),
   ("Type a dimension", "hold Tab, type on the left numpad, Enter on T"),
   ("Isolate / colors", "Fun layer: Isolate · Unisolate · Colors")]),
 ("Blender (3D)", "#e07b28", [
   ("Grab / Rotate / Scale", "tap G / R / S"),
   ("Edit mode", "tap Tab"),
   ("Vertex / Edge / Face", "<kbd>hold Tab</kbd> + 1 / 2 / 3"),
   ("Camera views", "<kbd>Tab</kbd> + <kbd>A (Alt)</kbd> + 7 top · 1 front · 3 right · 5 ortho · 0 camera"),
   ("Add / Duplicate", "CAD mode: <kbd>F</kbd> then A / D"),
   ("Loop cut / Bevel", "CAD mode: <kbd>D</kbd> then R / B"),
   ("Search (F3)", "<kbd>'</kbd> + <kbd>Tab</kbd> (hold) + V")]),
 ("Obsidian (notes)", "#7a4fc2", [
   ("[[links]] · # · - · * · `", "Symbols layer"),
   ("Line start / end", "Nav: <kbd>'</kbd> + Home / End"),
   ("Select to line end", "Nav: <kbd>A (Shift)</kbd> + End"),
   ("Back / forward", "Nav: Back / Fwd"),
   ("Command palette", "<kbd>hold D (Ctrl)</kbd> + P"),
   ("Code / CAPS", "Sym <kbd>`</kbd> · <kbd>F</kbd> + <kbd>J</kbd> = Caps Word")]),
 ("Windows", "#149086", [
   ("Switch windows", "Nav: hold X (Switch), tap N or arrows"),
   ("Virtual desktop ← / →", "Nav: M then , (finger sweep)"),
   ("Close window (Alt+F4)", "Nav: right outer thumb"),
   ("Snap window", "Nav: <kbd>B (Win)</kbd> + arrow"),
   ("Screenshot / Lock PC", "Fun: Snip · Lock"),
   ("Calculator", "Media: <kbd>Space</kbd> + B"),
   ("Next / previous tab", "<kbd>hold D (Ctrl)</kbd> + Tab thumb (+ F for previous)"),
   ("Keep KeyPeek on Bluetooth", "Media: <kbd>Space</kbd> + U (Out BT)")]),
]

# ---------------- geometry ----------------
KW, KH, GAP = 54, 54, 8
COL_Y = [26, 10, 0, 10, 18]          # column stagger, left half pinky -> inner
RIGHT_X0 = 5 * (KW + GAP) + 34
THUMBS = [  # (x, y, rotation) for positions 30..35
    (150, 232, 14), (213, 222, 8), (276, 216, 2),
    (RIGHT_X0 + 0, 216, -2), (RIGHT_X0 + 63, 222, -8), (RIGHT_X0 + 126, 232, -14)]
BOARD_W = RIGHT_X0 + 5 * (KW + GAP) - GAP
BOARD_H = 300

def pos_xy(p):
    if p >= 30:
        return THUMBS[p - 30]
    row, col = divmod(p, 10)
    if col < 5:
        x = col * (KW + GAP); y = COL_Y[col] + row * (KH + GAP)
    else:
        c = col - 5; x = RIGHT_X0 + c * (KW + GAP); y = COL_Y[4 - c] + row * (KH + GAP)
    return (x, y, 0)

def esc(s): return html.escape(s)

def key_html(p, spec, base_names=None):
    x, y, r = pos_xy(p)
    style = f"left:{x}px;top:{y}px;transform:rotate({r}deg)"
    kind = spec[0]
    if kind == "trans":
        return f'<div class="k trans" style="{style}">▽</div>'
    if kind == "none":
        return f'<div class="k none" style="{style}"></div>'
    if kind == "held":
        sub = f'<span class="s">{esc(spec[1])}</span>' if len(spec) > 1 else ""
        return f'<div class="k held" style="{style}"><span class="dot"></span>{sub}</div>'
    if kind == "ghost":
        return f'<div class="k ghost" style="{style}"><span class="t">{esc(spec[1])}</span></div>'
    if kind == "thumb":
        _, t, s, layer = spec
        col = LAYER_COLOR[layer]
        return (f'<div class="k thumbk" style="{style};border-color:{col};color:{col}">'
                f'<span class="t" style="color:#1d1d1f">{esc(t)}</span><span class="s">{esc(s)}</span></div>')
    _, t, s, c, flash = spec
    bg, bd, fg = CAT[c]
    long = " xlong" if len(t) > 8 else (" long" if len(t) > 5 else "")
    sub = f'<span class="s">{esc(s)}</span>' if s else ""
    return (f'<div class="k{long}" style="{style};background:{bg};border-color:{bd};color:{fg}">'
            f'<span class="t">{esc(t)}</span>{sub}</div>')

def board(keys):
    inner = "".join(key_html(i, s) for i, s in enumerate(keys))
    return f'<div class="board" style="width:{BOARD_W}px;height:{BOARD_H}px">{inner}</div>'

def combo_board():
    base = LAYERS[0][3]
    keys = []
    for i, s in enumerate(base):
        label = s[1] if s[0] in ("key", "thumb") else ""
        keys.append(("ghost", label))
    inner = "".join(key_html(i, s) for i, s in enumerate(keys))
    svg, chips = [], []
    for ps, label in COMBOS:
        pts = []
        for p in ps:
            x, y, _ = pos_xy(p); pts.append((x + KW / 2, y + KH / 2))
        cx = sum(a for a, _ in pts) / len(pts); cy = sum(b for _, b in pts) / len(pts)
        if ps == (31, 32): cy += 66; cx -= 34
        elif ps == (32, 33): cy += 66; cx += 40
        elif ps == (0, 1): cy -= 26
        elif ps == (21, 22, 23): cy += 34
        elif ps in ((21, 22), (22, 23), (20, 21)): cy += 20
        for a, b in pts:
            svg.append(f'<line x1="{a}" y1="{b}" x2="{cx}" y2="{cy}"/>')
        chips.append(f'<div class="chip" style="left:{cx}px;top:{cy}px">{esc(label)}</div>')
    return (f'<div class="board" style="width:{BOARD_W}px;height:{BOARD_H+40}px">{inner}'
            f'<svg class="lines" width="{BOARD_W}" height="{BOARD_H+40}">{"".join(svg)}</svg>{"".join(chips)}</div>')

def card(title, desc, body, color):
    d = f'<p class="desc">{esc(desc)}</p>' if desc else ''
    return (f'<section class="card" style="border-top-color:{color}"><h2><span class="ldot" style="background:{color}"></span>{esc(title)}</h2>'
            f'{d}{body}</section>')

LEGEND_KEYS = [("A", "", "key", "<b>Big label</b> = what the key types when tapped."),
               ("S", "Alt", "key", "<b>Small label</b> = what it does when <b>held</b>. Tap S for \"s\", hold it for Alt (\"homerow mods\")."),
               ("'", "hold: Nav", "thumb", "<b>Colored thumb key</b> = tap for the character, hold to switch to that layer (color = layer)."),
               ("", "", "held", "<b>Dark key</b> = the key your thumb is already holding to be on this layer."),
               ("▽", "", "trans", "<b>Dashed ▽</b> = not used here; the key keeps doing what it does on Base."),
               ("D", "Ctrl ⚡", "mod", "⚡ = instant modifier (CAD mode only), for one-handed shortcuts while the right hand is on the mouse.")]

def legend():
    rows = []
    for t, s, c, text in LEGEND_KEYS:
        if c == "thumb":
            kh = f'<div class="k sk thumbk" style="border-color:{LAYER_COLOR["Nav"]};color:{LAYER_COLOR["Nav"]}"><span class="t" style="color:#1d1d1f">{esc(t)}</span><span class="s">{esc(s)}</span></div>'
        elif c == "held":
            kh = '<div class="k sk held"><span class="dot"></span></div>'
        elif c == "trans":
            kh = '<div class="k sk trans">▽</div>'
        else:
            bg, bd, fg = CAT[c]
            sub = f'<span class="s">{esc(s)}</span>' if s else ""
            kh = f'<div class="k sk" style="background:{bg};border-color:{bd};color:{fg}"><span class="t">{esc(t)}</span>{sub}</div>'
        rows.append(f'<div class="lrow">{kh}<div>{text}</div></div>')
    return "".join(rows)

COLOR_NAMES = [("mod","Modifier (Ctrl / Shift / Alt / Win)"),("edit","Editing (copy, undo, delete…)"),("cursor","Cursor movement"),
               ("mouse","Mouse control"),("media","Media / volume"),("win","Windows: apps & windows"),("app","App-specific shortcut"),
               ("sys","System: reset / flash / forget"),("bt","Bluetooth / output select")]

def colors():
    items = "".join(f'<span class="sw"><i style="background:{CAT[c][0]};border-color:{CAT[c][1]}"></i>{esc(n)}</span>' for c, n in COLOR_NAMES)
    return (f'<div class="swatches">{items}</div><p class="note"><b>Layers</b> work like Shift does for capitals: hold a thumb key and the whole keyboard '
            'changes to that layer\'s keys. Each layer card\'s color matches the thumb key that opens it on Base. <b>Combos</b>: press two keys at the '
            'same instant for a third action (map at the bottom).</p>')

def cheat(title, color, rows):
    body = "".join(f'<tr><th>{esc(a)}</th><td>{b}</td></tr>' for a, b in rows)
    return f'<section class="card cheat" style="border-top-color:{color}"><h3>{esc(title)}</h3><table>{body}</table></section>'

CSS = """
*{box-sizing:border-box}body{margin:0;background:#f1f0ec;font-family:Inter,'Segoe UI',system-ui,sans-serif;color:#1d1d1f}
.page{width:1500px;padding:34px 34px 20px}
header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px}
h1{font-size:34px;margin:0 0 6px;letter-spacing:-.5px}.sub{margin:0;color:#555;font-size:15px}
.stats{display:flex;gap:10px}.stat{background:#1d1d1f;color:#fff;border-radius:10px;padding:8px 14px;text-align:center;min-width:64px}
.stat b{display:block;font-size:22px}.stat span{font-size:11px;color:#c9c9c9}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.card{background:#fff;border:1px solid #e3e1db;border-top:6px solid #ccc;border-radius:14px;padding:18px 18px 16px}
.card h2{margin:0 0 4px;font-size:19px;display:flex;align-items:center;gap:10px}.ldot{width:12px;height:12px;border-radius:50%;display:inline-block}
.desc{margin:0 0 10px;color:#555;font-size:13px;line-height:1.4;min-height:36px}
.board{position:relative;margin:0 auto}
.k{position:absolute;width:54px;height:54px;border:1.5px solid #d9d6cf;border-radius:9px;background:#f7f6f3;display:flex;flex-direction:column;
   align-items:center;justify-content:center;text-align:center;box-shadow:0 2px 0 rgba(0,0,0,.06);padding:2px;line-height:1.1}
.k .t{font-weight:700;font-size:15px}.k.long .t{font-size:12px}.k.xlong .t{font-size:10.5px}.k .s{font-size:9px;margin-top:3px;opacity:.85}
.k.trans{border-style:dashed;background:#fff;color:#bbb;box-shadow:none;font-size:13px}
.k.none{border-style:dashed;background:#fff;box-shadow:none}
.k.held{background:#1d1d1f;border-color:#1d1d1f;color:#fff}.k.held .dot{width:12px;height:12px;border-radius:50%;background:#fff}
.k.held .s{font-size:8.5px;margin-top:4px}
.k.thumbk{border-width:2px;background:#fff}.k.thumbk .s{font-size:8.5px;font-weight:600}
.k.ghost{background:#fafaf8;border-color:#e6e4de;color:#a5a29b;box-shadow:none}
.lines{position:absolute;left:0;top:0;pointer-events:none}.lines line{stroke:#1d1d1f;stroke-width:1.6;stroke-dasharray:4 3}
.chip{position:absolute;transform:translate(-50%,-50%);background:#1d1d1f;color:#fff;font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px;white-space:nowrap}
.legend .lrow{display:flex;align-items:center;gap:14px;margin:8px 0;font-size:13px}.k.sk{position:relative;flex:none}
.swatches{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:13px;margin:4px 0 14px}.sw{display:flex;align-items:center;gap:6px}
.sw i{width:15px;height:15px;border:1.5px solid;border-radius:4px;display:inline-block}.note{font-size:13px;color:#444;line-height:1.5}
.cheats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:18px}
.cheat h3{margin:0 0 8px;font-size:16px}.cheat table{border-collapse:collapse;font-size:12.5px;width:100%}
.cheat th{text-align:left;padding:5px 8px 5px 0;vertical-align:top;width:44%;font-weight:600;border-bottom:1px solid #eee}
.cheat td{padding:5px 0;border-bottom:1px solid #eee;color:#333}
kbd{font-family:inherit;font-size:11px;background:#f0efeb;border:1px solid #d6d3cc;border-radius:4px;padding:0 4px;white-space:nowrap}
footer{display:flex;justify-content:space-between;color:#777;font-size:12px;margin-top:14px}
h2 + .desc{}
"""

def build():
    cards = [card("How to read this", "", f'<div class="legend">{legend()}</div>', "#e3e1db"),
             card("Key colors", "", colors(), "#e3e1db")]
    for name, title, desc, keys in LAYERS:
        assert len(keys) == 36, (name, len(keys))
        cards.append(card(title, desc, board(keys), LAYER_COLOR[name]))
    cards.append(card("Combos", "Press the joined keys at the same instant. Letter combos only work while typing on Base (or CAD mode), so they never fire mid-number.",
                      combo_board(), "#1d1d1f"))
    stats = [("36","keys"),("7","layers"),(str(len(COMBOS)),"combos"),("12","tap / hold keys"),("14","macros")]
    st = "".join(f'<div class="stat"><b>{a}</b><span>{b}</span></div>' for a, b in stats)
    cheats = "".join(cheat(*c) for c in CHEATS)
    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Chocofi keymap</title><style>{CSS}</style></head><body><div class="page">
<header><div><h1>Chocofi split keyboard — full keymap</h1><p class="sub">36 keys doing the work of a full keyboard, plus CAD, Blender and Obsidian workflows · ZMK firmware · QWERTY</p></div>
<div class="stats">{st}</div></header>
<div class="grid">{''.join(cards)}</div><div class="cheats">{cheats}</div>
<footer><span>Board: beekeeb Chocofi (Kailh Choc low profile, nice!nano v2, nice!view displays) · Firmware: ZMK v0.3 · live layer overlay: KeyPeek</span><span>Each half has 3×5 keys + 3 thumb keys</span></footer>
</div></body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print("wrote", OUT)

if __name__ == "__main__":
    build()
    if "--png" in sys.argv:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1500, "height": 1000}, device_scale_factor=2)
            pg.goto(OUT.resolve().as_uri()); pg.wait_for_timeout(300)
            pg.locator(".page").screenshot(path=str(OUT.with_suffix(".png")))
            b.close()
        try:  # shrink ~1.9 MB -> ~0.6 MB with no visible loss
            from PIL import Image
            png = OUT.with_suffix(".png")
            Image.open(png).convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(png, optimize=True)
        except ImportError:
            pass
        print("wrote", OUT.with_suffix(".png"))
