import numpy as np

import QUTP


def test_list_cells_written_in_full_without_numpy_reprs():
    cell = QUTP.format_cell([np.float64(3.81), np.float64(3.81) + 2.0, np.int32(1)])
    assert cell == '[3.81, 5.81, 1]'


def test_long_arrays_not_truncated():
    cell = QUTP.format_cell(np.arange(1, 1801, dtype=float))
    assert '...' not in cell
    assert cell.startswith('[1.0, 2.0, ') and cell.endswith(', 1800.0]')


def test_nested_lists_and_scalars():
    assert QUTP.format_cell([[0, 1.5], [np.float64(2.0), 3]]) == '[[0, 1.5], [2.0, 3]]'
    assert QUTP.format_cell(np.float64(1369.37)) == np.float64(1369.37)   # plain numbers stay numeric cells
    assert QUTP.format_cell('CURVE') == 'CURVE'
