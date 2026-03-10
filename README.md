# Basic-Stock-Prediction
A simplistic attempt at applying machine learning to stock information that works surprisingly well for long term investments.

## Installation

Create a virtual environment (recommended), then install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Key libraries:
- `scikit-learn==1.8.0` for modeling and time-series cross-validation
- `yfinance` for historical price data and metadata
- `pandas`, `numpy`, `matplotlib` for data handling and plotting
- `streamlit` for the web UI

## Model evaluation (time-series aware)

The core model (`training/model.py`) now uses **chronological splits** for evaluation:
- Features and labels are sorted by time index.
- The **last 25% of observations** are used as a hold-out test set (no shuffling).
- Cross-validation uses `TimeSeriesSplit(n_splits=7)` so each fold respects the arrow of time.

This better reflects the real-world scenario where the model is trained on past data and evaluated on unseen future data.

## Output to exe

PyInstaller is used.
In PyCharm, `-m PyInstaller` is used for interpreter options.
Also, the following are imported to avoid problems with using PyInstaller:

```python
import sklearn.utils._cython_blas
import sklearn.neighbors.typedefs
import sklearn.neighbors.quad_tree
import sklearn.tree
import sklearn.tree._utils
```
