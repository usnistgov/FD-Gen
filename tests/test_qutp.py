import numpy as np

import QUTP


def test_list_cells_written_in_full_without_numpy_reprs():
    cell = QUTP.format_cell([np.float64(3.81), np.float64(3.81) + 2.0, np.int32(1)])
    assert cell == '[3.81, 5.81, 1]'


def test_long_arrays_not_truncated():
    cell = QUTP.format_cell(np.arange(1, 1801, dtype=float))
    assert '...' not in cell
    assert cell.startswith('[1.0, 2.0, ') and cell.endswith(', 1800.0]')


class FakeHRC:
    def __init__(self, ID, times, hrrs):
        self.ID, self.TIME_SLICE_SAMPLES, self.HRR_SAMPLES = ID, times, hrrs


def test_hrr_curves_written_to_csv_in_full(tmp_path):
    curve = FakeHRC('CURVE', [np.arange(1.0, 1801.0), np.array([0.0, 0.5])],
                    [np.linspace(0, 1500, 1800), np.array([np.float64(0.1) + 0.2, 7.0])])
    outputs = {'HRC': [curve]}
    QUTP.PRINT_HRR_CURVES_CSV(2, outputs, str(tmp_path), 'hrr_curves.csv')
    lines = (tmp_path / 'hrr_curves.csv').read_text().splitlines()
    assert lines[0] == 'HRC_ID,Case,Time (s),HRR (kW)'
    assert len(lines) == 1 + 1800 + 2
    assert lines[1] == 'CURVE,0,1.0,0.0'
    assert lines[1800] == 'CURVE,0,1800.0,1500.0'
    assert lines[-2:] == ['CURVE,1,0.0,0.3', 'CURVE,1,0.5,7.0']


def test_no_hrr_csv_without_curves(tmp_path):
    QUTP.PRINT_HRR_CURVES_CSV(2, {'HRC': []}, str(tmp_path), 'hrr_curves.csv')
    assert not (tmp_path / 'hrr_curves.csv').exists()


def test_nested_lists_and_scalars():
    assert QUTP.format_cell([[0, 1.5], [np.float64(2.0), 3]]) == '[[0, 1.5], [2.0, 3]]'
    assert QUTP.format_cell(np.float64(1369.37)) == np.float64(1369.37)   # plain numbers stay numeric cells
    assert QUTP.format_cell('CURVE') == 'CURVE'
