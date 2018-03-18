The scripts were made by python3
- Local.py split already downloaded text in local with keyword as a rule. And every splitted texts, it calculate the readability and output to csv file.
- Extraction.py extract partial texts from original one. 
- Readability.py calculate readability for the texts from Extraction.py and generate final output csv. 

### Dependencies
    pip install -r requirements.txt
    
### Execution
    python local.py [input_csv] [input_directory] [output_directory] [output_csv]
    ex: C:\Python35\python.exe C:\Users\renchengw\Dropbox\Copy\data\sec_edgar\zhangyintai\key_words_search\section_title_count1\local.py E:\sec_test\input\exhibits_ex10.csv E:\sec_text\input E:\sec_text\output E:\sec_text\output\output.csv
    
    python extract.py [input_csv] [input_directory] [output_directory] [output_csv]
    ex: C:\Python35\python.exe C:\Users\renchengw\Dropbox\Copy\data\sec_edgar\zhangyintai\key_words_search\section_title_count1\extract.py E:\sec_test\input\exhibits_ex10.csv E:\sec_text\input E:\sec_text\output E:\sec_text\output\extract.csv

    python readability.py [input_csv] [output_csv]
    ex: C:\Python35\python.exe C:\Users\renchengw\Dropbox\Copy\data\sec_edgar\zhangyintai\key_words_search\section_title_count1\readability.py E:\sec_test\output\extract.csv E:\sec_text\output\output.csv
    
    Note: The output of extract.py should be the input of the readability.py