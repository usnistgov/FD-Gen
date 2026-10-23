import os
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

import FDSdata

REPO = Path(__file__).resolve().parents[1]


def test_run_leaves_working_directory_unchanged(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    FDSdata.FDSdata(str(REPO / 'test_cases' / 'test_script_HRC.txt'), assume_yes=True)
    assert Path(os.getcwd()) == tmp_path
    project = tmp_path / 'test_script_HRC'
    assert len(list((project / 'CASE_FOLDER').glob('*.fds'))) == 10
    assert (project / 'PARAMETER_FILE_FOLDER' / 'parameter_outputs.xlsx').exists()
    assert (project / 'PARAMETER_FILE_FOLDER' / 'hrr_curves.csv').exists()
    assert (project / 'SEEDS_FOLDER' / 'SAVE_SEEDS_file.txt').exists()
    assert list((project / 'OUTPUT_FOLDER').glob('*.jpg'))
    assert {p.name for p in tmp_path.iterdir()} == {'test_script_HRC'}   # nothing written outside the project folder


def test_no_windows_only_path_separators_or_chdir_in_source():
    for source in (REPO / 'main_code').glob('*.py'):
        text = source.read_text(encoding='utf-8')
        assert not re.search(r'"\\\\"', text), f'{source.name} builds paths with "\\\\"; use os.path.join'
        assert 'os.chdir' not in text, f'{source.name} changes the working directory'
