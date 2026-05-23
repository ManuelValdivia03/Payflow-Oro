COMISION_FIJA = 15.00

CONCEPTOS_VALIDOS = ["Renta", "Luz", "Internet"]


def pagar_concepto_fijo(saldo_actual, concepto, monto_pago):
    """
    Procesa el pago de un concepto fijo de PayFlow.

    Reglas:
    - Los conceptos válidos son Renta, Luz e Internet.
    - Renta y Luz mantienen una comisión fija de $15.00.
    - Internet no cobra comisión.
    - Si el saldo no alcanza para monto + comisión, el pago se rechaza.
    - Si el pago es exitoso, se descuenta el total del saldo.
    """

    if concepto not in CONCEPTOS_VALIDOS:
        return {
            "estado": "Rechazado",
            "saldo_final": saldo_actual,
            "mensaje": "Concepto no válido",
            "comision": 0.00
        }

    if monto_pago <= 0:
        return {
            "estado": "Rechazado",
            "saldo_final": saldo_actual,
            "mensaje": "El monto debe ser mayor a cero",
            "comision": 0.00
        }

    if concepto == "Internet":
        comision = 0.00
    else:
        comision = COMISION_FIJA

    total_a_cobrar = monto_pago + comision

    if saldo_actual < total_a_cobrar:
        return {
            "estado": "Rechazado",
            "saldo_final": saldo_actual,
            "mensaje": "Saldo insuficiente",
            "comision": comision
        }

    saldo_final = saldo_actual - total_a_cobrar

    return {
        "estado": "Exitoso",
        "saldo_final": saldo_final,
        "mensaje": "Pago realizado correctamente",
        "comision": comision
    }

def clasificar_salud_financiera(saldo_actual, presupuesto_total):
    """
    Clasifica la salud financiera del usuario según su saldo disponible.

    Reglas:
    - Si el presupuesto total es menor o igual a cero, se rechaza.
    - Si el saldo es cero o negativo, el estado es CRITICO.
    - Si el saldo es menor al 10% del presupuesto, el estado es EN RIESGO.
    - En cualquier otro caso, el estado es SALUDABLE.
    """

    if presupuesto_total <= 0:
        return {
            "estado": "RECHAZADO",
            "mensaje": "El presupuesto total debe ser mayor a cero"
        }

    limite_riesgo = presupuesto_total * 0.10

    if saldo_actual <= 0:
        return {
            "estado": "CRITICO",
            "mensaje": "El saldo disponible es crítico"
        }

    if saldo_actual < limite_riesgo:
        return {
            "estado": "EN RIESGO",
            "mensaje": "El saldo es menor al 10% del presupuesto"
        }

    return {
        "estado": "SALUDABLE",
        "mensaje": "El saldo se mantiene estable"
    }

def procesar_suscripcion(saldo_actual, nombre_suscripcion, costo):
    """
    Procesa el pago automático de una suscripción digital.

    Reglas:
    - La suscripción debe tener nombre.
    - El costo debe ser mayor a cero.
    - Si hay saldo suficiente, queda PAGADA y descuenta el costo.
    - Si no hay saldo suficiente, queda SUSPENDIDA y no descuenta saldo.
    """

    if nombre_suscripcion == "":
        return {
            "estado": "RECHAZADA",
            "saldo_final": saldo_actual,
            "mensaje": "La suscripción debe tener un nombre válido"
        }

    if costo <= 0:
        return {
            "estado": "RECHAZADA",
            "saldo_final": saldo_actual,
            "mensaje": "El costo de la suscripción debe ser mayor a cero"
        }

    if saldo_actual < costo:
        return {
            "estado": "SUSPENDIDA",
            "saldo_final": saldo_actual,
            "mensaje": "Saldo insuficiente para pagar la suscripción"
        }

    return {
        "estado": "PAGADA",
        "saldo_final": saldo_actual - costo,
        "mensaje": "Suscripción pagada correctamente"
    }