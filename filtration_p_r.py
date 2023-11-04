#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import argparse
import os


# In[2]:

parser = argparse.ArgumentParser(
    prog='filtration_p_r.py',
    description='Filter BANC-seq peaks with KdApps data by r and p (predicted-observed correlation coefficient and p-value)')
parser.add_argument('-i', '--input', type=os.path.normpath, help='Path to input file', required=True)
parser.add_argument('-o', '--output', type=os.path.normpath, help='Path to output file', required=True)
parser.add_argument('-p', '--p-threshold', type=float, help='P-value threshold', default=.01)
parser.add_argument('-r', '--r-threshold', type=float, help='Correlation coefficient threshold', default=.9)
parser.add_argument('-s', '--input-separator', type=str, help='Input file separator', default='\t')
parser.add_argument('-S', '--output-separator', type=str, help='Output file separator', default='\t')

args = parser.parse_args()


# In[3]:


def filter_df(df, p_col, r_col):
    return df.loc[(df[p_col] <= args.p_threshold) & (df[r_col] >= args.r_threshold)]

def get_sub_df(df, sub_division, common_cols):
    df_sub = df[common_cols + [col for col in df.columns if sub_division in col]]
    df_sub.columns = [col.replace('R1_' + sub_division + '_', '').replace('_' + sub_division, '') for col in df_sub]
    return df_sub

def print_info(prevlen, newlen, add_info=None):
    print('\n', parser.prog)
    print('Peaks count%s:' % ('' if add_info is None else ' in ' + add_info))
    print('Before filtering:', prevlen, sep='\t')
    print('After filtering:', newlen, sep='\t')

def exclude(df, keep, exclude):
    sub_df = get_sub_df(df, keep, ['Chr', 'Start', 'End'])
    prevlen = len(sub_df)
    sub_df = filter_df(sub_df, 'p', 'n')
    outpath = args.output.replace(exclude, '')
    sub_df.to_csv(outpath, sep=args.output_separator, index=False)
    print_info(prevlen, len(sub_df), keep)

# In[4]:

# data = pd.read_csv(args.input, sep=args.input_separator)
# prev_len = len(data)
# if 'p_ESC' in data.columns:
#     data = filter_df(data, 'p_ESC', 'n_ESC')
# if 'p_NPC' in data.columns:
#     data = filter_df(data, 'p_NPC', 'n_NPC')
# if 'p' in data.columns:
#     data = filter_df(data, 'p', 'n')
# print(parser.prog)
# print('Input file:', os.path.basename(args.input), sep='\t')
# print('Peaks count:', prev_len, sep='\t')
# print('Output file:', os.path.basename(args.output), sep='\t')
# print('Peaks count:', len(data), sep='\t')
# data.to_csv(args.output, sep=args.output_separator, index=False)


# In[5]:

data = pd.read_csv(args.input, sep=args.input_separator)
prev_len = len(data)
if 'p_ESC' in data.columns and 'p_NPC' in data.columns:
    exclude(data, 'ESC', 'NPC_')
    exclude(data, 'NPC', 'mESC_')
else:
    prevlen_data = len(data)
    data = filter_df(data, 'p', 'n')
    data.to_csv(args.output, sep=args.output_separator, index=False)
    print_info(prevlen_data, len(data))