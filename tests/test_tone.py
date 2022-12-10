from chirp_convert.main import *


def test_tone():
    assert process_tone("100Hz") == ('Tone', 100, 88.5)
    assert process_tone("100 Hz") == ('Tone', 100, 88.5)
    assert process_tone("99 HZ") == ('Tone', 99, 88.5)
    assert process_tone("99HZ") == ('Tone', 99, 88.5)
    assert process_tone("100") == ('Tone', 100, 88.5)
    assert process_tone("100 hz") == ('Tone', 100, 88.5)
    assert process_tone("") == ('', 88.5, 88.5)
    assert process_tone(" ") == ('', 88.5, 88.5)
    assert process_tone("Hz") == ('', 88.5, 88.5)
