# Exam Parser Usage
This repo contains an exam parser for ASTR 150. Students will upload PDFs to Canvas created from a Google Doc template (direct them to [this google doc template](https://docs.google.com/document/d/16sFO9A9mKuK1A1YiLu8jwJaOwnI8aZpMqAZsAn7EYTI/edit?usp=sharing)) and this parser will split them into separate questions after they've been checked for plagiarism on Canvas. Here's how you do it

1. Download PDFs from students on Canvas
2. Put PDFs in `exam_submissions` folder
3. Run `python exam_parser.py`
    - You may also need to install pymupdf with `python -m pip install --upgrade pymupdf`
4. Find split exams in the `split_exams` folder
5. ...
6. Profit?
