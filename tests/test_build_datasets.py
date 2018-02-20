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
def mock_channel():
    ret = mock.Mock()
    ret.results = [ ]
    ret.put.side_effect = lambda t, *a, **k: ret.results.append(t(*a, **k))
    ret.receive.return_value = ret.results
    return ret

def test_mock_channel(mock_channel):
    mock_channel.put(pow, 2, 3)
    mock_channel.put(dict, a=10, b=30)
    assert [8, {'a': 10, 'b': 30}] == mock_channel.receive()

@pytest.fixture()
def mock_alphatwirl(monkeypatch, mock_channel):
    ret = mock.Mock()
    module = sys.modules['atnanoaod.query']
    monkeypatch.setattr(module, 'alphatwirl', ret)
    ret.parallel.build_parallel().communicationChannel = mock_channel
    return ret

@pytest.fixture()
def mock_mk_dataset_files_list(monkeypatch, mock_alphatwirl):
    ret = mock.Mock()
    module = sys.modules['atnanoaod.query']
    monkeypatch.setattr(module, 'mk_dataset_files_list', ret)
    return ret

def test_build_datasets(mock_mk_dataset_files_list):

    dataset_dict = collections.OrderedDict([
        ('QCD_HT200to300', ['/QCD_HT200to300_13TeV/05Feb2018-v1/NANOAODSIM']),
        ('QCD_HT500to700', [
            '/QCD_HT500to700_13TeV/05Feb2018-v1/NANOAODSIM',
            '/QCD_HT500to700_13TeV/05Feb2018_ext1-v1/NANOAODSIM'
        ]),
        ('QCD_HT700to1000', ['/QCD_HT700to1000_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        ('QCD_HT1000to1500', ['/QCD_HT1000to1500_13TeV/05Feb2018-v1/NANOAODSIM']),
        ('QCD_HT1500to2000', ['/QCD_HT1500to2000_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        ('QCD_HT2000toInf', [
            '/QCD_HT2000toInf_13TeV/05Feb2018-v1/NANOAODSIM',
            '/QCD_HT2000toInf_13TeV/05Feb2018_ext1-v1/NANOAODSIM'
        ])
    ])

    atnanoaod.query.build_datasets(dataset_dict=dataset_dict)

    expected = [
        mock.call('QCD_HT200to300', ['/QCD_HT200to300_13TeV/05Feb2018-v1/NANOAODSIM']),
        mock.call('QCD_HT500to700', ['/QCD_HT500to700_13TeV/05Feb2018-v1/NANOAODSIM', '/QCD_HT500to700_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        mock.call('QCD_HT700to1000', ['/QCD_HT700to1000_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        mock.call('QCD_HT1000to1500', ['/QCD_HT1000to1500_13TeV/05Feb2018-v1/NANOAODSIM']),
        mock.call('QCD_HT1500to2000', ['/QCD_HT1500to2000_13TeV/05Feb2018_ext1-v1/NANOAODSIM']),
        mock.call('QCD_HT2000toInf', ['/QCD_HT2000toInf_13TeV/05Feb2018-v1/NANOAODSIM', '/QCD_HT2000toInf_13TeV/05Feb2018_ext1-v1/NANOAODSIM'])
    ]
    assert expected == mock_mk_dataset_files_list.call_args_list

##__________________________________________________________________||
