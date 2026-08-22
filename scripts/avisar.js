#!/usr/bin/env node
// RomaTareas — avisa al movil de lo que vence.
//
//   node scripts/avisar.js            envia de verdad
//   node scripts/avisar.js --seco     muestra que enviaria, sin enviar
//
// Corre cada hora desde .github/workflows/avisos.yml. Sin dependencias:
// solo fetch, que Node trae desde la 18.

const SUPABASE = process.env.SUPABASE_URL || 'https://zorhclhvykikaachfrmp.supabase.co';
const ANON = process.env.SUPABASE_ANON_KEY ||
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpvcmhjbGh2eWtpa2FhY2hmcm1wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxNDQzMzUsImV4cCI6MjA4NzcyMDMzNX0.reauF3UfNTFJFZ3Mnzf8ctYH1d5p7C3msi7AvYJUaos';
const TOPIC = process.env.NTFY_TOPIC || 'roma-tareas';
const WEB = process.env.ROMATAREAS_URL || 'https://tusalon.github.io/RomaTareas/';

// Cuanto antes del plazo se avisa, y cada cuanto se repite el aviso de una
// tarea ya vencida. Sin el segundo limite, el cron horario avisaria 24 veces
// al dia de la misma tarea y dejarias de mirar las notificaciones.
const AVISAR_CON_HORAS = 24;
const REPETIR_CADA_HORAS = 20;

const SECO = process.argv.includes('--seco');
const API = `${SUPABASE}/rest/v1/tareas`;

function cabeceras(extra = {}) {
  return {
    apikey: ANON,
    Authorization: `Bearer ${ANON}`,
    'Content-Type': 'application/json',
    ...extra
  };
}

async function pedir(url, opciones = {}) {
  const r = await fetch(url, { ...opciones, headers: cabeceras(opciones.headers) });
  if (!r.ok) throw new Error(`${r.status} ${r.statusText} — ${await r.text()}`);
  return r.status === 204 ? null : r.json();
}

function textoPlazo(iso) {
  const d = new Date(iso);
  const ahora = new Date();
  const horas = Math.round((d - ahora) / 3600000);
  if (horas < -24) return `vencida hace ${Math.floor(-horas / 24)} días`;
  if (horas < 0) return `vencida hace ${-horas} h`;
  if (horas === 0) return 'vence ahora';
  if (horas < 24) return `vence en ${horas} h`;
  return `vence el ${d.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'short' })}`;
}

// --- recurrencias -----------------------------------------------------------
// Se resuelven aqui ademas de en la web: el boton "Completar" de la
// notificacion hace un PATCH directo a Supabase y no puede ejecutar la logica
// del navegador. Sin esto, completar una tarea semanal desde el movil la
// borraria para siempre en vez de reprogramarla.
function proximaFecha(desde, recurrencia) {
  const d = new Date(desde);
  if (recurrencia === 'diaria') { d.setDate(d.getDate() + 1); return d; }
  if (recurrencia === 'mensual') { d.setMonth(d.getMonth() + 1); return d; }
  const m = /^semanal:([0-6])$/.exec(recurrencia || '');
  if (m) {
    const objetivo = Number(m[1]);
    d.setDate(d.getDate() + 1);
    while (d.getDay() !== objetivo) d.setDate(d.getDate() + 1);
    return d;
  }
  return null;
}

