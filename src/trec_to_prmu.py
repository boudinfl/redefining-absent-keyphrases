# -*- coding: utf-8 -*-

"""Extract PRMU keyphrases from TREC formatted files."""

import os
import re
import gzip
import argparse
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tqdm import tqdm

def average(lst):
    return sum(lst) / len(lst)

def extract_content(tagged_line, tag):
    """Extract content from SGML line."""
    return tagged_line.replace("<"+tag+">", "").replace("</"+tag+">","")

def tokenize(s):
    """Tokenize an input text."""
    return word_tokenize(s)

def lowercase_and_stem(_words):
    """lowercase and stem sequence of words."""
    return [PorterStemmer().stem(w.lower()) for w in _words]

def contains(subseq, inseq):
    return any(inseq[pos:pos + len(subseq)] == subseq for pos in range(0, len(inseq) - len(subseq) + 1))

def flatten_list(a):
    return [item for sublist in a for item in sublist]

def pmru_uw(tok_title, tok_text, tok_kps):
    """Distribute keyphrases within PMRU categories."""
    p, r, m, u = [], [], [], []
    absent_words = set()
    
    # loop through the keyphrases
    for j, kp in enumerate(tok_kps):

        # if kp is present
        if contains(kp, tok_title) or contains(kp, tok_text):
            p.append(j)

        # if kp is considered as absent
        else:

            # find present and absent words
            present_words = [w for w in kp if w in tok_title or w in tok_text]
            absent_words.update([w for w in kp if w not in tok_title and w not in tok_text])

            # if "all" words are present
            if len(present_words) == len(kp):
                r.append(j)

            # if "some" words are present
            elif len(present_words) > 0:
                m.append(j)
            # if "no" words are present
            else:
                u.append(j)

    uw = len(absent_words) / len(set(flatten_list(tok_kps)))
    return p, r, m, u, uw


# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input file in TREC format.",
                    type=str)

parser.add_argument("--output",
                    help="output file.",
                    type=str)

args = parser.parse_args()

# initialize containers
collection = defaultdict(list)
all_keyphrases = defaultdict(list)
present = defaultdict(list)
reordered = defaultdict(list)
mixed = defaultdict(list)
unseen = defaultdict(list)
uw = defaultdict(list)

# looping through the files
with gzip.open(args.input, 'rt') as f:

    doc_id = None
    title = None
    text = None
    keyphrases = None
    is_in_document = False

    nb_lines = sum(True for _ in f)
    f.seek(0)
    for i, line in enumerate(tqdm(f, total=nb_lines)):
    # for i, line in enumerate(f):
        line = line.strip()

        if line.startswith('<DOC>'):
            is_in_document = True

        elif line.startswith('<DOCNO>'):
            doc_id = extract_content(line, "DOCNO")
            collection[doc_id].append(line)

        elif line.startswith('<TITLE>'):
            title = extract_content(line, "TITLE")
            collection[doc_id].append(line) 

        elif line.startswith('<TEXT>'):
            text = extract_content(line, "TEXT")
            collection[doc_id].append(line)

        elif line.startswith('<HEAD>'):
            keyphrases = extract_content(line, "HEAD")
            keyphrases = [k.strip() for k in keyphrases.split("//")]

        elif line.startswith('</DOC>'):

            # if document has keyphrases
            if keyphrases:
                pp_title = lowercase_and_stem(tokenize(title))
                pp_text = lowercase_and_stem(tokenize(text))

                pp_keyphrases = [lowercase_and_stem(tokenize(k)) for k in keyphrases]
                all_keyphrases[doc_id] = keyphrases

                # get PRMU keyphrases from document
                present[doc_id], reordered[doc_id], mixed[doc_id], unseen[doc_id], uw[doc_id] = pmru_uw(pp_title, pp_text, pp_keyphrases)
                

            doc_id = None
            title = None
            text = None
            keyphrases = None
            is_in_document = False

            # if len(uw) > 1000:
            #     break

        elif is_in_document:
            print("parse error at line {}".format(str(i)))
            exit(0)

# # write the output collections
# output_filename = args.input.split('/')[-1].replace("all.gz", '')

# # P // creating output path if it does not exist
# output_file = args.output+'/'+output_filename+'p/'+output_filename+'p.gz'
# if not os.path.isdir(args.output+'/'+output_filename+'p/'):
#     os.makedirs(args.output+'/'+output_filename+'p/', exist_ok=True)

# with gzip.open(output_file, 'wt') as o:
#     for doc_id in collection:
#         o.write("<DOC>\n")
#         o.write("\n".join(collection[doc_id])+"\n")
#         if len(present[doc_id]):
#             o.write("<HEAD>{}</HEAD>\n".format(" // ".join([all_keyphrases[doc_id][j] for j in present[doc_id]])))
#         o.write("</DOC>\n\n")

# # R // creating output path if it does not exist
# output_file = args.output+'/'+output_filename+'r/'+output_filename+'r.gz'
# if not os.path.isdir(args.output+'/'+output_filename+'r/'):
#     os.makedirs(args.output+'/'+output_filename+'r/', exist_ok=True)

# with gzip.open(output_file, 'wt') as o:
#     for doc_id in collection:
#         o.write("<DOC>\n")
#         o.write("\n".join(collection[doc_id])+"\n")
#         if len(reordered[doc_id]):
#             o.write("<HEAD>{}</HEAD>\n".format(" // ".join([all_keyphrases[doc_id][j] for j in reordered[doc_id]])))
#         o.write("</DOC>\n\n")

# # M // creating output path if it does not exist
# output_file = args.output+'/'+output_filename+'m/'+output_filename+'m.gz'
# if not os.path.isdir(args.output+'/'+output_filename+'m/'):
#     os.makedirs(args.output+'/'+output_filename+'m/', exist_ok=True)

# with gzip.open(output_file, 'wt') as o:
#     for doc_id in collection:
#         o.write("<DOC>\n")
#         o.write("\n".join(collection[doc_id])+"\n")
#         if len(mixed[doc_id]):
#             o.write("<HEAD>{}</HEAD>\n".format(" // ".join([all_keyphrases[doc_id][j] for j in mixed[doc_id]])))
#         o.write("</DOC>\n\n")

# # u // creating output path if it does not exist
# output_file = args.output+'/'+output_filename+'u/'+output_filename+'u.gz'
# if not os.path.isdir(args.output+'/'+output_filename+'u/'):
#     os.makedirs(args.output+'/'+output_filename+'u/', exist_ok=True)

# with gzip.open(output_file, 'wt') as o:
#     for doc_id in collection:
#         o.write("<DOC>\n")
#         o.write("\n".join(collection[doc_id])+"\n")
#         if len(unseen[doc_id]):
#             o.write("<HEAD>{}</HEAD>\n".format(" // ".join([all_keyphrases[doc_id][j] for j in unseen[doc_id]])))
#         o.write("</DOC>\n\n")

# # absent RMU // creating output path if it does not exist
# output_file = args.output+'/'+output_filename+'rmu/'+output_filename+'rmu.gz'
# if not os.path.isdir(args.output+'/'+output_filename+'rmu/'):
#     os.makedirs(args.output+'/'+output_filename+'rmu/', exist_ok=True)

# with gzip.open(output_file, 'wt') as o:
#     for doc_id in collection:
#         o.write("<DOC>\n")
#         o.write("\n".join(collection[doc_id])+"\n")
#         rmu = flatten_list([reordered[doc_id], mixed[doc_id], unseen[doc_id]])
#         if len(rmu):
#             o.write("<HEAD>{}</HEAD>\n".format(" // ".join([all_keyphrases[doc_id][j] for j in rmu])))
#         o.write("</DOC>\n\n")

# # highlight PR // creating output path if it does not exist
# output_file = args.output+'/'+output_filename+'pr/'+output_filename+'pr.gz'
# if not os.path.isdir(args.output+'/'+output_filename+'pr/'):
#     os.makedirs(args.output+'/'+output_filename+'pr/', exist_ok=True)

# with gzip.open(output_file, 'wt') as o:
#     for doc_id in collection:
#         o.write("<DOC>\n")
#         o.write("\n".join(collection[doc_id])+"\n")
#         pr = flatten_list([present[doc_id], reordered[doc_id]])
#         if len(pr):
#             o.write("<HEAD>{}</HEAD>\n".format(" // ".join([all_keyphrases[doc_id][j] for j in pr])))
#         o.write("</DOC>\n\n")

# # Expand MU // creating output path if it does not exist
# output_file = args.output+'/'+output_filename+'mu/'+output_filename+'mu.gz'
# if not os.path.isdir(args.output+'/'+output_filename+'mu/'):
#     os.makedirs(args.output+'/'+output_filename+'mu/', exist_ok=True)

# with gzip.open(output_file, 'wt') as o:
#     for doc_id in collection:
#         o.write("<DOC>\n")
#         o.write("\n".join(collection[doc_id])+"\n")
#         mu = flatten_list([mixed[doc_id], unseen[doc_id]])
#         if len(mu):
#             o.write("<HEAD>{}</HEAD>\n".format(" // ".join([all_keyphrases[doc_id][j] for j in mu])))
#         o.write("</DOC>\n\n")

# Compute some statistics
p, r, m, u = [], [], [], []
nb_docs_with_kps = len(all_keyphrases)

for doc_id in all_keyphrases:
    p.append(len(present[doc_id])/len(all_keyphrases[doc_id]))
    r.append(len(reordered[doc_id])/len(all_keyphrases[doc_id]))
    m.append(len(mixed[doc_id])/len(all_keyphrases[doc_id]))
    u.append(len(unseen[doc_id])/len(all_keyphrases[doc_id]))

print("%P:{:.1f} %R:{:.1f} %M:{:.1f} %U:{:.1f} %uw:{:.1f}".format(sum(p)/nb_docs_with_kps*100, sum(r)/nb_docs_with_kps*100, sum(m)/nb_docs_with_kps*100, sum(u)/nb_docs_with_kps*100, sum(uw.values())/nb_docs_with_kps*100))








