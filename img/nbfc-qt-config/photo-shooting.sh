#!/bin/bash

for file in \
  nbfc-qt-config-basic.png \
  nbfc-qt-config-fan-basic.png \
  nbfc-qt-config-fan-temperature-thresholds.png \
  nbfc-qt-config-fan-speed-overrides.png \
  nbfc-qt-config-register-write-configurations.png; do

  for i in $(seq 5 -1 0); do
    echo "$i"
    sleep 1
  done

  scrot -s "$file"
done
