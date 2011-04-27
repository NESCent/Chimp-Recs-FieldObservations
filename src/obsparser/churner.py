'''
Created on Feb 10, 2011

@author: vgapeyev
'''

import os.path, sys, shutil
from obsparser import app


def mk_fname(dir, base, ext):
    return os.path.join(dir, base + "." + ext)

    

def churn(src_dir, dest_dir, work_dir):
    #Ensure work_dir is empty
    work_files = [f for f in os.listdir(work_dir) if not f.startswith(".")]
    if work_files:
        print "Working directory (%s) is not empty." % (work_dir)
        answer = ""
        while answer == "":
            answer = raw_input("[C]lean? [A]bort? ").strip().lower()
            print "The response was: %s" % answer  #--
            if answer.startswith("c"):
                for file in work_files:
                    fullpath = os.path.join(work_dir, file)
                    os.remove(fullpath)
                print "Deleted all files from the working directory"
                break
            elif answer.startswith("a"):
                print "Aborted. (At non-empty working directory)"
                sys.exit(0)
            else:
                answer = ""
     
    #Check that previously-processed files still parse the same
    ## For each file in dest_dir, parse the counterpart in src_dir, putting it in work_dir
    print "Checking previously-processed files..."
    processed_basenames = [f.split(".csv")[0] for f in os.listdir(dest_dir) if not f.startswith(".")]
    for b in processed_basenames:
        app.parse_one_file(mk_fname(src_dir, b, "txt"), mk_fname(work_dir, b, "csv"))
        print b,
    print ""
    ## Compare each file pair and print out names of those that differ
    disagreements = [b for b in processed_basenames
                        if open(mk_fname(work_dir, b, "csv")).readlines() != open(mk_fname(dest_dir, b, "csv")).readlines()]
    if disagreements:
        answer = "0"
        while answer.isdigit():
            print "There are previously-processed files that parse differently now:"    
            for i,b in enumerate(disagreements):
                print "[%i] %s" % (i+1,b)
            ## Upon request, show differences between the files
            answer = raw_input("File [n]umber to display the difference? [A]bort? [P]roceed? ").strip().lower()
            if answer.startswith("a"):
                print "Aborted. (At the list of files with parsing disagreements)"
                sys.exit(0)
            elif answer.startswith("p"):
                break
            elif answer.isdigit():
                i = int(answer) - 1
                print "%s.csv: old vs new:" % disagreements[i]
                oldparse = mk_fname(dest_dir, disagreements[i], "csv")
                newparse = mk_fname(work_dir, disagreements[i], "csv")
#                #diffcommand = "diff --side-by-side --width=200 --left-column --suppress-common-lines --strip-trailing-cr  %s %s" % (oldparse, newparse)
#                diffcommand = "diff --suppress-common-lines --strip-trailing-cr   %s %s" % (oldparse, newparse)
#                # --unified=1  --context=1
#                difftext = commands.getoutput(diffcommand)
#                print difftext
                app.compare_parses(oldparse, newparse)
            else:
                pass
        
        #Decide what to do about the disagreements
        answer = ""
        while answer == "":    
            answer = raw_input("Accept the [n]ew parses or stick with the [o]ld ones? [A]bort? ").strip().lower()
            if answer.startswith("a"):
                sys.exit(0)
            elif answer.startswith("o"):
                for b in disagreements:
                    os.remove(mk_fname(work_dir, b, "csv"))
                print "Deleted from %s: " % work_dir
                print disagreements
                break
            elif answer.startswith("n"): 
                for b in disagreements:
                    shutil.move(mk_fname(work_dir, b, "csv"), mk_fname(dest_dir, b, "csv"))
                print "Moved from %s to %s: " % (work_dir, dest_dir)
                print disagreements
                break
            else: 
                answer = ""

    #Disagreements or not, work_dir does not contain anything valuable by now, so let's just clean it
    for file in os.listdir(work_dir):
        fullpath = os.path.join(work_dir, file)
        os.remove(fullpath)

    #Now to parsing files never processed before
    print "Parsing new files..."
    processed_basenames = [f.split(".csv")[0] for f in os.listdir(dest_dir) if not f.startswith(".")]
    input_basenames     = [f.split(".txt")[0] for f in os.listdir(src_dir)  if not f.startswith(".")]
    unproc_basenames = list(set(input_basenames).difference(processed_basenames))
    unproc_basenames.sort()
    print "Files still to be parsed: "
    print unproc_basenames
    
    while unproc_basenames:
        bname = unproc_basenames.pop(0)
        print "Parsing file %s" % bname
        txt_file = mk_fname(src_dir, bname, "txt")
        csv_file = mk_fname(work_dir, bname, "csv")
        app.parse_one_file(txt_file, csv_file)
        app.display_parse(txt_file, csv_file) 
        answer = ""
        while answer == "":
            answer = raw_input("[G]ood parse? (move to dest_dir)  [B]ad parse? (keep in work_dir) [A]bort? ").strip().lower()
            if answer.startswith("a"):
                print "Aborted. (in parsing new files)"
                sys.exit(0)
            elif answer.startswith("g"):
                shutil.move(mk_fname(work_dir, bname, "csv"), mk_fname(dest_dir, bname, "csv"))
                print "Moved %s from work_dir to dest_dir" % bname
                break
            elif answer.startswith("b"):
                break
            else:
                answer = ""
                
    work_files = [f for f in os.listdir(work_dir) if not f.startswith(".")]
    if work_files:
        print "All files were parsed, but some were not accepted -- see work_dir."
    else:
        print "All files are parsed and accepted. Congratulations!"
    
    
    
def main_hardwired():
    src_dir = os.path.abspath("test_data/inputs")
    dest_dir = os.path.abspath("test_data/outputs")
    work_dir = os.path.abspath("test_data/work")
    churn(src_dir, dest_dir, work_dir)
    
if __name__ == '__main__':
    main_hardwired()    