# Evidencia HU-11 — Mejorar interfaz movil

Responsable: benjaosan.

## Codigo

- `vigildata-frontend/src/assets/mobile.css`
- `vigildata-frontend/src/components/BottomSheet.vue`
- `vigildata-frontend/src/views/MapaView.vue` (boton "Filtros" en mobile, FAB "+" para reportar, BottomSheet)
- `vigildata-frontend/src/views/ReportarView.vue` (form en columna, submit sticky, `vigil-form`)
- `vigildata-frontend/src/views/AdminView.vue` (cards en mobile via `vigil-admin-cards` / `vigil-admin-table`)
- `vigildata-frontend/src/views/LoginView.vue` (touch targets 44px)
- `vigildata-frontend/src/main.js` (import de `mobile.css`)

## Reglas aplicadas

- Touch targets >= 44 px (clase `.touch-target` + override global a `button`).
- Inputs con `font-size: 16px` para evitar zoom en iOS.
- Safe-area iOS via `env(safe-area-inset-*)`.
- Mapa a pantalla completa; filtros movidos a Bottom Sheet con drag-to-close.
- FAB "Reportar aqui" disponible solo en mobile (`md:hidden`).
- Admin: tabla en desktop, cards de accion grande (3 botones) en mobile.

## QA caja negra movil

Probar en Chrome DevTools "Device toolbar" con perfiles:
- iPhone 12 (390x844)
- Pixel 5 (393x851)
- 360x780 (Android pequeno)

| Caso | Esperado | Resultado |
|------|----------|-----------|
| MapaView en 360x780 | Sin scroll horizontal; boton "Filtros" visible arriba a la derecha; FAB "+" abajo a la derecha | OK |
| Abrir Bottom Sheet de filtros | Se desliza desde abajo, cierra por swipe-down o tap en backdrop, no tapa el FAB | OK |
| ReportarView en 360x780 | Form en una columna; submit accesible con teclado abierto | OK |
| AdminView en 360x780 | Lista en cards con 3 botones grandes (Aprobar / Rechazar / Borrar) | OK |
| LoginView en 360x780 | Boton Google y boton Ingresar tocables sin zoom | OK |

## Capturas

Dejar aqui las capturas de cada caso:
- `mapaview-360.png`
- `bottomsheet-filtros.png`
- `reportarview-360.png`
- `adminview-360.png`
- `loginview-360.png`
