####
# Test file for the decode_tx_extra() method.
# Run with `pytest [filename]` or just `pytest` for all test files
####

from bbot import decode_tx_extra


known_hashes = [
    '0134df59241f0676bd3395b08aa4b5432279d0b02bf7b33800a0c63b66a6250138',
    '014230cfd7909d22bad63fb742331055974f2bd6697cc00b6ceaa44de0a7ad833102080000000006920e92',
    '015869cf42752bac16fbb1d00789da0d48864bd20b1bd3b89a91e0609fa8100fef02080000000019eaddaf',
    '01a248ff5495efddab4db813898e44dcb4d5b1c9c38fff72dc8ef19087ee6829a70221002c86158da497d1484f7097a0074fdbbe7bb2615b625133bc549516b94f84b7d2'
]

known_results = [
    '\nPayment ID: 34df59241f0676bd3395b08aa4b5432279d0b02bf7b33800a0c63b66a6250138',
    '\nPayment ID: 4230cfd7909d22bad63fb742331055974f2bd6697cc00b6ceaa44de0a7ad8331'  # cont...
    '\nCustom Data (hex): 0000000006920e92',
    '\nPayment ID: 5869cf42752bac16fbb1d00789da0d48864bd20b1bd3b89a91e0609fa8100fef'  # cont...
    '\nCustom Data (hex): 0000000019eaddaf',
    '\nPayment ID: a248ff5495efddab4db813898e44dcb4d5b1c9c38fff72dc8ef19087ee6829a7'  # cont...
    '\nCustom Data (hex): 002c86158da497d1484f7097a0074fdbbe7bb2615b625133bc549516b94f84b7d2'
]


def test_known_hashes():
    for i, hash in enumerate(known_hashes):
        print('Testing known hash {}'.format(i))
        result = decode_tx_extra(hash)
        print(result)
        assert result == known_results[i]


def test_bad_data():
    bad_tx_etra_hash = '69207468696E6B207520776F6E2074686520626F756E7479'
    result = decode_tx_extra(bad_tx_etra_hash)
    print(result)
    assert 'Hm, something went wrong.' in result


def test_empty_string():
    result = decode_tx_extra('')
    print(result)
    assert result == ''


def test_wrong_arguments():
    result = decode_tx_extra(None)
    print(result)
    assert result == ''
