set terminal postscript eps enhanced color 20 "Helvetica"
set output "all.eps"
set title ""
set yrange [0:100]
set xrange [0.5:5]
set border lw 0
set xlabel "Dataset"
set ylabel "Value in %"
set xtics nomirror rotate by -45 offset character 0, 0, 0     norangelimit
set size ratio 1
set key inside vert right bottom noreverse noenhanced autotitle nobox
plot "data" using 1:3:4:5:xticlabels(2) with yerrorbars lw 2 title "Bellwether", \
     "data" using ($1+0.25):6:7:8 with errorbars lw 2 title "Local"