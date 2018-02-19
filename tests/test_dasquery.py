# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atnanoaod

##__________________________________________________________________||
@pytest.fixture()
def mocksubprocess(monkeypatch):
    ret = mock.MagicMock()
    module = sys.modules['atnanoaod.dasquery']
    monkeypatch.setattr(module, 'subprocess', ret)
    return ret

def test_query_files_for(mocksubprocess):
    cmsdataset = '/QCD_HT500to700/RunIISummer16NanoAOD/NANOAODSIM'
    mocksubprocess.Popen().communicate.return_value = 'file1.root\nfile2.root\n', ''
    results = atnanoaod.dasquery.query_files_for(cmsdataset)
    assert [mock.call(),
            mock.call(
                'dasgoclient -query="file dataset={}" -unique'.format(cmsdataset),
                shell=True, stderr=mocksubprocess.PIPE, stdout=mocksubprocess.PIPE
            )] == mocksubprocess.Popen.call_args_list
    assert ['file1.root', 'file2.root'] == results

##__________________________________________________________________||
