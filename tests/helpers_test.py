# -*- coding: UTF-8 -*-

# Import from standard library
import os
import pharmatools

# Import from our lib
from pharmatools.helpers import get_disease_term
import pytest


def test_get_disease_term():
    assert get_disease_term("Diabetes, heart disease") == "Diabetes OR heart disease"
