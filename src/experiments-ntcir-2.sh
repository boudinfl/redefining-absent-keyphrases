#!/usr/bin/env bash

echo 'Converting documents to TREC format'

# Create collection for Title+Abstract
python3 src/ntcir_to_trec.py --input data/ntcir-2/docs/ \
                             --output data/ntcir-2/collections/ntcir-2-t+a/ntcir-2-t+a.gz


# Create collection for Title+Abstract + all keyphrases
python3 src/ntcir_to_trec.py --input data/ntcir-2/docs/ \
                             --output data/ntcir-2/collections/ntcir-2-t+a-all/ntcir-2-t+a-all.gz \
                             --include_keywords

# # Create collections for PRMU keyphrases
if [[ ! -f "data/ntcir-2/collections/ntcir-2-t+a-mu/ntcir-2-t+a-mu.gz" ]]
then
	python3 src/trec_to_prmu.py --input data/ntcir-2/collections/ntcir-2-t+a-all/ntcir-2-t+a-all.gz \
								--output data/ntcir-2/collections/
fi

echo 'Indexing documents using anserini'

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

echo 'Retrieving documents using anserini'

TOPICFIELD="description"
mkdir -p data/ntcir-2/output
for INDEX in data/ntcir-2/indexes/*
do
    EXP=${INDEX##*/lucene-index.}
    for MODEL in "bm25" # "qld"
    do
        if [[ ! -f "data/ntcir-2/output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics data/ntcir-2/topics/topic-e0101-0149.title+desc+narr.trec \
               -output data/ntcir-2/output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt -${MODEL} \
               -topicfield ${TOPICFIELD}
        fi
        if [[ ! -f "data/ntcir-2/output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics data/ntcir-2/topics/topic-e0101-0149.title+desc+narr.trec \
               -output data/ntcir-2/output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt -${MODEL} -rm3 \
               -topicfield ${TOPICFIELD}
        fi
    done
done

echo 'Evaluating retrieval effectiveness'

for RUN in 'ntcir-2-t+a' 'ntcir-2-t+a-p' 'ntcir-2-t+a-r' 'ntcir-2-t+a-m' 'ntcir-2-t+a-u' 'ntcir-2-t+a-rmu' 'ntcir-2-t+a-pr' 'ntcir-2-t+a-mu' 'ntcir-2-t+a-all'
do

    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m map -q \
                                            data/ntcir-2/qrels/rel1_ntc2-e2_0101-0149.qrels \
                                            data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25.txt > data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25.results
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m map -q \
                                            data/ntcir-2/qrels/rel1_ntc2-e2_0101-0149.qrels \
                                            data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25+rm3.txt > data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25+rm3.results
done                                            
    
for RUN in 'ntcir-2-t+a' 'ntcir-2-t+a-p' 'ntcir-2-t+a-r' 'ntcir-2-t+a-m' 'ntcir-2-t+a-u' 'ntcir-2-t+a-rmu' 'ntcir-2-t+a-pr' 'ntcir-2-t+a-mu' 'ntcir-2-t+a-all'
do

    echo -n "${RUN}.bm25  "
    python3 src/ttest.py data/ntcir-2/output/run.ntcir-2-t+a.description.bm25.results data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25.results
    # python3 src/ttest.py data/ntcir-2/output/run.ntcir-2-t+a-p.description.bm25.results data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25.results
done

for RUN in 'ntcir-2-t+a' 'ntcir-2-t+a-p' 'ntcir-2-t+a-r' 'ntcir-2-t+a-m' 'ntcir-2-t+a-u' 'ntcir-2-t+a-rmu' 'ntcir-2-t+a-pr' 'ntcir-2-t+a-mu' 'ntcir-2-t+a-all'
do

    echo -n "${RUN}.bm25+rm3  "
    python3 src/ttest.py data/ntcir-2/output/run.ntcir-2-t+a.description.bm25+rm3.results data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25+rm3.results
    # python3 src/ttest.py data/ntcir-2/output/run.ntcir-2-t+a-p.description.bm25.results data/ntcir-2/output/run.${RUN}.${TOPICFIELD}.bm25.results
done





