# Tai Sakuma <tai.sakuma@cern.ch>
import subprocess
import logging

import pandas as pd

import alphatwirl

logger = logging.getLogger(__name__)

from .dasquery import query_files_for
from .dataset import Dataset

##__________________________________________________________________||
def build_datasets(tbl_dataset_cmsdataset, datasets=None):

    try:
        # assume tbl_dataset_cmsdataset is a path to a tbl
        tbl_dataset_cmsdataset = pd.read_table(tbl_dataset_cmsdataset, delim_whitespace=True)
    except ValueError:
        # otherwise, assume tbl_dataset_cmsdataset is a tbl itself
        pass

    parallel = alphatwirl.parallel.build_parallel(
        parallel_mode='multiprocessing'
    )
    parallel.begin()
    
    for i in tbl_dataset_cmsdataset.index:
        row = tbl_dataset_cmsdataset.loc[[i]]
        dataset = row.dataset.iloc[0]
        if datasets is not None and dataset not in datasets:
            continue
        cmsdataset = row.cmsdataset.iloc[0]
        parallel.communicationChannel.put(mk_dataset_files_list, dataset, cmsdataset)

    results = parallel.communicationChannel.receive()

    parallel.end()

    return results
    
##__________________________________________________________________||
def mk_dataset_files_list(dataset, cmsdataset):
    files = query_files_for(cmsdataset)
    return Dataset(name=dataset, files=files)

##__________________________________________________________________||


