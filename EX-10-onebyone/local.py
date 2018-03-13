import sys
import os
import re
import logging
import csv

import pandas as pd

import utility
import config


def split(input_directory, fname, output_directory):
    with open(os.path.join(input_directory, fname)) as f:
        raw_text = f.read()

    split_texts = re.findall("<DOCUMENT>.+?<TYPE>EX-10.+?</DOCUMENT>", raw_text, flags=re.S)
    for index, split_text in enumerate(split_texts):
        file_path = os.path.join(output_directory, fname[:-4] + "." + str(index+1) + ".txt")
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path, 'w') as f:
            f.write(split_text)

        readability = utility.get_readability(split_text)
        notable_words_count = len(utility.remove_tables(split_text).split(' '))
        words_count = len(split_text.split(' '))

        yield [str(index+1)] + readability + [notable_words_count, words_count] + [file_path]

def main():
    df = pd.read_csv(input_csv)
    print (df.columns)
    logger.info("All input entries: %s" %len(df))

    new_df = pd.DataFrame(columns=config.outputCsv_columns)
    new_index = 0
    for index, row in df.iterrows():
        existing_values = [row.cik, row.coname, row.form, row.fdate, row.fname]
        fname = row.fname
        if os.path.exists(os.path.join(input_directory, fname)):
            print (fname)
            readability_wordscount = list(split(input_directory, fname, output_directory))
            if readability_wordscount:
                new_rows = [existing_values + ['success'] + item for item in readability_wordscount]

        #     else:
        #         # new_rows = [existing_values + ["Fail"] + ['']* 13]
        #         new_rows = []
        # else:
        #     # new_rows = [existing_values + ["Fail"] + ['']* 13]
        #     new_rows = []

                for new_row in new_rows:
                    new_df.loc[new_index] = new_row
                    new_index += 1

    new_df.to_csv(output_csv)


if __name__ == "__main__":
    logger = logging.getLogger('mylogger')
    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    fileHandler = logging.FileHandler('log/local_count.log')
    streamHandler = logging.StreamHandler()
    fileHandler.setFormatter(fomatter)
    streamHandler.setFormatter(fomatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)

    logger.info("==================================")
    logger.info('start')

    if len(sys.argv) == 5:
        input_csv = sys.argv[1]
        input_directory = sys.argv[2]
        output_directory = sys.argv[3]
        output_csv = sys.argv[4]

        main()

    else:
        print ('else')
        raise Exception("Unknown command")


