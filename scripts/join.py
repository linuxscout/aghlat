#!/usr/bin/python
# -*- coding=utf-8 -*-
#-----------------------------------------------------------------------
# Name:        Build a corpus to test and val stemmers and morphological analyzer
# Purpose:     build an advanced stemmer for Information retreival 
#  
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     2018-08-25
# Copyright:   (c) Taha Zerrouki 2018
# Licence:     GPL
#-----------------------------------------------------------------------
"""
    Build a corpus for evaluation
"""

import sys
import re
from operator import xor
import argparse
import os
import pandas as pd
import numpy as np
import qalsadi.analex
import pyarabic.araby as araby
import numpy as np
def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    parser.add_argument("-f2", dest="filename2", required=False,
    help="input file to convert", metavar="FILE2")
    parser.add_argument("-f3", dest="filename3", required=False,
    help="input file to convert", metavar="FILE3")
    
    parser.add_argument("-c", dest="command", required=True,
    help="command( build, or analyze)", metavar="COMMAND")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    #~ parser.add_argument("--dir", dest="data_directory",
    #~ help="Data directory for other external stemmers results", metavar="data_directory")
    
    parser.add_argument("-l", dest = 'limit', type=int, nargs='?',
                        const=0, 
                        help="limit lines to read")
    parser.add_argument("--all", type=bool, nargs='?',
                        const=True, 
                        help="Test all stemmers.")
    args = parser.parse_args()
    return args

class spell_index:
        
    def __init__(self,):
        pass

    def read(self, filename ):
        """ read csv """
        df = pd.read_csv(filename, delimiter="\t", encoding="utf8")
        return df
    def save(self, adapted_result, outfile):
        df = pd.DataFrame(adapted_result)
        return df
    def calcul_stats(self, dataframe):
        """
        Calculer 
        """
        df = dataframe
        df.loc[:, 'lemma'] = df['original'].apply(araby.strip_tashkeel)
        df.loc[:, 'word_nm'] = df['word'].apply(araby.strip_tashkeel)
        #~ # display= data stats
        #~ print('********* ROOT ****************')

        total = df.shape[0]
        stats_list={
        "count":total,
        "uniq roots":df['root'].nunique(),
        "uniq lemmas":df['lemma'].nunique(),
        "uniq words":df['word_nm'].nunique(),
        "mean words by root":  df[['word_nm','root' ]].groupby('root').count().mean(),
        "min words by root":   df[['word_nm','root' ]].groupby('root').count().min(),
        "max words by root":   df[['word_nm','root' ]].groupby('root').count().max(),
        "mean words by lemmas":df[['word_nm','lemma']].groupby('lemma').count().mean(),
        }

        dstats = pd.DataFrame.from_dict(stats_list, orient='index')
        
        return dstats
    def read_text_csv(self, filename):
        lines =[]
        try:
            with open(filename,) as inputfile:
                for line in inputfile:
                    lines.append(line.decode('utf8'))
          
        except:
            print " Can't Open the given File ", filename;
            sys.exit();

        tokens = []
        for line in lines:
            tokens.extend(araby.tokenize(line))
        tokens = [ t.replace('\n', '\\n') for t in tokens]
        df1 = pd.DataFrame({'word': tokens})
        return df1
    def join(self, filename, outfile, filename2 = "", how_join="outer"):
        # read first text
        df = self.read_text_csv(filename)
        df.loc[:,"correct"] =u""
        print(df.head())

        # read suggestions
        df2 = self.read(filename2) # read the output as second input file
        df2 = df2[['word','n1','suggest']].drop_duplicates()

        # join text words to suggestions

        df_cmp1 = pd.merge(df, df2, how=how_join, on='word')
        df_cmp1['n1'] = df_cmp1['n1'].fillna(0)
        df_cmp1['suggest'] = df_cmp1['suggest'].fillna("")
        df_cmp1.to_csv(outfile, sep="\t", encoding="utf8")
        print(df_cmp1.head())
        
        # 
        df2.to_csv(outfile+".wrong", sep="\t", encoding="utf8")
        
        print("Data is saved on %s file"%(outfile))
        print("Data (wrong only) is saved on %s file"%(outfile+".wrong"))
        
    def run(self, command, filename="", outfile="", filename2 = "",filename3 = ""):
        """
        run command 
        """
        if command == "join":
            # build unknown data
           self.join(filename, outfile, filename2 = filename2, how_join="left")

        else:
            pass
        
def main():
        
    args =grabargs()
    filename = args.filename
    filename_2 = args.filename2
    filename_3 = args.filename3
    outfile = args.outfile
    all_stemmers = args.all
    limit = args.limit
    command = args.command

    qi = spell_index()
    
    qi.run(command, filename, outfile, filename2 = filename_2)
    
    return True

if __name__ == '__main__':
    main()
