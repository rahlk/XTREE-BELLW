set terminal postscript eps enhanced mono 20 "Helvetica"
set output "recall.eps"
set title ""
set xrange [0:10]
set yrange [0:100]
set border lw 0
set xlabel "Dataset"
set ylabel "Recall"
set xtics nomirror rotate by -45 offset character 0, 0, 0     norangelimit
set size ratio 1
unset key
plot "Bellwether Train and Plan.dat" using 1:3:6:9:xticlabels(2) with yerrorbars ls 1 lw 2 title ""
