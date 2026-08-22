# RomaTareas

Lista de tareas personal con **avisos al móvil**, plazos y marcar completado.
Construida sobre lo que ya usas: Supabase, GitHub Pages y ntfy.

```
tusalon.github.io/RomaTareas     la web (una sola página, sin framework)
          ↕
   Supabase · tabla `tareas`     el estado
          ↑
GitHub Actions · cada hora       lee lo que vence → ntfy → tu móvil
```

---

## Puesta en marcha

Cuatro pasos. Los dos primeros solo los puedes dar tú.

### 1. Crear la tabla en Supabase

Abre el **SQL Editor** del proyecto `zorhclhvykikaachfrmp`, pega el contenido de
[`sql/tareas.sql`](sql/tareas.sql) y ejecútalo. Crea la tabla, el índice y la política de acceso.

### 2. Suscribirte al topic en el móvil

En la app de **ntfy** (la misma donde recibes los avisos de reservas), añade el topic:

```
roma-tareas
```

Va aparte de `rservas-roma` a propósito, para que los recordatorios personales no
se mezclen con las notificaciones del negocio.

### 3. Subir el repo y activar Pages

```bash
git init && git add -A && git commit -m "RomaTareas"
git remote add origin https://github.com/tusalon/RomaTareas.git
git push -u origin main
```

Luego en **Settings → Pages**, servir desde la rama `main`.
El cron de Actions arranca solo en la siguiente hora en punto.

### 4. Entrar y elegir el PIN

Abre la web, escribe un PIN de 4 o más caracteres. La primera vez carga solas las
tareas del plan de contenido. El PIN queda guardado en ese navegador.

---

## Comprobar que funciona

```bash
node scripts/avisar.test.js
```
Verifica la lógica de fechas y recurrencias. Debe decir `OK`.

```bash
node scripts/avisar.js --seco
```
Muestra qué avisaría, sin enviar nada.

```bash
node scripts/avisar.js
```
Envía de verdad. **Crea antes una tarea que venza en una hora**: si no llega la
notificación al móvil, nada más importa.

También puedes lanzarlo desde **Actions → Avisos de tareas → Run workflow**.

---

## Cómo se comporta

**Avisa** de lo que vence en las próximas 24 horas.
**Repite** el aviso de lo vencido una vez al día, no cada hora.
**Dos botones** en la notificación: *Completar*, que marca la tarea sin abrir nada,
y *Abrir*, que lleva a la web.

**Recurrencias.** Al completar una tarea que se repite, aparece sola la siguiente.
La fecha se calcula desde su plazo anterior, no desde hoy, para que una tarea
semanal no se vaya corriendo de día. Esto lo resuelven tanto la web como el cron,
porque el botón de la notificación no puede ejecutar el código del navegador.

**Tareas que carga al principio:** la tanda de historias del domingo, correr
`radar.py`, grabar los reels de La Escuela, grabar los del viernes y sábado el
jueves, responder comentarios cada día, publicar la pieza del día, revisar las
métricas el viernes y podar la peor sección cada mes.

---

## Dos límites que conviene saber

**El cron de GitHub Actions no es puntual.** Puede retrasarse entre 5 y 15 minutos.
Para recordatorios de tareas da igual, pero no lo uses para nada que dependa del minuto exacto.

**Se desactiva solo si el repo pasa 60 días sin actividad.** GitHub lo hace con todos
los cron. Si algún día dejan de llegar avisos, es lo primero que hay que mirar:
Actions → Avisos de tareas → reactivar.

---

## Sobre la privacidad — dicho claro

El PIN es **una puerta con llave, no una caja fuerte**.

La anon key de Supabase es pública — está en el JavaScript de RomaHub, a la vista de
cualquiera. Quien la tenga y además adivine tu PIN podría leer tus tareas. Postgres RLS
no puede exigir por sí solo que el cliente aplique el filtro del PIN.

Es el mismo nivel de confianza que ya aceptas con ntfy: cualquiera que sepa el topic
`rservas-roma` puede leer esas notificaciones hoy. Para una lista de tareas de contenido
es proporcionado — pero que sea una decisión, no una suposición.

**Si algún día entra ahí algo sensible**, el siguiente paso es Supabase Auth de verdad.
