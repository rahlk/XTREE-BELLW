set terminal postscript eps enhanced mono 20 "Helvetica"
set output "Gain.eps"
set title ""
set xrange [0:10]
set yrange [0:100]
set border lw 0
set xlabel "Dataset"
set ylabel "% Improvement"
set xtics nomirror rotate by -45 offset character 0, 0, 0     norangelimit
set size ratio 1
unset key
plot "Bellwether Train and Plan.dat" using 1:5:8:11:xticlabels(2) with errorbars lw 2 title ""
