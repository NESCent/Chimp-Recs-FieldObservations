'''
Created on Mar 25, 2011

@author: vgapeyev
'''

import os, shutil, csv, codecs
import sqlite3



#The headers are expected to be in the same quantity and order as in the loaded files.  
#The names, however, may differ.  The names here will be used in the database.  
AUDIO_FIELDS = ['wav_file', 'editing_notes', 'rec_device', 'rec_individual', 'rec_num',  'level', 'quality',  
                 'month',  'day',     'year',  'other_individuals', 'transcript',  'context',  
                 'cut_num',    'cut_len',  'level_timing_note']

OBSERVATION_FIELDS = ['year', 'month', 'day', 'line_num', 'time', 'rec_device', 'rec_individual', 'rec_num', 'observation']

BIOGRAPHY_FIELDS = ['animal_id', 'animal_name', 'birth_date', 'min_birth_date', 'max_birth_date', 
                     'birth_group', 'first_born', 'mom_id', 'sex', 'entry_date', 'entry_type', 'depart_date', 'depart_type'] 

ANOTHERVOCAL_FIELDS = ['rec_device', 'rec_individual', 'rec_num', 
                       'another_indiv'] 


def csv2newtable(db_conn, csv_file, table_name):
    '''TODO'''
    
def display_headers_fields(file, fields):
    csv_file = open(file, "U")
    csv_reader = csv.reader(csv_file)
    headers = csv_reader.next()
    csv_file.close()
    
    if (len(headers) != len(fields)):
        print "LIKELY ERROR: numbers of file headers and DB fields are not the same."
    
    field_max = max ([len(f) for f in fields])
    
    for (h, f) in zip(headers, fields):
        fmt = "  %-" + str(field_max + 1) + "s <--- %s"
        print fmt % (f, h)

   
def exec_parameterless(db_conn, query):
        '''Careful!  This eats any ProgrammingError exceptions.'''
        cur = db_conn.cursor()
        try:
            cur.execute(query)
        except sqlite3.ProgrammingError:
            pass
        finally:
            db_conn.commit()
            cur.close()
        

def create_table(db_conn, table_name, table_fields):
    fields_spec = ',\n  '.join(['"%s"' % f for f in table_fields]) 
    q = '''
create table "%s" (\n  %s) 
''' % (table_name, fields_spec)
    print q
    exec_parameterless(db_conn, q)
    
def empty_to_null(seq):
    for (i,x) in enumerate(seq):
        if x == '':
            seq[i] = None
    
    
def load_csv(db_conn, file, table, fields, row_adjuster):    
    print "Loading %s ..." % file
    display_headers_fields(file, fields)
    create_table(db_conn, table, fields)

#    csv_stream = csv.reader(codecs.open(file, "rU", "utf-8"))  # with this SQLite Manager does not show diacritics
    csv_stream = csv.reader(open(file, "rU"))   # with this, SQL Manager shows diacritics ... go figure ... 
    csv_stream.next()   # eat the header
    
    cur = db_conn.cursor()
    args_spec = ', '.join(['?' for _ in fields])
    q = 'insert into "%s" values (%s)' % (table, args_spec)
    
    #for row in csv_stream:
    for (i, row) in enumerate(csv_stream):
        empty_to_null(row)
        if i < 100: print row
        adj_row = row_adjuster(row)
        cur.execute(q, adj_row)
    
    db_conn.commit()
    cur.close()
      

def load_biography(db_conn, file):
    def adjust_bio(row):
        for (i, x) in enumerate(row):
            if x == 'null':
                row[i] = None
        return row
    load_csv(db_conn, file, "biography", BIOGRAPHY_FIELDS, adjust_bio)      

    
def load_observation(db_conn, file):
    idx_month = OBSERVATION_FIELDS.index('month')
    idx_day = OBSERVATION_FIELDS.index('day')
    idx_line_num = OBSERVATION_FIELDS.index('line_num')
    
    def adjust_observation(row):
        if row[idx_month]: row[idx_month]    = row[idx_month].zfill(2)
        if row[idx_day]: row[idx_day]      = row[idx_day].zfill(2)
        if row[idx_line_num]: row[idx_line_num] = row[idx_line_num].zfill(3)
        return row
    
    load_csv(db_conn, file, "observation", OBSERVATION_FIELDS, adjust_observation)
    
    
