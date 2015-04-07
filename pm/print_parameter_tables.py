"""
Script to print tables of parameter ranges, to be included in Sphinx docs.
"""

import pyNN.hardware.brainscales as sim
sim.setup(useSystemSim=True,
          hardware=sim.hardwareSetup["one-reticle"],
          hardwareNeuronSize=1)

BIG_HW_CAP = 2.16456e-3
SMALL_HW_CAP = 164.2e-6

def print_param_table():
    print
    print "==========  =======  =======  ======="
    print "Parameter   Default  Min      Max"
    print "==========  =======  =======  ======="
    for key in sim.IF_cond_exp.default_parameters:
        print "%-10s  %-7.1f  %-7.1f  %-7.1f" % (key,  sim.IF_cond_exp.default_parameters[key],
                                                 sim.IF_cond_exp.parameter_ranges[key][0],
                                                 sim.IF_cond_exp.parameter_ranges[key][1])
    print "==========  =======  =======  ======="
    print

print "The default ranges for the :class:`IF_cond_exp` are:"

print_param_table()

print "Some configuration options can modify these ranges. With ``speedUpFactor = 1000``, the ranges for all parameters with dimension time are modified:"

sim.IF_cond_exp.scaleParameterRangesTime(1000)

print_param_table()

sim.IF_cond_exp.scaleParameterRangesTime(10000)

print "With ``useSmallCap = True``, only the range of `tau_m` is modified:"

sim.IF_cond_exp.scaleParameterRangesCap(SMALL_HW_CAP, BIG_HW_CAP)

print_param_table()
