#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import argparse
import json
import os


# In[2]:

parser = argparse.ArgumentParser(
    prog='chrom_tab2json.py',
    description='Convert information about chromosomes from tsv to json format')
parser.add_argument('-i', '--input', type=os.path.normpath, help='Path to input file', required=True)
parser.add_argument('-o', '--output', type=os.path.normpath, help='Path to output file', required=True)
parser.add_argument('-f', '--filter', type=bool, 
                    help='Filter sequences by FIX & ALT, etc (include only primary assembled chromosomes)', 
                    default=False, action=argparse.BooleanOptionalAction)

args = parser.parse_args()


# In[3]:

data = pd.read_csv(args.input, sep='\t')
if args.filter:
    data['Needed'] = data['UCSC style name'].str.match(r'^chr(([0-9]+)|([A-Z]))$').astype(bool)
    data = data[data['Needed']]
chrom_id = pd.Series(data['RefSeq seq accession'].values, index=data['UCSC style name']).to_dict()

print('\n', parser.prog)
print('Filtering out additional sequences from patches' if args.filter else 'No filtering')
print(args.input)
with open(args.output, 'w') as outfile:
    outfile.write(json.dumps(chrom_id, indent=4))

