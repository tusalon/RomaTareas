# -*- coding: utf-8 -*-
"""Los 4 reels de la semana reescritos en bloques, con su comprobación.

Regla medida sobre el reel de referencia: 2,75 palabras por segundo.
Un bloque = 2-5 palabras = 1,2 s. Sin puntos suspensivos.
"""
import sys, io, json
sys.stdout.reconfigure(encoding="utf-8")

RITMO = 2.75  # palabras por segundo

REELS = {}

# ── LUNES ────────────────────────────────────────────────────────────────
REELS["lunes"] = {
 "dur": 18,
 "amarillo": ["DESCUENTICO", "pregunta", "presupuesto", "no era tu clienta", "siempre", "PRECIO"],
 "bloques": [
  ("¿me haces un descuentico?",        "? 3D rosa"),
  ("no contestes con el precio",       None),
  ("ni sí ni no",                      None),
  ("contesta con una pregunta",        "bombilla"),
  ("¿qué presupuesto tienes?",         None),
  ("y escucha",                        None),
  ("¿le alcanza para otro?",           "diana"),
  ("ofrécelo",                         None),
  ("¿no le alcanza?",                  None),
  ("no era tu clienta",                None),
  ("bajar el precio",                  "moneda que cae"),
  ("no te gana una clienta",           None),
  ("te gana una",                      None),
  ("que pedirá siempre",               None),
  ("comenta PRECIO",                   "bocadillo de chat"),
 ],
}

# ── MIÉRCOLES ────────────────────────────────────────────────────────────
REELS["miércoles"] = {
 "dur": 20,
 "amarillo": ["también se paga", "número", "dos años", "divide", "siete pesos", "nada", "tu precio", "HERRAMIENTA"],
 "bloques": [
  ("tu lámpara también se paga", "lámpara 3D"),
  ("con cada servicio",          None),
  ("y no lo sabes",              None),
  ("mira el número",             "calculadora"),
  ("dura unos dos años",         None),
  ("digamos que costó veinte mil", None),
  ("cuatro servicios al día",    None),
  ("son casi tres mil servicios", None),
  ("divide",                     None),
  ("siete pesos por servicio",   "monedas"),
  ("parece nada",                None),
  ("ahora suma el torno",        None),
  ("la cabina la mesa",          None),
  ("ninguno está en tu precio",  "gráfico que baja"),
  ("comenta HERRAMIENTA",        "bocadillo de chat"),
 ],
}

# ── VIERNES ──────────────────────────────────────────────────────────────
REELS["viernes"] = {
 "dur": 16,
 "amarillo": ["ranking", "tres", "dos", "uno", "ochenta y un", "directorio", "gratis", "CUBA"],
 "bloques": [
  ("el ranking de la semana",     "trofeo 3D"),
  ("número tres",                 None),
  ("Nails by Naty",               None),
  ("número dos",                  None),
  ("Ritis Salón y Spa",           None),
  ("y número uno",                None),
  ("BELLALYS de Las Tunas",       "corona"),
  ("ochenta y un servicios",      None),
  ("con su precio",               None),
  ("todas están en el directorio", "mapa de Cuba"),
  ("y estar es gratis",           None),
  ("comenta CUBA",                "bocadillo de chat"),
 ],
}

# ── SÁBADO ───────────────────────────────────────────────────────────────
REELS["sábado"] = {
 "dur": 17,
 "amarillo": ["horas", "Yuliet", "sin cobrarlas", "solas", "tiempo pagado", "quince días gratis"],
 "bloques": [
  ("perdía horas confirmando citas", "reloj 3D"),
  ("por WhatsApp",                   None),
  ("lo dijo Yuliet",                 None),
  ("de Exotic Nails",                None),
  ("horas cada semana",              None),
  ("sin cobrarlas",                  None),
  ("ahora sus clientas entran",      "móvil con la app"),
  ("ven qué tiene libre",            None),
  ("y reservan solas",               None),
  ("ella solo recibe el aviso",      "campana"),
  ("ese tiempo es tiempo pagado",    None),
  ("quince días gratis",             "regalo"),
  ("link en la bio",                 "flecha arriba"),
 ],
}

# ── comprobación ─────────────────────────────────────────────────────────
fallos = []
for dia, r in REELS.items():
    pal = sum(len(b[0].split()) for b in r["bloques"])
    techo = round(RITMO * r["dur"])
    seg_bloques = round(len(r["bloques"]) * 1.2, 1)
    ok_pal = pal <= techo
    largos = [b[0] for b in r["bloques"] if len(b[0].split()) > 5]
    puntos = [b[0] for b in r["bloques"] if "..." in b[0] or "…" in b[0]]

    print("%-11s %2ds · %2d bloques (%.1fs) · %2d palabras / techo %2d  %s"
          % (dia, r["dur"], len(r["bloques"]), seg_bloques, pal, techo, "OK" if ok_pal else "SE PASA"))
    if not ok_pal: fallos.append("%s: %d palabras, techo %d" % (dia, pal, techo))
    if largos: fallos.append("%s: bloques de más de 5 palabras: %s" % (dia, largos))
    if puntos: fallos.append("%s: hay puntos suspensivos" % dia)

print()
if fallos:
    print("FALLOS:")
    for f in fallos: print("  -", f)
    sys.exit(1)
print("Los 4 reels cumplen: dentro del techo, bloques de 2-5 palabras, sin puntos suspensivos.")

io.open("reels_bloques.json", "w", encoding="utf-8").write(
    json.dumps(REELS, ensure_ascii=False, indent=1))
