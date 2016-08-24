# machinery for a progress bar
import time
from tempfile import TemporaryFile
import uuid
from itertools import izip

import requests

from IPython.display import HTML, Javascript, display

import numpy as np
from scipy.io import loadmat

# First, create a helper class for an HTML/Javascript progress bar

# HTML template for progress bar, needs to be interpolated
PB_TEMPLATE = """
<div style="border: 1px solid black; width:500px">
  <div id="%s" style="background-color:%s; width:0%%">&nbsp;</div>
</div> 
"""

class ProgressBar(object):
    """HTML/Javascript progress bar for IPython Notebook"""
    def __init__(self, color='green'):
        # to avoid name collisions, use a UUID for the div ID
        self.divid = str(uuid.uuid4())
        # display the HTML; initially the progress bar is set at zero
        display(HTML(PB_TEMPLATE % (self.divid, color)))
    def set_progress(self, fraction):
        # set progress to the given fraction between 0 and 1
        pct = 100 * fraction # convert to percent
        # set the width property on the div; this will change the size
        # of the colored bar inside the larger black-outlined bar
        display(Javascript("$('div#%s').width('%i%%')" % (self.divid, pct)))

# helper function to call parallel function and track
# progress using a ProgressBar
def progress_map(pfn, args):
    N = len(args)
    pb = ProgressBar()
    progress = 1. * np.arange(1,N+1) / N
    for i, r in izip(progress, pfn.map(args)):
        if r is not None:
            yield r
        pb.set_progress(i)

def loadmat_url(url):
    with TemporaryFile() as f:
        f.write(requests.get(url, stream=True).content)
        return loadmat(f, squeeze_me=True)
