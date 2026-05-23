from payflow_pago import (
    pagar_concepto_fijo,
    clasificar_salud_financiera,
    procesar_suscripcion
)

def test_pago_renta_con_comision_exitoso():
    resultado = pagar_concepto_fijo(
        saldo_actual=2000,
        concepto="Renta",
        monto_pago=1000
    )

    assert resultado["estado"] == "Exitoso"
    assert resultado["saldo_final"] == 985
    assert resultado["comision"] == 15


def test_pago_luz_con_comision_exitoso():
    resultado = pagar_concepto_fijo(
        saldo_actual=500,
        concepto="Luz",
        monto_pago=300
    )

    assert resultado["estado"] == "Exitoso"
    assert resultado["saldo_final"] == 185
    assert resultado["comision"] == 15


def test_pago_rechazado_por_saldo_insuficiente():
    resultado = pagar_concepto_fijo(
        saldo_actual=1000,
        concepto="Renta",
        monto_pago=1000
    )

    assert resultado["estado"] == "Rechazado"
    assert resultado["saldo_final"] == 1000
    assert resultado["mensaje"] == "Saldo insuficiente"


def test_pago_rechazado_por_concepto_no_valido():
    resultado = pagar_concepto_fijo(
        saldo_actual=1000,
        concepto="Agua",
        monto_pago=300
    )

    assert resultado["estado"] == "Rechazado"
    assert resultado["saldo_final"] == 1000
    assert resultado["mensaje"] == "Concepto no válido"


def test_pago_rechazado_por_monto_negativo():
    resultado = pagar_concepto_fijo(
        saldo_actual=1000,
        concepto="Luz",
        monto_pago=-100
    )

    assert resultado["estado"] == "Rechazado"
    assert resultado["saldo_final"] == 1000
    assert resultado["mensaje"] == "El monto debe ser mayor a cero"

def test_pago_internet_sin_comision():
    resultado = pagar_concepto_fijo(
        saldo_actual=1000,
        concepto="Internet",
        monto_pago=1000
    )

    assert resultado["estado"] == "Exitoso"
    assert resultado["saldo_final"] == 0
    assert resultado["comision"] == 0

def test_salud_financiera_saludable():
    resultado = clasificar_salud_financiera(
        saldo_actual=1500,
        presupuesto_total=3000
    )

    assert resultado["estado"] == "SALUDABLE"
    assert resultado["mensaje"] == "El saldo se mantiene estable"


def test_salud_financiera_en_riesgo():
    resultado = clasificar_salud_financiera(
        saldo_actual=200,
        presupuesto_total=3000
    )

    assert resultado["estado"] == "EN RIESGO"
    assert resultado["mensaje"] == "El saldo es menor al 10% del presupuesto"


def test_salud_financiera_critico():
    resultado = clasificar_salud_financiera(
        saldo_actual=0,
        presupuesto_total=3000
    )

    assert resultado["estado"] == "CRITICO"
    assert resultado["mensaje"] == "El saldo disponible es crítico"


def test_salud_financiera_rechaza_presupuesto_invalido():
    resultado = clasificar_salud_financiera(
        saldo_actual=100,
        presupuesto_total=0
    )

    assert resultado["estado"] == "RECHAZADO"
    assert resultado["mensaje"] == "El presupuesto total debe ser mayor a cero"

def test_suscripcion_pagada_con_saldo_suficiente():
    resultado = procesar_suscripcion(
        saldo_actual=500,
        nombre_suscripcion="Netflix",
        costo=199
    )

    assert resultado["estado"] == "PAGADA"
    assert resultado["saldo_final"] == 301
    assert resultado["mensaje"] == "Suscripción pagada correctamente"


def test_suscripcion_rechazada_por_saldo_insuficiente():
    resultado = procesar_suscripcion(
        saldo_actual=100,
        nombre_suscripcion="Spotify",
        costo=129
    )

    assert resultado["estado"] == "SUSPENDIDA"
    assert resultado["saldo_final"] == 100
    assert resultado["mensaje"] == "Saldo insuficiente para pagar la suscripción"


def test_suscripcion_rechazada_por_costo_invalido():
    resultado = procesar_suscripcion(
        saldo_actual=500,
        nombre_suscripcion="Netflix",
        costo=0
    )

    assert resultado["estado"] == "RECHAZADA"
    assert resultado["saldo_final"] == 500
    assert resultado["mensaje"] == "El costo de la suscripción debe ser mayor a cero"


def test_suscripcion_rechazada_por_nombre_vacio():
    resultado = procesar_suscripcion(
        saldo_actual=500,
        nombre_suscripcion="",
        costo=199
    )

    assert resultado["estado"] == "RECHAZADA"
    assert resultado["saldo_final"] == 500
    assert resultado["mensaje"] == "La suscripción debe tener un nombre válido"

def test_flujo_e2e_payflow_guardian():
    saldo = 1000

    suscripcion = procesar_suscripcion(
        saldo_actual=saldo,
        nombre_suscripcion="Netflix",
        costo=199
    )

    pago_luz = pagar_concepto_fijo(
        saldo_actual=suscripcion["saldo_final"],
        concepto="Luz",
        monto_pago=300
    )

    salud = clasificar_salud_financiera(
        saldo_actual=pago_luz["saldo_final"],
        presupuesto_total=1000
    )

    assert suscripcion["estado"] == "PAGADA"
    assert pago_luz["estado"] == "Exitoso"
    assert pago_luz["saldo_final"] == 486
    assert salud["estado"] == "SALUDABLE"