# Tai Sakuma <tai.sakuma@cern.ch>
import subprocess
import logging
import collections

import pandas as pd

import alphatwirl

logger = logging.getLogger(__name__)

from .dasquery import query_files_for
from .dataset import Dataset

##__________________________________________________________________||
def build_datasets(dataset_dict):

    parallel = alphatwirl.parallel.build_parallel(
        parallel_mode='multiprocessing'
    )
    parallel.begin()

    for dataset, cmsdatasets in dataset_dict.items():
        parallel.communicationChannel.put(mk_dataset_files_list, dataset, cmsdatasets)

    results = parallel.communicationChannel.receive()

    parallel.end()

    return results

##__________________________________________________________________||
def mk_dataset_files_list(dataset, cmsdatasets):
    files =  [ ]
    for s in cmsdatasets:
        files += query_files_for(s)
    files = ['root://cms-xrd-global.cern.ch/{}'.format(f) for f in files]
    return Dataset(name=dataset, files=files)

##__________________________________________________________________||
def build_datasets_from_tbl(tbl_cmsdataset, datasets=None):

    dataset_dict = collections.OrderedDict()

    if datasets is not None:
        tbl_cmsdataset = tbl_cmsdataset.loc[datasets]

    for dataset in tbl_cmsdataset.index.unique():
        row = tbl_cmsdataset.loc[[dataset]]
        cmsdatasets = row.cmsdataset.loc[[dataset]].unique().tolist()
        dataset_dict[dataset] = cmsdatasets

    return build_datasets(dataset_dict)

##__________________________________________________________________||
def build_datasets_from_tbl_paths(tbl_cmsdataset_paths, datasets=None):

    tbls = [ ]
    for p in tbl_cmsdataset_paths:
        tbl_ = pd.read_table(
            p, delim_whitespace=True, index_col='dataset', comment='#',
        )
        tbls.append(tbl_)
    tbl = pd.concat(tbls)
    return build_datasets_from_tbl(tbl, datasets=datasets)

##__________________________________________________________________||
