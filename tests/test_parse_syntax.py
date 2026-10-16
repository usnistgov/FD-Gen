import numpy as np

import parse_syntax as PS


LINE = "&OBST ID='fire source', XB=0.7,3.7,22.1,26.3,0.0,0.2, SURF_IDS='CURVE','INERT','INERT'/"


def test_numpy_floats_written_as_plain_numbers():
    xb = [np.float64(3.81), np.float64(3.81) + 2.0, np.float64(24.67), np.float64(25.67), np.float64(0.0), np.float64(0.2)]
    out = PS.replace_value(LINE, replaced_args='XB', replaced_after_args='SURF_IDS', replaced_value=xb)
    assert 'np.' not in out
    assert out.startswith("&OBST ID='fire source', XB=3.81, 5.81, 24.67, 25.67, 0.0, 0.2, ")
    assert out.endswith("SURF_IDS='CURVE','INERT','INERT'/")


def test_float_noise_is_trimmed_but_magnitude_kept():
    out = PS.replace_value(LINE, 'XB', 'SURF_IDS', [3.81 + 2.0, 1e-15, 1800.0, np.float32(0.1)])
    assert 'XB=5.81, 1e-15, 1800.0, 0.1, ' in out


def test_numpy_ints_and_strings():
    out = PS.replace_value("&HEAD CHID='old'/", 'CHID', None, ['case_00001'])
    assert out.startswith("&HEAD CHID='case_00001', ")
    out = PS.replace_value(LINE, 'XB', 'SURF_IDS', [np.int64(3)])
    assert 'XB=3, ' in out


def test_format_ramp_value():
    assert PS.format_value(np.float64(0.30000000000000004)) == '0.3'
    assert PS.format_value(np.int64(60)) == '60'
