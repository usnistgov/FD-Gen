import os
import sys

# main_code uses flat imports (e.g. `import parse_syntax`), so put it on the path.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'main_code'))


def pytest_addoption(parser):
    parser.addoption('--update-baselines', action='store_true',
                     help='regenerate tests/regression/baselines from the current code')
