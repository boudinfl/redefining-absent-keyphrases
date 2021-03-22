# Redefining Absent Keyphrases and their Effect on Retrieval Effectiveness

This repository contains the code for reproducing the experiments from the paper:

 - **Redefining Absent Keyphrases and their Effect on Retrieval Effectiveness.**
   Florian Boudin, Ygor Gallina.
   Annual Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT), 2021.

Parts of the code/data were taken from [https://github.com/boudinfl/ir-using-kg](https://github.com/boudinfl/ir-using-kg).

## Outline

* [Data](#data)
* [Installing anserini](#installing-anserini)

## Data

```
├── data
    ├── ntcir-2
        ├── docs
            ├── 
        ├── qrels
            ├── rel1_ntc2-e2_0101-0149 // judgments for relevant documents 
        ├── topics
            ├── topic-e0101-0149.title+desc+narr.trec // English topics for NTCIR-2
    ├── acm-ir-30
        ├── docs
            ├── 
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
