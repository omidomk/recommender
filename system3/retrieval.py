"""
Retrieval
=========

Console application for general-purpose retrieval.

Usage
-----

::

  python -m nordlys.services.er -c <config_file> -q <query>

If `-q <query>` is passed, it returns the results for the specified query and prints them in terminal.


Config parameters
------------------

- **index_name**: name of the index,
- **first_pass**:
      - **1st_num_docs**: number of documents in first-pass scoring (default: 100)
      - **field**: field used in first pass retrieval (default: Elastic.FIELD_CATCHALL)
      - **fields_return**: comma-separated list of fields to return for each hit (default: "")
- **num_docs**: number of documents to return (default: 100)
- **start**: starting offset for ranked documents (default:0)
- **model**: name of retrieval model; accepted values: [lm, mlm, prms] (default: lm)
- **field**: field name for LM (default: catchall)
- **fields**: single field name for LM (default: catchall)
              list of fields for PRMS (default: [catchall])
              dictionary with fields and corresponding weights for MLM (default: {catchall: 1})
- **smoothing_method**: accepted values: [jm, dirichlet] (default: dirichlet)
- **smoothing_param**: value of lambda or mu; accepted values: [float or "avg_len"], (jm default: 0.1, dirichlet default: 2000)
- **query_file**: name of query file (JSON),
- **output_file**: name of output file,
- **run_id**: run id for TREC output


Example config
---------------

.. code:: python

	{"index_name": "dbpedia_2015_10",
	  "first_pass": {
	    "1st_num_docs": 1000
	  },
	  "model": "prms",
	  "num_docs": 1000,
	  "smoothing_method": "dirichlet",
	  "smoothing_param": 2000,
	  "fields": ["names", "categories", "attributes", "similar_entity_names", "related_entity_names"],
	  "query_file": "path/to/queries.json",
	  "output_file": "path/to/output.txt",
	  "run_id": "test"
	}
------------------------

:Authors: Krisztian Balog, Faegheh Hasibi
"""
import argparse
import json
import sys

import time
from pprint import pprint

from elastic import Elastic
from elastic_cache import ElasticCache
from scorer import Scorer, ScorerLM
from file_utils import FileUtils
from config import PLOGGER


