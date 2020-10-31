#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Apode Project (https://github.com/ngrion/apode).
# Copyright (c) 2020, Néstor Grión and Sofía Sappia
# License: MIT
#   Full Text: https://github.com/ngrion/apode/blob/master/LICENSE.txt

# =============================================================================
# DOCS
# =============================================================================

"""Plots for Apode."""


# =============================================================================
# IMPORTS
# =============================================================================


# import numpy as np
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import attr


# =============================================================================
# FUNCTIONS
# =============================================================================


@attr.s(frozen=True)
class PlotAccsesor:
    idf = attr.ib()

    def __call__(self, method=None, **kwargs):
        method = "hist" if method is None else method
        method_func = getattr(self, method)
        return method_func(**kwargs)

    # tipo = 'r' o None  simple
    # tipo = 'g'  generalizada
    #  tipo = 'a' absoluta
    # ver n=0,1
    def lorenz(self, alpha="r"):
        df = lorenz_data(self, alpha)
        q = df.population
        z = df.variable
        qd = df.line

        plt.plot(q, z)
        plt.plot(q, qd)
        plt.xlabel("Cumulative % of population")
        if alpha == "r":
            plt.ylabel("Cumulative % of variable")
            plt.title("Lorenz Curve")
        elif alpha == "g":
            plt.ylabel("Scaled Cumulative % of variable")
            plt.title("Generalized Lorenz Curve")
        elif alpha == "a":
            plt.ylabel("Cumulative deviaton")
            plt.title("Absolut Lorenz Curve")
        plt.show()

    # Pen Parade
    # ver n=0,1
    def pen(self, pline=None):
        df, me = pen_data(self, pline=None)
        q = df.population
        z = df.variable
        qd = df.line
        plt.plot(q, z)
        plt.plot(q, qd, label="Mean")
        if not (pline is None):
            qpl = np.ones(len(z)) * pline / me
            plt.plot(q, qpl, label="Poverty line")
        plt.xlabel("Cumulative % of population")
        plt.ylabel("Medianized variable")
        plt.title("Pen's Parade")
        plt.legend()
        plt.show()

    # TIP Curve
    def tip(self, pline, plot=True):
        """TIP curve.
        Three 'I's of Poverty (TIP) curves, based on distributions
        of poverty gaps, provide evocative graphical summaries of
        the incidence, intensity, and inequality dimensions of
        poverty, and a means for checking for unanimous poverty
        orderings according to a wide class of poverty indices.
        More info: Jenkins and Lambert (1997)
        """
        df = tip_data(self, pline)
        p = df.population
        z = df.variable
        plt.plot(p, z)
        plt.title("TIP Curve")
        plt.ylabel("Cumulated poverty gaps")
        plt.xlabel("Cumulative % of population")
        plt.show()

    def __getattr__(self, aname):
        return getattr(self.idf.data.plot, aname)


# tipo = 'r' o None  simple
# tipo = 'g'  generalizada
#  tipo = 'a' absoluta
# ver n=0,1
def lorenz_data(self, alpha="r"):
    y = self.idf.data[self.idf.varx].values
    y = np.sort(y)
    n = len(y)
    z = np.cumsum(y) / y.sum()
    q = np.arange(0, n + 1) / n
    qd = q
    if alpha == "r":
        pass
    elif alpha == "g":
        mu = np.mean(y)
        z = z * mu
        qd = q * mu
    elif alpha == "a":
        mu = np.mean(y)
        qd = q * 0
        z = np.cumsum(y - mu)
    z = np.insert(z, 0, 0)
    return pd.DataFrame({"population": q, "variable": z, "line": qd})


# Pen Parade
# ver n=0,1
def pen_data(self, pline=None):
    y = self.idf.data[self.idf.varx].values
    y = np.sort(y)
    n = len(y)
    me = np.median(y)
    q = np.arange(0, n + 1) / n
    mu = np.mean(y)
    qd = np.ones(n + 1) * mu / me
    z = np.copy(y) / me
    z = np.insert(z, 0, 0)
    return pd.DataFrame({"population": q, "variable": z, "line": qd}), me


# TIP Curve
def tip_data(self, pline):
    if pline < 0:
        raise ValueError(f"'pline' must be >= 0. Found '{pline}'")
    y = self.idf.data[self.idf.varx].values
    ys = np.sort(y)
    n = len(ys)
    q = sum(ys < pline)
    ygap = np.zeros(n)
    ygap[0:q] = (pline - ys[0:q]) / pline

    z = np.cumsum(ygap) / n
    z = np.insert(z, 0, 0)
    p = np.arange(0, n + 1) / n
    return pd.DataFrame({"population": p, "variable": z})
