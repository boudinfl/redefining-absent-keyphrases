#!/usr/bin/env bash

echo 'Converting documents to TREC format'

mkdir -p data/acm-cr/collections

# Create collection for Title+Abstract
mkdir -p data/acm-cr/collections/acm-cr-t+a/
if [[ ! -f "data/acm-cr/collections/acm-cr-t+a/acm-cr-t+a.gz" ]]
then
  cp data/acm-cr/docs/acm-102k.trec.gz data/acm-cr/collections/acm-cr-t+a/acm-102k.trec.gz
  gzip -d data/acm-cr/collections/acm-cr-t+a/acm-102k.trec.gz
  grep -v '^<HEAD>' data/acm-cr/collections/acm-cr-t+a/acm-102k.trec > data/acm-cr/collections/acm-cr-t+a/acm-cr-t+a
  rm -f data/acm-cr/collections/acm-cr-t+a/acm-102k.trec
  gzip -9 data/acm-cr/collections/acm-cr-t+a/acm-cr-t+a
fi

# Create collection for Title+Abstract + all keyphrases
mkdir -p data/acm-cr/collections/acm-cr-t+a-all/
if [[ ! -f "data/acm-cr/collections/acm-cr-t+a-all/acm-cr-t+a-all.gz" ]]
then
  cp data/acm-cr/docs/acm-102k.trec.gz data/acm-cr/collections/acm-cr-t+a-all/acm-cr-t+a-all.gz
fi

# # Create collections for PRMU keyphrases
if [[ ! -f "data/acm-cr/collections/acm-cr-t+a-mu/acm-cr-t+a-mu.gz" ]]
then
	python3 src/trec_to_prmu.py --input data/acm-cr/collections/acm-cr-t+a-all/acm-cr-t+a-all.gz \
								              --output data/acm-cr/collections/
fi

echo 'Indexing documents using anserini'

for EXP in data/acm-cr/collections/*
do
    if [[ ! -d "data/acm-cr/indexes/lucene-index.${EXP##*/}" ]]
    then
        sh anserini/target/appassembler/bin/IndexCollection \
            -collection TrecCollection \
            -threads 2 \
            -input ${EXP}/ \
            -index data/acm-cr/indexes/lucene-index.${EXP##*/}/ \
            -storePositions -storeDocvectors -storeRaw
    else
        echo "Index for ${EXP##*/} already exists"
    fi
done

echo 'Retrieving documents using anserini'

TOPICFIELD="description"
mkdir -p data/acm-cr/output
for INDEX in data/acm-cr/indexes/*
do
    EXP=${INDEX##*/lucene-index.}
    for MODEL in "bm25" # "qld"
    do
        if [[ ! -f "data/acm-cr/output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics data/acm-cr/topics/acm-cr-30.trec \
               -output data/acm-cr/output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt -${MODEL} \
               -topicfield ${TOPICFIELD}
        fi
        if [[ ! -f "data/acm-cr/output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics data/acm-cr/topics/acm-cr-30.trec \
               -output data/acm-cr/output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt -${MODEL} -rm3 \
               -topicfield ${TOPICFIELD}
        fi
    done
done

echo 'Evaluating retrieval effectiveness'

for RUN in 'acm-cr-t+a' 'acm-cr-t+a-p' 'acm-cr-t+a-r' 'acm-cr-t+a-m' 'acm-cr-t+a-u' 'acm-cr-t+a-rmu' 'acm-cr-t+a-pr' 'acm-cr-t+a-mu' 'acm-cr-t+a-all'
do

    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m recall.10 -q \
                                            data/acm-cr/qrels/acm-cr-30.qrels \
                                            data/acm-cr/output/run.${RUN}.${TOPICFIELD}.bm25.txt > data/acm-cr/output/run.${RUN}.${TOPICFIELD}.bm25.results
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m recall.10 -q \
                                            data/acm-cr/qrels/acm-cr-30.qrels \
                                            data/acm-cr/output/run.${RUN}.${TOPICFIELD}.bm25+rm3.txt > data/acm-cr/output/run.${RUN}.${TOPICFIELD}.bm25+rm3.results
done                                            
    
for RUN in 'acm-cr-t+a' 'acm-cr-t+a-p' 'acm-cr-t+a-r' 'acm-cr-t+a-m' 'acm-cr-t+a-u' 'acm-cr-t+a-rmu' 'acm-cr-t+a-pr' 'acm-cr-t+a-mu' 'acm-cr-t+a-all'
do

    echo -n "${RUN}.bm25  "
    python3 src/ttest.py data/acm-cr/output/run.acm-cr-t+a.description.bm25.results data/acm-cr/output/run.${RUN}.${TOPICFIELD}.bm25.results
done

for RUN in 'acm-cr-t+a' 'acm-cr-t+a-p' 'acm-cr-t+a-r' 'acm-cr-t+a-m' 'acm-cr-t+a-u' 'acm-cr-t+a-rmu' 'acm-cr-t+a-pr' 'acm-cr-t+a-mu' 'acm-cr-t+a-all'
do

    echo -n "${RUN}.bm25+rm3  "
    python3 src/ttest.py data/acm-cr/output/run.acm-cr-t+a.description.bm25+rm3.results data/acm-cr/output/run.${RUN}.${TOPICFIELD}.bm25+rm3.results
done





