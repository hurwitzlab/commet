#!/usr/bin/env python3
"""docstring"""

import argparse
import os
import sys
import subprocess
import tempfile as tmp

# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-q', '--query',
                        help='Directory of input files',
                        metavar='str',
                        type=str,
                        default='')

    parser.add_argument('-Q', '--query_set',
                        help='File describing sets for Commet',
                        metavar='str',
                        type=str,
                        default='')

    parser.add_argument('-o', '--out_dir',
                        help='Output directory',
                        metavar='str',
                        type=str,
                        default=os.path.join(os.getcwd(), 'commet-out'))

    parser.add_argument('-k', '--kmer_size',
                        help='Kmer size',
                        metavar='int',
                        type=int,
                        default=None)

    parser.add_argument('-t', '--min_num_shared_kmers',
                        help='Minimal number of shared k-mers',
                        metavar='int',
                        type=int,
                        default=None)

    parser.add_argument('-l', '--min_len_keep_read',
                        help='Minimal length to keep a read',
                        metavar='int',
                        type=int,
                        default=None)

    parser.add_argument('-n', '--max_num_ns_keep_read',
                        help='Maximal number of Ns to keep read',
                        metavar='int',
                        type=int,
                        default=None)

    parser.add_argument('-e', '--min_shannon_keep_read',
                        help='Minimal Shannon index to keep read',
                        metavar='int',
                        type=int,
                        default=None)

    parser.add_argument('-m', '--max_num_selected_reads',
                        help='Maximum number of selected reads',
                        metavar='int',
                        type=int,
                        default=None)

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
def make_commet_args(args):
    """Turn user args to Commet args"""
    commet_args = ['-o', args.out_dir, '-b', '/usr/local/bin']

    if args.kmer_size is not None:
        commet_args.extend('-k', str(args.kmer_size))

    if args.min_num_shared_kmers is not None:
        commet_args.extend('-t', str(args.min_num_shared_kmers))

    if args.min_len_keep_read is not None:
        commet_args.extend('-l', str(args.min_len_keep_read))

    if args.max_num_ns_keep_read is not None:
        commet_args.extend('-n', str(args.max_num_ns_keep_read))

    if args.min_shannon_keep_read is not None:
        commet_args.extend('-e', str(args.min_shannon_keep_read))

    if args.max_num_selected_reads is not None:
        commet_args.extend('-m', str(args.max_num_selected_reads))

    return commet_args

# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    query_dir = args.query
    query_set = args.query_set
    out_dir = args.out_dir

    if (query_dir and query_set) or (not query_dir and not query_set):
        die('Please provide either --query or --query_set')

    if query_set and not os.path.isfile(query_set):
        die('--query_set "{}" is not a file'.format(query_set))

    if query_dir:
        if os.path.isdir(query_dir):
            tmpfile = tmp.NamedTemporaryFile(delete=False,
                                             mode='wt',
                                             dir=os.getcwd())

            for fname in os.listdir(query_dir):
                fpath = os.path.join(query_dir, fname)
                if os.path.isfile(fpath):
                    tmpfile.write('{}:{}\n'.format(fname, fpath))

            tmpfile.close()
            query_set = tmpfile.name
        else:
            die('--query "{}" is not a directory'.format(query_dir))

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    cmd = ['Commet.py'] + make_commet_args(args) + [query_set]
    warn(cmd)
    subprocess.run(cmd)

    print('Done, see output dir "{}"'.format(os.path.abspath(out_dir)))

# --------------------------------------------------
if __name__ == '__main__':
    main()
