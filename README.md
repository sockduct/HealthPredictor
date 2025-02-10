# HealthPredictor

## CIS 579 Group 1 Healthcare Project

## Setup

* Install git - see [here](https://git-scm.com/downloads/win) for Windows
* Clone the repo from GitHub:
  `git clone https://github.com/sockduct/HealthPredictor.git`
* ~~Install Python 3.13~~
  * Note:  As of February 10, 2025 - the CatBoost Python package used in this
    Jupyter Notebook is not compatible with Python 3.13.  See [here](
    https://catboost.ai/docs/en/concepts/python-installation) for details.
* Install Python 3.12, 64 bit - see
  [here](https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe) for
  Windows as of February 10, 2025
* Setup and activate a Python virtual environment:
  * Windows:

    ```PowerShell
    py -3.12 -m venv .venv
    .venv\scripts\activate
    ```

* Install required libraries from within Python virtual environment:
  `pip install -r requirements.txt`
  * Note:  If some of the dependencies fail to install with an error message
           about missing rustc, look at installing Visual Studio Build Tools and
           the Rust Compiler as outlined below.
* You may need to install the Visual Studio Build Tools and Rust Compiler to
  build some of the dependencies:
  * [Install Rust](https://www.rust-lang.org/tools/install)
  * [Install Rust from CLI on Windows](
    https://www.petergirnus.com/blog/how-to-install-rust-on-windows)
* Start the Jupyter lab environment to browse/work on the Notebooks:
  `jupyter lab`
