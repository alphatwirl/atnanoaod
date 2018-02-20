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
def build_datasets_from_tbl(tbl_dataset_cmsdataset, datasets=None):

    try:
        # assume tbl_dataset_cmsdataset is a path to a tbl
        tbl_dataset_cmsdataset = pd.read_table(
            tbl_dataset_cmsdataset,
            delim_whitespace=True,
            index_col='dataset',
            comment='#',
        )
    except ValueError:
        # otherwise, assume tbl_dataset_cmsdataset is a tbl itself
        pass

    dataset_dict = collections.OrderedDict()

    for dataset in tbl_dataset_cmsdataset.index.unique():
        row = tbl_dataset_cmsdataset.loc[[dataset]]
        if datasets is not None and dataset not in datasets:
            continue
        cmsdatasets = row.cmsdataset.loc[[dataset]].tolist()
        dataset_dict[dataset] = cmsdatasets

    return build_datasets(dataset_dict, datasets)

def build_datasets(dataset_dict, datasets=None):

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
