#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import argparse
import json
import os


# In[2]:

parser = argparse.ArgumentParser(
    prog='bancseq2bed.py',
    description='Convert BANC-seq peaks to .bed format')
parser.add_argument('-i', '--input', type=os.path.normpath, help='Path to input file', required=True)
parser.add_argument('-o', '--output', type=os.path.normpath, help='Path to output file', required=True)
parser.add_argument('-c', '--chrom-config', type=os.path.normpath, help='Path to chromosome config file', required=True)
parser.add_argument('-s', '--input-separator', type=str, help='Input file separator', default='\t')

args = parser.parse_args()


# In[3]:

data = pd.read_csv(args.input, sep=args.input_separator)
chrom_config_file = open(args.chrom_config, 'r')
chrom_config = json.load(chrom_config_file)
chrom_config_file.close()

prev_len = len(data)
data = data[data['Chr'].isin(chrom_config.keys())]

data['chromID'] = data['Chr'].map(chrom_config)
data['Index'] = data.index
data = data[['chromID', 'Start', 'End', 'Index']]
# print(data.head())
# data.columns = ['chrom', 'chromStart', 'chromEnd']
data.to_csv(args.output, sep='\t', index=False, header=False)

print('\n', parser.prog)
print('Amount of peaks:')
print('Before converting to BED:', prev_len, sep='\t')
print('After converting to BED:', len(data), sep='\t')
print('Filtered (FIX & ALT, etc.):', prev_len - len(data), sep='\t')