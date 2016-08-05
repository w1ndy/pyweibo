#
# This file is mostly taken from https://gist.github.com/cdiener/10491632
# Copyright (c) cdiener

from PIL import Image
import numpy as np

chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

def convertImageToString(img):
    WCF = 7/4
    S = (round(img.size[0] * 0.75 * WCF), round(img.size[1] * 0.75))
    img = np.array(img.resize(S), copy=True)
    img -= img.min()
    img = (img / img.max()) * (chars.size - 1)
    return '\n'.join((''.join(r) for r in chars[img.astype(int)]))
