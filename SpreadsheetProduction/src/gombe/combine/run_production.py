'''
Created on Mar 24, 2011

@author: vgapeyev
'''

from gombe.combine.combine import * 

# This has hard-wired locations for input and output....
def run_test():
    indir = "/Users/vgapeyev/Work/SpSc/FransPlooij/SpreadsheetProduction/3.ObservationCSVs"
    outfile = "/Users/vgapeyev/Work/SpSc/FransPlooij/SpreadsheetProduction/4.CombinedCSVs/observations.csv"

    process_observations(indir, outfile)

if __name__ == '__main__':
    run_test()

