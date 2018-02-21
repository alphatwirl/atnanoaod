# Tai Sakuma <tai.sakuma@cern.ch>
import subprocess
import logging

import ROOT

logger = logging.getLogger(__name__)

##__________________________________________________________________||
def convert_lfn_to_pfn_or_aaa(path):
    if not path.startswith('/store/'): return path

    pfn = subprocess.check_output(['edmFileUtil', '-d', path]).strip()
    f = ROOT.TFile.Open(pfn)
    if not IsROOTNullPointer(f) and f.IsOpen():
        logger.info('successfully opened local file: {}'.format(pfn))
        return pfn

    aaa = 'root://cms-xrd-global.cern.ch/{}'.format(path)
    logger.info('cannot open local file. will use AAA: {}'.format(aaa))
    return aaa

##__________________________________________________________________||
def IsROOTNullPointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##__________________________________________________________________||
