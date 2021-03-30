# Redefining Absent Keyphrases and their Effect on Retrieval Effectiveness

This repository contains the code for reproducing the experiments from the paper:

 - **Redefining Absent Keyphrases and their Effect on Retrieval Effectiveness.**
   Florian Boudin, Ygor Gallina.
   Annual Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT), 2021.

The **ACM-CR-30 test collection** introduced as new benchmark dataset for scientific document retrieval through the task of 
context-aware citation recommendation is available as direct download [here](data/acm-cr/acm-cr.v1.tar.gz).

## Outline

* [Data](#data)
* [Installing anserini](#installing-anserini)
* [Replication Guides](#replication-guides)
  * [NTCIR-2](#ntcir-2)
  * [ACM-CR-30](#acm-cr-30)

## Data

```
├── data
    ├── ntcir-2
        ├── docs
            ├── ntc1.e1.gz  // NTCIR-1 (#187,080) collection converted with ACCN-e.pl 
            ├── ntc2-e1g.gz // NTCIR-2 (#77,433) NACSIS Academic Conference Papers Database
            ├── ntc2-e1k.gz // NTCIR-2 (#57,545) NACSIS Grant-in-Aid Scientific Research Database
        ├── qrels
            ├── rel1_ntc2-e2_0101-0149.qrels // judgments for relevant documents 
        ├── topics
            ├── topic-e0101-0149.title+desc+narr.trec // English topics for NTCIR-2
    ├── acm-cr-30
        ├── docs
            ├── acm-102k.trec.gz // ACM bibliographic records (title/abstract/keywords) 
        ├── qrels
            ├── acm-cr-30.qrels // judgments for relevant documents (cited documents)
        ├── topics
            ├── acm-cr-30.topics // manually extracted citation contexts
```

## Installing anserini

Here, we use the open-source information retrieval toolkit 
[anserini](http://anserini.io/) which is built on 
[Lucene](https://lucene.apache.org/).
Below are the installation steps for a mac computer (tested on OSX 10.14) based
on their [colab demo](https://colab.research.google.com/drive/1s44ylhEkXDzqNgkJSyXDYetGIxO9TWZn).

```bash
# install maven
brew cask install adoptopenjdk
brew install maven

# cloning / installing anserini
git clone https://github.com/castorini/anserini.git --recurse-submodules
cd anserini/
# for 10.14 issues -> changing jacoco from 0.8.2 to 0.8.3 in pom.xml to build correctly
# for 10.13 issues -> https://github.com/castorini/anserini/issues/648
mvn clean package appassembler:assemble

# compile evaluation tools and other scripts
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
```

## Replication Guides

### NTCIR-2

```
sh src/experiments-ntcir-2.sh

%P:61.9 %R:8.1 %M:16.5 %U:13.5 %uw:21.4

ntcir-2-t+a.bm25  all: 0.2955 (sign@.05: False, pvalue: nan)
ntcir-2-t+a-p.bm25  all: 0.3074 (sign@.05: True, pvalue: 0.0018)
ntcir-2-t+a-r.bm25  all: 0.2979 (sign@.05: False, pvalue: 0.3931)
ntcir-2-t+a-m.bm25  all: 0.3080 (sign@.05: True, pvalue: 0.0071)
ntcir-2-t+a-u.bm25  all: 0.2967 (sign@.05: False, pvalue: 0.7024)
ntcir-2-t+a-rmu.bm25  all: 0.3077 (sign@.05: True, pvalue: 0.0398)
ntcir-2-t+a-pr.bm25  all: 0.3064 (sign@.05: True, pvalue: 0.0077)
ntcir-2-t+a-mu.bm25  all: 0.3083 (sign@.05: True, pvalue: 0.0161)
ntcir-2-t+a-all.bm25  all: 0.3192 (sign@.05: True, pvalue: 0.0002)

ntcir-2-t+a.bm25+rm3  all: 0.3283 (sign@.05: False, pvalue: nan)
ntcir-2-t+a-p.bm25+rm3  all: 0.3347 (sign@.05: False, pvalue: 0.1840)
ntcir-2-t+a-r.bm25+rm3  all: 0.3348 (sign@.05: False, pvalue: 0.1596)
ntcir-2-t+a-m.bm25+rm3  all: 0.3385 (sign@.05: False, pvalue: 0.1498)
ntcir-2-t+a-u.bm25+rm3  all: 0.3394 (sign@.05: False, pvalue: 0.0587)
ntcir-2-t+a-rmu.bm25+rm3  all: 0.3487 (sign@.05: True, pvalue: 0.0217)
ntcir-2-t+a-pr.bm25+rm3  all: 0.3382 (sign@.05: False, pvalue: 0.1244)
ntcir-2-t+a-mu.bm25+rm3  all: 0.3434 (sign@.05: False, pvalue: 0.0754)
ntcir-2-t+a-all.bm25+rm3  all: 0.3548 (sign@.05: True, pvalue: 0.0082)
```

### ACM-CR-30

```
sh src/experiments-acm-cr.sh

%P:53.6 %R:11.7 %M:19.3 %U:15.4 %uw:25.5

acm-cr-t+a.bm25  all: 0.3564 (sign@.05: False, pvalue: nan)
acm-cr-t+a-p.bm25  all: 0.3602 (sign@.05: False, pvalue: 0.4835)
acm-cr-t+a-r.bm25  all: 0.3543 (sign@.05: False, pvalue: 0.1596)
acm-cr-t+a-m.bm25  all: 0.3622 (sign@.05: False, pvalue: 0.4343)
acm-cr-t+a-u.bm25  all: 0.3624 (sign@.05: False, pvalue: 0.3319)
acm-cr-t+a-rmu.bm25  all: 0.3662 (sign@.05: False, pvalue: 0.2251)
acm-cr-t+a-pr.bm25  all: 0.3582 (sign@.05: False, pvalue: 0.7188)
acm-cr-t+a-mu.bm25  all: 0.3721 (sign@.05: False, pvalue: 0.1162)
acm-cr-t+a-all.bm25  all: 0.3665 (sign@.05: False, pvalue: 0.3601)

acm-cr-t+a.bm25+rm3  all: 0.3409 (sign@.05: False, pvalue: nan)
acm-cr-t+a-p.bm25+rm3  all: 0.3409 (sign@.05: False, pvalue: 0.9973)
acm-cr-t+a-r.bm25+rm3  all: 0.3340 (sign@.05: False, pvalue: 0.4647)
acm-cr-t+a-m.bm25+rm3  all: 0.3341 (sign@.05: False, pvalue: 0.5430)
acm-cr-t+a-u.bm25+rm3  all: 0.3378 (sign@.05: False, pvalue: 0.7368)
acm-cr-t+a-rmu.bm25+rm3  all: 0.3410 (sign@.05: False, pvalue: 0.9927)
acm-cr-t+a-pr.bm25+rm3  all: 0.3236 (sign@.05: False, pvalue: 0.1632)
acm-cr-t+a-mu.bm25+rm3  all: 0.3338 (sign@.05: False, pvalue: 0.5429)
acm-cr-t+a-all.bm25+rm3  all: 0.3288 (sign@.05: False, pvalue: 0.3487)

```

