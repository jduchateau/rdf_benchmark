#!/usr/bin/env python
# RDFLib 7+ currently displays an isodate error as warning with negative (BC) dates, which can be ignored.

from sys import argv, stderr
import re
from time import perf_counter
import psutil

from rdflib import Graph, RDF, URIRef


def task_parse():
    filename = argv[2]
    syntax = argv[3] if len(argv) > 3 else "nt"
    process = psutil.Process()
    m0 = process.memory_info().vms
    t0 = perf_counter()
    g = Graph()
    g.parse(filename, format=syntax)
    t1 = perf_counter()
    m1 = process.memory_info().vms
    time_load = t1 - t0
    mem_graph = m1 - m0
    print(f"{time_load},{mem_graph}")


def task_query(query_num=1):
    filename = argv[2]
    syntax = argv[3] if len(argv) > 3 else "nt"
    process = psutil.Process()
    m0 = process.memory_info().vms
    t0 = perf_counter()
    g = Graph()
    g.parse(filename, format=syntax)
    t1 = perf_counter()
    m1 = process.memory_info().vms
    time_load = t1 - t0
    mem_graph = m1 - m0

    patterns = {
        1: (None, RDF.type, URIRef("http://dbpedia.org/ontology/Person")),
        2: (URIRef("http://dbpedia.org/resource/Vincent_Descombes_Sevoie"), None, None),
    }
    pattern = patterns[query_num]
    time_first = None
    c = 1
    t0 = perf_counter()
    for triple in g.triples(pattern):
        if time_first is None:
            time_first = perf_counter() - t0
            t0 = perf_counter()
        c += 1
    time_rest = perf_counter() - t0
    print("matching triples: {}".format(c), file=stderr)

    print(f"{time_load},{mem_graph},{time_first},{time_rest}")


def main():
    if argv[1] == "parse":
        task_parse()
    elif argv[1] == "query":
        task_query()
    elif argv[1] == "query2":
        task_query(2)


if __name__ == "__main__":
    main()
