from chirp_convert.main import *


def test_names():
    assert process_name('W1XSC-1', True) == 'W1XSC-1'
    assert process_name('W1XSC-1', False) == 'W1XSC-1'

    assert process_name('W1XSCC-1', True) == 'W1XSCC-1'
    assert process_name('W1XSCC-1', False) == 'W1XSCC1'

    assert process_name('K6SNYr', True) == 'K6SNYr'
    assert process_name('K6SNYr', False) == 'K6SNY R'

    assert process_name('KI6SNYr', True) == 'KI6SNYr'
    assert process_name('KI6SNYr', False) == 'KI6SNYR'

    assert process_name('LOSa', True) == 'LOSa'
    assert process_name('LOSa', False) == 'LOS A'
