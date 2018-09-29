PS C:\Users\T901\Anaconda3> .\python D:/github/evol-alg/tsp/tsp_generic_alg.py
Or run in Spyder.

***Alternative:
# WE PROBABLY USE MUTATE PROBABILITY FOR WHOLE GENERATION
for i in range(0, self.size):
   if random.random() < self.mutation_rate:
   self.population[i].mutate() 

***Future work:
- Update eval_func
- Update Individual attributes (not only chromosome, adding other features)
- Update Individual methods, e.g. crossover, mutate for your problems
e.g. for TSP problem, crossover - mutate methods are changed so that the genomes in each chromosome are still kept the same, but only their ordering changes. 
     for Patient-Virus Dynamics problem, crossover - mutate methods will change in different way; more methods are introduced, e.g. birth, clear...

***Comparison of generic algorithm GA vs. simulated anneal SA (the same city database - city100.txt):
+ Speed (Runtime performance): GA << SA
+ Score (TSP - travelling length): GA << SA

Tested: mutate = 0.1, crossover (generating new children) = 0.9, newindividualrate = 0.6
SA - 50000 evaluations
GA - population_size=100, 100 generations >>> score=20743.819582515946
GA - population_size=100, 10000 generations >>> score=16338.731522009184
GA - population_size=1000, 100 generations >>> score=19934.746063667564

Suggested new test: 
Try: mutate = 0.005, crossover (replace with child) = 0.9, newindividualrate = 0.1 
(reference: Patient-Virus Dynamics problem)
GA - population_size=1000, 100 generations >>> score=16071.770437130748
GA - population_size=1000, 1000 generations >>> score=9031.560838547977
GA - population_size=1000, 10000 generations >>> score=5905.005207628114
GA - population_size=1000, 50000 generation

Try: mutate = 0.005, crossover (replace with child) = 0.9, newindividualrate = 0.05
GA - population_size=1000, 1000 generations >>> score=10312.657460741122

Try: mutate = 0.005, crossover (replace with child) = 0.9, newindividualrate = 0.1 (line 236: double children to replace)
GA - population_size=1000, 1000 generations >>> score=8726.107201790785

Try: mutate = 0.005, crossover (replace with child) = 0.9, newindividualrate = 0.2 (line 236: double children to replace)
GA - population_size=1000, 1000 generations >>> score=7384.553870940318   <<<< LOOK GOOD, INCREASE GENERATIONS

Try: mutate = 0.005, crossover (replace with child) = 0.9, newindividualrate = 0.6 (line 236: double children to replace)
GA - population_size=1000, 1000 generations >>> score=18233.127495618206

Comment: 
1. mutate - similar to swapped_cities in SA
   crossover - similar to reversed_sections in SA (instead of reverse, crossover does remove genomes 
                                                   and then insert them in different positions)
2. In some simulations, for the first runs, the scores are decreased every quickly; but for the next runs, 
   the scores go down very slowly, it looks like the solutions converge to local optimum.
   Try to increase the mutation rate (apply for low fitness rank individuals) to keep the search space divergent in generations.
   We would select individuals with highest fitness rank and the ones with the highest diversity rank.

***CONCLUSION: SHOULD TAKE ABOUT 100 RUNS AND MAKE THE AVERAGED SCORE (TRAVELLING LENGTH)
INSTEAD OF ONE RUN AND THEN MAKING CONCLUSION

***Reference:
https://zhanggw.wordpress.com/2009/11/07/resolve-tsp-traveling-saleman-problem-in-genetic-algorithm/