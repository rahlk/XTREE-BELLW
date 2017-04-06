#!/usr/bin/env bash


for f in *.gp
  do
    gnuplot $f
  done

for f in *.eps
  do
    convert -density 600 -flatten ${f%.*}.eps ${f%.*}.png
    rm ${f%.*}.eps
  done