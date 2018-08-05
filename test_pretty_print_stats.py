####
# Test file for the prettyPrintStats() method.
# Run with `pytest [filename]` or just `pytest` for all test files
####

from bbot import prettyPrintStats


block_stats = {
    'height': 608996,
    'hash': '09e3ae8549828aea33abcce604b1fe40f297a86b1431c7f2d27b245287b1d76a',
    'orphan': False,
    'reward': 29269.36,
    'bsizes': 26408,
    'blocktime': 'Took 89 seconds to make, pretty nice',
    'ntxs': 6,
    'hashes': [
        'ae5f648a0c5812de318f82021f1cffebfae64184dac9b3b9aabdaeb3f2a517c5',
        '6bde79407c74188072468701c997547ff1525b274f8c17bc99d0b34ce06af26c',
        'f8658c741f15ed490da7c64f890e5b4bc7e3473fd2e5f81eca1eb885e2583876',
        'ae76be2bb7b9c7858fab2c439f8c8dbb0212bc47b56df7a9e85401373b7625da',
        '097edbfdf66b12bc480d48f8cefcc0df251844fab52bf3c4bd544d4ebec58bb3',
        '09e3ae8549828aea33abcce604b1fe40f297a86b1431c7f2d27b245287b1d76a'
    ],
    'hahsizes': [300, 3145, 868, 1267, 1594, 18955],
    'txsizes': 26129,
    'teta': '014841165464244b894a6dc10256de06fc0225e718975937bb2cd0e288ed3f48d9',
    'deteta': "",
    'txes': 279,
    'txp': 98.94350196910028,
    'txep': 1.0564980308997274,
    'pingrock': ""
}

expected_output = """```WE FOUND A NEW BLOCK!

Height: 608996
Hash: 09e3ae8549828aea33abcce604b1fe40f297a86b1431c7f2d27b245287b1d76a
Orphan: False
Reward: 29269.36
Size: 26408
Time took to make: Took 89 seconds to make, pretty nice

No. of txs in the block: 6
Tx hashes in the block: ['ae5f648a0c5812de318f82021f1cffebfae64184dac9b3b9aabdaeb3f2a517c5', '6bde79407c74188072468701c997547ff1525b274f8c17bc99d0b34ce06af26c', 'f8658c741f15ed490da7c64f890e5b4bc7e3473fd2e5f81eca1eb885e2583876', 'ae76be2bb7b9c7858fab2c439f8c8dbb0212bc47b56df7a9e85401373b7625da', '097edbfdf66b12bc480d48f8cefcc0df251844fab52bf3c4bd544d4ebec58bb3', '09e3ae8549828aea33abcce604b1fe40f297a86b1431c7f2d27b245287b1d76a']
Size of each tx: [300, 3145, 868, 1267, 1594, 18955]
Size of all the txs: 26129

tx_extra hash: 014841165464244b894a6dc10256de06fc0225e718975937bb2cd0e288ed3f48d9
Decoded version of tx_extra:
Size of tx_extra: 279

Percentage of txs in the block: 98.94350196910028 %
Percentage of tx_extra in the block: 1.0564980308997274 % ```
"""


def test_with_six_transactions():
    msg = prettyPrintStats(block_stats)
    split_msg = msg.splitlines()  # split this up for easier readouts

    for idx, line in enumerate(expected_output.splitlines()):
        # ignore leading/trailing whitespace
        assert split_msg[idx].strip() == line.strip()
