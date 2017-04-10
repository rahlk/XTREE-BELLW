set terminal postscript eps enhanced color 20 "Helvetica"
set output "local_vs_bellwether.eps"
set title "Percentage reduction in defects"
set yrange [0:100]
set xrange [0.5:4.5]
set border lw 0
set xlabel "Dataset"
set ylabel "Value in %"
set xtics nomirror rotate by -45 offset character 0, 0, 0     norangelimit
set size ratio 1
set key inside vert right bottom noreverse noenhanced autotitle nobox
plot "Data" using 1:3:4:5:xticlabels(2) with yerrorbars lw 2 title "Bellwether", \
     "Data" using 1:6:7:8:xticlabels(2) with errorbars lw 2 title  "Local "
