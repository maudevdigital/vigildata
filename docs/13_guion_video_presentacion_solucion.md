# Guion — Video de Presentación de Solución (VigilData)

Actividad: Video de Presentación de Solución (máximo 5 minutos)
Foco pedido: propuesta de valor + usabilidad (interacción del usuario con la app)
Objetivo: retroalimentación temprana sobre funcionalidad, UX, claridad de la propuesta de valor y nivel de avance.

> A diferencia del video de Sprint 1/2 (que era de proceso: Taiga, sprints, pruebas),
> este video es **de producto**: muestra qué problema resuelve VigilData y cómo se usa.
> Salvo la apertura, la mayor parte del tiempo debe ser **app en pantalla**, no diapositivas.

## Reparto y tiempos (objetivo 4:30, tope 5:00)

| # | Integrante | Rol | Bloque | Tiempo |
|---|------------|-----|--------|--------|
| 1 | Lucas Maulen | Product Owner | Apertura: problema y propuesta de valor | ~0:50 |
| 2 | benjaosan | Frontend / Developer | Demo de usabilidad: flujo del ciudadano (reportar + mapa + filtros + móvil) | ~1:30 |
| 3 | Sebastián López (SebaNG) | Backend / Developer | Confianza en los datos: login seguro y control de duplicados | ~1:00 |
| 4 | Felipe Vergara R | Scrum Master | Valor para la comunidad: moderación, resumen y próximos pasos | ~1:00 |

Tip de grabación: que cada quien grabe su voz **sobre la pantalla compartida** mostrando lo que describe. Evitar leer monótono; hablar como explicando a un vecino.

---

## 1. Apertura — Lucas (Product Owner) · ~0:50

> En pantalla: logo/portada de VigilData y, al final, la home de la app ya abierta.

"Hola, somos el equipo de **VigilData**. Soy Lucas, Product Owner del proyecto.

El problema que vimos es simple: los vecinos **sí saben** dónde pasan cosas en su barrio —un asalto, un poste caído, una zona oscura—, pero esa información queda perdida en grupos de WhatsApp, redes sociales o conversaciones. Nadie más la aprovecha.

VigilData es un **mapa colaborativo de seguridad ciudadana**. Nuestra propuesta de valor es convertir ese conocimiento del barrio en **datos útiles y ubicables**: cualquier vecino reporta un incidente con su ubicación en segundos, y todos pueden **ver, filtrar y entender** las zonas de riesgo en un mapa, en tiempo real y sin formularios complicados.

Les mostramos cómo se usa."

---

## 2. Demo de usabilidad — benjaosan (Frontend) · ~1:30

> En pantalla: la app real. Hacer el recorrido en vivo. Es el corazón del video.

"Te muestro el flujo completo de un ciudadano.

**(1) Entrar.** Inicio sesión —se puede con email o directo con **‘Continuar con Google’**, un clic y estoy dentro.

**(2) Reportar.** Para crear un reporte basta con **tocar el mapa en el lugar del hecho**, o usar el botón ‘+’. La app toma mi **ubicación GPS automáticamente**, así que no escribo coordenadas. Solo elijo el **tipo** de incidente, el **nivel de riesgo** —bajo, medio o alto— y la **región y comuna** en cascada, agrego una descripción y listo. Tras enviarlo, el mapa **se centra solo en el nuevo punto**.

**(3) Visualizar.** Cada incidente es un marcador, y el **color indica el riesgo**: verde, amarillo o rojo. Al tocarlo veo tipo, descripción, fecha y comuna.

**(4) Filtrar.** Puedo filtrar por **comuna** y por **rango de fechas**, combinándolos, para ver solo lo que me importa de mi zona.

**(5) Móvil.** Y todo esto está pensado para el celular: mapa a pantalla completa, los filtros se abren en un panel deslizable desde abajo y un botón flotante para reportar al instante. Es donde realmente lo usaría un vecino en la calle."

---

## 3. Confianza en los datos — Sebastián / SebaNG (Backend) · ~1:00

> En pantalla: opcional, mostrar dos reportes parecidos consolidándose, o el botón de Google.

"Para que un mapa así sirva, los datos tienen que ser **confiables**. De eso me encargo en el backend.

Primero, **seguridad**: solo usuarios autenticados pueden reportar. Manejamos sesión con tokens JWT y el inicio con Google se valida en el servidor, así cada reporte queda asociado a una cuenta real.

Y lo más interesante: el **control de reportes repetidos**. Cuando llegan varios reportes del **mismo hecho** —descripciones parecidas, en la misma zona y dentro de una ventana de tiempo—, el sistema los **detecta por similitud de texto** y los **agrupa en un solo incidente** en vez de llenar el mapa de duplicados. Es más, si un mismo hecho lo reportan varios vecinos, gana credibilidad y se **auto-aprueba**. Eso mantiene el mapa limpio y la información creíble."

---

## 4. Valor para la comunidad y cierre — Felipe (Scrum Master) · ~1:00

> En pantalla: vista de administración (aprobar/rechazar) y el panel de resumen por comuna y tipo.

"Además del reporte individual, VigilData entrega **valor a toda la comunidad**.

Por un lado, hay **moderación**: un analista revisa los reportes y puede **aprobar, rechazar o eliminar**, de modo que la información falsa o irrelevante no se muestra como activa en el mapa. Eso protege la calidad de los datos.

Por otro lado, el **resumen**: la app agrupa los incidentes **por comuna y por tipo**, así de un vistazo se entiende **qué zonas y qué situaciones concentran más riesgo** —y respeta los filtros activos.

En resumen, hoy VigilData ya resuelve su flujo completo: registrarse, reportar con ubicación, visualizar, filtrar, moderar y obtener un panorama de la comuna. Como próximos pasos buscamos sumar **alertas y avisos** y pulir aún más la experiencia.

Gracias, y esperamos su retroalimentación."

---

## Checklist para grabar

- [ ] Total bajo 5:00 (apuntar a ~4:30); cronometrar cada bloque.
- [ ] Mostrar la **app real en pantalla**, no solo slides (sobre todo el bloque 2).
- [ ] Tener datos de ejemplo cargados (varios incidentes, distintas comunas y niveles) antes de grabar.
- [ ] Probar el flujo una vez completo antes de grabar (login → reportar → mapa → filtros → móvil → admin/resumen).
- [ ] Cada integrante habla al menos una vez (la actividad pide los 4).
- [ ] Audio claro; si se graba por separado, cuidar transiciones entre voces.
- [ ] Cerrar pidiendo explícitamente feedback (es el objetivo de la actividad).

## Mapa propuesta de valor ↔ qué se muestra (por si el profe lo pregunta)

| Necesidad del usuario | Cómo lo resuelve VigilData | Dónde se ve en el video |
|---|---|---|
| Compartir lo que pasa en el barrio sin fricción | Reporte con GPS automático y pocos campos | Bloque 2 (reportar) |
| Entender zonas de riesgo de un vistazo | Mapa con marcadores por nivel (verde/amarillo/rojo) | Bloque 2 (visualizar) |
| Consultar solo lo relevante a mi contexto | Filtros por comuna y fecha | Bloque 2 (filtrar) |
| Usarlo en la calle, desde el celular | UI móvil: pantalla completa, bottom sheet, FAB | Bloque 2 (móvil) |
| Que la información sea creíble | Login seguro + control de duplicados/auto-aprobación | Bloque 3 |
| Evitar información falsa o repetida | Moderación (aprobar/rechazar) | Bloque 4 |
| Tener un panorama de la comuna | Resumen por comuna y tipo | Bloque 4 |
