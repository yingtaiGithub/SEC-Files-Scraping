import sys
import os
import time
import logging

import pandas as pd

import utility
import config


def main():
    print (input_csv)
    input_df = pd.read_csv(input_csv)
    logger.info("All input entries: %s" %len(input_df))

    if os.path.exists(output_csv):
        existing_df = pd.read_csv(output_csv)
        scanned_fnames = list(set(existing_df['filename']))
    else:
        utility.create_csv(output_csv, config.outputCsv_columns)
        scanned_fnames = []

    unscanned_entires_count = len(input_df)-len(scanned_fnames)
    logger.info("Scanned entries Count: %s"% len(scanned_fnames))
    logger.info("Unscanned entries Count: %s" %unscanned_entires_count)
    time.sleep(5)

    unscanned_df = input_df[~input_df.filename.isin(scanned_fnames)]
    unscanned_df = unscanned_df.reset_index()
    unscanned_df.fillna('', inplace=True)
    for index, row in unscanned_df.iterrows():
        location = row.location
        logger.info("Processing: %s/%s - %s" %(index+1, unscanned_entires_count, location))

        existing_value = list(row)[1:]

        if (location):
            # if os.path.exists(location):
            with open(location) as f:
                raw_text = f.read()

            no_html = utility.remove_htmlTags(raw_text)
            readability = utility.get_readability(no_html)
            new_row = existing_value + readability
            # else:
            #     new_row = existing_value + ['']* 10
        else:
            new_row = existing_value + ['']* 10

        utility.add_row(output_csv, new_row)


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

    if len(sys.argv) == 3:
        input_csv = sys.argv[1]
        output_csv = sys.argv[2]

        main()
    else:
        raise Exception("Unknown command")


