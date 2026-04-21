import sys

import copy

from crossword import *

import pandas as pd


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def SelectUnassignedVar(self, assignment):
        vars = []
        for var, words in assignment.items():
            if words is None:
                vars.append(var)
        return vars

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable, words in self.domains.items():
            Vlength = variable.length
            for word in list(words):
                Wlength = len(word)

                if Vlength != Wlength:
                    self.domains[variable].remove(word)

            else:
                continue

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        """
        revised = False
        # adding this set to remove the error of doamins changing during itteration
        remove_x = set()
        for v1 in self.domains[x]:
            for v2 in self.domains[y]:
                # check if there is overlap 
                if not self.crossword.overlaps[x, y]:
                    revised = False
                else:
                    i, j = self.crossword.overlaps[x, y]
                    if v1[i] != v2[j]:
                        remove_x.add(v1)
                        revised = True
                    else:
                        # return false as not arc consistency needed to be satisfised as no overlap
                        revised = False
        # after itteration remove variables
        self.domains[x] = self.domains[x] - remove_x

        return revised
    
    """
        revised = False
        remove_x = set()
        # adding this set to remove the error of doamins changing during itteration

        for v1 in self.domains[x]:
            arc_consistent = False
            overlap = self.crossword.overlaps[x, y]

            # if there is no overlap then its arc consistent
            if overlap is None:
                arc_consistent = True

            else:
                i, j = self.crossword.overlaps[x, y]
                for v2 in self.domains[y]:
                    if v1 != v2:
                        try:
                            if v1[i] == v2[j]:
                                arc_consistent = True
                                break  # as we found atleast 1 consistent value
                        except IndexError:
                            pass
            if not arc_consistent:
                remove_x.add(v1)
                revised = True

        # after itteration remove variables
        self.domains[x] = self.domains[x] - remove_x

        return revised

    """
        for variable, words in self.domains.items():
            Vlength = variable.length
            for word in list(words):
    """

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # taken from notes for cs50ai

        """
        function AC-3(csp):
            queue = all arcs in csp
            while queue non-empty:
                (X, Y) = Dequeue(queue)
                    if Revise(csp, X, Y):
                        if size of X.domain == 0:
                            return false
                        for each Z in X.neighbors - {Y}:
                            Enqueue(queue, (Z,X))
            return true
        """
        # use pandas to create the list of arcs
        if arcs == None:
            set1 = self.crossword.variables
            set2 = self.crossword.variables

            df1 = pd.DataFrame({"s1": list(set1)})
            df2 = pd.DataFrame({"s2": list(set2)})
            join_df = df1.merge(df2, how="cross")
            # list of all arcs
            arcs = list(join_df.itertuples(index=False, name=None))

            for v in arcs:
                i, j = v  # if v = (hello,morning) i=hello , j =morning
                if i == j:
                    arcs.remove(v)  # remove any duplicate values

        while arcs:
            for v in arcs:
                arcs.remove(v)
                if self.revise(v[0], v[1]):
                    if self.domains[v[0]] == 0 or None:
                        return False
                    for Z in self.crossword.neighbors(v[0]):
                        """
                        we need to see if all the arcs associated with X are still consistent.
                        That is, we take all of X’s neighbors except Y,
                        and we add the arcs between them and X to the queue
                        """
                        if Z != v[1]:
                            arcs.append((Z, v[0]))
        return False

    def assignment_complete(self, assignment):
        for variable in self.domains:
            # if statment loops through all variables and if they are all in aissignment it returns True if not false
            if variable not in assignment:
                return False
        # moved to end of for loop to ensure full cycle of If funtion
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        "An assignment is consistent if it satisfies all of the constraints of the problem: that is to say, "
        "all values are distinct, every value is the correct length, "
        "and there are no conflicts between neighboring variables."

        for var, word in assignment.items():
            # check if node consistent in terms of length
            if var.length != len(word):
                return False
                # check consistenc in terms of neighbours not having the same word
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    # we focus on the neighbors that have been assigned a word
                    W = assignment[neighbor]

                    if var != neighbor:
                        i, j = self.crossword.overlaps[var, neighbor]
                        if word[i] != W[j]:
                            return False
        # leave True at the end and only return it if a value if found. Allowing the module to loop through all vars,words, neigbors, W etc

        return True

        """
                        for neighbor in self.crossword.neighbors(var):
                    i, j = self.crossword.overlaps[var, neighbor]

                    for v2 in self.domains[y]:
                        if v1[i] == v2[j]:
                            arc_consistent = True
                            break  # as we found atleast 1 consistent value
                        
        """

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        """
        get the variable # var is given to us 
            get a word for each variable 
            if we pick this word, how does it constrain neighbouring variables? 
                identify if we use this word how many words are the neighbours able to use? use overlap words and thus number
                add this number to a list.append()
                sort the list 
        """
        n = {}
        # make sure var isnt already assigned and thus rule them out as neighbours
        neighbors = self.crossword.neighbors(var).copy()

        """
        for v in neighbors:
            if v in assignment:
                neighbors.remove(v)
        """
        unassigned_neighbors = [
            v for v in self.crossword.neighbors(var) if v not in assignment
        ]

        for w1 in self.domains[var]:
            number = 0
            for v2 in unassigned_neighbors:
                i, j = self.crossword.overlaps[var, v2]
                for w2 in self.domains[v2]:
                    if w1[i] != w2[j]:
                        number += 1
            n[w1] = number

        list = sorted(n.items(), key=lambda item: item[1])
        return [word for word, count in list]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # self.crossword.variables

        unassigned = [
            var for var in set(self.domains.keys()) if var not in set(assignment.keys())
        ]
        unassigned.sort(
            key=lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x)))
        )

        return unassigned[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        """ (with inference)
        function Backtrack(assignment, csp):

            if assignment complete:
                return assignment
            var = Select-Unassigned-Var(assignment, csp)
            for value in Domain-Values(var, assignment, csp):
                if value consistent with assignment:
                    add {var = value} to assignment
                    inferences = Inference(assignment, csp)
                    if inferences ≠ failure:
                        add inferences to assignment
                    result = Backtrack(assignment, csp)
                    if result ≠ failure:
                        return result
                    remove {var = value} and inferences from assignment
            return failure
        """

        """ without inference
        function Backtrack(assignment, csp):

            if assignment complete:
                return assignment
            var = Select-Unassigned-Var(assignment, csp)
            for value in Domain-Values(var, assignment, csp):
                if value consistent with assignment:
                    add {var = value} to assignment
                result = Backtrack(assignment, csp)
                if result ≠ failure:
                    return result
                remove {var = value} from assignment
            return failure
        """

        # lets do it without inference first
        if self.assignment_complete(assignment):
            return assignment
        """select_unassigned_variable"""
        """vars = self.SelectUnassignedVar(assignment)"""
        var = self.select_unassigned_variable(assignment)
        # check_consistency = copy.deepcopy(assignment)

        for word in self.order_domain_values(var, assignment):
            # check_consistency[var] = word
            assignment[var] = word

            if self.consistent(assignment) is True:
                result = self.backtrack(assignment)
                if result:
                    # assignment[var] = word
                    return result
            del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