def load_audio(db_conn, file):
    idx_month = AUDIO_FIELDS.index('month')
    idx_day = AUDIO_FIELDS.index('day')
    idx_rec_device = AUDIO_FIELDS.index('rec_device')
    idx_rec_individual = AUDIO_FIELDS.index('rec_individual')
    idx_rec_num = AUDIO_FIELDS.index('rec_num')
    idx_other_individuals = AUDIO_FIELDS.index('other_individuals')

    av_table = "anothervocal"
    create_table(db_conn, av_table, ANOTHERVOCAL_FIELDS)
    av_cur = db_conn.cursor()
    av_args_spec = ', '.join(['?' for _ in ANOTHERVOCAL_FIELDS])
    av_q = 'insert into "%s" values (%s)' % (av_table, av_args_spec)
    
    def adjust_audio(row):
        if row[idx_other_individuals]:
            for other_indiv in row[idx_other_individuals].split(","):
                other_indiv = other_indiv.strip()
                av_row = (row[idx_rec_device], 
                          row[idx_rec_individual], 
                          row[idx_rec_num],
                          other_indiv
                          )
                av_cur.execute(av_q, av_row)

        if row[idx_month]: row[idx_month]    = row[idx_month].zfill(2)
        if row[idx_day]: row[idx_day]      = row[idx_day].zfill(2)
        return row
    
    load_csv(db_conn, file, "audio", AUDIO_FIELDS, adjust_audio)
    
    

def load_into_db(db_conn, audio_file, biogr_file, observ_file):
    load_biography(db_conn, biogr_file)
    load_observation(db_conn, observ_file)
    load_audio(db_conn, audio_file)
    
    
QUERY_AUDIO = '''
select rec_device as "Recorder", rec_individual as "Focal individual", rec_num as "Record number", 
       level as "Recording level", quality as "Outstanding quality", 
       year, month, day, 
       other_individuals as "Other vocalizing individuals", 
       transcript as "Transcript", context as "Behavioral context"
from audio
'''    
  
QUERY_OBSERVATION= '''
select year, month, day, line_num as "log line", time, 
     rec_device as "Recorder", rec_individual as "Focal individual", rec_num as "Record number",
     observation as "Observation"
from observation
order by year, month, day, line_num
'''

QUERY_OTHERVOCALIZERS = '''
select 
  rec_device as "Recorder", rec_individual as "Focal individual", rec_num as "Record number", 
  another_indiv as "Another vocalizing individual"
from anothervocal
'''

QUERY_BIOGRAPHY = '''
select animal_id as "Animal Id", animal_name as "Animal Name", 
   birth_date as "Birth Date", 
   min_birth_date as "Min Birth Date", max_birth_date as "Max Birth Date", 
   birth_group as "Birth Group", first_born as "First Born", mom_id as "Mom Id", 
   sex as "Sex", entry_date as "Entry Date", entry_type as "Entry Type", 
   depart_date as "Depart Date", depart_type as "Depart Type"
from biography
'''
    
QUERY_COMBINED = '''
select a.rec_device, a.rec_individual, a.rec_num, 
       a.level, a.quality, 
       a.year, a.month, a.day, 
       a.other_individuals,
       a.transcript, a.context, 
       o.line_num, o.time, o.observation
from audio a left join observation o
  on a.rec_device = o.rec_device and a.rec_individual = o.rec_individual and a.rec_num = o.rec_num
where (a.year = o.year and a.month = o.month and a.day = o.day)
   or o.rowid is null
'''
#limit 100
#TODO: drop the LIMIT above

MACAULAY_FIELDS = [
"Recordist's Reference Number (RRN)", "Scientific Name", "Sound File Name(s)", "Same as RRN",
"Recordist",  "Recordist2", "How Identified", "Confidence in ID (%)", 
"Time", "Day", "Month", "Year", 
"Closest Distance to Subject (m)", "Furthest Distance from Subject (m)", 
"Country", "State, Province, or Dept.", "County (U.S. Only)", 
"Distance (km) from", "Direction from", "Specific Locality", 
"Latitude (Degrees)", "Longitude (Degrees)", "Elevation (m)",     
"Song", "Call", "Mechanical", "Subsong", "Duet", "Counter-singing",     
"Flight Song", "Flight Call", "Whisper", "Dawn Song", "Dusk Song", "Mimicry",     
"Natural", "Includes Natural", "Playback of Own Sound", "Playback of Same Species", 
"Human Imitation", "Pishing", "No Response", 
"Orient", "Approach", "Normal Sound", "Different Sound", 
"Attack", "Advertising", "Courtship", "Mate", "Contact", "Alarm", "Scold", "Aggression", 
"Flying", "Foraging", "Flock Contact",     "Visual Display", 
"Adult Male(s)", "Adult Female(s)", "Adult Unknown Sex", "Unknown Age & Unknown Sex", 
"Habitat", "Air Temp. (C)", "Water Temp (C)", 
"Recorder", "Mono/Stereo", "Sampling Rate (kHz)", "Bit Depth", "Microphone(s)", "Parabola", 
"Specimen Collected?", "Background Species", "Notes"
]

