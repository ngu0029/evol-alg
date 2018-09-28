***Using PowerShell
PS C:\Users\T901\Anaconda3> .\python D:/github/evol-alg/tsp/part_two/tsp.py -o "D:/github/evol-alg/tsp/part_two/tsp.png"
 -v -m "reversed_sections" -n 50000 "D:/github/evol-alg/tsp/part_two/city100.txt"
2018-09-26 17:01:11,090 INFO using move_operator: <function reversed_sections at 0x000002C303E86598>
2018-09-26 17:01:11,091 INFO (re)starting hillclimb 50000/50000 remaining
2018-09-26 17:01:11,093 INFO hillclimb started: score=-27654.159586
2018-09-26 17:01:13,110 INFO hillclimb finished: num_evaluations=45681, best_score=-4213.777009
2018-09-26 17:01:13,111 INFO (re)starting hillclimb 4319/50000 remaining
2018-09-26 17:01:13,113 INFO hillclimb started: score=-26896.108643
2018-09-26 17:01:13,379 INFO hillclimb finished: num_evaluations=4319, best_score=-6883.332705
50000 -4213.777009102513 [78, 26, 41, 63, 23, 22, 67, 88, 21, 34, 18, 36, 61, 16, 54, 3, 51, 84, 48, 65, 47, 52, 11, 64, 13, 53, 71, 15, 32, 94, 55, 76, 95, 72, 58, 37, 45, 6, 93, 12, 2, 42, 25, 98, 40, 91, 27, 17, 29, 89, 24, 70, 46, 7, 81, 33, 87, 82, 60, 69, 77, 44, 66, 99, 50, 92, 5, 68, 0, 35, 39, 56, 86, 73, 10, 96, 9, 30, 19, 31, 20, 79, 59, 57, 28, 4, 75, 62, 80, 85, 83, 74, 43, 8, 14, 38, 49, 97, 90, 1]

***Reference:
http://www.psychicorigami.com/2007/04/17/tackling-the-travelling-salesman-problem-part-one/
http://www.psychicorigami.com/2007/05/12/tackling-the-travelling-salesman-problem-hill-climbing/
