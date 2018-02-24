# Tai Sakuma <tai.sakuma@gmail.com>
import ROOT

from alphatwirl.roottree import BEvents

from .cmsfilepath import convert_lfn_to_pfn_or_aaa

##__________________________________________________________________||
class EventBuilder(object):
    def __init__(self, config):
        self.config = config

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self.config
        )

    def __call__(self):
        chain = ROOT.TChain(self.config.treeName)
        for path in self.config.inputPaths:
            path = convert_lfn_to_pfn_or_aaa(path)
            chain.Add(path)
        events = BEvents(chain, self.config.maxEvents, self.config.start)
        events.config = self.config
        return events

##__________________________________________________________________||
