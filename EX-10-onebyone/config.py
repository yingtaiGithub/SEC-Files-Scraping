outputCsv_columns = ['cik', 'company_name', 'form_type', 'date_filed', 'filename', 'success', 'MultiDoc', 'noTable_words_count', 'words_count', 'location', 'flesch_reading_ease', 'smog_index', 'flesch_kincaid_grade', 'automated_readability_index', 'dale_chall_readability_score', 'difficult_words', 'linsear_write_formula', 'gunning_fog', 'coleman_liau_index', 'text_standard']
extract_Columns = ['cik', 'company_name', 'form_type', 'date_filed', 'filename', 'success', 'MultiDoc', 'noTable_words_count', 'words_count', 'location']
# for i in range(1, 51):
#     csv_columns.append('freq1_title%d'%i)
#     csv_columns.append('freq2_title%d'%i)
#     csv_columns.append('freq12_title%d'%i)

starting = "<DOCUMENT>\n<TYPE>EX-10"
ending = "</TEXT>\n</DOCUMENT>"