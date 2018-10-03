Course: 
- Udemy: Evolutionary Algorithms - AI Tetris Bot
- Youtube: 12a. Neural Nets, 12b. Deep Neural Nets
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

The question: How to measure the diversity of the graph?
I did the same way I measured the fitness. That is to say, I calculated the actual metric distance of all of the
candidates for the next generation from all of the candidates that had already been selected. I summed that up.
And from that sum, I could rank them according to how different they were from the individuals that were already
in the next generation. It's like giving a rank, and then from the rank, I use that kind of calculation to determine
the fitness, ie, probability of survival, and then I just combine the two kinds of probabilities.

Diversity is good. We noticed we put diversity into the genetic algorithm calculations, we are much better at 
finding solutions. But the next gold star idea that I'd really like to have you go away with is the idea that you
have to ask where credit lies. Does it lie with ingenuity of the programmer or with the value of the algorithm 
itself? In this case, impressive as it is, the credit lies IN THE RICHNESS OF THE SPACE AND IN THE INTELLIGENCE OF
THE PROGRAMMER, NOT NECESSARILY IN THE IDEA OF GENETIC ALGORITHMS.