# -*- coding: utf-8 -*-

"""Convert NTCIR formatted files to TREC format."""

import re
import os
import sys
import html
import glob
import json
import gzip
import argparse

from tqdm import tqdm
from bs4 import BeautifulSoup


def punctuation_mark_cleanser(s):
    """Add spacing in muddled sentences."""
    s = re.sub(r'([A-Za-z])([\.\?\!\(\)])([A-Za-z\(\)])', r'\g<1>\g<2> \g<3>', s)
    return s


# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input directory containing files in NTCIR format.",
                    type=str)

parser.add_argument("--output",
                    help="output directory in TREC format.",
                    type=str)

parser.add_argument('--include_keywords',
                    action='store_true',
                    help='keep the author keywords.')

args = parser.parse_args()

# creating output path if it does not exist
output_dir = os.path.split(args.output)[0]
if not os.path.isdir(output_dir) and output_dir:
    os.makedirs(output_dir, exist_ok=True)

# skip if file already exists
if os.path.isfile(args.output):
    print("file {} already exists - stopping now".format(args.output))
    sys.exit(0)

tag = lambda tag_name, content: "<{}>{}</{}>\n".format(tag_name, html.escape(content.strip()), tag_name)


for filename in glob.iglob(args.input+"/**", recursive=True):

    if os.path.isfile(filename):
        print('loading documents from {}'.format(filename))

        # looping through the files
        with gzip.open(filename, 'rt') as f:
            is_in_document = False
            doc_id = None
            nb_lines = sum(True for _ in f)
            f.seek(0)
            with gzip.open(args.output, 'at') as o:
                for i, line in enumerate(tqdm(f, total=nb_lines)):
                    if line.startswith('<REC>'):
                        is_in_document = True
                        o.write("<DOC>\n")

                    # document identifier
                    elif line.startswith('<ACCN'):
                        doc_id = BeautifulSoup(line.strip(), 'html.parser').text
                        o.write(tag('DOCNO', doc_id))

                    # title
                    elif line.startswith('<TITE') or line.startswith('<PJNE'):
                        title = BeautifulSoup(line.strip(), 'html.parser').text
                        o.write(tag('TITLE', title))

                    # abstract
                    elif line.startswith('<ABSE'):
                        abstract = BeautifulSoup(line.strip(), 'html.parser').text
                        abstract = punctuation_mark_cleanser(abstract)
                        o.write(tag('TEXT', abstract))

                    # keywords
                    elif args.include_keywords and line.startswith('<KYWE'):
                        keywords = BeautifulSoup(line.strip(), 'html.parser').text
                        keywords = [kp.strip() for kp in keywords.split('//')]
                        # special case of " , " separator
                        if len(keywords) < 2:
                            if "," in keywords[0]:
                                keywords = keywords[0].split(",")
                            if ' / ' in keywords[0]:
                                keywords = keywords[0].split(" / ")
                            if ' ; ' in keywords[0]:
                                keywords = keywords[0].split(" ; ")

                        # keywords = re.sub('\s+', " ", keywords.replace("//", " "))
                        o.write(tag('HEAD', ' // '.join(keywords)))

                    elif line.startswith('</REC>'):
                        if not is_in_document:
                            print("ERROR, document no valid at line {}".format(i))
                        o.write("</DOC>\n\n")
                        is_in_document = False
                        doc_id = None

