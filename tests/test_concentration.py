#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Apode Project (https://github.com/mchalela/apode).
# Copyright (c) 2020, Néstor Grión and Sofía Sappia
# License: MIT
#   Full Text: https://github.com/ngrion/apode/blob/master/LICENSE.txt

from apode import datasets
from apode.basic import ApodeData

import numpy as np

import pandas as pd

import pytest


# =============================================================================
# TESTS COMMON
# =============================================================================


def test_default_call():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    call_result = data.concentration("herfindahl")
    method_result = data.concentration.herfindahl()
    assert call_result == method_result


def test_invalid():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    with pytest.raises(AttributeError):
        data.concentration("foo")


# =============================================================================
# TESTS HERFINDAHL
# =============================================================================
def test_herfindahl_method():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    assert (
        data.concentration.herfindahl(normalized=True) == 0.0011776319218515382
    )
    assert (
        data.concentration.herfindahl(normalized=False) == 0.004507039815445367
    )


def test_herfindahl_call():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    assert (
        data.concentration("herfindahl", normalized=True)
        == 0.0011776319218515382
    )
    assert (
        data.concentration("herfindahl", normalized=False)
        == 0.004507039815445367
    )


def test_herfindahl_call_equal_method():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    call_result = data.concentration("herfindahl")
    method_result = data.concentration.herfindahl()
    assert call_result == method_result


def test_herfindahl_empty_array():
    y = []
    df = pd.DataFrame({"x": y})
    data = ApodeData(df, income_column="x")
    assert data.concentration.herfindahl() == 0


# =============================================================================
# TESTS ROSENBLUTH
# =============================================================================
def test_rosenbluth_method():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    np.testing.assert_allclose(
        data.concentration.rosenbluth(), 0.00506836225627098
    )


def test_rosenbluth_call():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    np.testing.assert_allclose(
        data.concentration("rosenbluth"), 0.00506836225627098
    )


def test_rosenbluth_call_equal_method():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    call_result = data.concentration("rosenbluth")
    method_result = data.concentration.rosenbluth()
    assert call_result == method_result


def test_rosenbluth_symmetry():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    y = data.data["x"].tolist()
    np.random.shuffle(y)
    df2 = pd.DataFrame({"x": y})
    dr2 = ApodeData(df2, income_column="x")
    assert data.concentration(method="rosenbluth") == dr2.concentration(
        method="rosenbluth"
    )


# =============================================================================
# TESTS CONCENTRATION_RATIO
# =============================================================================
def test_concentration_ratio_method():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    assert data.concentration.concentration_ratio(k=20) == 0.12913322818634668


def test_concentration_ratio_call():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    assert (
        data.concentration("concentration_ratio", k=20) == 0.12913322818634668
    )


def test_concentration_ratio_call_equal_method():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    call_result = data.concentration("concentration_ratio", k=20)
    method_result = data.concentration.concentration_ratio(k=20)
    assert call_result == method_result


def test_concentration_ratio_symmetry():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    y = data.data["x"].tolist()
    np.random.shuffle(y)
    df2 = pd.DataFrame({"x": y})
    dr2 = ApodeData(df2, income_column="x")
    assert data.concentration(
        method="concentration_ratio", k=20
    ) == dr2.concentration(method="concentration_ratio", k=20)


def test_concentration_k_range():
    data = datasets.make_uniform(seed=42, size=300, mu=1, nbin=None)
    n = len(data.data.values)
    with pytest.raises(ValueError):
        data.concentration(method="concentration_ratio", k=n + 1)
    with pytest.raises(ValueError):
        data.concentration(method="concentration_ratio", k=-1)
