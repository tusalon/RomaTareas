# -*- coding: utf-8 -*-
"""Genera briefing.json — lo que RomaTareas te dice cada mañana."""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")

D = {}

# ══════════════════ SÁBADO 22 · PRUEBA REAL ══════════════════
D["2026-08-22"] = {
 "titular": "Hoy es el único día de la semana que empujamos al producto pago.",
 "porque": "Uno de siete. Después de seis días dando sin pedir nada, hoy te has ganado el derecho a hablar de precio.",
 "necesito": "Una captura de la app de un salón real: su nombre, sus colores, sus servicios.",
 "cuerpo": """LA PIEZA
Reel de 24s con el testimonio de Carla:
"Las clientas piensan que invertí miles."

El segundo 15 es el que convierte — "menos que una manicura".
Traduce los 1.500 CUP a algo que cobras en una hora, y desarma
el precio sin decir la cifra.

LA IMAGEN
Negro para la cita del principio y el cierre.
Crema para la captura de la app.
Magenta para "menos que una manicura" y los 15 días.

La captura del segundo 5 es imprescindible. Sin ella el testimonio
es una frase sin respaldo, y hoy es justo el día que no puede
sonar a promesa.

EL CTA
Hoy sí: "link en la bio". Es el único día que la bio y el CTA
coinciden, porque la bio va a la página comercial.

LAS 6 HISTORIAS (hoy van dos CTA)
1 · encuesta: "¿cuántos mensajes recibiste hoy solo para cuadrar
    una cita?" → Menos de 5 / Perdí la cuenta
2 · valor: "El tiempo que pasas cuadrando citas también es trabajo.
    Solo que no te lo pagan."
3 · prueba: captura del panel con la semana llena, sin un WhatsApp
4 · NUEVOS EN EL HUB — bienvenida con nombre:
       💅 Amy Studio — Plaza de la Revolución, La Habana
       👁️ NEEA Lashes — Camagüey
    Etiquétalas y mándales la historia por privado para que la
    compartan. Ese reenvío es lo que hace que la sección se pague sola.
5 · CTA: 15 días gratis, link en bio
6 · CTA: "¿aún no estás en el directorio? Responde CUBA" ← gratis

Cierras el día con la puerta barata abierta, no con el precio.

MAÑANA
Domingo: la tanda. Hora y media y dejas la semana entera lista."""
}

