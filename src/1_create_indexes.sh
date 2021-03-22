#!/usr/bin/env bash
for EXP in data/ntcir-2/docs/
do
    if [[ ! -d "data/indexes/lucene-index.${EXP##*/}" ]]
    then
        sh anserini/target/appassembler/bin/IndexCollection \
            -collection TrecCollection \
            -threads 2 \
            -input ${EXP}/ \
            -index data/indexes/lucene-index.ntcir-2/ \
            -storePositions -storeDocvectors -storeRaw
    else
        echo "Index for ${EXP##*/} already exists"
    fi
done