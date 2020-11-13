# -*- coding: UTF-8 -*-

# Import from standard library
import os
import pharmatools

# Import from our lib
from pharmatools.clinical_trials import get_trial_data
import pytest


def test_get_trial_data():
    assert get_trial_data("rivaroxaban", "pulmonary embolism", "2019-01-01") != None