def make_macaulay_record():
    '''Creates a Macaulay record dictionary prepopulated with common (non-null) values'''
    return {
        "Scientific Name" : "Pan troglodytes schweinfurthii", 
        "Sound File Name(s)" : "<???>", 
        "Same as RRN" : "<???>",
        "Recordist" : "Dr. Hetty van de Rijt", 
        "How Identified" : "Sight & Sound", 
        "Confidence in ID (%)" : "100",
        "Closest Distance to Subject (m)" : "5", 
        "Furthest Distance from Subject (m)" : "15", 
        "Country" : "Tanzania, United Republic of", 
        "State, Province, or Dept." : "Kigoma",
        "Specific Locality" : "Gombe National Park",  
        "Latitude (Degrees)" : "<TODO>", "Longitude (Degrees)" : "<TODO>", "Elevation (m)" : "<TODO>",
        "Natural" : "x",
        "Habitat" : "<TODO>",
        "Recorder" : "<TODO>",   # Nagra ???????
        "Mono/Stereo" : "Mono",
        "Microphone(s)" : "",   # Sennheiser directional microphone type ????????????
            }

def not_null_or_blank(x):
    if x == None:  return ""
    else:  return x 

def populate_macaulay_record(row):
    import simplejson as json
    mrec = make_macaulay_record()
    mrec["Recordist's Reference Number (RRN)"] = "%s-%s-%s" % (row[0], row[1], row[2])
    mrec["Time"] = not_null_or_blank(row[12])
    mrec["Day"] = not_null_or_blank(row[7])
    mrec["Month"] = not_null_or_blank(row[6])
    mrec["Year"] = not_null_or_blank(row[5])
    mrec["Notes"] = json.dumps({
                       "Recording level" : row[3],
                       "Outstanding quality" : row[4], 
                       "Other vocalizing individuals" : row[8],
                       "Transcript" : row[9],
                       "Behavioral context" : row[10],
                       "Raw observation log line" : row[11], 
                       "Raw observation log entry" : row[13],
                       "Info" : "This is a JSON dump of detailed metadata for this audio.  They may also be available in tabular form, elsewhere on the web, together with the metadata for all other records from this collection. Until further notice, search for 'Gombe chimp vocalizations of Hetty van de Rijt/Frans X. Plooij'.", 
                                })
    return mrec
        
def macaulay_query_to_csv(db_conn, query, csvfile):
    '''Creates Macaulay deposition file, with JSON Notes field'''
    file = open(csvfile, 'w')
##?    file = codecs.open(csvfile, 'w', 'utf-8')
    dictwriter = csv.DictWriter(file, MACAULAY_FIELDS, "")
    header = dict([ (f,f) for f in MACAULAY_FIELDS]) 
    dictwriter.writerow(header)

    cur = db_conn.cursor()
    cur.execute(query)
    for rec in cur:
        mrec = populate_macaulay_record(rec)
        dictwriter.writerow(mrec)
    cur.close()
    file.close()
        

def query_to_csv(db_conn, query, csvfile):
    file = open(csvfile, 'w')
##?    file = codecs.open(csvfile, 'w', 'utf-8')
    csvwriter = csv.writer(file)
    cur = db_conn.cursor()
    cur.execute(query)
    colnames = [ d[0] for d in cur.description ] 
    csvwriter.writerow(colnames)
    for rec in cur:
        csvwriter.writerow(rec)
    cur.close()
    file.close()

    
def extract_from_db(db_conn, dest_dir):
    '''Produce files for the Macaulay and native depositions'''
    native_dir = os.path.join(dest_dir, "native")
    macaulay_dir = os.path.join(dest_dir, "macaulay")
    shutil.rmtree(native_dir); os.mkdir(native_dir)
    shutil.rmtree(macaulay_dir); os.mkdir(macaulay_dir)
    
    query_to_csv(db_conn, QUERY_BIOGRAPHY, os.path.join(native_dir, "biography.csv"))
    query_to_csv(db_conn, QUERY_AUDIO, os.path.join(native_dir, "audio.csv"))
    query_to_csv(db_conn, QUERY_OTHERVOCALIZERS, os.path.join(native_dir, "othervocalizers.csv"))
    query_to_csv(db_conn, QUERY_OBSERVATION, os.path.join(native_dir, "observation.csv"))
    
    macaulay_query_to_csv(db_conn, QUERY_COMBINED, os.path.join(macaulay_dir, "macaulay.csv"))

def run_production():
    from os.path import join 
    sourcefiles_dir = "/Users/vgapeyev/Work/SpSc/FransPlooij/SpreadsheetProduction/4.CombinedCSVs" 
    audio_file  = join(sourcefiles_dir, "audio-utf8.csv")
    biogr_file  = join(sourcefiles_dir, "biography.csv")
    observ_file = join(sourcefiles_dir, "observations-utf8.csv")

    destfiles_dir = "/Users/vgapeyev/Work/SpSc/FransPlooij/SpreadsheetProduction/6.OutputCSVs"

    sqlite_file =  "/Users/vgapeyev/Work/SpSc/FransPlooij/SpreadsheetProduction/5.SQLite/gombe-utf8.sqlite"
    try:
        os.remove(sqlite_file)
    except OSError:
        pass
    
    
    db_conn = sqlite3.connect(sqlite_file)
    
    load_into_db(db_conn, audio_file, biogr_file, observ_file)
    extract_from_db(db_conn, destfiles_dir)
    
    db_conn.close()

if __name__ == '__main__':
    run_production()