async function reprogramarRecurrentes() {
  const desde = new Date(Date.now() - 30 * 86400000).toISOString();
  const completadas = await pedir(
    `${API}?select=*&recurrencia=not.is.null&completada_en=gte.${desde}&order=completada_en.desc`
  );
  const pendientes = await pedir(`${API}?select=pin_hash,titulo,recurrencia&completada_en=is.null`);
  const yaHay = new Set(pendientes.map((t) => `${t.pin_hash}|${t.titulo}|${t.recurrencia}`));

  const nuevas = [];
  const vistas = new Set();
  for (const t of completadas) {
    const clave = `${t.pin_hash}|${t.titulo}|${t.recurrencia}`;
    if (yaHay.has(clave) || vistas.has(clave)) continue;
    vistas.add(clave);
    const proxima = proximaFecha(t.vence_en || t.completada_en, t.recurrencia);
    if (!proxima) continue;
    nuevas.push({
      pin_hash: t.pin_hash,
      titulo: t.titulo,
      detalle: t.detalle,
      vence_en: proxima.toISOString(),
      recurrencia: t.recurrencia
    });
  }

  if (!nuevas.length) return 0;
  if (SECO) { console.log(`[seco] reprogramaria ${nuevas.length} recurrentes`); return nuevas.length; }
  await pedir(API, { method: 'POST', headers: { Prefer: 'return=minimal' }, body: JSON.stringify(nuevas) });
  return nuevas.length;
}

// --- avisos -----------------------------------------------------------------
async function porAvisar() {
  const limite = new Date(Date.now() + AVISAR_CON_HORAS * 3600000).toISOString();
  const tareas = await pedir(
    `${API}?select=*&completada_en=is.null&vence_en=not.is.null&vence_en=lte.${limite}&order=vence_en.asc`
  );
  const corte = Date.now() - REPETIR_CADA_HORAS * 3600000;
  return tareas.filter((t) => !t.avisada_en || new Date(t.avisada_en).getTime() < corte);
}

function accionCompletar(tarea) {
  // El body lleva un solo campo a proposito: ntfy separa los argumentos de
  // una accion por comas, y un JSON con dos claves las rompe.
  const body = `{"completada_en":"${new Date().toISOString()}"}`;
  return [
    'http',
    'Completar',
    `${API}?id=eq.${tarea.id}`,
    'method=PATCH',
    `headers.apikey=${ANON}`,
    `headers.Authorization=Bearer ${ANON}`,
    'headers.Content-Type=application/json',
    `body='${body}'`,
    'clear=true'
  ].join(', ');
}

async function avisar(tarea) {
  const vencida = new Date(tarea.vence_en) < new Date();
  const cabs = {
    Title: tarea.titulo,
    Priority: vencida ? 'high' : 'default',
    Tags: vencida ? 'rotating_light' : 'alarm_clock',
    Actions: `${accionCompletar(tarea)}; view, Abrir, ${WEB}`
  };
  const cuerpo = [textoPlazo(tarea.vence_en), tarea.detalle].filter(Boolean).join('\n');

  if (SECO) {
    console.log(`[seco] ${tarea.titulo} — ${textoPlazo(tarea.vence_en)}`);
    return;
  }

  const r = await fetch(`https://ntfy.sh/${TOPIC}`, { method: 'POST', headers: cabs, body: cuerpo });
  if (!r.ok) throw new Error(`ntfy ${r.status}: ${await r.text()}`);

  await pedir(`${API}?id=eq.${tarea.id}`, {
    method: 'PATCH',
    headers: { Prefer: 'return=minimal' },
    body: JSON.stringify({ avisada_en: new Date().toISOString() })
  });
}

async function main() {
  const reprogramadas = await reprogramarRecurrentes();
  if (reprogramadas) console.log(`Recurrentes reprogramadas: ${reprogramadas}`);

  const tareas = await porAvisar();
  if (!tareas.length) { console.log('Nada que avisar.'); return; }

  console.log(`Avisando de ${tareas.length} tarea(s)${SECO ? ' [modo seco]' : ''}:`);
  for (const t of tareas) {
    await avisar(t);
    console.log(`  ✓ ${t.titulo} — ${textoPlazo(t.vence_en)}`);
  }
}

// Solo corre al invocarlo directamente, para que las pruebas puedan importar
// las funciones de fecha sin disparar avisos reales.
if (require.main === module) {
  main().catch((e) => { console.error('Error:', e.message); process.exit(1); });
}

module.exports = { proximaFecha, textoPlazo };
