'''
Created on Feb 23, 2011

@author: vgapeyev
'''
from gombe.combine.combine import * 

from os.path import join 

def run_test():
    indir = "test_data"
    outdir = "test_out"
    #process_biography(join(indir, "Bio", "biography.csv"), join(outdir, "biogr.csv"))
    process_observations(join(indir, "Observations"), join(outdir, "observations.csv"))
    #process_audio(join(indir, "Audio"), join(outdir, "audio.csv"), 
    #                                    join(outdir, "anothervocal.csv"))

if __name__ == '__main__':
    run_test()

