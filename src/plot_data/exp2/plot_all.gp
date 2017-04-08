set terminal postscript eps enhanced color 20 "Helvetica"
set output "all.eps"
set title ""
set yrange [-100:100]
set xrange [0.5:5]
set border lw 0
set xlabel "Dataset"
set ylabel "Value in %"
set xtics nomirror rotate by -45 offset character 0, 0, 0     norangelimit
set size ratio 1
set key inside vert right bottom noreverse noenhanced autotitle nobox
plot "Data" using 1:9:10:11:xticlabels(2) with yerrorbars lw 2 title "Local", \
     "Data" using 1:12:13:14:xticlabels(2) with errorbars lw 2 title "Bellwether"