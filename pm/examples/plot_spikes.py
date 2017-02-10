#!/usr/bin/env python

import matplotlib
#matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse

ticker.Locator.MAXTICKS *= 100

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('--plotfilename', default="")
parser.add_argument('--xlim', type=float, nargs=2,default=None)
parser.add_argument('--ylim', type=float, nargs=2,default=None)
parser.add_argument('--membrane_file', type=str, default="")
parser.add_argument('--neuron_idx', type=int, default=None)
parser.add_argument('--show', action="store_true")
args = parser.parse_args()

def raster(times, neurons, color='k'):

    ax = plt.gca()

    neurons = np.array(neurons)

    plt.vlines(times, neurons-0.45, neurons + 0.45, color=color, linewidth=1.5)

    plt.xlabel('bio time [ms]')
    plt.ylabel('neuron index')

    return ax

def plot(infilename, outfilename="", xlim=None, ylim=None, membrane_file="", neuron_idx=None):
    """
    infilename: first column neuron ids
                second column spike times

    outfilename: e.g. result.pdf, result.png

    xlim: (xmin, xmax)

    ylim: (ymin, ymax)

    membrane_file: voltage trace (time [ms], membrane [V])

    neuron_idx: neuron index for overlay with membrane trace
    """

    spikes = np.loadtxt(args.file.name)

    if not len(spikes):
        print "no spikes in {}".format(infilename)
        return

    margins={"left":0.11, "right":0.95, "top":0.95, "bottom":0.11}

    fig = plt.figure()

    times, neurons = spikes[:,1], spikes[:,0]

    ax = raster(times, neurons)

    plt.subplots_adjust(**margins)

    if args.xlim:
        plt.xlim(*args.xlim)

    if args.ylim:
        plt.ylim(*args.ylim)
        yticks = np.arange(args.ylim[0], args.ylim[1], 10.0)
    else:
        plt.ylim(min(neurons)-0.5, max(neurons)+0.5)
        yticks = np.arange(min(neurons), max(neurons)+1, 10.0)

    plt.yticks(yticks)

    if membrane_file and neuron_idx != None:
        membrane = np.loadtxt(membrane_file)
        membrane_times, membrane_values  = membrane[:,1], membrane[:,2]

        mean_membrane_values = np.mean(membrane_values)
        min_membrane_values = np.min(membrane_values)
        max_membrane_values = np.max(membrane_values)

        membrane_values -= min_membrane_values
        membrane_values /= (max_membrane_values - min_membrane_values)
        membrane_values += neuron_idx - 0.5

        plt.plot(membrane_times, membrane_values, "-.")

    if args.plotfilename:
        plt.savefig(args.plotfilename)

if __name__ ==  "__main__":

    plot(args.file.name, args.plotfilename, args.xlim, args.ylim, args.membrane_file, args.neuron_idx)

    if args.show:
        plt.show()
