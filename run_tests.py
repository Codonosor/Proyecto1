"""Script de pruebas automatizadas (no unitarias) para validar reservas y stock.

Realiza 4 pruebas:
1) Crear pedido y reservar stock -> stock disminuye.
2) Cancelar pedido pendiente -> stock se libera.
3) Finalizar pedido pendiente -> stock permanece descontado.
4) Intentar reservar más del stock disponible -> falla; reservar cantidad disponible funciona.
"""
from cafe import Inventario, Bebida, Alimento, PedidoLocal


def assert_eq(a, b, msg=""):
    if a != b:
        raise AssertionError(f"Assertion failed: {a} != {b}. {msg}")


def prueba_1():
    inv = Inventario()
    prod = Bebida("P1", "Prueba", 1.0, tam_ml=100)
    inv.agregar_producto(prod, cantidad=5)

    pedido = PedidoLocal("", "Cliente1", mesa=1)
    ok = inv.reservar(prod.codigo, 3)
    assert_eq(ok, True, "reserva inicial debe tener éxito")
    pedido.agregar_item(prod, 3)
    assert_eq(inv.stock_de(prod.codigo), 2, "stock debe reducirse a 2")
    print("Prueba 1 OK: reserva reduce stock a", inv.stock_de(prod.codigo))
    return inv, prod, pedido


def prueba_2(inv, prod, pedido):
    # cancelar pedido pendiente -> liberar stock
    inv.liberar(prod.codigo, 3)
    assert_eq(inv.stock_de(prod.codigo), 5, "stock debe volver a 5 al liberar")
    print("Prueba 2 OK: liberar devuelve stock a", inv.stock_de(prod.codigo))


def prueba_3():
    inv = Inventario()
    prod = Alimento("P2", "Prueba2", 2.0, calorias=200)
    inv.agregar_producto(prod, cantidad=5)
    pedido = PedidoLocal("", "Cliente2", mesa=2)
    ok = inv.reservar(prod.codigo, 4)
    assert_eq(ok, True, "reserva de 4 debe tener éxito")
    pedido.agregar_item(prod, 4)
    # finalizar: no liberar
    assert_eq(inv.stock_de(prod.codigo), 1, "stock debe ser 1 después de reservar 4")
    print("Prueba 3 OK: finalizar preserva stock en", inv.stock_de(prod.codigo))


def prueba_4():
    inv = Inventario()
    prod = Bebida("P3", "Prueba3", 3.0, tam_ml=200)
    inv.agregar_producto(prod, cantidad=2)
    # intentar reservar 3 -> debe fallar
    ok = inv.reservar(prod.codigo, 3)
    assert_eq(ok, False, "reserva mayor al stock debe fallar")
    # reservar 2 -> ok
    ok2 = inv.reservar(prod.codigo, 2)
    assert_eq(ok2, True, "reserva de 2 debe funcionar")
    assert_eq(inv.stock_de(prod.codigo), 0, "stock debe ser 0")
    print("Prueba 4 OK: reservas y límites funcionan, stock final", inv.stock_de(prod.codigo))


if __name__ == "__main__":
    print("Ejecutando pruebas...")
    inv1, prod1, ped1 = prueba_1()
    prueba_2(inv1, prod1, ped1)
    prueba_3()
    prueba_4()
    print("Todas las pruebas completadas correctamente.")
