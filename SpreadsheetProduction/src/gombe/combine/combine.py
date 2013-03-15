'''
Created on Feb 23, 2011

@author: vgapeyev
'''
import os, csv


def empty_csv_line(strlist):
    return all(len(x)==0 for x in strlist)

def clean_dir(dir):    #? not needed?
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        os.remove(fullpath)

###########  Biography #################

BIOGR_IN_HEADER  = ['Animal Id', 'Animal Name', 'Birth Date', 'Min Birth Date', 'Max Birth Date', 'Birth Group', 'First Born', 'Mom Id', 'Sex', 'Entry Date', 'Entry Type', 'Depart Date', 'Depart Type']
BIOGR_OUT_HEADER = ['Animal Id', 'Animal Name', 'Birth Date', 'First Born', 'Mom Id', 'Sex']

def get_biogr_line(line):
    return [ line[BIOGR_IN_HEADER.index(t)] for t in BIOGR_OUT_HEADER ]
            
def process_biography(in_file, out_file):
    "Take only the necessary fields from the biography file"
    print "Processing biography from %s to %s" % (in_file, out_file)
    fin = open(in_file, "U")
    csv_in = csv.reader(fin)
    fout = open (out_file, "w+")  # "+" clears the file first
    csv_out = csv.writer(fout)
    
    header = csv_in.next()
    assert BIOGR_IN_HEADER == header
    #print header
    
    #print BIOGR_OUT_HEADER
    csv_out.writerow(BIOGR_OUT_HEADER)
    for csv_line in csv_in:
        if not empty_csv_line(csv_line):
            row_out = get_biogr_line(csv_line)
            #print row_out 
            csv_out.writerow(row_out)
    fin.close(); fout.close()


################### Observations ########################

OBSERV_OUT_HEADER = ["year", "month", "day", "line_num", "time", "rec_device", "rec_focal_ind", "rec_num", "observation"]

def process_observations(in_dir, out_file):
    print "Processing observations from %s to %s" % (in_dir, out_file)
    fout = open(out_file, "w+")
    csv_out = csv.writer(fout)
    csv_out.writerow(OBSERV_OUT_HEADER)
    
    in_files = [f for f in os.listdir(in_dir) if not f.startswith(".")]
    for f in in_files:
        yyyy_mm_dd = f.split(".")[0].split("-") 
        year_month_day = [int(x) for x in yyyy_mm_dd]  #drops leading zeroes in some mm and dd
        fin = open(os.path.join(in_dir, f))
        csv_in = csv.reader(fin)
        for in_line in csv_in:
            out_line = []
            out_line.extend(year_month_day)
            out_line.extend(in_line)
            csv_out.writerow(out_line)
        fin.close()
    fout.close()


#################### Audio #############################

def process_audio(in_dir, out_audio, out_anothervocal):
    print "Processing biography from %s to %s and %s" % (in_dir, out_audio, out_anothervocal)

if __name__ == '__main__':
    from gombe.run_test import run_test
    run_test()

