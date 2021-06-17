# Basic-Stock-Prediction
A simplistic attempt at applying machine learning to stock information that works surprisingly well for long term investments.

# Output to exe
PyInstaller is used.
In Pycharm, -m PyInstaller is used for interpreter options.
Also, the following are imported to avoid problems with using pyinstaller.

import sklearn.utils._cython_blas
import sklearn.neighbors.typedefs
import sklearn.neighbors.quad_tree
import sklearn.tree
import sklearn.tree._utils
