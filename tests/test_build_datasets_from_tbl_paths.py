# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import collections

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atnanoaod

##__________________________________________________________________||
@pytest.fixture()
def tbl_cmsdataset_paths():
    thisdir = os.path.dirname(os.path.abspath(__file__))
    return [
        os.path.join(thisdir, 'tbl', 'tbl_dataset_cmsdataset_01.txt'),
        os.path.join(thisdir, 'tbl', 'tbl_dataset_cmsdataset_02.txt'),
        os.path.join(thisdir, 'tbl', 'tbl_dataset_cmsdataset_empty.txt')
    ]

@pytest.fixture()
def mock_build_datasets(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['atnanoaod.query']
    monkeypatch.setattr(module, 'build_datasets', ret)
    return ret

def test_build_datasets_from_tbl_paths(tbl_cmsdataset_paths, mock_build_datasets):

    atnanoaod.query.build_datasets_from_tbl_paths(
        tbl_cmsdataset_paths=tbl_cmsdataset_paths
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

##__________________________________________________________________||
