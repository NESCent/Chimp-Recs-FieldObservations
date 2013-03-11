#TODO: silent vs verbose mode 
import os, os.path, shutil
import re

month_numbers = {"jan" : "01", "feb" : "02", "mar" : "03", "apr" : "04", 
                 "may" : "05", "jun" : "06", "jul" : "07", "aug" : "08", 
                 "sep" : "09", "oct" : "10", "nov" : "11", "dec" : "12", }

def parse_date_as_iso(str):
    """Convert date like '2August1972' into an ISO date like '1972-08-02'"""
    datepat = re.compile(r"(?P<day>[0-9]+)(?P<month>.+?)(?P<year>[0-9]+)")
    m = datepat.match(str)
    if None == m: return None
    (day, month, year) = m.group('day', 'month', 'year')
    day = day.zfill(2) 
    month = month.strip().lower()[0:3]
    month = month_numbers.get(month, "XX")
    return year + "-" + month + "-" + day

def iso_name(file):
    "Converts a file name from, e.g.,  2August1972.ext to 1972-08-02.txt"
    (base, ext) = os.path.splitext(file)
    iso_date = parse_date_as_iso(base)
    if iso_date:
        return iso_date + ext
    else:
        return None

def clear_dir(dir):
    """Erase all contents of dir"""
    for entry in os.listdir(dir):
        fullentry = os.path.join(dir,entry)
        if os.path.isdir(fullentry):
            shutil.rmtree(fullentry)
        else: 
            os.remove(fullentry)
    

def rename_dated_files(srcdirname, destdirname):
    "Copies date-named files from srcdirname to destdirname, renaming them with ISO dates "
    srcdir = os.path.abspath(srcdirname)
    destdir = os.path.abspath(destdirname)
    print "Copying and renaming files"
    print "  from %s" % srcdir 
    print "  to   %s"   % destdir 

    print "Cleaning %s" % destdir
    clear_dir(destdir)

    srcfiles = os.listdir(srcdir) 
    for src in srcfiles:
        dest = iso_name(src)
        if dest:
            print "Copying \t%s to \t%s" % (src, dest)
            fullsrc = os.path.join(srcdir, src)
            fulldest = os.path.join(destdir, dest)
            shutil.copy(fullsrc, fulldest)
        else:
            print "Ignoring %s" % src 



if __name__ == '__main__': 
    import optparse, sys
    p = optparse.OptionParser()
    p.set_usage("%prog source_dir dest_dir")
    p.set_description("Copies date-named files from source_dir to dest_dir, while renaming them to ISO dates.\n E.g., file 2August1972.ext becomes 1972-08-02.txt.   Directories and other files are ignored. Spaces in filename permitted, month can be abbreviated (3 letters or more) and use any combination of lower and upper case letters. File extension is preserved. Destination directory is assumed to exist and is cleaned first.")
    opt, args = p.parse_args()

    if len(args) != 2:
        sys.stderr.write(p.get_usage())
        raise SystemExit(1) 
    src_dir = args[0]
    dest_dir = args[1]
    
    rename_dated_files(src_dir, dest_dir)
 

