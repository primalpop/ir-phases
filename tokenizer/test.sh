program=$1
in=$2
exp_len=$3
num_exp=$4
#usage: ./test.sh tokenize.py files "100 200 300 400 500" 10

echo "" > times.txt
for i in $exp_len
do
  for j in {1..10}
  do
    /usr/bin/time  python "$program" $in $i 2>> times.txt
  done
done
