#!/usr/bin/env python
"""
fgfr4_variant_scan.py

Scans a bunch of TCGA variant bigwigs output by Rail-RNA for evidence of 
hg38 chr5:177093734-177093735 G>A in RNA-seq data.

Usage: arg 1 is path to directory on JHPCE (Hopkins cluster) with TCGA variant
bigwigs.

Output: TSV with file uuids and raw coverages of G>A at 
chr5:177093734-177093735 iff any G>A reads are detected.

Requires https://github.com/brentp/bw-python. We ran:

python fgfr_variant_scan.py /dcl01/leek/data/tcga/v1 | sort -k2,2g \
    >fgfr_mutation_coverages.sorted.tsv on JHPCE.
"""
from bw import BigWig
import sys
import os
import glob

if __name__ == '__main__':
    root_dir = sys.argv[1]
    for batch_dir in glob.glob(os.path.join(root_dir, 'batch_*')):
        for bigwig in glob.glob(
                    os.path.join(batch_dir, 'coverage_bigwigs', '*.A.bw')
                ):
            '''Excludes all files with "unique" in filenam, 
            which correspond to bigwigs considering unique alignments only.
            We use the bigwigs that count all primary alignments.'''
            tcga_bw = BigWig(bigwig)
            try:
               coverage = tcga_bw.values('chr5', 177093733, 177093734)[0]
            except IndexError:
                # Nothing to see in this bigwig
                pass
            else:
                print '\t'.join([bigwig, str(coverage)])
            tcga_bw.close()

