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

##__________________________________________________________________||
def test_mk_dataset_files_list_one_cmsdataset(query_files_for):
    dataset = 'QCD_HT200to300'
    cmsdatasets = ['/QCD_HT200to300_13TeV/05Feb2018-v1/NANOAODSIM']
    results = atnanoaod.query.mk_dataset_files_list(dataset, cmsdatasets)
    assert atnanoaod.dataset.Dataset(name=dataset, files=[]) == results
    assert [mock.call(e) for e in cmsdatasets] == query_files_for.call_args_list

##__________________________________________________________________||
