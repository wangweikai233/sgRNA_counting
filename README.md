# sgRNA_counting
sgRNA_counting is a tool for quantifying sgRNA libraries used in perturb-seq data. Currently, sgRNA_counting is still under testing. For basic operation, please refer to the following commands.


## 1. Merge sgRNA reads
```shell
sample=CR_1_5_sgRNA
fq1=/data/input/Files/RawData/wangweikai/imap_spleen/sgRNA_fq/DP8480012856TR_L01_11_1.fq.gz
fq2=/data/input/Files/RawData/wangweikai/imap_spleen/sgRNA_fq/DP8480012856TR_L01_11_2.fq.gz
outdir=/data/work/speel_CD4T_analysis/01.PISA
mkdir -p ${outdir}/${sample}

/scRNA-seq-v3.1.5-pipeline/bin/PISA parse -t 16 -q 4 -dropN -config /data/input/Files/RawData/wangweikai/scRNA_beads_darkReaction.json -cbdis ${outdir}/${sample}/barcode_counts_raw.txt -1 ${outdir}/${sample}/reads.fq -report ${outdir}/${sample}/sequencing_report.csv ${fq1} ${fq2}

```

## 2. sgRNA counting
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