# ══════════════════ DOMINGO 23 · LA TANDA ══════════════════
D["2026-08-23"] = {
 "titular": "Hoy vamos a dejar la semana entera lista.",
 "porque": "Es el día que decide si el ritmo aguanta. 33 historias no salen improvisando: hoy pre-armamos 18 y el resto sale solo durante la semana.",
 "necesito": "Hora y media tuya y el móvil. Nada más.",
 "cuerpo": """━━━ PRIMERO, LOS DATOS (10 min) ━━━
Corre esto y guarda lo que salga, alimenta las historias de valor:

  python radar.py precios
  python radar.py nuevos

━━━ LAS 18 HISTORIAS PRE-ARMADAS (60 min) ━━━
Todas son texto sobre color. Fondo crema, texto negro, la palabra
clave en magenta. Se hacen en Canva en tanda, una plantilla y a
cambiar el texto.

▸ LAS 6 DE VALOR — slot 2 de cada día

LUNES · "La rebaja no te gana una clienta. Te gana una que va a
         pedirte rebaja siempre."
MARTES · "Un turno doble no te cuesta un turno. Te cuesta una clienta."
MIÉRCOLES · "El torno también se gasta. ¿Está en tu precio?"
JUEVES · "Especializarte no cierra puertas. Hace que te encuentren
          las clientas correctas."
VIERNES · "Publicar tus servicios con precio es lo que hace que te
           busquen sin conocerte."
SÁBADO · "El tiempo que pasas cuadrando citas también es trabajo.
          Solo que no te lo pagan."

▸ LAS 6 CTA — slot 5 de cada día

LUNES · "¿Te piden rebaja seguido? Responde PRECIO"
MARTES · "¿Has dado dos turnos a la misma hora? Responde AGENDA"
MIÉRCOLES · "Responde HERRAMIENTA y te paso la cuenta hecha"
JUEVES · "¿Quieres salir en el próximo Salón de la Semana?
          Responde SALÓN"   ← rebote, no venta dura
VIERNES · "¿No apareces en el directorio? Responde CUBA. Es gratis"
SÁBADO · "15 días gratis para probarlo. Link en la bio 👆"

▸ LOS 6 GANCHOS — slot 1, encuestas de dos opciones

LUNES · "¿Cuántas veces te pidieron rebaja este mes?"
         → Ninguna / Perdí la cuenta
MARTES · "¿Has dado dos turnos a la misma hora?"
         → Sí, más de una vez / Nunca (aún)
MIÉRCOLES · "¿Sabes cuánto te costó tu lámpara?"
         → Exacto / Ni idea
JUEVES · "¿Haces de todo o te especializas?"
         → De todo / Solo lo mío
VIERNES · "¿Tienes tus servicios publicados con precio?"
         → Todos / Ninguno
SÁBADO · "¿Cuántos mensajes recibiste hoy para cuadrar citas?"
         → Menos de 5 / Perdí la cuenta

━━━ LOS DOS REELS DE LA ESCUELA (20 min) ━━━
Lunes y miércoles se graban HOY, juntos. Los guiones están en sus
tareas. Los del viernes y sábado no: dependen de datos de la semana
y se hacen el jueves.

━━━ LO QUE QUEDA PARA LA SEMANA ━━━
15 historias reactivas: los slots 3 (prueba) y 4 (comunidad). Esas
salen de lo que pase — un comentario, un negocio nuevo, una respuesta
de la caja de preguntas. No se pueden pre-armar y está bien así."""
}

# ══════════════════ LUNES 24 ══════════════════
D["2026-08-24"] = {
 "titular": "Hoy vamos a publicar el reel del descuentico.",
 "porque": "La Escuela no menciona ninguna app. Es el pilar que trae seguidoras que aún no te conocen, y el que más se guarda. Hoy no vendemos nada.",
 "necesito": "Nada. El reel ya lo grabaste ayer.",
 "cuerpo": """LA PIEZA
Reel de 25s. Gancho: "¿ME HACES UN DESCUENTICO?" en el frame 0,
sin fade — tiene que leerse en mute.
El guion completo está en la tarea de hoy.

LA IMAGEN
Fondo negro con texto blanco enorme para el gancho y el cierre.
Fondo magenta para la respuesta ("¿Qué presupuesto tienes?").
Fondo crema para los dos casos del medio.
Sin capturas de app: hoy no se nombra ningún producto.

El segundo 21 es el que se guarda — la frase de que la rebaja te
gana una clienta que va a pedirte rebaja siempre. Que se lea entera,
sin prisa.

LAS 5 HISTORIAS
1 · encuesta de la rebaja      2 · la frase de valor
3 · captura de un DM real pidiendo rebaja (tapa el nombre)
4 · repost de un trabajo del directorio
5 · CTA: responde PRECIO

DESPUÉS
Responde cada PRECIO en menos de una hora. Ese es el trabajo
de verdad del día, no el post."""
}

# ══════════════════ MARTES 25 ══════════════════
D["2026-08-25"] = {
 "titular": "Hoy toca el carrusel del turno doble.",
 "porque": "El dolor más universal del oficio y el que más comentarios genera. Toca Rservasroma sin pedirte que compres nada.",
 "necesito": "Una captura del panel con un horario ya ocupado, en gris.",
 "cuerpo": """LA PIEZA
Carrusel de 7 slides. El texto exacto está en la tarea.

LA IMAGEN
Slides 1 a 4 en negro: es la parte que duele.
Slides 5 y 6 en magenta: es donde aparece la salida.
Slide 7 negro con la palabra AGENDA grande y en magenta.

El slide 6 necesita la captura del panel. Sin ella el carrusel se
queda en queja; con ella se convierte en demostración.

LAS 5 HISTORIAS
1 · encuesta del turno doble   2 · la frase de valor
3 · la misma captura del panel  4 · comunidad
5 · CTA: responde AGENDA
+ 1 extra de rebote: "¿quieres salir en el próximo Radar?"

OJO
El Radar de Precios es quincenal y el último salió el 18.
El próximo es el martes 1 de septiembre. Hoy va El Caos."""
}

