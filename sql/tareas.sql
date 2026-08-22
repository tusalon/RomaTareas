-- RomaTareas — tabla de tareas personales con plazo y aviso al movil.
--
-- Ejecutar una sola vez en el SQL Editor de Supabase (proyecto zorhclhvykikaachfrmp).
-- Despues, abrir la web una vez con el PIN para cargar las tareas semilla.

create table if not exists tareas (
  id            uuid primary key default gen_random_uuid(),
  -- SHA-256 del PIN. Es lo que separa tus tareas de las de cualquier otro.
  -- Ojo: la anon key es publica, asi que esto es una puerta con llave, no una
  -- caja fuerte. Ver el README antes de meter aqui algo sensible.
  pin_hash      text not null,
  titulo        text not null,
  detalle       text,
  vence_en      timestamptz,
  -- null | 'diaria' | 'semanal:0'..'semanal:6' (0=domingo) | 'mensual'
  recurrencia   text,
  completada_en timestamptz,
  -- Marca del ultimo aviso enviado, para no repetirlo cada hora.
  avisada_en    timestamptz,
  creada_en     timestamptz not null default now()
);

-- El cron y la web siempre filtran por estas tres columnas, en este orden.
create index if not exists tareas_pendientes_idx
  on tareas (pin_hash, completada_en, vence_en);

alter table tareas enable row level security;

-- Politica abierta a la anon key: la separacion real la hace el filtro por
-- pin_hash que aplican la web y el cron. PostgREST no puede exigir que un
-- filtro venga en la peticion, asi que esto no sustituye a un login.
--
-- Se conceden solo lectura, alta y edicion. DELETE queda fuera a proposito:
-- la anon key es publica, y una politica `for all` dejaria que cualquiera
-- vaciara la tabla entera con una peticion. Ni la web ni el cron borran nada
-- (completar una tarea escribe completada_en, no la elimina), asi que no se
-- pierde nada. Para borrar de verdad, usa el SQL Editor.
drop policy if exists tareas_anon on tareas;
drop policy if exists tareas_leer on tareas;
drop policy if exists tareas_crear on tareas;
drop policy if exists tareas_editar on tareas;

create policy tareas_leer   on tareas for select to anon using (true);
create policy tareas_crear  on tareas for insert to anon with check (true);
create policy tareas_editar on tareas for update to anon using (true) with check (true);
