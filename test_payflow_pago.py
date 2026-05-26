import pytest

from payflow_pago import (
    configurar_presupuesto,
    pagar_concepto_fijo,
    procesar_suscripcion,
    clasificar_salud_financiera,
    procesar_flujo_payflow,
)


def test_configurar_presupuesto_valido_reserva_ahorro():
    resultado = configurar_presupuesto(5000, 1000)
    assert resultado["estado"] == "EJERCICIO"
    assert resultado["saldo"] == 4000


def test_configurar_presupuesto_rechaza_valores_invalidos():
    resultado = configurar_presupuesto(0, 100)
    assert resultado["estado"] == "RECHAZADO"


def test_configurar_presupuesto_detecta_deficit_por_ahorro():
    resultado = configurar_presupuesto(1000, 1000)
    assert resultado["estado"] == "EJERCICIO_DEFICIT"
    assert resultado["saldo"] == 0


def test_procesar_suscripcion_pagada_con_saldo_suficiente():
    resultado = procesar_suscripcion(500, "Netflix", 199)
    assert resultado["estado"] == "PAGADA"
    assert resultado["saldo"] == 301


def test_procesar_suscripcion_suspendida_por_saldo_insuficiente():
    resultado = procesar_suscripcion(100, "Spotify", 129)
    assert resultado["estado"] == "SUSPENDIDA"
    assert resultado["saldo"] == 100


def test_procesar_suscripcion_rechaza_nombre_vacio():
    resultado = procesar_suscripcion(500, "", 199)
    assert resultado["estado"] == "RECHAZADA"


def test_procesar_suscripcion_rechaza_costo_invalido():
    resultado = procesar_suscripcion(500, "Netflix", 0)
    assert resultado["estado"] == "RECHAZADA"


def test_pagar_concepto_fijo_aprueba_luz_con_comision():
    resultado = pagar_concepto_fijo(500, "Luz", 300)
    assert resultado["estado"] == "APROBADA"
    assert resultado["saldo"] == 195


def test_pagar_concepto_fijo_rechaza_concepto_no_valido():
    resultado = pagar_concepto_fijo(500, "Gasolina", 100)
    assert resultado["estado"] == "RECHAZADA"


def test_pagar_concepto_fijo_rechaza_monto_invalido():
    resultado = pagar_concepto_fijo(500, "Luz", -1)
    assert resultado["estado"] == "RECHAZADA"


def test_pagar_concepto_fijo_rechaza_saldo_insuficiente():
    resultado = pagar_concepto_fijo(100, "Internet", 150)
    assert resultado["estado"] == "RECHAZADA"
    assert resultado["saldo"] == 100


def test_clasificar_salud_financiera_saludable():
    assert clasificar_salud_financiera(1000, 5000) == "SALUDABLE"


def test_clasificar_salud_financiera_en_riesgo():
    assert clasificar_salud_financiera(300, 5000) == "EN RIESGO"


def test_clasificar_salud_financiera_critico_por_pagos_prioritarios():
    assert clasificar_salud_financiera(200, 5000, pagos_prioritarios=300) == "CRITICO"


def test_clasificar_salud_financiera_rechaza_presupuesto_invalido():
    assert clasificar_salud_financiera(200, 0) == "RECHAZADO"


def test_flujo_e2e_payflow_guardian_exitoso():
    resultado = procesar_flujo_payflow(
        presupuesto_mensual=5000,
        ahorro_meta=1000,
        suscripcion_nombre="Netflix",
        suscripcion_costo=199,
        servicio_nombre="Luz",
        servicio_monto=300,
    )

    assert resultado["presupuesto"]["estado"] == "EJERCICIO"
    assert resultado["suscripcion"]["estado"] == "PAGADA"
    assert resultado["servicio"]["estado"] == "APROBADA"
    assert resultado["saldo_final"] == 3496
    assert resultado["salud_financiera"] == "SALUDABLE"


def test_flujo_e2e_payflow_detiene_por_deficit_de_ahorro():
    resultado = procesar_flujo_payflow(
        presupuesto_mensual=1000,
        ahorro_meta=1200,
        suscripcion_nombre="Netflix",
        suscripcion_costo=199,
        servicio_nombre="Luz",
        servicio_monto=300,
    )

    assert resultado["presupuesto"]["estado"] == "EJERCICIO_DEFICIT"
    assert resultado["suscripcion"] is None
    assert resultado["servicio"] is None
    assert resultado["salud_financiera"] == "CRITICO"
