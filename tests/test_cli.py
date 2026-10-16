import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FDSDATA = REPO / 'main_code' / 'FDSdata.py'
SCRIPT = REPO / 'test_cases' / 'test_script_FSL.txt'


def run(args, work_dir, stdin=''):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg')
    return subprocess.run([sys.executable, str(FDSDATA), *args], cwd=work_dir, env=env,
                          input=stdin, capture_output=True, text=True, timeout=300)


def test_yes_runs_all_steps_without_prompts(tmp_path):
    result = run([str(SCRIPT), '--yes'], tmp_path, stdin='')   # no answers available
    assert result.returncode == 0, result.stdout[-1500:] + result.stderr
    project = tmp_path / 'test_script_FSL'
    assert len(list((project / 'CASE_FOLDER').glob('*.fds'))) == 10
    assert (project / 'OUTPUT_FOLDER').is_dir()


def test_sample_only_stops_before_case_files(tmp_path):
    result = run([str(SCRIPT), '--sample-only', '-y'], tmp_path)
    assert result.returncode == 0, result.stdout[-1500:] + result.stderr
    project = tmp_path / 'test_script_FSL'
    assert (project / 'PARAMETER_FILE_FOLDER' / 'parameter_outputs.xlsx').exists()
    assert not (project / 'CASE_FOLDER').exists()


def test_prompts_unchanged_without_flags(tmp_path):
    result = run([str(SCRIPT)], tmp_path, stdin='y\nn\n')      # yes to sampling, no to wrapping
    assert result.returncode == 0, result.stdout[-1500:] + result.stderr
    assert 'Do you want to proceed to the SAMPLING step?' in result.stdout
    assert 'Operation aborted.' in result.stdout
    assert not (tmp_path / 'test_script_FSL' / 'CASE_FOLDER').exists()


def test_help_lists_options(tmp_path):
    result = run(['--help'], tmp_path)
    assert result.returncode == 0
    assert '--yes' in result.stdout and '--sample-only' in result.stdout
