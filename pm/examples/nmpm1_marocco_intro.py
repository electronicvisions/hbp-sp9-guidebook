import pyhmf as pynn
import Coordinate as C
from pymarocco import PyMarocco

import pylogging
for domain in ["Calibtic", "marocco"]:
    pylogging.set_loglevel(pylogging.get(domain), pylogging.LogLevel.INFO)

marocco = PyMarocco()
pynn.setup(marocco = marocco)

neuron = pynn.Population(1, pynn.IF_cond_exp)

marocco.placement.add(neuron, C.HICANNGlobal(C.HICANNOnWafer(C.X(5), C.Y(5)), C.Wafer(3)))

pynn.run(10)

pynn.end()
