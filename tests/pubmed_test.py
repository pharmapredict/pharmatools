# -*- coding: UTF-8 -*-

# Import from standard library
import os
import pandas as pd
import pharmatools

# Import from our lib
from pharmatools.pubmed import get_pubmed_data
import pytest


def test_get_pubmed_data():
    assert (
        type(
            get_pubmed_data(
                "rivaroxaban", "pulmonary embolism", pd.to_datetime("2018-01-01")
            )
        )
        == tuple
    )
