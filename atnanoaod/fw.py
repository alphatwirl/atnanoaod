# Tai Sakuma <tai.sakuma@cern.ch>
import os
import sys
import logging

import gzip

try:
   import cPickle as pickle
except:
   import pickle

import alphatwirl

from .yes_no import query_yes_no

##__________________________________________________________________||
import logging
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler(stream=sys.stdout)
log_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

##__________________________________________________________________||
class AtNanoAOD(object):
    """A simple framework for looping over NanoAOD events with alphatwirl

    """
    def __init__(self, outdir,
                 force=False, quiet=False,
                 parallel_mode='multiprocessing',
                 htcondor_job_desc_extra=[ ],
                 process=4,
                 user_modules=(),
                 max_events_per_dataset=-1, max_events_per_process=-1,
                 profile=False, profile_out_path=None
    ):
        self.parallel = alphatwirl.parallel.build_parallel(
            parallel_mode=parallel_mode,
            quiet=quiet,
            processes=process,
            user_modules=user_modules,
            htcondor_job_desc_extra=htcondor_job_desc_extra
        )

##__________________________________________________________________||
