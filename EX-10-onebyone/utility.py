import requests
import json
import re
import csv

from config import *
from textstat.textstat import textstat

class Master_idx:
    def __init__(self, description='', last_data='', comments='', ftp='', entries=[], year = 0, quarter = 0):
        self.description = description
        self.last_data = last_data
        self.comments = comments
        self.ftp = ftp
        self.entries = entries
        self.year = year
        self.quarter = quarter

    def to_json(self):
        def entry_to_json(entry):
            return entry.to_json()
        return {
            'description': self.description,
            'last_data':   self.last_data,
            'comments':    self.comments,
            'ftp':         self.ftp,
            'entries':     list(map(entry_to_json, self.entries)),
            'year':        self.year,
            'quarter':     self.quarter
        }

    def to_json_file(self, filename):
        out = open(filename, 'w')
        json.dump(self.to_json(), out, indent = 2)
        out.flush()
        out.close()

class Master_idx_entry:
    def __init__(self, cik='', company_name='', form_type='', date_filed='', filename=''):
        self.cik = cik
        self.company_name = company_name
        self.form_type = form_type
        self.date_filed = date_filed
        self.filename = filename

    def to_json(self):
        return {
            'cik':          self.cik,
            'company_name': self.company_name,
            'form_type':    self.form_type,
            'date_filed':   self.date_filed,
            'filename':     self.filename
        }

    def to_list(self):
        return [self.cik, self.company_name, self.form_type, self.date_filed, self.filename]

    def form_url(self):
        # return 'ftp://ftp.sec.gov/' + self.filename
        return 'https://www.sec.gov/Archives/' + self.filename

    def contents(self):
        return requests.get(self.form_url(), timeout=url_timeout).text
        # stream = urlopen(self.form_url(), timeout=url_timeout)
        # res = stream.read()
        # stream.close()
        # return res.decode('utf-8')

def split_colon_line(line):
    pos = line.find(':')

    if not pos:
        return False

    return [line[:pos], line[pos + 1:].strip()]

def Master_idx_entry_of_string(csv_line):
    # parts = string.strip().split('|')
    return Master_idx_entry(cik          = csv_line[0],
                            company_name = csv_line[3],
                            form_type    = csv_line[2],
                            date_filed   = csv_line[1],
                            filename     = csv_line[4])
def read_Master_idx(reader):
    # line = stream.readline()
    # line = stream.readline().decode('utf-8')
    description = False
    last_data = False
    comments = False
    ftp = False
    entries = []

    hit_entries = False

    for line in reader:
        entries.append(Master_idx_entry_of_string(line))


        # line = stream.readline().decode('utf-8')

    return Master_idx(entries = entries)

def Master_idx_of_file(filename, year=0, quarter=0):
    try:
        with open(filename)as f:
            reader = csv.reader(f)
            res = read_Master_idx(reader)

        res.year = year
        res.quarter = quarter
        return res
    except IOError:
        print ("There is not csv file. Please input correct path.")

def remove_htmlTags(htmlText):
    return re.sub(r"<.+?>", '', htmlText, flags=re.I|re.DOTALL)

def remove_tables(htmltext):
    return re.sub(r"<table.+?</table>", '', htmltext, flags=re.I|re.DOTALL)

def removeNumber(text):
    return re.sub(r'\d+(\.\d+)*', '', text)


def distance_count(text, keyword, word_lists):
    c = 0
    # word_list = text.split()
    while True:
        try:
            keyword_position = text.index(keyword)
            partial_text = text[keyword_position-500:keyword_position+500]
            text = text[:keyword_position] + text[keyword_position + len(keyword):]

            checker = 0
            for word_list in word_lists:
                for word in word_list:
                    if word in partial_text:
                        checker += 1

                        break

            if checker ==  len(word_lists):
                c += 1

        except ValueError:
            break

    return c


def get_parts(contents):
    parts = re.findall(r'%s.+?%s'%(starting, ending), contents, re.S)
    return parts

def get_title(contents):
    try:
        index = contents.index('<TYPE>EX-10')
    except:
        return ''
    contents = contents[index:]
    lines = contents.split("\n")
    lines = list(filter(None, lines))
    return "\n".join(lines[:30])


def get_readability(contents):
    readability = []
    readability.append(textstat.flesch_reading_ease(contents))
    readability.append(textstat.smog_index(contents))
    readability.append(textstat.flesch_kincaid_grade(contents))
    readability.append(textstat.automated_readability_index(contents))
    readability.append(textstat.dale_chall_readability_score(contents))
    readability.append(textstat.difficult_words(contents))
    readability.append(textstat.linsear_write_formula(contents))
    readability.append(textstat.gunning_fog(contents))
    readability.append(textstat.coleman_liau_index(contents))
    readability.append(textstat.text_standard(contents))

    return readability

def create_csv(filename, columns):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)

def add_rows(filename, rows):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# text = "aaaa\n<Table \n aaaa \n </Table>\ncde\n<TABLE>\needdddd\n</TABLE>\nccccc"
# print (text)
# print (len(text.split()))
# text1 = remove_tables(text)
# print (text1)
# print (len(text1.split()))

