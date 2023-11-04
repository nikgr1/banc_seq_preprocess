#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import argparse
import json
import os


# In[2]:

parser = argparse.ArgumentParser(
    prog='include_seq.py',
    description='Include peaks\' sequences to BANC-seq data')
parser.add_argument('-i', '--input', type=os.path.normpath, help='Path to input BANC-seq file', required=True)
parser.add_argument('-o', '--output', type=os.path.normpath, help='Path to output file', required=True)
parser.add_argument('-p', '--peaks-sequences', type=os.path.normpath, help='Path to sequences of peaks', required=True)
parser.add_argument('-s', '--input-separator', type=str, help='Input file separator', default='\t')
parser.add_argument('-S', '--output-separator', type=str, help='Output file separator', default='\t')
parser.add_argument('-c', '--soft-clipping', type=bool, 
                    help='Keep soft-clipping from genome sequences', 
                    default=False, action=argparse.BooleanOptionalAction)

args = parser.parse_args()


# In[3]:

data = pd.read_csv(args.input, sep=args.input_separator)
seqs = pd.read_csv(args.peaks_sequences, sep='\t', names=['bed_name', 'Sequence'])
seqs = pd.read_csv(args.peaks_sequences, sep='\t', names=['bed_name', 'Sequence'])
# seqs['Index'] = seqs['bed_name'].str.split(':', n=1).str[0]
seqs.index = seqs['bed_name'].str.split(':', n=1).str[0].astype(int)
if not args.soft_clipping:
    seqs['Sequence'] = seqs['Sequence'].str.upper()
result = seqs.join(data)
# result = pd.merge(data, seqs, left_index=True, right_index=True)

print('\n', parser.prog)
print('Amount of peaks:')
print('Before adding sequences:', len(data), sep='\t')
print('After  adding sequences:', len(result), sep='\t')
if len(data) != len(result):
    print('Warning! Amount of peaks has changed due to discrepancies between input BANC-seq data file and BED file.')
result = result[['Sequence', 'Chr', 'kd', 'n']]
result.to_csv(args.output, sep=args.output_separator, index=False)

