program=$1
in=$2
out=$3
exp_len=$4

#usage: ./test.sh calcwts ../input_files out_files "100 200 300 400 500" 

echo "" > times.csv
for i in $exp_len
do
  /usr/bin/time "$program" $in $out $i 2>> times.csv
done