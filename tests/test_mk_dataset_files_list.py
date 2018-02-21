# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atnanoaod

##__________________________________________________________________||
@pytest.fixture()
def query_files_for(monkeypatch):
    ret = mock.MagicMock()
    module = sys.modules['atnanoaod.query']
    monkeypatch.setattr(module, 'query_files_for', ret)
    return ret


@pytest.fixture()
def convert_lfn_to_pfn_or_aaa(monkeypatch):
    ret = mock.MagicMock()
    module = sys.modules['atnanoaod.query']
    monkeypatch.setattr(module, 'convert_lfn_to_pfn_or_aaa', ret)
    ret.side_effect = lambda x: 'root:/{}'.format(x)
    return ret

##__________________________________________________________________||
def test_mk_dataset_files_list_one_cmsdataset(query_files_for, convert_lfn_to_pfn_or_aaa):
    dataset = 'QCD_HT200to300'
    cmsdatasets = ['/QCD_HT200to300_13TeV/05Feb2018-v1/NANOAODSIM']
    query_files_for.return_value = ['/store/file1.root', '/store/file2.root']
    results = atnanoaod.query.mk_dataset_files_list(dataset, cmsdatasets)
    assert atnanoaod.dataset.Dataset(
        name=dataset,
        files=['root://store/file1.root', 'root://store/file2.root']) == results
    assert [mock.call(e) for e in cmsdatasets] == query_files_for.call_args_list
    assert [mock.call('/store/file1.root'), mock.call('/store/file2.root')] ==convert_lfn_to_pfn_or_aaa.call_args_list

##__________________________________________________________________||
