# sgRNA_counting
sgRNA_counting is a tool for quantifying sgRNA libraries used in perturb-seq data. Currently, sgRNA_counting is still under testing. For basic operation, please refer to the following commands.

```shell
python process_sgRNA_counting_V2.py \
    -f /data/work/speel_CD4T_analysis/01.PISA/CR_1_5_sgRNA/reads.fq \
    -r transf_1913_ref.csv \
    -t TTCCAGCATAGCTCTTAAAC \
    -l 20 \
    -n 32 \
    -o CR_1_5_sgRNA_matrix \
    -m 1 \
    -c 1000000 \
    -b /data/work/speel_CD4T_analysis/01.PISA/BCT/CR_1_5_BT.csv
````

