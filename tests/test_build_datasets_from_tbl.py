# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import collections
import pandas as pd

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atnanoaod

##__________________________________________________________________||
@pytest.fixture()
def tbl_cmsdataset():
    thisdir = os.path.dirname(os.path.abspath(__file__))
    tblpath = os.path.join(thisdir, 'tbl', 'tbl_dataset_cmsdataset_combined.txt')
    return pd.read_table(
        tblpath,
        delim_whitespace=True,
        index_col='dataset',
        comment='#',
    )

@pytest.fixture()
def tbl_cmsdataset_empty():
    thisdir = os.path.dirname(os.path.abspath(__file__))
    tblpath = os.path.join(thisdir, 'tbl', 'tbl_dataset_cmsdataset_empty.txt')
    return pd.read_table(
        tblpath,
        delim_whitespace=True,
        index_col='dataset',
        comment='#',
    )

@pytest.fixture()
def mock_build_datasets(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['atnanoaod.query']
    monkeypatch.setattr(module, 'build_datasets', ret)
    return ret

def test_build_datasets_from_tbl(tbl_cmsdataset, mock_build_datasets):

    atnanoaod.query.build_datasets_from_tbl(
        tbl_cmsdataset=tbl_cmsdataset
    )

    expected = [mock.call(collections.OrderedDict([
        ('QCD_HT200to300', ['/QCD_HT200to300_13TeV/05Feb2018-v1/NANOAODSIM']),
        ('QCD_HT500to700', [
            '/QCD_HT500to700_13TeV/05Feb2018-v1/NANOAODSIM',
            '/QCD_HT500to700_13TeV/05Feb2018_ext1-v1/NANOAODSIM',
            '/QCD_HT500to700_13TeV/05Feb2018_ext1-v2/NANOAODSIM'
        ]),
        ('QCD_HT700to1000', ['/QCD_HT700to1000_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        ('QCD_HT1000to1500', ['/QCD_HT1000to1500_13TeV/05Feb2018-v1/NANOAODSIM']),
        ('QCD_HT1500to2000', ['/QCD_HT1500to2000_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        ('QCD_HT2000toInf', [
            '/QCD_HT2000toInf_13TeV/05Feb2018-v1/NANOAODSIM',
            '/QCD_HT2000toInf_13TeV/05Feb2018_ext1-v1/NANOAODSIM'
        ]),
        ('TTJets', ['/TTJets_13TeV/05Feb2018_v2-v1/NANOAODSIM'
        ])
    ]))]

    assert expected == mock_build_datasets.call_args_list

def test_build_datasets_from_tbl_specify_datasets(tbl_cmsdataset, mock_build_datasets):

    atnanoaod.query.build_datasets_from_tbl(
        tbl_cmsdataset=tbl_cmsdataset,
        datasets=['QCD_HT700to1000', 'QCD_HT2000toInf']
    )

    expected = [mock.call(collections.OrderedDict([
        ('QCD_HT700to1000', ['/QCD_HT700to1000_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        ('QCD_HT2000toInf', [
            '/QCD_HT2000toInf_13TeV/05Feb2018-v1/NANOAODSIM',
            '/QCD_HT2000toInf_13TeV/05Feb2018_ext1-v1/NANOAODSIM'
        ]),
    ]))]

    assert expected == mock_build_datasets.call_args_list

def test_build_datasets_from_tbl_specify_empty_list(tbl_cmsdataset, mock_build_datasets):

    atnanoaod.query.build_datasets_from_tbl(
        tbl_cmsdataset=tbl_cmsdataset,
        datasets=[ ]
    )

    expected = [mock.call(collections.OrderedDict([]))]

    assert expected == mock_build_datasets.call_args_list

def test_build_datasets_from_tbl_empty_tbl(tbl_cmsdataset_empty, mock_build_datasets):

    atnanoaod.query.build_datasets_from_tbl(
        tbl_cmsdataset=tbl_cmsdataset_empty,
        datasets=[ ]
    )

    expected = [mock.call(collections.OrderedDict([]))]

    assert expected == mock_build_datasets.call_args_list

##__________________________________________________________________||
