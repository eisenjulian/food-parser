# -*- coding: utf-8 -*-

from expressions import *
from terms import *

exp = 0.8
for i in range(13):
    globals()['x'  + str(i)] = lambda term, _i=i, **args: x(term, implicit=exp**_i, **args)
    globals()['xm' + str(i)] = lambda term, _i=i, **args: x(term, memory=(.8, .9), implicit=exp**_i, **args)
xm = lambda term, **args: x(term, memory=(.8, .9), implicit=0.0, **args)

x_carne = xm2(carne)
x_pizza = xm3(pizza)
x_tarta = xm4(tarta)
x_empanada = xm2(empanada)
x_panini = xm(panini)
x_caprese = x(caprese) | (x10(queso) & x(albahaca) & x5(tomate))
x_sprite = xm(sprite)
x_coca = xm(coca)
x_jamon_queso = x(jamon_queso) | (x(jamon) & x(queso))

x_ml600 = x(ml600) | x(mini)
x_ml1500 = x(ml1500) | x(grande)

def emp(name, exp, tags=frozenset(), desc=""):
    return it(
        name="Empanada de {0}".format(name),
        exp=x_empanada & exp,
        tags=tags,
        desc=desc,
        price=18,
    )

items = [
    emp(name="espinica con queso", exp=x(espinaca) & x12(queso)),
    emp(name="espinica con salsa blanca", exp=x(espinaca) & x6(salsa) & x6(blanca)),
    emp(name="caprese", exp=x_caprese),
    emp(name="jamón y queso", exp=x_jamon_queso),
    emp(name="pollo", exp=x(pollo)),
    emp(name="salteado de vegetales", exp=x0(salteado) & x(vegetal)),
    emp(name="carne picante", exp=x_carne & x(picante)),
    emp(name="carne suave", exp=x_carne & x2(suave)),
    emp(name="champignon, queso y jerez", exp=x7(champignon) & x0(queso) & x7(jerez)),
    emp(name="carne cortada a cuchillo", exp=x_carne & x7(cortada) & x7(cuchillo)),
    emp(name="carne salteña", exp=x_carne & x(saltena)),
    emp(name="carne dulce", exp=x_carne & x(dulce)),
    emp(name="roquefort con jamón", exp=x(roquefort) & x1(jamon)),
    emp(name="pollo laqueado con miel y cerveza", exp=x(pollo) & x5(laqueado) & x5(miel) & x5(cerveza)),
    emp(name="panceta, ciruela y muzzarella", exp=x7(panceta) & x7(ciruela) & x1(muzzarella) & x0(queso)),
    emp(name="fusión de cuatro quesos", exp=x(cuatro_quesos) | (x(fusion) & x(queso))),
    it(name="Pizza fugazzeta", exp=x_pizza & x(fugazzeta) & x0(grande), price=120),
    it(name="Pizza de muzzarella", exp=x_pizza & x(muzzarella) & x0(grande), price=100),
    it(name="Panini relleno de jamón y queso", exp=x_panini & x_jamon_queso, price=45),
    it(name="Panini Caprese", exp=x_panini & x_caprese, price=55),
    it(name="Chipa", exp=x(chipa), price=lambda n: (n % 12) * 6 +  (n // 12) * 4),
    it(name="Tarta de jamón y queso", exp=x_tarta & x_jamon_queso, price=80),
    it(name="Tarta pascualina", exp=x_tarta & x(pascualina), price=90),
    it(name="Tarta zapallitos", exp=x_tarta & x(zapallitos), price=85),
    it(name="Mini tarta de acelga", exp=x_tarta & x(mini) & x(pascualina), price=60),
    it(name="Mini tarta de cebolla glaseada con queso azul", exp=x_tarta & x(mini) & x7(cebolla) & x0(glaceada) & x0(queso) & x7(azul), price=60) ,
    it(name="Spirte 600 ml", exp=x_sprite & x_ml600, price=20, tags=(x(bebida))),
    it(name="Coca-Cola 600 ml", exp=x_coca & x_ml600, price=20, tags=(x(bebida))),
    it(name="Coca-Cola Light 600 ml", exp=x_coca & x(light) & x_ml600, price=20, tags=(x(bebida))),
    it(name="Coca-Cola 1,5 lts", exp=x_coca & x_ml1500, price=40, tags=(x(bebida))),
    it(name="Coca-Cola Light 1,5 lts", exp=x_coca & x(light) & x_ml1500, price=40, tags=(x(bebida))),
]