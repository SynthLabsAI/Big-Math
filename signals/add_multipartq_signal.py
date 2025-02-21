from datasets import load_dataset
import multiprocessing as mp
import re

# load the utilities to add a new signal to the master dataset
from utils import DATASET_PATH

def has_multi_part_q(row):
    lower_problem = row['problem'].lower()
    pattern1 = r'\([IⅠ\s,\.]\).*\([IⅡ\s,\.]\)' # Roman numerals
    pattern2 = r'\([1-9][^\)]*\).*\([1-9][^\)]*\)' # Numbered parts in parentheses
    pattern3 = r'(?:\d+\.).*(?:\d+\.)' # Numbered parts with period
    pattern4 = r'\(I+\).*\(I+\)' # Traditional Roman numerals
    pattern5 = r'(?:(?:^|\s)(?:1[.\)]|[Ii][.\)]|①).*(?:\s|$)(?:2[.\)]|[Ii]{2}[.\)]|②))' # Mixed types

    # try the patterns in order
    if re.search(pattern1, lower_problem):
        row['is_multi_part_q_regex'] = True
    elif re.search(pattern2, lower_problem):
        row['is_multi_part_q_regex'] = True
    elif re.search(pattern3, lower_problem):
        row['is_multi_part_q_regex'] = True
    elif re.search(pattern4, lower_problem):
        row['is_multi_part_q_regex'] = True
    elif re.search(pattern5, lower_problem):
        row['is_multi_part_q_regex'] = True
    else:
        row['is_multi_part_q_regex'] = False
    
    return row

def main():

    # load the dataset
    dataset = load_dataset(DATASET_PATH, split="train")

    # run multi-part question detection over the full dataset
    dataset = dataset.map(has_multi_part_q, num_proc=mp.cpu_count())

    # push the updated dataset
    dataset.push_to_hub(DATASET_PATH)


if __name__ == "__main__":
    main()