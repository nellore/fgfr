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

python fgfr_variant_scan.py /dcl01/leek/data/tcga/v1 \
    >fgfr_mutation_coverages.tsv on JHPCE.

We subsequently downloaded http://duffel.rail.bio/recount/TCGA/TCGA.tsv 
containing TCGA metadata and ran

cat TCGA.tsv | cut -f11,19,22,90,179,170 >tcga_meta.tsv

to obtain the much smaller metadata file tcga_meta.tsv that has bigwig AUCs
for normalization.

FGFR1: 18 exons; two kinase subdomains within exons 10-18

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
               A_coverage = tcga_bw.values('chr5', 177093733, 177093734)[0]
            except IndexError:
                # Nothing to see in this bigwig
                pass
            else:
                tcga_bw.close()
                # Grab total coverage at variant
                tcga_bw = BigWig('.'.join(bigwig.split('.')[:-2] + ['bw']))
                try:
                    coverage = tcga_bw.values('chr5', 177093733, 177093734)[0]
                except IndexError:
                    coverage = 0.0
                print '\t'.join(
                        [bigwig.rpartition('/')[-1].partition('.')[0],
                            str(A_coverage),
                            str(coverage)]
                    )
                sys.stdout.flush()
                tcga_bw.close()
