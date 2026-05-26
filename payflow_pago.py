"""MVP minimo de PayFlow - Guardian de suscripciones.

Este modulo concentra la logica de negocio necesaria para TAR04:
presupuesto, ahorro/meta, suscripcion, pago de servicio, salud financiera
y una funcion orquestadora final.
"""

CONCEPTOS_VALIDOS = {"Renta", "Luz", "Internet"}
COMISION_SERVICIO = 5.0


def configurar_presupuesto(presupuesto_mensual, ahorro_meta):
    """Reserva el ahorro/meta y devuelve el saldo operativo inicial."""
    if presupuesto_mensual <= 0 or ahorro_meta < 0:
        return {
            "estado": "RECHAZADO",
            "saldo": 0.0,
            "mensaje": "Presupuesto o ahorro invalido.",
        }

    if presupuesto_mensual <= ahorro_meta:
        return {
            "estado": "EJERCICIO_DEFICIT",
            "saldo": 0.0,
            "mensaje": "El presupuesto no cubre la meta de ahorro.",
        }

    saldo = presupuesto_mensual - ahorro_meta
    return {
        "estado": "EJERCICIO",
        "saldo": float(saldo),
        "mensaje": "Presupuesto configurado correctamente.",
    }


def pagar_concepto_fijo(saldo, concepto, monto):
    """Procesa un pago de servicio basico con comision fija."""
    if concepto not in CONCEPTOS_VALIDOS:
        return {
            "estado": "RECHAZADA",
            "saldo": float(saldo),
            "mensaje": "Concepto no valido.",
        }

    if monto <= 0:
        return {
            "estado": "RECHAZADA",
            "saldo": float(saldo),
            "mensaje": "Monto invalido.",
        }

    total = monto + COMISION_SERVICIO
    if saldo < total:
        return {
            "estado": "RECHAZADA",
            "saldo": float(saldo),
            "mensaje": "Saldo insuficiente para pagar el servicio.",
        }

    return {
        "estado": "APROBADA",
        "saldo": float(saldo - total),
        "mensaje": "Pago de servicio aprobado.",
    }


def procesar_suscripcion(saldo, nombre, costo):
    """Procesa el cobro de una suscripcion digital."""
    if not nombre or not nombre.strip():
        return {
            "estado": "RECHAZADA",
            "saldo": float(saldo),
            "mensaje": "Suscripcion sin nombre.",
        }

    if costo <= 0:
        return {
            "estado": "RECHAZADA",
            "saldo": float(saldo),
            "mensaje": "Costo de suscripcion invalido.",
        }

    if saldo < costo:
        return {
            "estado": "SUSPENDIDA",
            "saldo": float(saldo),
            "mensaje": "Suscripcion suspendida por saldo insuficiente.",
        }

    return {
        "estado": "PAGADA",
        "saldo": float(saldo - costo),
        "mensaje": "Suscripcion pagada correctamente.",
    }


def clasificar_salud_financiera(saldo, presupuesto_mensual, pagos_prioritarios=0):
    """Clasifica la salud financiera despues de las operaciones."""
    if presupuesto_mensual <= 0 or saldo < 0:
        return "RECHAZADO"

    if saldo < pagos_prioritarios:
        return "CRITICO"

    if saldo < presupuesto_mensual * 0.10:
        return "EN RIESGO"

    return "SALUDABLE"


def procesar_flujo_payflow(
    presupuesto_mensual,
    ahorro_meta,
    suscripcion_nombre,
    suscripcion_costo,
    servicio_nombre,
    servicio_monto,
    pagos_prioritarios=0,
):
    """Funcion orquestadora final del MVP minimo de PayFlow."""
    presupuesto = configurar_presupuesto(presupuesto_mensual, ahorro_meta)
    if presupuesto["estado"] != "EJERCICIO":
        return _respuesta_final(presupuesto, None, None, "CRITICO")

    suscripcion = procesar_suscripcion(
        presupuesto["saldo"], suscripcion_nombre, suscripcion_costo
    )
    servicio = pagar_concepto_fijo(
        suscripcion["saldo"], servicio_nombre, servicio_monto
    )
    salud = clasificar_salud_financiera(
        servicio["saldo"], presupuesto_mensual, pagos_prioritarios
    )

    return _respuesta_final(presupuesto, suscripcion, servicio, salud)


def _respuesta_final(presupuesto, suscripcion, servicio, salud):
    """Agrupa los resultados del flujo para facilitar pruebas y salida en consola."""
    ultimo_resultado = servicio or suscripcion or presupuesto

    return {
        "presupuesto": presupuesto,
        "suscripcion": suscripcion,
        "servicio": servicio,
        "saldo_final": float(ultimo_resultado["saldo"]),
        "salud_financiera": salud,
    }
