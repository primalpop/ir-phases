program=$1
in=$2
out=$3
exp_len=$4

#usage: ./test.sh tokenize.py files out_files "100 200 300 400 500" 

echo "" > times.txt
for i in $exp_len
do
  for j in {1..10}
  do
    /usr/bin/time -f "$i,%e,%U,%S" python "$program" $in $out $i 2>> times.csv
  done
done
