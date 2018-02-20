# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging

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

@pytest.fixture()
def mockproc(mocksubprocess):
    ret = mock.MagicMock()
    ret.returncode = 0
    mocksubprocess.Popen.return_value = ret
    return ret

##__________________________________________________________________||
def test_query_files_for_subprocess_call(mocksubprocess, mockproc):
    cmsdataset = '/QCD_HT500to700/RunIISummer16NanoAOD/NANOAODSIM'
    mockproc.communicate.return_value = 'file1.root\nfile2.root\n', ''
    results = atnanoaod.dasquery.query_files_for(cmsdataset)
    assert mock.call(
        'dasgoclient -query="file dataset={}" -unique'.format(cmsdataset),
        shell=True, stderr=mocksubprocess.PIPE, stdout=mocksubprocess.PIPE
    ) == mocksubprocess.Popen.call_args
    assert ['file1.root', 'file2.root'] == results

##__________________________________________________________________||
params = ('\n', ' ', '\t')
ids = ['{!r}'.format(p) for p in params]
@pytest.mark.parametrize('sep', params, ids=ids)
def test_query_files_for_separator(mockproc, sep):
    cmsdataset = '/QCD_HT500to700/RunIISummer16NanoAOD/NANOAODSIM'
    files = ['file1.root', 'file2.root']
    return_value_stdout = sep.join(files)
    mockproc.communicate.return_value = return_value_stdout, ''
    results = atnanoaod.dasquery.query_files_for(cmsdataset)
    assert files == results

##__________________________________________________________________||
params = ('\n', '', ' ')
ids = ['{!r}'.format(p) for p in params]
@pytest.mark.parametrize('return_value_stdout', params, ids=ids)
def test_query_files_for_empty_result(mockproc, return_value_stdout):
    cmsdataset = '/QCD_HT500to700/RunIISummer16NanoAOD/NANOAODSIM'
    mockproc.communicate.return_value = return_value_stdout, ''
    results = atnanoaod.dasquery.query_files_for(cmsdataset)
    assert [ ] == results

##__________________________________________________________________||
def test_query_files_for_error(mockproc, caplog):
    mockproc.returncode = 1
    stdin = 'result'
    stderr = 'error msg'
    mockproc.communicate.return_value = stdin, stderr
    cmsdataset = '/QCD_HT500to700/RunIISummer16NanoAOD/NANOAODSIM'
    with caplog.at_level(logging.DEBUG, logger='atnanoaod'):
        results = atnanoaod.dasquery.query_files_for(cmsdataset)

    assert [ ] == results

    assert len(caplog.records) == 3
    assert caplog.records[0].levelname == 'DEBUG'
    assert caplog.records[1].levelname == 'ERROR'
    assert caplog.records[2].levelname == 'ERROR'
    assert 'dasquery' in caplog.records[1].name
    assert stderr in caplog.records[2].msg

##__________________________________________________________________||
def test_query_files_for_stderr(mockproc, caplog):
    stdin = 'result'
    stderr = 'error msg'
    mockproc.communicate.return_value = stdin, stderr
    cmsdataset = '/QCD_HT500to700/RunIISummer16NanoAOD/NANOAODSIM'
    with caplog.at_level(logging.DEBUG, logger='atnanoaod'):
        results = atnanoaod.dasquery.query_files_for(cmsdataset)

    assert [stdin] == results

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'DEBUG'
    assert caplog.records[1].levelname == 'WARNING'
    assert 'dasquery' in caplog.records[1].name
    assert stderr in caplog.records[1].msg

##__________________________________________________________________||
