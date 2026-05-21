# Evidencia HU-09 — Control de repeticion con BERT

Responsable: SebaNG (backend) y benjaosan (badge UI).

## Codigo

- `vigildata-backend/app/services/duplicados_bert.py`
- `vigildata-backend/app/models/incidente.py` (`incidente_raiz_id`, `reportes_asociados`)
- `vigildata-backend/app/routers/incidentes.py` (hook en `POST /incidentes/`)
- `vigildata-backend/app/schemas/incidente.py` (`auto_aprobado`, `incidente_raiz_id`, `reportes_asociados`)

## Pruebas unitarias

Archivo: `vigildata-backend/tests/test_duplicados_bert.py`

Ejecutar:

```bash
cd vigildata-backend
pytest -v tests/test_duplicados_bert.py
```

Casos cubiertos:
- `test_similitud_coseno_simetria_y_normalizacion`
- `test_distancia_metros_haversine_misma_ubicacion_es_cero`
- `test_distancia_metros_200m_aproximado`
- `test_duplicado_detecta_descripciones_similares_cercanas`
- `test_duplicado_descarta_si_estan_lejos`
- `test_duplicado_descarta_si_paso_mas_de_30_min`
- `test_auto_aprueba_al_llegar_al_tercer_reporte`

## Reglas configurables (env vars)

- `HU09_VENTANA_MIN=30`
- `HU09_DISTANCIA_MAX_M=200`
- `HU09_UMBRAL_SIMILITUD=0.85`
- `HU09_AUTO_APROBAR_DESDE=3`
- `HU09_MODELO=paraphrase-multilingual-MiniLM-L12-v2`

## Caja negra manual

| Caso | Esperado | Resultado |
|------|----------|-----------|
| 3 reportes con texto similar dentro de 30 min en misma comuna y < 200 m, 4to llega | 4to se marca `auto_aprobado=true` y `reportes_asociados >= 4` en raiz | OK |
| Reportes distantes (> 1 km) con texto identico | No se consolidan; cada uno es incidente independiente | OK |
| Reportes similares separados > 30 min | No se consolidan | OK |

## Capturas

Dejar aqui capturas del flujo:
- `4to-reporte-auto-aprobado.png` (mapa con badge "auto-aceptado por similitud")
- `pytest-output.png` (salida de la suite pytest)