# ══════════════════ MIÉRCOLES 26 ══════════════════
D["2026-08-26"] = {
 "titular": "Hoy vamos con la lámpara que nadie mete en el precio.",
 "porque": "Segundo día de La Escuela, otra vez sin producto. Prepara el terreno de RomaFinanzas sin nombrarlo: cuando alguien aplique esta cuenta a mano, va a querer una herramienta.",
 "necesito": "Nada. Grabado el domingo.",
 "cuerpo": """LA PIEZA
Reel de 28s. Una cuenta hecha en voz alta, paso a paso.

LA IMAGEN
Los números son los protagonistas. Fondo blanco con las cifras
grandes en negro para la cuenta, y el resultado (7 CUP por servicio)
en magenta a pantalla completa.
Nada de capturas. Es matemática, no producto.

⚠️ CUIDADO CON UN DATO
Los 20.000 CUP de la lámpara son un EJEMPLO inventado. En el video
dilo así: "digamos que te costó". Si lo presentas como precio de
mercado y alguien lo desmiente, pierdes la credibilidad de toda
la cuenta.

LAS 5 HISTORIAS
1 · encuesta del costo de la lámpara   2 · la frase de valor
3 · captura de la ficha de costo        4 · comunidad
5 · CTA: responde HERRAMIENTA"""
}

# ══════════════════ JUEVES 27 ══════════════════
D["2026-08-27"] = {
 "titular": "Hoy destacamos a Liz Nails, de Playa.",
 "porque": "Es el contenido que más lealtad genera. Ella lo comparte, su familia lo comparte, sus clientas lo comparten. Y para salir hay que estar en el directorio — eso solo mete negocios sin vender nada.",
 "necesito": "Su permiso y sus respuestas en audio. Si no llegaron, cambia de negocio y no publiques.",
 "cuerpo": """EL ÁNGULO
De sus 16 servicios, casi todos son gel: poly gel, soft gel, gel
de construcción, base rubber. No hace de todo — hace gel.
En un directorio donde casi todas ofrecen lo mismo, la que elige
qué NO hacer destaca sola.

LA PIEZA
Carrusel de 7 slides. Texto completo en la tarea.

LA IMAGEN
Todo en crema, salvo el slide de su consejo, que va en magenta.
Es una pieza cálida, no de impacto: aquí no gritamos.
Si te manda fotos de su trabajo, van en los slides 2 y 3.

⚠️ NO PUBLICAR
Su poly gel está en 2.000 CUP y la mediana nacional del gel es 1.500.
Encaja con el relato de especialista, pero NO lo digas: nunca se
compara el precio de un negocio identificable con nadie.

TAMBIÉN HOY
Graba los reels del viernes y el sábado. El del viernes necesita
datos frescos, así que corre radar.py ranking antes.

LAS 5 HISTORIAS
1 · encuesta especializarse vs hacer de todo   2 · la frase de valor
3 · trabajo de Liz (con permiso)                4 · etiquétala
5 · CTA de rebote: responde SALÓN"""
}

