import cPickle as pickle
import numpy as np
import matplotlib
matplotlib.use("pgf")
from cycler import cycler

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 12,               # LaTeX default is 10pt font.
    "font.size": 12,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "pgf.preamble": [
       r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
       r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
    ],
    "axes.prop_cycle" : cycler('color', ['#1f77b4', '#d62728', '#7f7f7f', '#2ca02c'])
}


matplotlib.rcParams.update(pgf_with_latex)
import matplotlib.pyplot as plt

def plot_training_curves(losses, logt_losses, lim=2400, smooth=20):
    lengths = [5, 20, 100, 200]
    def smooth(l, k=smooth):
        l = (1./k) * np.convolve(np.ones(k), l, 'valid')
        return l

    f, ax = plt.subplots(2, 1, figsize=(8, 4))

    for i, (l, r) in enumerate(zip(losses, logt_losses)):
        l = smooth(l[:lim])
        r = smooth(r[:lim])
        ax[0].plot(np.arange(len(l)), l, label="$T_{\\textrm{max}}$ = " + str(lengths[i]))
        ax[1].plot(np.arange(len(r)), r, label="$T_{\\textrm{max}}$ = " + str(lengths[i]))
    plt.tight_layout()
    for a in ax:
        a.legend()
        a.set_xlim([0, lim])
        a.set_ylabel('Loss')
        a.tick_params(axis="x", which="both", top="off")
        a.tick_params(axis="y", which="both", right="off")
    ax[1].set_xlabel('Iteration')

loc = np.load("data/location_losses.npy")
loc_logt = np.load("data/location_logt_losses.npy")
nn = np.load("data/nn_losses.npy")
nn_logt = np.load("data/nn_logt_losses.npy")

plot_training_curves(loc, loc_logt)
plt.savefig("location_training_curves.svg")
plot_training_curves(nn, nn_logt, lim=4000, smooth=20)
plt.savefig("nn_training_curves.svg")

def plot_weight_increase():
    model_lens = [5, 10, 20, 50, 100, 200]
    max_w = [5.1414762, 6.0363622, 6.9166207, 7.9150348, 8.7278414, 9.484705]
    max_w_logt = [3.4473486, 3.3840003, 3.2114298, 2.9805777, 2.7852652, 2.6212788]
    f, ax = plt.subplots(figsize=(4, 3))
    ax.plot(model_lens, max_w, 'ko', markersize=5)
    ax.plot(model_lens, max_w, 'k-', label="Unscaled")
    ax.plot(model_lens, max_w_logt, 'o', color="#1f77b4", markersize=5)
    ax.plot(model_lens, max_w_logt, '-', color="#1f77b4", label="Scaled")
    def scale_fn(lens, k):
        lens = np.array(lens)
        lens = lens - 1
        k_inv = 1.0 / k
        return k_inv * np.log(lens / (k_inv - 1))

    lens = np.arange(5,201,.5)
    plt.plot(lens, scale_fn(lens, .98), 'k--')
    plt.tight_layout()
    plt.legend(loc=4)
    ax.set_xlim([0, 210])
    ax.set_ylim([0, 10])
    ax.set_ylabel('Maximum Weight')
    ax.set_xlabel("$T_{\\textrm{max}}$")
    ax.tick_params(axis="x", which="both", top="off")
    ax.tick_params(axis="y", which="both", right="off")

    plt.savefig("weight_increase.svg")

plot_weight_increase()

def plot_cer_length_scale(cers, logt_cers, ymax):
    model_lens = [5, 10, 20, 50, 100, 200]
    
    f, ax = plt.subplots(figsize=(4, 3))
    ax.plot(model_lens, cers, 'ko', markersize=4)
    ax.plot(model_lens, cers, 'k-', label="Unscaled")
    ax.plot(model_lens, logt_cers, 'o', color="#1f77b4", markersize=4)
    ax.plot(model_lens, logt_cers, '-', color="#1f77b4", label="Scaled")
    plt.tight_layout()
    plt.legend(loc=0)
    ax.set_xlim([0, 210])
    ax.set_ylim([-0.05, ymax])
    ax.set_ylabel('CER')
    ax.set_xlabel("$T_{\\textrm{max}}$")
    ax.tick_params(axis="x", which="both", top="off")
    ax.tick_params(axis="y", which="both", right="off")

# CERs for loc_len10
cers = [0.0, 0.0, 0.0, 0.47794618975192743, 0.9730986788942552, 1.2339573020539036]
logt_cers = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
plot_cer_length_scale(cers, logt_cers, ymax=1.3)
plt.savefig("location_error_length_scale.svg")

# CERs for nn_len10
cers = [0.0, 0.0031756318859364873, 0.20973870803463, 0.6555698500255538, 0.8663413374168611, 0.9692130111453819]
logt_cers = [9.765625e-05, 0.00299830530569678, 0.2084683017121703, 0.6526417387574176, 0.8362526735009956, 0.9763687947404023]
plot_cer_length_scale(cers, logt_cers, ymax=1.0)
plt.savefig("nn_error_length_scale.svg")

def plot_cer_repeats():
    """
    nn_50_logt model evaled on 300 repeats of examples of length 100
    """
    repeats = (3, 4, 5, 6, 7, 8, 9, 10, 11)
    cers = (0.022233333333333334, 0.033966666666666666, 0.06726666666666667, 0.11216666666666666, 0.18543333333333334, 0.26156666666666667, 0.2985, 0.30706666666666665, 0.3285)
   
    f, ax = plt.subplots(figsize=(4, 3))
    ax.plot(repeats, cers, 'ko', markersize=4)
    ax.plot(repeats, cers, 'k-')
    plt.tight_layout()
    ax.set_xlim([2.7, 11.3])
    ax.set_ylim([0.0, 0.35])
    ax.set_ylabel('CER')
    ax.set_xlabel("Longest repeat subsequence")
    ax.tick_params(axis="x", which="both", top="off")
    ax.tick_params(axis="y", which="both", right="off")
    plt.savefig("cer_repeats.svg")

plot_cer_repeats()

def plot_alignments(inputs, outputs, alis, size):
    # TODO, colorscheme
    f, ax = plt.subplots(figsize=size)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    plt.pcolor(np.flipud(alis), cmap="Blues");
    plt.tight_layout()
    plt.xlabel("Inputs")
    plt.xticks(np.arange(len(inputs)) + 0.5, inputs, fontsize=7)
    plt.yticks(np.arange(len(outputs)) + 0.5, reversed(outputs), fontsize=7)
    plt.tick_params(axis="x", which="both", top="off", bottom="off")
    plt.tick_params(axis="y", which="both", right="off", left="off")
    plt.ylabel("Outputs")

with open("data/repeat_alis_loop.bin", 'r') as fid:
    alis = pickle.load(fid)[:50, :] 
    outputs = pickle.load(fid)[:50] 
    inputs = pickle.load(fid) 
plot_alignments(inputs, outputs, alis, (4, 5))
plt.savefig("repeat_alis_loop.svg")
with open("data/repeat_alis_skip.bin", 'r') as fid:
    alis = pickle.load(fid) 
    outputs = pickle.load(fid) 
    inputs = pickle.load(fid) 
plot_alignments(inputs, outputs, alis, (5, 2))
plt.savefig("repeat_alis_skip.svg")

