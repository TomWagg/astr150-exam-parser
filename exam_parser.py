import re
import argparse
import os

# this one handles pdf to text conversion (python -m pip install --upgrade pymupdf)
import fitz

def main():
    """ main function to just handle command line arguments """
    parser = argparse.ArgumentParser(description='Process student exam submissions')
    parser.add_argument('-i', '--input_path', default="exam_submissions/", type=str,
                        help='Path to folder containing student submissions')
    parser.add_argument('-o', '--output_path', default="split_exams/", type=str,
                        help='Path to folder in which to put output')

    args = parser.parse_args()

    # ensure the given paths are valid
    if not os.path.isdir(args.input_path):
        raise ValueError("No folder exists at the given input path")
    if not os.path.isdir(args.output_path):
        raise ValueError("No folder exists at the given output path")

    # perform the split
    split_student_submissions(args.input_path, args.output_path)

def split_student_submissions(input_path, output_path):
    """Split every student exam in the input path into separate question files

    Parameters
    ----------
    input_path : `str`
        Path to a folder that contains all of the student exam submissions
    output_path : `str`
        Path to a folder in which to place the split up exams
    """
    # first loop over every file in the input path
    students = []
    for file in os.listdir(input_path):
        # assume every text file is an exam submission
        if file.endswith(".pdf"):
            # split it and store the information
            name, answers = read_student_submission(input_path + file)
            students.append({
                "name": name,
                "answers": answers,
                "file": file
            })

    # now loop over all of the students
    for student in students:
        # and for each answer in the exam
        for i, answer in enumerate(student["answers"]):
            # create a new file and write their name and answers
            file_name = output_path + "q{}_".format(i + 1) + student["file"].replace(".pdf", ".txt")
            with open(file_name, "w") as split_file:
                split_file.write(student["name"] + "\n---\n\n")
                split_file.write(answer)

def read_student_submission(file_path):
    """Split up a student exam submission

    Parameters
    ----------
    file_path : str
        Path to the student exam file

    Returns
    -------
    name : `str`
        Student name
    answers : `list`
        List of student answers for each question
    """
    # read the file into text
    file_str = convert_pdf_to_txt(file_path)

    # split the file on the Answer string
    answers = re.split(r"=* Answer [0-9]* =*", file_str)
    # strip off any leading or trailing newlines
    answers = [answer.strip() for answer in answers]

    # split into name and answers
    name, answers = answers[0], answers[1:]
    # strip off the start so you just have the name
    name = name.split("Full name:")[1].strip()

    return name, answers


def convert_pdf_to_txt(file_path):
    """Read a PDF into a text string

    Parameters
    ----------
    file_path : `str`
        Path to the pdf file

    Returns
    -------
    text : `str`
        String containing the text in the PDF
    """
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text


if __name__ == "__main__":
    main()
