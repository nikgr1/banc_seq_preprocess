prefix='index.html?acc=GSE193553&format=file&file='
original_data=/home/nikgr/BIGDATA/BANC_seq/unpacked
for file in $original_data/${prefix}*
do
    new_name=${file#"$prefix"}
    mv $file $new_name
done
