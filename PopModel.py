__author__ = 'Ben Sabath'

"""
A module to allow for evolutionary game theory to be easily modeled.
includes an object representing an individual population.
"""

class OutcomeMatrix(object):
    """ a class allowing for creation of a matrix representing the outcome of an
    encounter within a population
    """

    def __init__(self, xx=1, xy=1, yx=1, yy=1):
        self.outcomes = [[xx, xy], [yx, yy]]

    def __str__(self):
        line1 = "    x | y \n"
        line2 = "   -------\n"
        line3 = "x | " + str(self.outcomes[0][0]) + " | " + str(self.outcomes[0][1]) + " \n"
        line5 = "y | " + str(self.outcomes[1][0]) + " | " + str(self.outcomes[1][1]) + " \n"

        return line1 + line2 + line3 + line2 + line5

    def copy(self):
        xx = self.outcomes[0][0]
        xy = self.outcomes[0][1]
        yx = self.outcomes[1][0]
        yy = self.outcomes[1][1]
        return OutcomeMatrix(xx, xy, yx, yy)


class PopModel(object):
    """a basic model representing a mixed population of two distinct groups
       with a reproduction matrix describing how contact produces the next model generation.
       assumes constant reproductive rate without being given explicit OutcomeMatrix
    """

    def __init__(self, share, matrix=OutcomeMatrix()):
        assert 0 <= share <= 1
        self.share = round(share, 5)
        self.matrix = matrix
        self.num_generations = 0

    def __str__(self):
        share_y = round(1 - self.share, 5)
        out = "share x: " + str(self.share) + "\nshare y: " + str(share_y) + "\n"
        out += "Reproduction Matrix: \n" + str(self.matrix)
        out += "Number of generations: " + str(self.num_generations)

        return out

    def __repr__(self):
        return str(self)


    def next_gen(self):
        """
        change the share of the population to represent a random
        reproduction in an infinite population.
        """
        self.num_generations += 1
        share_y = 1 - self.share
        new_x = self.share*self.matrix.outcomes[0][0] + share_y*self.matrix.outcomes[0][1]
        new_x *= self.share
        new_y = self.share*self.matrix.outcomes[1][0] + share_y*self.matrix.outcomes[1][1]
        new_y *= share_y
        self.share = round(new_x/(new_x + new_y), 5)

    def copy(self):
        """
        return a deep copy of the model
        """
        return PopModel(self.share, self.matrix.copy())

    def run_sim(self, n):
        """
        simulate and record the path of the population share over n generations
        return the data as a list of length 2 tuples.
        The first element in each tuple is the generation number
        """

        model = self.copy()
        data = [(model.num_generations, model.share)]
        for i in range(n):
            model.next_gen()
            data.append((model.num_generations, model.share))

        return data




