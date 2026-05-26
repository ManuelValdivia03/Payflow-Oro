# PayFlow - MVP minimo TAR04

MVP academico ejecutable por consola para PayFlow, Guardian de suscripciones.

## Alcance
- Configuracion de presupuesto mensual.
- Reserva de ahorro/meta.
- Pago de suscripcion digital.
- Pago de servicio basico.
- Clasificacion de salud financiera.
- Funcion orquestadora final.
- Interfaz minima por consola.

## Ejecutar pruebas
```bash
pytest -v
pytest --cov=payflow_pago --cov-report=term-missing -v
radon cc payflow_pago.py -s
```

## Ejecutar MVP
```bash
python main_payflow.py
```
