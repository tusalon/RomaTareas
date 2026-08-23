# -*- coding: utf-8 -*-
"""Quita el fondo de los iconos y recorta al objeto.

    python scripts/quitar_fondo.py

Lee iconos/origen/*.jpeg y escribe iconos/alfa/*.png con transparencia.

Dos decisiones que no son obvias y que costaron una pasada fallida:

1. El fondo NO se quita por color, se quita por CONEXIÓN: solo desaparece lo
   claro que toca el borde de la imagen. Un umbral de color a secas agujerearía
   los puntos blancos del bocadillo y la esfera del reloj, que también son casi
   blancos pero están dentro del objeto.

2. El fondo no es blanco liso. La "iluminación de estudio" del prompt le mete
   un degradado que baja hasta 230 en las esquinas. Con el umbral en 236 el
   relleno se paraba a medio camino y dejaba un halo sucio alrededor.
   De ahí el umbral bajo, con la SATURACIÓN como guardián: el fondo es gris
   (sus tres canales casi iguales), los amarillos claros del objeto no.

Efecto secundario deseado: el contorno blanco de sticker que el modelo le puso
a la calculadora y al mapa de Cuba desaparece solo, porque también es claro y
también toca el borde.
"""
import os, sys
from collections import deque
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "iconos")
ORIGEN = os.path.join(RAIZ, "origen")
DESTINO = os.path.join(RAIZ, "alfa")

CLARO = 200      # por debajo de esto ya no es fondo, ni con degradado
GRIS = 26        # diferencia máxima entre canales para considerarlo gris
SUAVE = 30       # ancho de la rampa de alfa en el borde, en niveles
MARGEN = 20      # píxeles transparentes alrededor tras recortar

try:
    import numpy as np
except ImportError:
    np = None


def mascara_fondo(im):
    """True donde hay fondo: claro, gris y conectado al borde."""
    w, h = im.size
    if np is not None:
        a = np.asarray(im.convert("RGB")).astype(np.int16)
        mn = a.min(axis=2)
        mx = a.max(axis=2)
        cand = (mn >= CLARO) & ((mx - mn) <= GRIS)

        # Propagación desde el borde: se expande la marca hasta que deja de crecer.
        marca = np.zeros_like(cand)
        marca[0, :] = cand[0, :]
        marca[-1, :] = cand[-1, :]
        marca[:, 0] = cand[:, 0]
        marca[:, -1] = cand[:, -1]
        while True:
            crecida = marca.copy()
            crecida[1:, :] |= marca[:-1, :]
            crecida[:-1, :] |= marca[1:, :]
            crecida[:, 1:] |= marca[:, :-1]
            crecida[:, :-1] |= marca[:, 1:]
            crecida &= cand
            if np.array_equal(crecida, marca):
                return marca, mn
            marca = crecida

    # Sin numpy: misma idea, en cola.
    px = im.load()
    def es_fondo(x, y):
        r, g, b, _ = px[x, y]
        return min(r, g, b) >= CLARO and (max(r, g, b) - min(r, g, b)) <= GRIS
    vis = bytearray(w * h)
    cola = deque()
    for x in range(w):
        for y in (0, h - 1):
            if es_fondo(x, y) and not vis[y * w + x]:
                vis[y * w + x] = 1; cola.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if es_fondo(x, y) and not vis[y * w + x]:
                vis[y * w + x] = 1; cola.append((x, y))
    while cola:
        x, y = cola.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and not vis[ny*w+nx] and es_fondo(nx, ny):
                vis[ny*w+nx] = 1; cola.append((nx, ny))
    return vis, None


def quitar(ruta_in, ruta_out):
    im = Image.open(ruta_in).convert("RGBA")
    w, h = im.size
    marca, mn = mascara_fondo(im)

    if np is not None:
        a = np.asarray(im).copy()
        alfa = a[:, :, 3].astype(np.int16)
        alfa[marca] = 0
        # Rampa en el borde: un corte duro deja dientes de sierra, y el JPEG ya
        # trae medio tono ahí.
        #
        # La rampa SOLO se aplica a los píxeles que tocan el fondo, no a todo
        # lo claro de la imagen. Aplicarla a todo lo claro borró la esfera del
        # reloj y la pantalla de la calculadora, que son claras pero están
        # dentro del objeto: quedaron como agujeros negros.
        vecino = np.zeros_like(marca)
        vecino[1:, :] |= marca[:-1, :]
        vecino[:-1, :] |= marca[1:, :]
        vecino[:, 1:] |= marca[:, :-1]
        vecino[:, :-1] |= marca[:, 1:]
        for _ in range(2):          # ensancha la franja un par de píxeles
            crece = vecino.copy()
            crece[1:, :] |= vecino[:-1, :]
            crece[:-1, :] |= vecino[1:, :]
            crece[:, 1:] |= vecino[:, :-1]
            crece[:, :-1] |= vecino[:, 1:]
            vecino = crece
        borde = vecino & (~marca) & (mn > CLARO - SUAVE)
        alfa[borde] = np.clip(((CLARO - mn[borde] + SUAVE) * 255) // SUAVE, 0, 255)
        a[:, :, 3] = alfa.astype(np.uint8)
        im = Image.fromarray(a, "RGBA")
    else:
        px = im.load()
        for y in range(h):
            for x in range(w):
                r, g, b, _ = px[x, y]
                if marca[y * w + x]:
                    px[x, y] = (r, g, b, 0)

    caja = im.getbbox()
    if caja:
        x0, y0, x1, y1 = caja
        im = im.crop((max(0, x0 - MARGEN), max(0, y0 - MARGEN),
                      min(w, x1 + MARGEN), min(h, y1 + MARGEN)))
    im.save(ruta_out, "PNG")
    return im.size


def main():
    os.makedirs(DESTINO, exist_ok=True)
    archivos = sorted(f for f in os.listdir(ORIGEN) if f.lower().endswith((".jpeg", ".jpg", ".png")))
    if not archivos:
        print("No hay imágenes en", ORIGEN); return
    print("motor:", "numpy" if np is not None else "cola (lento)")
    for f in archivos:
        nombre = os.path.splitext(f)[0] + ".png"
        w, h = quitar(os.path.join(ORIGEN, f), os.path.join(DESTINO, nombre))
        print("  %-22s → %dx%d" % (nombre, w, h))
    print("\n%d iconos con transparencia en iconos/alfa/" % len(archivos))


if __name__ == "__main__":
    main()
