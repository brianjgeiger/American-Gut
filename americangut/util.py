#!/usr/bin/env python

from itertools import izip

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The American Gut Project"
__credits__ = ["Daniel McDonald", "Adam Robbins-Pianka"]
__license__ = "BSD"
__version__ = "unversioned"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

import os

def pick_rarifaction_level(id_, lookups):
    """Determine which lookup has the appropriate key

    id_ is a barcode, e.g., '000001000'
    lookups is a list of tuples, e.g., [('10k',{'000001000':'000001000.123'})]

    The order of the lookups matters. The first lookup found with the key will
    be returned.

    None is returned if the key is not found
    """
    for name, lookup in lookups:
        if id_ in lookup:
            return name
    return None

def parse_mapping_file(open_file):
    """return (header, [(sample_id, all_other_fields)])

    """
    header = open_file.readline().strip()
    res = []

    for l in open_file:
        res.append(l.strip().split('\t',1))

    return (header, res)

def verify_subset(table, mapping):
    """Returns True/False if the table is a subset"""
    ids = set([i[0] for i in mapping])
    t_ids = set(table.SampleIds)

    return t_ids.issubset(ids)

def slice_mapping_file(table, mapping):
    """Returns a new mapping corresponding to just the ids in the table"""
    t_ids = set(table.SampleIds)
    res = []

    for id_, l in mapping:
        if id_ in t_ids:
            res.append('\t'.join([id_, l]))

    return res

def check_file(f, e=IOError):
    """Verify a file (or directory) exists"""
    if not os.path.exists(f):
        raise e("Cannot continue! The file %s does not exist!" % f)

def trim_fasta(input_fasta, output_fasta, length):
    """Trim FASTA sequences to a given length

    input_fasta: should be an open file. Every two lines should compose a
                 complete FASTA record (header, sequence)
    output_fasta: should be an open file ready for writing
    length: what length to trim the sequences to. Sequences shorter than
            length will not be modified.
    """
    # reads the FASTA file two lines at at a time
    # Assumptions: 1) each FASTA record is two lines
    #              2) There are no incomplete FASTA records
    for header, sequence in izip(input_fasta, input_fasta):
        header = header.strip()
        sequence = sequence.strip()[:length]
        output_fasta.write("%s\n%s\n" % (header, sequence))

def concatenate_files(input_files, output_file, read_chunk=10000):
    """Concatenate all input files and produce an output file

    input_fps is a list of open files
    output_fp is an open file ready for writing
    """
    for infile in input_files:
        chunk = infile.read(read_chunk)
        while chunk:
            output_file.write(chunk)
            chunk = infile.read(read_chunk)
