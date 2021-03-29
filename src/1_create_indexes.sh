#!/usr/bin/env bash
for EXP in data/ntcir-2/collections/*
do
    if [[ ! -d "data/ntcir-2/indexes/lucene-index.${EXP##*/}" ]]
    then
        sh anserini/target/appassembler/bin/IndexCollection \
            -collection TrecCollection \
            -threads 2 \
            -input ${EXP}/ \
            -index data/ntcir-2/indexes/lucene-index.${EXP##*/}/ \
            -storePositions -storeDocvectors -storeRaw
    else
        echo "Index for ${EXP##*/} already exists"
    fi
done