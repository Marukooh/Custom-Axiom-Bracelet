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


def bracelet(cx, cy, s, uid="b"):
    """A thick gold bangle seen from above at an angle: back inner wall, top rim, then the outer face
    with cylindrical shading, engraved lines and one faceted gem per buff group set into it."""
    rx, ry = 165 * s, 66 * s          # outer rim
    w = 20 * s                        # rim thickness
    ri, ryi = rx - w, ry - w * ry / rx
    h = 46 * s                        # band height
    n = len(GEMS)
    out = [f'''<defs>
  <linearGradient id="{uid}face" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#4a3210"/><stop offset="0.18" stop-color="{GOLD3}"/>
    <stop offset="0.38" stop-color="{GOLD1}"/><stop offset="0.5" stop-color="#fff3c8"/>
    <stop offset="0.62" stop-color="{GOLD2}"/><stop offset="0.85" stop-color="{GOLD3}"/>
    <stop offset="1" stop-color="#3a260c"/>
  </linearGradient>
  <linearGradient id="{uid}faceV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0.35"/><stop offset="0.25" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.45"/>
  </linearGradient>
  <linearGradient id="{uid}rim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{GOLD1}"/><stop offset="0.5" stop-color="{GOLD2}"/><stop offset="1" stop-color="{GOLD1}"/>
  </linearGradient>
  <linearGradient id="{uid}wall" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5c3e14"/><stop offset="1" stop-color="#1e1206"/>
  </linearGradient>
  <mask id="{uid}hole"><rect x="{cx-rx-50}" y="{cy-ry-50}" width="{2*rx+100}" height="{2*ry+h+100}" fill="black"/>
    <ellipse cx="{cx}" cy="{cy}" rx="{ri}" ry="{ryi}" fill="white"/>
    <ellipse cx="{cx}" cy="{cy+h}" rx="{ri}" ry="{ryi}" fill="black"/></mask>
  <radialGradient id="{uid}aura" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{GOLD2}" stop-opacity="0.35"/><stop offset="1" stop-color="{GOLD2}" stop-opacity="0"/>
  </radialGradient>
</defs>''']
    # warm glow behind and soft shadow under the bangle
    out.append(f'<ellipse cx="{cx}" cy="{cy+h*0.4}" rx="{rx*1.45}" ry="{ry*2.6}" fill="url(#{uid}aura)"/>')
    out.append(f'<ellipse cx="{cx}" cy="{cy+h+ry*0.55}" rx="{rx*0.95}" ry="{ry*0.35}" fill="#000" opacity="0.55" filter="url(#glow)"/>')
    out.append('<g filter="url(#shadow)">')
    # inner back wall, visible through the opening
    out.append(f'<rect x="{cx-rx}" y="{cy-ry}" width="{2*rx}" height="{2*ry+h}" fill="url(#{uid}wall)" mask="url(#{uid}hole)"/>')
    # top rim (ring between outer and inner ellipse)
    out.append(f'<path fill-rule="evenodd" fill="url(#{uid}rim)" stroke="{GOLD3}" stroke-width="{1.2*s}" d="'
               f'M{cx-rx},{cy} A{rx},{ry} 0 1 0 {cx+rx},{cy} A{rx},{ry} 0 1 0 {cx-rx},{cy} Z '
               f'M{cx-ri},{cy} A{ri},{ryi} 0 1 0 {cx+ri},{cy} A{ri},{ryi} 0 1 0 {cx-ri},{cy} Z"/>')
    # outer front face
    face = (f'M{cx-rx},{cy} A{rx},{ry} 0 0 0 {cx+rx},{cy} L{cx+rx},{cy+h} A{rx},{ry} 0 0 1 {cx-rx},{cy+h} Z')
    out.append(f'<path d="{face}" fill="url(#{uid}face)" stroke="#3a260c" stroke-width="{1.2*s}"/>')
    out.append(f'<path d="{face}" fill="url(#{uid}faceV)"/>')
    # engraved border lines and a bright edge where the rim meets the face
    for dy, col, op, sw in ((h * 0.16, "#3a260c", 0.8, 1.6), (h * 0.84, "#3a260c", 0.8, 1.6),
                            (h * 0.19, GOLD1, 0.5, 1.0), (0.8 * s, "#fff6d8", 0.9, 1.6)):
        out.append(f'<path d="M{cx-rx},{cy+dy} A{rx},{ry} 0 0 0 {cx+rx},{cy+dy}" fill="none" stroke="{col}" '
                   f'stroke-width="{sw*s}" opacity="{op}"/>')
    # gems: bezel + faceted stone, foreshortened toward the sides
    for i in range(n):
        a = math.pi * (0.14 + 0.72 * i / (n - 1))
        gx = cx - rx * math.cos(a)
        gy = cy + ry * math.sin(a) + h * 0.5
        k = 0.45 + 0.55 * math.sin(a)          # side foreshortening
        gr, gh = 15 * s * k, 15 * s
        c = GEMS[i]
        out.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{gr+4.5*s*k:.1f}" ry="{gh+4.5*s:.1f}" fill="url(#gold)" '
                   f'stroke="#3a260c" stroke-width="{1.2*s}"/>')
        out.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{gr:.1f}" ry="{gh:.1f}" fill="url(#gem{i})" '
                   f'stroke="#1a0c06" stroke-width="{0.8*s}"/>')
        # table facet and two highlight facets
        out.append(f'<path d="M{gx-gr*0.45:.1f},{gy-gh*0.15:.1f} L{gx:.1f},{gy-gh*0.55:.1f} L{gx+gr*0.45:.1f},{gy-gh*0.15:.1f} '
                   f'L{gx:.1f},{gy+gh*0.3:.1f} Z" fill="{c}" stroke="#fff" stroke-opacity="0.35" stroke-width="{0.8*s}"/>')
        out.append(f'<path d="M{gx-gr*0.55:.1f},{gy-gh*0.35:.1f} L{gx-gr*0.15:.1f},{gy-gh*0.62:.1f} L{gx-gr*0.05:.1f},{gy-gh*0.4:.1f} Z" '
                   f'fill="#fff" opacity="0.75"/>')
        out.append(f'<circle cx="{gx+gr*0.35:.1f}" cy="{gy+gh*0.45:.1f}" r="{1.6*s:.1f}" fill="#fff" opacity="0.5"/>')
    out.append('</g>')
    # small four-point glints on the metal
    for gx, gy, r in ((cx - rx * 0.55, cy + ry * 0.83, 9), (cx + rx * 0.72, cy + ry * 0.7 + h * 0.1, 7),
                      (cx + rx * 0.2, cy - ry * 0.98, 6)):
        r *= s
        out.append(f'<path filter="url(#glow)" fill="#fffbe8" d="M{gx},{gy-r} Q{gx},{gy} {gx+r},{gy} Q{gx},{gy} {gx},{gy+r} '
                   f'Q{gx},{gy} {gx-r},{gy} Q{gx},{gy} {gx},{gy-r} Z"/>')
    return '\n'.join(out)


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
{bracelet(330, 235, 1.0, "bn")}
{title(1060, 200, 54)}
<line x1="740" y1="236" x2="1380" y2="236" stroke="{GOLD2}" stroke-width="1.5" opacity="0.6"/>
<circle cx="1060" cy="236" r="5" fill="{GOLD2}"/>
<text x="1060" y="290" text-anchor="middle" font-family="Noto Serif Display" font-size="34" fill="#efe3c8">Pick every buff, one by one</text>
<text x="1060" y="338" text-anchor="middle" font-family="Noto Serif Display" font-style="italic" font-size="24" fill="#c9b89a">28 options in 7 groups for Definitive Mod Manager</text>
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
{bracelet(640, 250, 1.3, "th")}
{title(640, 530, 58)}
<line x1="300" y1="560" x2="980" y2="560" stroke="{GOLD2}" stroke-width="1.5" opacity="0.6"/>
<text x="640" y="610" text-anchor="middle" font-family="Noto Serif Display" font-size="34" fill="#efe3c8">Pick every buff, one by one</text>
<text x="640" y="660" text-anchor="middle" font-family="Noto Serif Display" font-size="20" letter-spacing="6" fill="{GOLD2}" opacity="0.85">CRIMSON DESERT MOD</text>
</svg>'''


for name, svg in (("banner", banner()), ("thumbnail", thumbnail())):
    (OUT / f"{name}.svg").write_text(svg)
    subprocess.run(["rsvg-convert", "-o", str(OUT / f"{name}.png"), str(OUT / f"{name}.svg")], check=True)
    print(OUT / f"{name}.png")
