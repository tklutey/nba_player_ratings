import csv
import os

from definitions import RAW_DATA_DIR

TXT_DATA_FILEPATH = RAW_DATA_DIR + "/txt/"
CSV_DATA_FILEPATH = RAW_DATA_DIR + "/csv/"

def txt_to_csv(txt_filepath, csv_filepath):
    in_txt = csv.reader(open(txt_filepath, "rt"), delimiter='\t')
    out_csv = csv.writer(open(csv_filepath, 'wt'))
    out_csv.writerows(in_txt)

def __get_files_in_directory(directory):
    return os.listdir(directory)

def main():
    txt_files = __get_files_in_directory(TXT_DATA_FILEPATH)
    for txt_filename in txt_files:
        filename = txt_filename.split(".")[0]
        txt_filepath = TXT_DATA_FILEPATH + txt_filename
        csv_filepath = CSV_DATA_FILEPATH + filename + ".csv"
        txt_to_csv(txt_filepath, csv_filepath)

if __name__ == "__main__":
    main()