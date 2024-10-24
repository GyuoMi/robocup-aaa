#!/usr/bin/env bash
export OMP_NUM_THREADS=1

host=${1:-localhost}
port=${2:-3100}

for i in {1..11}; do
  python3 ./Run_Player.py -i $host -p $port -u $i -t Us -P 0 -D 0 &
done
