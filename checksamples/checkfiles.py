# from signal import all_signals as samples
from CMGTools.HNL.samples.signal import all_signals as samples
import numpy as np

for sample in samples:
   for i in np.arange(len(sample.files)):
      print(sample.files[i])
