# Tai Sakuma <tai.sakuma@cern.ch>
import subprocess
import logging

logger = logging.getLogger(__name__)

##__________________________________________________________________||
def query_files_for(cmsdataset):
    query = "file dataset={}".format(cmsdataset)
    command = 'dasgoclient -query="{}" -unique'.format(query)
    logger.debug('executing: {}'.format(command))
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = proc.communicate()
    return stdout.strip().split('\n')

##__________________________________________________________________||
