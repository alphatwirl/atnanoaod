# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import collections
import logging

try:
    ## https://root-forum.cern.ch/t/pyroot-hijacks-help/15207
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    pass

from .cmsfilepath import convert_lfn_to_pfn_or_aaa

##__________________________________________________________________||
EventBuilderConfig = collections.namedtuple(
    'EventBuilderConfig',
    'inputPaths treeName maxEvents start dataset name'
)

##__________________________________________________________________||
class EventBuilderConfigMaker(object):
    def __init__(self):
        self.treeName = 'Events'

    def create_config_for(self, dataset, files, start, length):
        config = EventBuilderConfig(
            inputPaths=files,
            treeName=self.treeName,
            maxEvents=length,
            start=start,
            dataset=dataset, # for scribblers
            name=dataset.name # for the progress report writer
        )
        return config

    def file_list_in(self, dataset, maxFiles):
        if maxFiles < 0:
            return dataset.files
        return dataset.files[:min(maxFiles, len(dataset.files))]

    def nevents_in_file(self, path):
        try:
            path = convert_lfn_to_pfn_or_aaa(path)
            file = ROOT.TFile.Open(path)
            tree = file.Get(self.treeName)
            return tree.GetEntriesFast()
        except StandardError as e:
            logger = logging.getLogger(__name__)
            logger.warning(str(e))
            logger.warning(path)
            logger.warning('returning 0')
            return 0

##__________________________________________________________________||
