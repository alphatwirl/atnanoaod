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
from alphatwirl.misc.deprecation import _deprecated_class_method_option

from .cfgmaker import EventBuilderConfigMaker
from .eventbuilder import EventBuilder
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
                 dispatcher_options=dict(),
                 process=4,
                 user_modules=(),
                 max_events_per_dataset=-1,
                 max_events_per_process=-1,
                 max_files_per_dataset=-1,
                 max_files_per_process=1,
                 profile=False, profile_out_path=None
    ):
        self.parallel = alphatwirl.parallel.build_parallel(
           parallel_mode=parallel_mode,
           quiet=quiet,
           processes=process,
           user_modules=user_modules,
           ## htcondor_job_desc_extra=htcondor_job_desc_extra,
           dispatcher_options=dispatcher_options
        )
        self.outdir = outdir
        self.force =  force
        self.max_events_per_dataset = max_events_per_dataset
        self.max_events_per_process = max_events_per_process
        self.max_files_per_dataset = max_files_per_dataset
        self.max_files_per_process = max_files_per_process
        self.profile = profile
        self.profile_out_path = profile_out_path
        self.parallel_mode = parallel_mode

    def run(self, datasets, reader_collector_pairs):
        self.parallel.begin()
        try:
            loop = self._configure(datasets, reader_collector_pairs)
            self._run(loop)
        except KeyboardInterrupt:
            logger = logging.getLogger(__name__)
            logger.warning('received KeyboardInterrupt')
            if query_yes_no('terminate running jobs'):
               logger.warning('terminating running jobs')
               self.parallel.terminate()
            else:
               logger.warning('not terminating running jobs')
        self.parallel.end()

    def _configure(self, datasets, reader_collector_pairs):

        dataset_readers = alphatwirl.datasetloop.DatasetReaderComposite()

        reader_top = alphatwirl.loop.ReaderComposite()
        collector_top = alphatwirl.loop.CollectorComposite()
        for r, c in reader_collector_pairs:
            reader_top.add(r)
            collector_top.add(c)
        eventLoopRunner = alphatwirl.loop.MPEventLoopRunner(self.parallel.communicationChannel)
        eventBuilderConfigMaker = EventBuilderConfigMaker()
        datasetIntoEventBuildersSplitter = alphatwirl.loop.DatasetIntoEventBuildersSplitter(
            EventBuilder=EventBuilder,
            eventBuilderConfigMaker=eventBuilderConfigMaker,
            maxEvents=self.max_events_per_dataset,
            maxEventsPerRun=self.max_events_per_process,
            maxFiles=self.max_files_per_dataset,
            maxFilesPerRun=self.max_files_per_process
        )
        eventReader = alphatwirl.loop.EventDatasetReader(
            eventLoopRunner=eventLoopRunner,
            reader=reader_top,
            collector=collector_top,
            split_into_build_events=datasetIntoEventBuildersSplitter
        )

        dataset_readers.add(eventReader)

        if self.parallel_mode in ('subprocess', 'htcondor'):
            loop = alphatwirl.datasetloop.ResumableDatasetLoop(
                datasets=datasets, reader=dataset_readers,
                workingarea=self.parallel.workingarea
            )
        else:
            loop = alphatwirl.datasetloop.DatasetLoop(
                datasets=datasets,
                reader=dataset_readers
            )

        return loop

    def _run(self, loop):
        if not self.profile:
            loop()
        else:
            alphatwirl.misc.print_profile_func(
               func=loop,
               profile_out_path=self.profile_out_path
            )

##__________________________________________________________________||