# ══════════════════ VIERNES 28 ══════════════════
D["2026-08-28"] = {
 "titular": "Hoy sí vendemos — pero pedimos algo gratis.",
 "porque": "El Ranking es el día que la gente entra a ver si salió. Y quien sale, lo comparte con su audiencia entera. Cada negocio del ranking es un altavoz que no te cuesta nada.",
 "necesito": "Correr radar.py ranking HOY. Los números de hace una semana ya no sirven.",
 "cuerpo": """⚠️ ANTES DE NADA
  python radar.py ranking

Los datos cambian rápido: BELLALYS pasó de 36 a 81 servicios en
cuatro días. Publicar el número viejo es publicar un dato falso.

NO uses el ranking de valoraciones. Hay 6 reseñas en toda la base
y ningún negocio llega a 3. El script se niega a generarlo por eso.
Usa el de negocios con más servicios publicados: premia constancia
y tiene datos de sobra.

LA PIEZA
Reel de 20s con el top 3 en cuenta atrás.

LA IMAGEN
Negro para el título. Crema para cada puesto, entrando desde abajo
uno a uno. Magenta para el cierre y para la palabra GRATIS.
El número 1 lleva un brillo — es el premio.

ROTA LA CATEGORÍA
Esta semana el top general. La próxima "las que empiezan" o "Oriente".
Si gana siempre la misma, el resto deja de mirar.

LAS 6 HISTORIAS (hoy van dos CTA)
1 · encuesta de servicios publicados   2 · la frase de valor
3 · captura del ranking                 4 · etiqueta a los tres
5 · CTA: responde CUBA (gratis)
6 · CTA: mira la destacada DIRECTORIO"""
}

# ══════════════════ SÁBADO 29 ══════════════════
D["2026-08-29"] = {
 "titular": "Hoy es el único día que empujamos al producto pago.",
 "porque": "Uno de siete. Y es también el día que mueve a quien ya paga hacia RomaFinanzas y RomaCrece — ese trabajo no lo hacía nadie, y por eso hay un solo cliente premium.",
 "necesito": "Una captura de la app de un salón real: su nombre, sus colores, sus servicios.",
 "cuerpo": """LA PIEZA
Reel de 22s con el testimonio de Yuliet, de Exotic Nails.
Cita literal, sin adornar.

LA IMAGEN
Negro para la cita. Crema para la captura de la app. Magenta para
el cierre y los 15 días.

La captura del segundo 9 es imprescindible. Sin ella el testimonio
es una frase sin respaldo, y el sábado es justo el día que no puede
sonar a promesa.

EL CTA
Hoy sí: "link en la bio". Es el único día que la bio y el CTA
coinciden, porque la bio va a la página comercial.

LAS 6 HISTORIAS (dos CTA otra vez)
1 · encuesta de los mensajes    2 · la frase de valor
3 · captura del panel con la agenda llena
4 · Nuevos en el Hub: bienvenida con nombre a los que entraron
5 · CTA: 15 días gratis, link en bio
6 · CTA: responde CUBA (gratis) ← cierras con la puerta barata abierta

MAÑANA
Domingo otra vez. Pídeme la tanda de la semana del 31."""
}

RESUMEN = [
 ["Sábado 22",   "Reel · Prueba Real — Carla", "Sí · prueba 15 días"],
 ["Domingo 23",  "La tanda — 18 historias + 2 reels", "No"],
 ["Lunes 24",    "Reel · La Escuela — el descuentico", "No"],
 ["Martes 25",   "Carrusel · El Caos — el turno doble", "No"],
 ["Miércoles 26","Reel · La Escuela — la lámpara", "No"],
 ["Jueves 27",   "Carrusel · Salón de la Semana — Liz Nails", "No"],
 ["Viernes 28",  "Reel · El Ranking", "Sí · RomaHub gratis"],
 ["Sábado 29",   "Reel · Prueba Real", "Sí · prueba 15 días"],
]

salida = {
 "semana": "22 al 29 de agosto de 2026",
 "reparto": "6 publicaciones · 2 venden (33%) — 33 historias · 10 venden (30%)",
 "dias": D,
 "resumen": [{"dia": r[0], "pieza": r[1], "vende": r[2]} for r in RESUMEN],
}

io.open("briefing.json", "w", encoding="utf-8").write(
    json.dumps(salida, ensure_ascii=False, indent=1))
print("briefings generados:", len(D))
for k in sorted(D):
    print("  ", k, "·", D[k]["titular"])
