from bbot import decode_tx_extra


known_hashes = [
    '0134df59241f0676bd3395b08aa4b5432279d0b02bf7b33800a0c63b66a6250138',
    '014230cfd7909d22bad63fb742331055974f2bd6697cc00b6ceaa44de0a7ad833102080000000006920e92'
]

known_results = [
    'Payment ID: 34df59241f0676bd3395b08aa4b5432279d0b02bf7b33800a0c63b66a6250138\n',
    'Payment ID: 4230cfd7909d22bad63fb742331055974f2bd6697cc00b6ceaa44de0a7ad8331\n'  # cont...
    'Custom Data Hex: 0000000006920e92\n'
]


def test_known_hashes():
    for i, hash in enumerate(known_hashes):
        print('Testing known hash {}'.format(i))
        result = decode_tx_extra(hash)
        print(result)
        assert result == known_results[i]
