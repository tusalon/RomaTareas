// Prueba de la logica de fechas. Sin framework: node scripts/avisar.test.js
//
// Lo que se comprueba es lo que rompe en silencio: una recurrencia mal
// calculada no da error, simplemente reprograma la tarea para el dia
// equivocado y no te enteras hasta que fallas una semana.

const assert = require('node:assert/strict');
const { proximaFecha, textoPlazo } = require('./avisar.js');

const DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

// --- diaria -----------------------------------------------------------------
const lunes = new Date(2026, 7, 17, 9, 0); // 17 ago 2026 es lunes
assert.equal(lunes.getDay(), 1, 'la fecha base debe ser lunes');

const d1 = proximaFecha(lunes, 'diaria');
assert.equal(d1.getDate(), 18);
assert.equal(d1.getHours(), 9, 'la hora se conserva');

// --- semanal ----------------------------------------------------------------
// Desde un lunes, "cada domingo" cae en el domingo siguiente.
const dom = proximaFecha(lunes, 'semanal:0');
assert.equal(dom.getDay(), 0);
assert.equal(dom.getDate(), 23, 'el domingo siguiente al 17 es el 23');

// El caso que importa: completar una tarea semanal EL MISMO DIA que toca no
// puede reprogramarla para hoy otra vez, o se avisa en bucle.
const otroLunes = proximaFecha(lunes, 'semanal:1');
assert.equal(otroLunes.getDay(), 1);
assert.equal(otroLunes.getDate(), 24, 'salta a la semana siguiente, no se queda en hoy');
assert.ok(otroLunes > lunes, 'siempre avanza');

// Todos los dias de la semana resuelven al dia correcto y hacia adelante.
for (let n = 0; n <= 6; n++) {
  const p = proximaFecha(lunes, `semanal:${n}`);
  assert.equal(p.getDay(), n, `semanal:${n} debe caer en ${DIAS[n]}`);
  assert.ok(p > lunes, `semanal:${n} debe ir hacia adelante`);
  assert.ok((p - lunes) / 86400000 <= 7, `semanal:${n} no debe saltarse una semana entera`);
}

// --- mensual ----------------------------------------------------------------
const mes = proximaFecha(new Date(2026, 0, 31, 10, 0), 'mensual');
assert.ok(mes > new Date(2026, 0, 31), 'mensual avanza aunque el mes destino sea mas corto');

// --- sin recurrencia --------------------------------------------------------
assert.equal(proximaFecha(lunes, null), null);
assert.equal(proximaFecha(lunes, ''), null);
assert.equal(proximaFecha(lunes, 'cada rato'), null, 'una recurrencia desconocida no inventa fechas');

// --- textoPlazo -------------------------------------------------------------
const ahora = Date.now();
assert.match(textoPlazo(new Date(ahora + 3 * 3600000).toISOString()), /vence en 3 h/);
assert.match(textoPlazo(new Date(ahora - 3 * 3600000).toISOString()), /vencida hace 3 h/);
assert.match(textoPlazo(new Date(ahora - 50 * 3600000).toISOString()), /vencida hace 2 días/);

console.log('OK: recurrencias y plazos verificados');
