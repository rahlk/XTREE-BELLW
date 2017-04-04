set terminal postscript eps enhanced color 20 "Helvetica"
set output "all.eps"
set title ""
set xrange [0:10]
set yrange [0:130]
set border lw 0
set xlabel "Dataset"
set ylabel "Value in %"
set xtics nomirror rotate by -45 offset character 0, 0, 0     norangelimit
set size ratio 1
set key inside vert right top noreverse noenhanced autotitle nobox
plot "Data" using 1:3:6:9:xticlabels(2) with yerrorbars lw 2 title "Recall", \
     "Data" using 1:4:7:10:xticlabels(2) with errorbars lw 2 title "False Alarm", \
     "Data" using 1:5:8:11:xticlabels(2) with errorbars lw 2 title "% Improvement"

