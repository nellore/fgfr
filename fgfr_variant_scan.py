#!/usr/bin/env python
"""
fgfr4_variant_scan.py

Scans a bunch of TCGA variant bigwigs output by Rail-RNA for evidence of 
hg38 chr5:177093734-177093735 G>A in RNA-seq data.

Usage: arg 1 is path to directory on JHPCE (Hopkins cluster) with TCGA variant
bigwigs.

Output: TSV with file uuids and raw coverages of G>A at 
chr5:177093734-177093735 iff any G>A reads are detected.

Requires https://github.com/brentp/bw-python
"""
from bw import BigWig
import sys
import os

if __name__ == '__main__':
    root_dir = sys.argv[1]
    for batch_dir in glob.glob(os.path.join(root_dir, 'batch_*')):
        for bigwig in glob.glob(os.path.join(batch_dir, '*.G.bw')):
            '''Excludes all files with "unique" in filenam, 
            which correspond to bigwigs considering unique alignments only.
            We use the bigwigs that count all primary alignments.'''
            bw_stream = pyBigWig.open(bw)
            try:
               coverage = bw_stream.values('chr5', 177093734, 177093735)[0]
            except IndexError:
                # Nothing to see in this bigwig
                pass
            else:
                print '\t'.join([bw, str(coverage)])
