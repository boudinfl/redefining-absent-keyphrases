#!/usr/bin/env bash
TOPICFIELD="description"
mkdir -p output
for INDEX in data/indexes/*
do
    EXP=${INDEX##*/lucene-index.}
    for MODEL in "bm25" # "qld"
    do
        if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics data/topics/topic-e0101-0149.title+desc+narr.trec \
               -output output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt -${MODEL} \
               -topicfield ${TOPICFIELD}
        fi

    done
done