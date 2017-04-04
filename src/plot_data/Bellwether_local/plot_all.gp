set terminal postscript eps enhanced color 20 "Helvetica"
set output "all.eps"
set title ""
set xrange [0:10]
set yrange [-19:110]
set border lw 0
set xlabel "Dataset"
set ylabel "Value in %"
set xtics nomirror rotate by -45 offset character 0, 0, 0     norangelimit
set size ratio 1
set key inside vert right bottom noreverse noenhanced autotitle nobox
plot "Data" using 1:5:9:13:xticlabels(2) with yerrorbars lw 2 title "Local", \
     "Data" using 1:6:10:14:xticlabels(2) with errorbars lw 2 title "Bellwether"