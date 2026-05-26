"""Interfaz minima por consola para el MVP de PayFlow."""

from payflow_pago import procesar_flujo_payflow


def mostrar_resumen(resultado):
    print("\n=== Resumen PayFlow ===")
    print(f"Presupuesto: {resultado['presupuesto']['estado']}")

    if resultado["suscripcion"]:
        print(f"Suscripcion: {resultado['suscripcion']['estado']}")

    if resultado["servicio"]:
        print(f"Servicio: {resultado['servicio']['estado']}")

    print(f"Saldo final: ${resultado['saldo_final']:.2f}")
    print(f"Salud financiera: {resultado['salud_financiera']}")


def main():
    print("PayFlow - Guardian de suscripciones")

    presupuesto = float(input("Presupuesto mensual total: "))
    ahorro = float(input("Meta de ahorro: "))
    suscripcion = input("Nombre de suscripcion: ")
    costo_suscripcion = float(input("Costo de suscripcion: "))
    servicio = input("Servicio a pagar (Renta/Luz/Internet): ")
    monto_servicio = float(input("Monto del servicio: "))

    resultado = procesar_flujo_payflow(
        presupuesto,
        ahorro,
        suscripcion,
        costo_suscripcion,
        servicio,
        monto_servicio,
    )
    mostrar_resumen(resultado)


if __name__ == "__main__":
    main()
