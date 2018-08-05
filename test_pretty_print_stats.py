####
# Test file for the prettyPrintStats() method.
# Run with `pytest [filename]` or just `pytest` for all test files
####

from bbot import prettyPrintStats, decode_tx_extra


teta = [
    '014841165464244b894a6dc10256de06fc0225e718975937bb2cd0e288ed3f48d9',
    '016f8c853082fb79efe9064312e2a4fc4e68b339a4572924b03d9df8bae382f619020800000001f05a18d1',
    '01d7943394d446bf47735807fbbc89315992f6fb3f9002a106b572474d3fd68dde',
    '0107e30e7757c3d875b581ff00b82ac75cdc04df189ec55b4ab6e6a88be2df990a0208000000008a92761f',
    '01271adf815acf5adf7220633b52f54a5506e64c74a15524e583ad896fa43c78850206747572746c65',
    '01ba138a547cd42884c69ee4941828315aa1ffe464d41f84d2b9cb47a2fee668c102080000000001dbc3b5'
]

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
    'teta': teta,
    'deteta': [decode_tx_extra(x) for x in teta],
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
Total size of the txs: 26129
Total size of tx_extra(s): 279

Tx 0 (size 300):
    hash: ae5f648a0c5812de318f82021f1cffebfae64184dac9b3b9aabdaeb3f2a517c5
    tx_extra: 014841165464244b894a6dc10256de06fc0225e718975937bb2cd0e288ed3f48d9
    Payment ID: 4841165464244b894a6dc10256de06fc0225e718975937bb2cd0e288ed3f48d9

Tx 1 (size 3145):
    hash: 6bde79407c74188072468701c997547ff1525b274f8c17bc99d0b34ce06af26c
    tx_extra: 016f8c853082fb79efe9064312e2a4fc4e68b339a4572924b03d9df8bae382f619020800000001f05a18d1
    Payment ID: 6f8c853082fb79efe9064312e2a4fc4e68b339a4572924b03d9df8bae382f619
    Custom Data (hex): 00000001f05a18d1

Tx 2 (size 868):
    hash: f8658c741f15ed490da7c64f890e5b4bc7e3473fd2e5f81eca1eb885e2583876
    tx_extra: 01d7943394d446bf47735807fbbc89315992f6fb3f9002a106b572474d3fd68dde
    Payment ID: d7943394d446bf47735807fbbc89315992f6fb3f9002a106b572474d3fd68dde

Tx 3 (size 1267):
    hash: ae76be2bb7b9c7858fab2c439f8c8dbb0212bc47b56df7a9e85401373b7625da
    tx_extra: 0107e30e7757c3d875b581ff00b82ac75cdc04df189ec55b4ab6e6a88be2df990a0208000000008a92761f
    Payment ID: 07e30e7757c3d875b581ff00b82ac75cdc04df189ec55b4ab6e6a88be2df990a
    Custom Data (hex): 000000008a92761f

Tx 4 (size 1594):
    hash: 097edbfdf66b12bc480d48f8cefcc0df251844fab52bf3c4bd544d4ebec58bb3
    tx_extra: 01271adf815acf5adf7220633b52f54a5506e64c74a15524e583ad896fa43c78850206747572746c65
    Payment ID: 271adf815acf5adf7220633b52f54a5506e64c74a15524e583ad896fa43c7885
    Custom Data (hex): 747572746c65
    Custom Data (utf-8 decoded): turtle

Tx 5 (size 18955):
    hash: 09e3ae8549828aea33abcce604b1fe40f297a86b1431c7f2d27b245287b1d76a
    tx_extra: 01ba138a547cd42884c69ee4941828315aa1ffe464d41f84d2b9cb47a2fee668c102080000000001dbc3b5
    Payment ID: ba138a547cd42884c69ee4941828315aa1ffe464d41f84d2b9cb47a2fee668c1
    Custom Data (hex): 0000000001dbc3b5

Percentage of txs in the block: 98.94350196910028 %
Percentage of tx_extra in the block: 1.0564980308997274 % ```
"""


def test_with_six_transactions():
    msg = prettyPrintStats(block_stats)
    split_msg = msg.splitlines()  # split this up for easier readouts

    for idx, line in enumerate(expected_output.splitlines()):
        # ignore leading/trailing whitespace
        assert split_msg[idx].strip() == line.strip()
