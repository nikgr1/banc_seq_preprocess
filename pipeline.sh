#!/bin/bash
source /home/nikgr/miniconda3/etc/profile.d/conda.sh
conda activate banc_seq

path_to_data=/home/nikgr/BIGDATA/BANC_seq
original_data=$path_to_data/unpacked
filtered_data=$path_to_data/filtered
bed_data=$path_to_data/bed
sliced_data=$path_to_data/sliced
final_data=$path_to_data/final

path_to_genomes=/home/nikgr/BIGDATA/BANC_seq/genomes
genome_variants=(hg38 mm10)
genomes_conf=$path_to_genomes/genome_conf.json

mkdir -p $filtered_data $bed_data $sliced_data $final_data

for genome in ${genome_variants[*]}
do
    conda activate banc_seq
    python chrom_tab2json.py \
        -i $path_to_genomes/$genome/genome.tsv \
        -o $path_to_genomes/$genome/genome.json \
        -f
done

for in_file in $original_data/*.txt
do
    basename=$(basename "$in_file")
    extension="${basename##*.}"
    filename="${basename%.*}"

    echo -e '\n' Filtering: '\t' $filename

    conda activate banc_seq
    python filtration_p_r.py \
        -i $in_file \
        -o $filtered_data/$filename.tsv
done


for in_file in $filtered_data/*.tsv
do
    basename=$(basename "$in_file")
    extension="${basename##*.}"
    filename="${basename%.*}"

    echo -e '\n' Processing: '\t' $filename

    conda activate banc_seq
    python filtration_p_r.py \
        -i $in_file \
        -o $filtered_data/$filename.tsv

    conda activate banc_seq
    genome_variant=$(cat $genomes_conf | jq -r --arg file "$filename" '.[$file].genome')
    echo -e Selected genome variant: '\t' $genome_variant

    conda activate banc_seq
    python bancseq2bed.py \
        -i $filtered_data/$filename.tsv \
        -o $bed_data/$filename.bed \
        -c $path_to_genomes/$genome_variant/genome.json

    conda activate samtools
    bedtools getfasta \
        -fi $path_to_genomes/$genome_variant/genome.fna \
        -bed $bed_data/$filename.bed \
        -tab -name \
        -fo $sliced_data/$filename.tsv

    conda activate banc_seq
    python include_seq.py \
        -i $filtered_data/$filename.tsv \
        -o $final_data/$filename.tsv \
        -p $sliced_data/$filename.tsv
done



