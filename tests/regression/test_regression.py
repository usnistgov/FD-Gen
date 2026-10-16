"""End-to-end regression tests.

Runs FD-Gen on every input in test_cases/ and example/ and compares the
generated FDS case files and parameter spreadsheet with saved baselines.

    python -m pytest tests                      # check against baselines
    python -m pytest tests --update-baselines   # accept current output as new baseline
"""
import json
import lzma
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import openpyxl
import pytest

REPO = Path(__file__).resolve().parents[2]
FDSDATA = REPO / 'main_code' / 'FDSdata.py'
BASELINES = Path(__file__).resolve().parent / 'baselines'
INPUTS = sorted((REPO / 'test_cases').glob('*.txt')) + sorted((REPO / 'example').glob('*.fds'))

NUMBER = re.compile(r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')
NUMPY_REPR = re.compile(r'np\.\w+\(([^()]*)\)')
REL_TOL = 1e-9
ABS_TOL = 1e-12


def run_fdgen(input_file, work_dir):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg')
    result = subprocess.run([sys.executable, str(FDSDATA), str(input_file)], cwd=work_dir, env=env,
                            input='y\ny\n', capture_output=True, text=True, timeout=900)
    assert result.returncode == 0 and 'Traceback' not in result.stderr, result.stdout[-2000:] + result.stderr
    project_dirs = [p for p in work_dir.iterdir() if p.is_dir()]
    assert len(project_dirs) == 1, project_dirs
    return project_dirs[0]


def collect_outputs(project_dir):
    outputs = {}
    for case_file in sorted((project_dir / 'CASE_FOLDER').glob('*.fds')):
        outputs['CASE_FOLDER/' + case_file.name] = case_file.read_text(encoding='utf-8')
    workbook = openpyxl.load_workbook(project_dir / 'PARAMETER_FILE_FOLDER' / 'parameter_outputs.xlsx', read_only=True)
    for sheet in workbook.worksheets:
        rows = ['\t'.join('' if cell is None else str(cell) for cell in row) for row in sheet.iter_rows(values_only=True)]
        outputs['parameter_outputs.xlsx/' + sheet.title] = '\n'.join(rows)
    workbook.close()
    hrr_curves = project_dir / 'PARAMETER_FILE_FOLDER' / 'hrr_curves.csv'
    if hrr_curves.exists():
        outputs['hrr_curves.csv'] = hrr_curves.read_text(encoding='utf-8')
    return outputs


def same_line(expected, actual):
    if expected == actual:
        return True
    expected, actual = NUMPY_REPR.sub(r'\1', expected), NUMPY_REPR.sub(r'\1', actual)
    if re.sub(r'\s', '', NUMBER.sub('#', expected)) != re.sub(r'\s', '', NUMBER.sub('#', actual)):
        return False
    return all(math.isclose(float(a), float(b), rel_tol=REL_TOL, abs_tol=ABS_TOL)
               for a, b in zip(NUMBER.findall(expected), NUMBER.findall(actual)))


def compare(expected, actual, max_report=10):
    problems = []
    for name in sorted(expected.keys() - actual.keys()):
        problems.append(f'missing output: {name}')
    for name in sorted(actual.keys() - expected.keys()):
        problems.append(f'unexpected output: {name}')
    for name in sorted(expected.keys() & actual.keys()):
        expected_lines, actual_lines = expected[name].splitlines(), actual[name].splitlines()
        if len(expected_lines) != len(actual_lines):
            problems.append(f'{name}: {len(expected_lines)} lines expected, got {len(actual_lines)}')
            continue
        for number, (e, a) in enumerate(zip(expected_lines, actual_lines), 1):
            if not same_line(e, a):
                problems.append(f'{name}:{number}\n  expected: {e.strip()[:300]}\n  actual:   {a.strip()[:300]}')
        if len(problems) >= max_report:
            break
    return problems[:max_report]


def baseline_path(input_file):
    return BASELINES / f'{input_file.parent.name}__{input_file.stem}.json.xz'


@pytest.mark.parametrize('input_file', INPUTS, ids=lambda p: p.stem)
def test_outputs_match_baseline(input_file, tmp_path, request):
    project_dir = run_fdgen(input_file, tmp_path)
    actual = collect_outputs(project_dir)
    path = baseline_path(input_file)

    reports = {f'PARAMETER_FILE_FOLDER/{p.name}': p.read_text() for p in (project_dir / 'PARAMETER_FILE_FOLDER').glob('*.txt')}
    leaked = [name for name, text in {**actual, **reports}.items() if 'np.' in text]
    assert not leaked, f'numpy reprs (np.xxx(...)) written to: {leaked[:5]}'

    if request.config.getoption('--update-baselines'):
        BASELINES.mkdir(exist_ok=True)
        path.write_bytes(lzma.compress(json.dumps(actual, indent=0, sort_keys=True).encode('utf-8')))
        pytest.skip(f'baseline written: {path.name}')

    assert path.exists(), f'no baseline for {input_file.name}; run pytest with --update-baselines'
    expected = json.loads(lzma.decompress(path.read_bytes()))
    problems = compare(expected, actual)
    assert not problems, f'{input_file.name} output differs from baseline:\n' + '\n'.join(problems)
