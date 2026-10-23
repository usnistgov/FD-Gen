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


def test_version_option_and_banner(tmp_path):
    from version import VERSION, RELEASE_DATE
    result = run(['--version'], tmp_path)
    assert result.returncode == 0 and result.stdout.strip() == f'FD-Gen {VERSION} ({RELEASE_DATE})'
    result = run([str(SCRIPT), '--sample-only', '--yes'], tmp_path)
    assert f'Version {VERSION}' in result.stdout and RELEASE_DATE in result.stdout


def make_existing_project(tmp_path):
    marker = tmp_path / 'test_script_FSL' / 'CASE_FOLDER' / 'old_result.fds'
    marker.parent.mkdir(parents=True)
    marker.write_text('earlier results')
    return marker


def test_existing_project_kept_when_user_answers_no(tmp_path):
    marker = make_existing_project(tmp_path)
    result = run([str(SCRIPT)], tmp_path, stdin='n\n')
    assert 'already exists' in result.stdout
    assert 'Operation aborted.' in result.stdout
    assert marker.read_text() == 'earlier results'


def test_existing_project_replaced_when_user_answers_yes(tmp_path):
    marker = make_existing_project(tmp_path)
    result = run([str(SCRIPT)], tmp_path, stdin='y\ny\ny\n')
    assert result.returncode == 0, result.stdout[-1500:] + result.stderr
    assert not marker.exists()
    assert len(list((tmp_path / 'test_script_FSL' / 'CASE_FOLDER').glob('*.fds'))) == 10


def test_existing_project_replaced_with_yes_flag(tmp_path):
    marker = make_existing_project(tmp_path)
    result = run([str(SCRIPT), '--yes'], tmp_path)
    assert result.returncode == 0, result.stdout[-1500:] + result.stderr
    assert 'already exists' in result.stdout
    assert not marker.exists()
