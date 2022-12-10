from chirp_convert.main import *


def test_frequency():
    assert process_frequency("") == (0, '', 0)
    assert process_frequency(" ") == (0, '', 0)
    assert process_frequency("100") == (100, '', 0)
    assert process_frequency(" 100") == (100, '', 0)
    assert process_frequency("100.0 ") == (100, '', 0)
    assert process_frequency(" 100.0 ") == (100, '', 0)
    assert process_frequency(" 100. ") == (100, '', 0)

    assert process_frequency("144.0") == (144, '', 0)
    assert process_frequency("144.9+") == (144.9, '+', 0.6)
    assert process_frequency("144.9-") == (144.9, '-', 0.6)

    assert process_frequency("444.9+") == (444.9, '+', 5.0)
    assert process_frequency("444.9") == (444.9, '', 0)
    # negative offset triggers a warning
    assert process_frequency("444.9-") == (444.9, '-', 5.0)
