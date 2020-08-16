import sys
import training.train as Train

import sklearn.utils._cython_blas
import sklearn.neighbors.typedefs
import sklearn.neighbors.quad_tree
import sklearn.tree
import sklearn.tree._utils

# main.py
if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
        input('Press ENTER to exit')

    # Generate a Buy or Sell Recommendation based on current properties of the stock
train = Train.Train()