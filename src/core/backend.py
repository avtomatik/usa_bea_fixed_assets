#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 20:21:27 2023

@author: green-machine
"""


from functools import cache

import pandas as pd
from core.classes import SeriesID


def stockpile(series_ids: list[SeriesID]) -> pd.DataFrame:
    """


    Parameters
    ----------
    series_ids : list[SeriesID]
        DESCRIPTION.

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================.

    """
    return pd.concat(
        map(
            lambda _: read_source(_).pipe(pull_by_series_id, _),
            series_ids
        ),
        axis=1,
        sort=True
    )


@cache
def read_source(series_id: SeriesID) -> pd.DataFrame:
    """


    Parameters
    ----------
    series_id : SeriesID
        DESCRIPTION.

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================.

    """
    return pd.read_csv(**series_id.source.get_kwargs())


def pull_by_series_id(df: pd.DataFrame, series_id: SeriesID) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================.
    series_id : SeriesID
        DESCRIPTION.

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================.

    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id.series_id].iloc[:, [1]].rename(
        columns={'value': series_id.series_id}
    )


# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: 'Section5ALL_Hist.xls'@['dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls' Offsets 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip']"""
# =============================================================================


def get_kwargs() -> dict[str, str]:
    return {
        'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'wb_name': 'Section5ALL_Hist.xls',
        'sh_name': '50900 Ann',
    }
