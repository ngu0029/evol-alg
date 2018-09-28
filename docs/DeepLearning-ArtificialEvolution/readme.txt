Course: 
- Udemy: Evolutionary Algorithms - AI Tetris Bot
- Youtube: 13. Learning: Genetic Algorithms (MIT course)
@21:00 introducing mechanisms for converting Fitness score of each individual to Probability 
to be selected to next generation.
#1 - Pi = Fi / sum(Fi)
#2 - Rank Space
P1 = Pc, P2 = (1-Pc)Pc,..., Pn-1 = (1-Pc)^(n-2) * Pc, Pn = (1-Pc)^(n-1) * Pc where 0 < constant Pc < 1
#3 - The problem is we lost diversity in our population, then we can measure diversity - not only the fitness
of the set of individuals we're selecting from, but we can measure how different they are on the individuals 
we've already selected for the next population.
> We would select individuals with highest fitness rank and the ones with the highest diversity rank.
> We've got to pick some individuals for the next population. When we pick the first individual, all we've got to
go on is how fit the individual is, because nobody else in that next generation. After the first individual selected,
then we can look at our set of candidates, and we can say which candidate would be more different from the set of
things we've already selected than all the others. That would get the highest diversity rank and so on down the 
candidate list.

References:
https://en.wikipedia.org/wiki/Neuroevolution
https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies