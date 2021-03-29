#!/usr/bin/env bash

echo 'Converting documents to TREC format'

# Create collection for Title+Abstract
python3 src/ntcir_to_trec.py --input data/ntcir-2/docs/ \
                             --output data/ntcir-2/collections/ntcir-2-t+a/ntcir-2-t+a.gz


# Create collection for Title+Abstract + all keyphrases
python3 src/ntcir_to_trec.py --input data/ntcir-2/docs/ \
                             --output data/ntcir-2/collections/ntcir-2-t+a-all/ntcir-2-t+a-all.gz \
                             --include_keywords

# Create collections for PRMU keyphrases
python3 src/trec_to_prmu.py --input data/ntcir-2/collections/ntcir-2-t+a-all/ntcir-2-t+a-all.gz \
							--output data/ntcir-2/collections/