class Retrieval(object):
    FIELDED_MODELS = {"mlm", "prms"}
    LM_MODELS = {"lm", "mlm", "prms"}
    finalresults = {}
    def __init__(self, config):
        self.check_config(config)
        self.__config = config
        self.__index_name = config["index_name"]
        self.__first_pass_num_docs = int(config["first_pass"]["1st_num_docs"])
        self.__first_pass_field = config["first_pass"]["field"]
        self.__first_pass_fields_return = config["first_pass"]["fields_return"]
        self.__first_pass_model = config["first_pass"]["model"]
        self.__start = int(config["start"])
        self.__model = config.get("model", None)
        self.__num_docs = int(config.get("num_docs", None))
        self.__query_file = config.get("query_file", None)
        self.__output_file = config.get("output_file", None)
        self.__run_id = config.get("run_id", self.__model)

        self.__elastic = ElasticCache(self.__index_name)

    @staticmethod
    def check_config(config):
        """Checks config parameters and sets default values."""
        try:
            if config.get("index_name", None) is None:
                raise Exception("index_name is missing")

            # Checks first pass parameters
            if config.get("first_pass", None) is None:
                config["first_pass"] = {}
            if config["first_pass"].get("1st_num_docs", None) is None:
                config["first_pass"]["1st_num_docs"] = 1000
            if config["first_pass"].get("field", None) is None:
                config["first_pass"]["field"] = Elastic.FIELD_CATCHALL
            if config["first_pass"].get("fields_return", None) is None:
                config["first_pass"]["fields_return"] = ""
            if config["first_pass"].get("model", None) is None:
                config["first_pass"]["model"] = Elastic.BM25

            if config.get("start", None) is None:
                config["start"] = 0
            if config.get("num_docs", None) is None:
                config["num_docs"] = 100

            if config.get("model", None) in Retrieval.LM_MODELS:
                if config.get("smoothing_method", None) is None:
                    config["smoothing_method"] = ScorerLM.DIRICHLET
                if config.get("smoothing_param", None) is None:
                    if config["smoothing_method"] == ScorerLM.DIRICHLET:
                        config["smoothing_param"] = 2000
                    elif config["smoothing_method"] == ScorerLM.JM:
                        config["smoothing_param"] = 0.1
                    else:
                        raise Exception("Smoothing method is not supported.")

            if config.get("model", None) == "lm":
                if config.get("fields", None) is None:
                    config["fields"] = Elastic.FIELD_CATCHALL
            if config.get("model", None) == "mlm":
                if config.get("fields", None) is None:
                    config["fields"] = {"similar_entity_names": 0.2, "catchall": 0.8}
            if config.get("model", None) == "prms":
                if config.get("fields", None) is None:
                    config["fields"] = [Elastic.FIELD_CATCHALL]
        except Exception as e:
            PLOGGER.error("Error in config file: ", e)
            sys.exit(1)

    def __get_fields(self):
        """Returns the name of all fields that will be used in the retrieval model."""
        fields = []
        if type(self.__config["fields"]) == str:
            fields.append(self.__config["fields"])
        elif type(self.__config["fields"]) == dict:
            fields = self.__config["fields"].keys()
        else:
            fields = self.__config["fields"]
        return fields


    def _first_pass_scoring(self, analyzed_query):
        """Returns first-pass scoring of documents.

        :param analyzed_query: analyzed query
        :return: RetrievalResults object
        """
        PLOGGER.debug("\tFirst pass scoring... ", )
        res1 = self.__elastic.search(analyzed_query, self.__first_pass_field, num=self.__first_pass_num_docs,
                                     fields_return=self.__first_pass_fields_return)
        return res1

    def _second_pass_scoring(self, res1, scorer):
        """Returns second-pass scoring of documents.

        :param res1: first pass results
        :param scorer: scorer object
        :return: RetrievalResults object
        """
        PLOGGER.debug("\tSecond pass scoring... ", )
        for field in self.__get_fields():
            self.__elastic.multi_termvector(list(res1.keys()), field)

        res2 = {}
        for doc_id in res1.keys():
            res2[doc_id] = {"score": scorer.score_doc(doc_id), "fields": res1[doc_id].get("fields", {})}
        PLOGGER.debug("done")
        return res2

    def retrieve(self, query, scorer=None):
        """Scores documents for the given query."""
        query = self.__elastic.analyze_query(query)

        # 1st pass retrieval
        res1 = self._first_pass_scoring(query)
        if self.__model == "bm25":
            return res1

        # 2nd pass retrieval
        scorer = scorer if scorer else Scorer.get_scorer(self.__elastic, query, self.__config)
        res2 = self._second_pass_scoring(res1, scorer)
        return res2

    def batch_retrieval(self):
        """Scores queries in a batch and outputs results."""
        queries = json.load(open(self.__query_file))

        # init output file
        open(self.__output_file, "w").write("")
        out = open(self.__output_file, "w")

          # type: Any
        #finalresults["recommendations"][userid].append({"article_id": doc_id, "score": str(score["score"])})



        # retrieves documents
        for query_id in sorted(queries):
            PLOGGER.info("scoring [" + query_id + "] " + queries[query_id])
            results = self.retrieve(queries[query_id])
            out.write(self.trec_format(results, query_id, self.__num_docs))

        out.write(self.arxivdigest_format((results), query_id, self.__num_docs))
        out.close()
        PLOGGER.info("Output file:" + self.__output_file)



    def arxivdigest_format(self, results, query_id, max_rank=100):
        """Outputs results in TREC format"""

        rank = 1
        arr=[]

        for doc_id, score in sorted(results.items(), key=lambda x: x[1]["score"], reverse=True):
            if rank > max_rank:
                break

            arr.append({"article_id": doc_id, "score": str(score["score"])})
            rank += 1
        Retrieval.finalresults.update(recommendations={query_id: arr})
        return str(Retrieval.finalresults)

    def trec_format(self, results, query_id, max_rank=100):
        """Outputs results in TREC format"""
        out_str = ""
        rank = 1
        for doc_id, score in sorted(results.items(), key=lambda x: x[1]["score"], reverse=True):
            if rank > max_rank:
                break
            out_str += query_id + "\tQ0\t" + doc_id + "\t" + str(rank) + "\t" + str(score["score"]) + "\t" + self.__run_id + "\n"
            rank += 1
        return out_str


def arg_parser():
    parser = argparse.ArgumentParser()
    ####parser.add_argument("config", help="config file", type=str)
    args = parser.parse_args()
    return args


def get_config():
    example_config = {"index_name": "arxiv",
                      "query_file": "queries.json",
                      "first_pass": {
                          "num_docs": 10,
                          "field": "content",
                          # "model": "LMJelinekMercer",
                          # "model_params": {"lambda": 0.1}
                      },
                      "fields": "content",
                      "model": "lm",
                      "smoothing_method": "jm",
                      "smoothing_param": 0.1,
                      "output_file": "output/test_retrieval.txt"
                      }
    return example_config


def main(args):
    s_t = time.time()  # start time

    #config = FileUtils.load_config(args.config) if args.config != "" else get_config()
    config = get_config()
    r = Retrieval(config)
    r.batch_retrieval()

    e_t = time.time()  # end time
    print("Execution time(min):\t" + str((e_t - s_t) / 60) + "\n")
    return r.finalresults

if __name__ == "__main__":
    main(arg_parser())
