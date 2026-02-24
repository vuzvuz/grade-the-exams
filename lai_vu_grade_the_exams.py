"""
Project: Grade the Exams
Description:
A Python module to parse, grade, and analyze multiple-choice exam results.
Meets all functional and non-functional requirements, utilizing Pandas 
and NumPy for vectorized grading and statistical analysis. Complies 
strictly with PEP 8 and Udacity Style Guide requirements.
"""

import os
import re
from typing import List, Tuple

import pandas as pd
import numpy as np


# Answer key array, formatted to strictly comply with 79-character limit
ANSWER_KEY = np.array([
    "B", "A", "D", "D", "C", "B", "D", "A", "C", "C",
    "D", "B", "A", "B", "A", "C", "B", "D", "A", "C",
    "A", "A", "B", "D", "D"
])


def get_file_name() -> str:
    """Prompt the user for a valid input file name.

    Continuously prompts the user until an existing file is provided.
    Catches FileNotFoundError to satisfy the exception handling requirement.

    Returns:
        str: The valid filename entered by the user.
    """
    while True:
        prompt_msg = "Enter a class file to grade (i.e. class1.txt): "
        filename = input(prompt_msg).strip()
        try:
            with open(filename, 'r') as file:
                print(f"Successfully opened {filename}")
                return filename
        except FileNotFoundError:
            print("File cannot be found.")


def parse_and_clean_data(filename: str) -> Tuple[pd.DataFrame, int, int]:
    """Parse raw text, validate format, and return a DataFrame.
    
    Scans line by line to handle dirty data without crashing Pandas.
    Checks for exactly 26 values and valid N# ID formats.

    Args:
        filename: The path to the text file to be read.

    Returns:
        Tuple[pd.DataFrame, int, int]: A tuple containing the DataFrame of 
        valid data, the valid line count, and the invalid line count.
    """
    valid_data = []
    invalid_lines = 0
    valid_lines = 0

    with open(filename, 'r') as file:
        for line in file:
            clean_line = line.strip()
            line_data = clean_line.split(",")

            # Check format 1: Exactly 26 values
            if len(line_data) != 26:
                print(
                    f"Invalid line of data: does not contain exactly "
                    f"26 values:\n{clean_line}"
                )
                invalid_lines += 1
                continue

            # Check format 2: Valid student ID using Regex
            student_id = line_data[0]
            if not re.match(r"^N\d{8}$", student_id):
                print(f"Invalid line of data: N# is invalid\n{clean_line}")
                invalid_lines += 1
                continue

            valid_data.append(line_data)
            valid_lines += 1

    if invalid_lines == 0:
        print("No errors found!")

    # Convert clean list of lists into a Pandas DataFrame
    df = pd.DataFrame(valid_data) if valid_data else pd.DataFrame()
    return df, valid_lines, invalid_lines


def analyze_and_export(
    df: pd.DataFrame, valid_count: int, invalid_count: int, filename: str
) -> None:
    """Grade exams using Pandas vectorization, print stats, and export.

    Args:
        df: DataFrame containing validated student IDs and answers.
        valid_count: Total valid lines processed.
        invalid_count: Total invalid lines skipped.
        filename: Original filename to derive the output filename.
    """
    print("**** REPORT ****")
    print(f"Total valid lines of data: {valid_count}")
    print(f"Total invalid lines of data: {invalid_count}")

    if df.empty:
        return

    # Separate IDs (Column 0) and Answers (Columns 1 to 25)
    student_ids = df.iloc[:, 0]
    answers = df.iloc[:, 1:]

    # Advanced Pandas Vectorization: Compare matrices directly
    is_correct = (answers.values == ANSWER_KEY)
    is_skipped = (answers.values == "")
    is_wrong = ~(is_correct | is_skipped)

    # Calculate scores: +4 for correct, -1 for wrong, 0 for skipped
    # sum(axis=1) computes the sum across rows for each student
    scores = is_correct.sum(axis=1) * 4 - is_wrong.sum(axis=1)

    # Statistical calculations using built-in methods
    mean_score = scores.mean()
    max_score = scores.max()
    min_score = scores.min()
    score_range = max_score - min_score
    median_score = np.median(scores)
    high_score_count = (scores > 80).sum()

    print(f"Mean (average) score: {mean_score:.2f}")
    print(f"Highest score: {max_score}")
    print(f"Lowest score: {min_score}")
    print(f"Range of scores: {score_range}")
    
    # Format median to match expected output perfectly
    if float(median_score).is_integer():
        print(f"Median score: {int(median_score)}")
    else:
        print(f"Median score: {median_score:.1f}")
        
    print(f"Total students with high scores: {high_score_count}")

    # Analyze most skipped questions (sum across columns - axis=0)
    skip_counts = is_skipped.sum(axis=0)
    max_skip = skip_counts.max()
    if max_skip > 0:
        skip_rate = max_skip / valid_count
        skipped_qs = [
            str(i + 1) for i, v in enumerate(skip_counts) if v == max_skip
        ]
        skipped_str = ', '.join(skipped_qs)
        print(
            f"Question that most people skip: "
            f"{skipped_str} - {max_skip} - {skip_rate:.3f}"
        )

    # Analyze most incorrectly answered questions
    wrong_counts = is_wrong.sum(axis=0)
    max_wrong = wrong_counts.max()
    if max_wrong > 0:
        wrong_rate = max_wrong / valid_count
        wrong_qs = [
            str(i + 1) for i, v in enumerate(wrong_counts) if v == max_wrong
        ]
        wrong_str = ', '.join(wrong_qs)
        print(
            f"Question that most people answer incorrectly: "
            f"{wrong_str} - {max_wrong} - {wrong_rate:.3f}"
        )

    # Export results cleanly using Pandas to_csv
    base_name = os.path.splitext(filename)[0]
    out_filename = f"{base_name}_grades.txt"
    
    result_df = pd.DataFrame({'ID': student_ids, 'Score': scores})
    try:
        result_df.to_csv(out_filename, index=False, header=False, sep=',')
    except IOError as e:
        print(f"Error writing to output file: {e}")


def main() -> None:
    """Main execution block coordinating the entire grading workflow."""
    filename = get_file_name()
    print("**** ANALYZING ****")
    df, valid_lines, invalid_lines = parse_and_clean_data(filename)
    analyze_and_export(df, valid_lines, invalid_lines, filename)


if __name__ == "__main__":

    main()
    
