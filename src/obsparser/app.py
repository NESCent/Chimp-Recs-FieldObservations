'''
Created on Feb 8, 2011

@author: vgapeyev
'''
import csv, re

__nonspace_whitespace = re.compile(r"[\t\n\r\f\v]")
__long_whitespace = re.compile(r"[ ]{2,}")

def normalize_whitespace(str):
    str = re.sub(__nonspace_whitespace, " ", str)
    str = re.sub(__long_whitespace, " ", str)
    return str

def empty_line(line):
    if line.isspace():
        return True
    else:
        return False
    
def at_beginning(matchobj, str):
    if not matchobj:
        return False
    prefix = str[:matchobj.start()]
    return prefix == "" or prefix.isspace()
    
def likely_chimp_name(prov_time, prov_rest):
    return (prov_time == "PM" or prov_time == "AM") \
           and prov_rest[0] == " "  \
           and prov_rest[1].isalpha()
           
def pad_zero(time):
    if time.isdigit() and len(time) == 3:
        return "0" + time
    else:
        return time
    
def pick_time(line):
#    timepat_spec = r"(?P<time>\d\d\d\d)"
#    timepat_spec = r"(?P<time>AM|PM|(\d{4}(\s*(-|until)\s*\d{4})?(\s*(AM|PM))?))"
    timepat_spec = r"(?P<time>AM|PM|(\d{3,4}(\s*(-|until)\s*\d{3,4})?(\s*(AM|PM))?))"
    timepat = re.compile(timepat_spec)
    time_match = re.search(timepat, line)
    if time_match and at_beginning(time_match, line):
        time = time_match.group("time")
        rest = line[time_match.end("time"):]
        if not likely_chimp_name(time, rest):
            return (pad_zero(time), rest.lstrip())
        else: return ("", line) 
    else:
        return ("", line)


def pick_recnum(line):
#    pat_spec = r"N-(?P<animal>[a-zA-Z]+)-(?P<num>\d+)"
#    pat_spec = r"N-(?P<animal>[a-zA-Z]+)-(?P<num>\d+\w*)"    
    pat_spec = r"[Nn]\s*(-|_|=)=?\s*(?P<animal>[a-zA-Z]+)\s*(-|_)?\s*(?P<num>\d+\w*)"
    pat = re.compile(pat_spec)
    match = re.search(pat, line)
    if match and at_beginning(match, line):
        equip = "N"
        animal = match.group("animal").upper() 
        num = match.group("num")
        rest = line[match.end():]
        return ((equip, animal, num), rest.lstrip())
    else:
        return (("", "", ""), line)


def parse_line(line):
    (time, line) = pick_time(line)
    (recnum, line) = pick_recnum(line)
    text = normalize_whitespace(line.strip())
    return (time, recnum[0], recnum[1], recnum[2], text)

def parse_one_file(src_file, dest_file):
    #print "Parsing %s" % src_file
    #print "Output to %s" % dest_file
    fin = open(src_file)
    fout = open(dest_file, "w")
    csv_writer = csv.writer(fout) 
    count = 0
    for line in fin:
        count = count + 1
        if not empty_line(line):
            (time, equip, animal, num, text) = parse_line(line)
            csv_writer.writerow([count, time, equip, animal, num, text])
    fin.close()
    fout.close()


__txt_fmt = "%-60.60s"
__csv_fmt = "%3.3s %5s %1.1s %3.3s %3s |%-120.120s|"

def display_parse(txt_fname, csv_fname):
    txt_file = open(txt_fname)
    csv_file = open(csv_fname)
    csv_reader = csv.reader(csv_file)
    txt_num = 1
    for csv_line in csv_reader:
        csv_num = int(csv_line[0])
        while txt_num < csv_num:
            txt_num = txt_num + 1 
            print __csv_fmt % ("", "", "", "", "", "",),
            print ("#"+__txt_fmt+"#") % txt_file.readline().rstrip()
        txt_num = txt_num + 1 
        print __csv_fmt % tuple(csv_line),
        print ("$"+__txt_fmt+"$") % txt_file.readline().rstrip()
    txt_file.close()
    csv_file.close()

def compare_parses(old_fname, new_fname):
    old_file, new_file = open(old_fname), open(new_fname)
    old_reader, new_reader = csv.reader(old_file), csv.reader(new_file)
    for (old_line, new_line) in zip(old_reader, new_reader):
        if old_line != new_line:
            print ("o"+__csv_fmt) % tuple(old_line)
            print ("n"+__csv_fmt) % tuple(new_line)
            print ""
    old_file.close(), new_file.close()


def main():
    import optparse, sys
    p = optparse.OptionParser() 
    p.set_usage("%prog source_file dest_file")
    p.set_description("TODO description")
    opt, args = p.parse_args()

    if len(args) != 2:
        sys.stderr.write(p.get_usage())
        raise SystemExit(1) 
    src_file = args[0]
    dest_file = args[1]
    
    parse_one_file(src_file, dest_file)
    

def main_hardwired(base):
    infile = "test_data/inputs/%s.txt" % base 
    outfile = "test_data/outputs/%s.csv" % base  
    parse_one_file(infile, outfile)

def display_hardwired(base):
    infile = "test_data/inputs/%s.txt" % base 
    outfile = "test_data/work/%s.csv" % base  
    display_parse(infile, outfile)
    
def compare_hardwired(base):
    workfile = "test_data/work/%s.csv" % base  
    outfile = "test_data/outputs/%s.csv" % base  
    compare_parses(workfile, outfile)
    

if __name__ == '__main__':
    #main()
    #main_hardwired("1971-07-15")
    #display_hardwired("1971-07-14")
    compare_hardwired("1971-07-14")