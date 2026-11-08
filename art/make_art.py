#!/usr/bin/env python3
"""Generates the banner (1600x500) and the Nexus thumbnail (1280x720) as SVG, then PNG via rsvg-convert.
Original artwork: no game assets. Font: Noto Serif Display (SIL Open Font License).
Same palette and frame as the author's other Crimson Desert mods."""
import math
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
GOLD1, GOLD2, GOLD3 = "#f6dc9a", "#d4a64a", "#8a6420"
# one colour per card group, in card order
GEMS = ["#e05a47", "#e8893a", "#4ade80", "#38bdf8", "#22d3ee", "#a78bfa", "#fbbf24"]


def defs():
    gems = "".join(
        f'<radialGradient id="gem{i}" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#ffffff"/>'
        f'<stop offset="0.35" stop-color="{c}"/><stop offset="1" stop-color="#1a0c06"/></radialGradient>'
        for i, c in enumerate(GEMS))
    return f'''<defs>
  <radialGradient id="bg" cx="50%" cy="45%" r="75%">
    <stop offset="0" stop-color="#3a1714"/><stop offset="0.55" stop-color="#1d0c0b"/><stop offset="1" stop-color="#080404"/>
  </radialGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GOLD1}"/><stop offset="0.55" stop-color="{GOLD2}"/><stop offset="1" stop-color="{GOLD3}"/>
  </linearGradient>
  {gems}
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" result="n"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.10 0"/>
  </filter>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
    <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity="0.7"/>
  </filter>
</defs>'''


def sigil(cx, cy, r, op=0.16):
    s = [f'<g opacity="{op}" stroke="{GOLD2}" fill="none">',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke-width="2"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.86}" stroke-width="1"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.55}" stroke-width="1.5" stroke-dasharray="2 6"/>']
    for i in range(72):
        a = i * math.tau / 72
        r1, r2 = r * 0.86, r * (0.93 if i % 6 else 1.0)
        s.append(f'<line x1="{cx+r1*math.cos(a):.1f}" y1="{cy+r1*math.sin(a):.1f}" '
                 f'x2="{cx+r2*math.cos(a):.1f}" y2="{cy+r2*math.sin(a):.1f}" stroke-width="1.2"/>')
    s.append('</g>')
    return '\n'.join(s)


def bracelet(cx, cy, s):
    """A gold bangle seen at an angle, with one socketed gem per buff group."""
    rx, ry, t = 150 * s, 62 * s, 26 * s
    p = [f'<g filter="url(#shadow)">',
         # back half of the band (darker), then the front half over the gems' backs
         f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GOLD3}" stroke-width="{t}"/>',
         f'<path d="M{cx-rx},{cy} A{rx},{ry} 0 0 0 {cx+rx},{cy}" fill="none" stroke="url(#gold)" stroke-width="{t}"/>',
         f'<path d="M{cx-rx},{cy} A{rx},{ry} 0 0 0 {cx+rx},{cy}" fill="none" stroke="{GOLD1}" stroke-width="{2*s}" '
         f'opacity="0.8" transform="translate(0,{-t*0.35})"/>']
    n = len(GEMS)
    for i in range(n):
        a = math.pi * (0.12 + 0.76 * i / (n - 1))  # spread along the front arc
        gx, gy = cx - rx * math.cos(a), cy + ry * math.sin(a)
        r = 12 * s * (0.8 + 0.2 * math.sin(a))
        p.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{r+3*s:.1f}" fill="{GOLD3}"/>'
                 f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{r:.1f}" fill="url(#gem{i})"/>')
    p.append('</g>')
    # sparks rising from the bracelet: the buffs you pick
    for i, c in enumerate(GEMS):
        a = math.pi * (0.12 + 0.76 * i / (n - 1))
        x = cx - rx * math.cos(a) * 0.9
        y = cy - 70 * s - 40 * s * math.sin(a)
        p.append(f'<g filter="url(#glow)"><path d="M{x:.1f},{y-12*s:.1f} L{x+4*s:.1f},{y:.1f} L{x:.1f},{y+12*s:.1f} '
                 f'L{x-4*s:.1f},{y:.1f} Z" fill="{c}" opacity="0.9"/></g>')
    return '\n'.join(p)


def frame(w, h, m=18):
    return (f'<rect x="{m}" y="{m}" width="{w-2*m}" height="{h-2*m}" fill="none" stroke="{GOLD2}" stroke-width="2" opacity="0.55"/>'
            f'<rect x="{m+8}" y="{m+8}" width="{w-2*m-16}" height="{h-2*m-16}" fill="none" stroke="{GOLD2}" stroke-width="1" opacity="0.3"/>')


def title(x, y, size):
    return (f'<g filter="url(#shadow)" font-family="Noto Serif Display" text-anchor="middle">'
            f'<text x="{x}" y="{y}" font-size="{size}" font-weight="bold" letter-spacing="{size*0.08:.1f}" '
            f'fill="url(#gold)">CUSTOM AXIOM BRACELET</text></g>')


def banner():
    W, H = 1600, 500
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{defs()}
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" filter="url(#grain)"/>
{sigil(330, 250, 210)}
{sigil(1330, 250, 170, 0.08)}
{frame(W, H)}
{bracelet(330, 285, 1.05)}
{title(1060, 200, 54)}
<line x1="740" y1="236" x2="1380" y2="236" stroke="{GOLD2}" stroke-width="1.5" opacity="0.6"/>
<circle cx="1060" cy="236" r="5" fill="{GOLD2}"/>
<text x="1060" y="290" text-anchor="middle" font-family="Noto Serif Display" font-size="34" fill="#efe3c8">Pick every buff, one by one</text>
<text x="1060" y="338" text-anchor="middle" font-family="Noto Serif Display" font-style="italic" font-size="24" fill="#c9b89a">29 options in 7 groups for Definitive Mod Manager</text>
<text x="1060" y="416" text-anchor="middle" font-family="Noto Serif Display" font-size="20" letter-spacing="6" fill="{GOLD2}" opacity="0.85">CRIMSON DESERT MOD</text>
</svg>'''


def thumbnail():
    W, H = 1280, 720
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{defs()}
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" filter="url(#grain)"/>
{sigil(640, 300, 250)}
{frame(W, H)}
{bracelet(640, 330, 1.35)}
{title(640, 530, 58)}
<line x1="300" y1="560" x2="980" y2="560" stroke="{GOLD2}" stroke-width="1.5" opacity="0.6"/>
<text x="640" y="610" text-anchor="middle" font-family="Noto Serif Display" font-size="34" fill="#efe3c8">Pick every buff, one by one</text>
<text x="640" y="660" text-anchor="middle" font-family="Noto Serif Display" font-size="20" letter-spacing="6" fill="{GOLD2}" opacity="0.85">CRIMSON DESERT MOD</text>
</svg>'''


for name, svg in (("banner", banner()), ("thumbnail", thumbnail())):
    (OUT / f"{name}.svg").write_text(svg)
    subprocess.run(["rsvg-convert", "-o", str(OUT / f"{name}.png"), str(OUT / f"{name}.svg")], check=True)
    print(OUT / f"{name}.png")
