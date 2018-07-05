#!/usr/bin/env python3
"""docstring"""

import argparse
import os
import sys

# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-b', '--bitvector_dir',
                        help='Directory containing the bit vector files',
                        metavar='str',
                        type=str,
                        required=True)

    parser.add_argument('-f', '--fasta_dir',
                        help='Directory containing the FASTA files',
                        metavar='str',
                        type=str,
                        required=True)

    parser.add_argument('-o', '--out_dir',
                        help='Directory to write files',
                        metavar='str',
                        type=str,
                        required=True)

    return parser.parse_args()

# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)

# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)

# --------------------------------------------------
def main():
    """main"""
    args = get_args()

    bv_dir = args.bitvector_dir
    fasta_dir = args.fasta_dir
    out_dir = args.out_dir

    if not os.path.isdir(bv_dir):
        die('--bitvector_dir "{}" is not a directory'.format(bv_dir))

    if not os.path.isdir(fasta_dir):
        die('--fasta_dir "{}" is not a directory'.format(fasta_dir))

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    bv_files = [fname for fname in os.listdir(bv_dir) if fname.endswith('.bv')]

    print(bv_files)

# --------------------------------------------------
if __name__ == '__main__':
    main()
