# Changelog

All notable changes to FD-Gen are listed here.

## [1.1.0] - 2026-10-23

### Changes that may affect existing projects

- **HRR curves moved out of the parameter spreadsheet.** The two `<HRC>` columns (time and HRR samples) are no longer in `parameter_outputs.xlsx`. The full curves are now written to `PARAMETER_FILE_FOLDER/hrr_curves.csv`, one row per time step (`HRC_ID, Case, Time (s), HRR (kW)`). Scripts that read HRR curves from the spreadsheet need to read the CSV instead.
- **Repeated random seeds are replaced.** In v1.0.0 two sampler lines (`&MRND`) could receive the same random seed. Now a seed that was already used is replaced, so those sampler lines get different values than in v1.0.0. Sampler lines that never got a repeated seed keep exactly the same values. Of the bundled examples, `example_commercial`, `example_Single_Story_Gas_1` and `example_CSTB_Tunnel_Test_2` are affected. To reproduce a v1.0.0 dataset exactly, use v1.0.0.
- **FD-Gen asks before deleting an existing project folder.** Re-running a project used to delete its previous results without warning. Answer `Y` to replace them, or use `--yes`.

### Fixed

- **NumPy 2 support.** With NumPy 2.x, generated FDS files contained text such as `XB=np.float64(3.81)`, which FDS cannot read. Values are now written as plain numbers, and floating-point noise is trimmed (`5.8100000000000005` → `5.81`). The parameter spreadsheet and the text reports are fixed too.
- **HRR curves cut short in the spreadsheet.** Curves with more than 1000 points were stored as `[1. 2. ... 1800.]` with the middle values missing. They are now stored in full in `hrr_curves.csv`.
- **Text inside quotes.** Commas, `/`, `=` and argument names inside quoted text were read as syntax. This gave wrong values (`FYI='room 1, north'`), a crash (`FYI='kW/m2'`), and corrupted FDS lines (for example `ID='HRRPUA_burner'` before `HRRPUA=`). It also crashed door/window inputs (`&IDWT`) whose device IDs contain a comma, such as `'T4_(10,11)'`.
- **More than 200 seeds.** Projects with many sampler lines crashed once the list of 200 seeds ran out. There is no limit now.
- **Linux and macOS.** Folder paths were built with Windows backslashes. They now work on any operating system, for example on HPC clusters.
- FD-Gen no longer changes the working directory while it runs, and it writes nothing outside the project folder.

### Added

- Command-line options: `--yes` / `-y` (answer Y to all prompts, for batch runs), `--sample-only` (stop after sampling), `--version` and `--help`.
- Automated tests (`python -m pytest tests`). They include regression tests that compare the output of every input in `test_cases/` and `example/` with saved results.

### Changed

- `requirements.txt` now gives version ranges (for example `numpy>=1.26.4,<3`) instead of exact versions. NumPy 1.26 and 2.x are both supported.
- Python cache files are no longer tracked in git, and a `.gitignore` was added.

## [1.0.0] - 2025-03-06

First public release. See the NIST Technical Note: https://doi.org/10.6028/NIST.TN.2332
