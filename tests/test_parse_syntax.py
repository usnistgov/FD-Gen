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


# ---- quoted text: commas, '/', '=' and argument names inside quotes are text, not syntax ----

def test_comma_inside_quotes():
    name, args = PS.parse_script_lines("&MRND GENERATOR_ID='A', FYI='room 1, north', MINIMUM=1/")
    assert args == {'GENERATOR_ID': 'A', 'FYI': 'room 1, north', 'MINIMUM': 1}


def test_slash_inside_quotes():
    name, args = PS.parse_script_lines("&MRND GENERATOR_ID='A', FYI='HRR in kW/m2', MINIMUM=1/")
    assert args == {'GENERATOR_ID': 'A', 'FYI': 'HRR in kW/m2', 'MINIMUM': 1}


def test_equals_inside_quotes():
    name, args = PS.parse_script_lines("&MRND GENERATOR_ID='A', FYI='x=2', MINIMUM=1/")
    assert args == {'GENERATOR_ID': 'A', 'FYI': 'x=2', 'MINIMUM': 1}


def test_existing_syntax_still_parsed():
    assert PS.parse_script_lines("&OBST ID='a' XB=1,2,3,4,5,6 SURF_ID='INERT'/")[1] == {'ID': 'a', 'XB': [1, 2, 3, 4, 5, 6], 'SURF_ID': 'INERT'}
    assert PS.parse_script_lines("&MATL ID='M', MATL_ID(1,1)='X', NU_MATL(1,1)=0.5/")[1] == {'ID': 'M', 'MATL_ID(1,1)': 'X', 'NU_MATL(1,1)': 0.5}
    assert PS.parse_script_lines("&OBST ID='fire source', SURF_IDS='CURVE','INERT','INERT'/")[1] == {'ID': 'fire source', 'SURF_IDS': ['CURVE', 'INERT', 'INERT']}
    assert PS.parse_script_lines("&MRND GENERATOR_ID='G', SHUFFLE_STATES=False, VALUE_TYPE='REAL'/")[1] == {'GENERATOR_ID': 'G', 'SHUFFLE_STATES': False, 'VALUE_TYPE': 'REAL'}


def test_replace_value_ignores_argument_name_inside_quotes():
    out = PS.replace_value("&SURF ID='HRRPUA_burner', HRRPUA=1000.0, RAMP_Q='r'/", 'HRRPUA', 'RAMP_Q', [500.0])
    assert out.startswith("&SURF ID='HRRPUA_burner', HRRPUA=500.0, ")
    assert out.endswith("RAMP_Q='r'/")


def test_replace_last_value_ignores_slash_inside_quotes():
    out = PS.replace_value("&HEAD TITLE='run a/b', CHID='old'/", 'CHID', None, ['new'])
    assert out == "&HEAD TITLE='run a/b', CHID='new', /"
