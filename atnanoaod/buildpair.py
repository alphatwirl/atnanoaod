# Tai Sakuma <tai.sakuma@gmail.com>

import alphatwirl

##__________________________________________________________________||
def build_counter_collector_pair(tblcfg):
    keyValComposer = alphatwirl.summary.KeyValueComposer(
        keyAttrNames=tblcfg['keyAttrNames'],
        binnings=tblcfg['binnings'],
        keyIndices=tblcfg['keyIndices'],
        valAttrNames=tblcfg['valAttrNames'],
        valIndices=tblcfg['valIndices']
    )
    nextKeyComposer = alphatwirl.summary.NextKeyComposer(tblcfg['binnings']) if tblcfg['binnings'] is not None else None
    summarizer = alphatwirl.summary.Summarizer(
        Summary=tblcfg['summaryClass']
    )
    reader = alphatwirl.summary.Reader(
        keyValComposer=keyValComposer,
        summarizer=summarizer,
        nextKeyComposer=nextKeyComposer,
        weightCalculator=tblcfg['weight'],
        nevents=tblcfg['nevents']
    )
    resultsCombinationMethod = alphatwirl.collector.ToTupleListWithDatasetColumn(
        summaryColumnNames = tblcfg['keyOutColumnNames'] + tblcfg['valOutColumnNames'],
        datasetColumnName='dataset'
    )
    deliveryMethod = alphatwirl.collector.WriteListToFile(tblcfg['outFilePath']) if tblcfg['outFile'] else None
    collector = alphatwirl.loop.Collector(resultsCombinationMethod, deliveryMethod)
    return reader, collector

##__________________________________________________________________||
