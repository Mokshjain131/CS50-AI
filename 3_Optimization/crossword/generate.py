import sys
from collections import deque
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
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
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


        # print(self.select_unassigned_variable({}))
        # print(self.consistent({}))
        # print(self.assignment_complete({}))
        # for x in self.domains:
        #     for y in self.domains:
        #         if x != y:
        #             self.revise(x, y)


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # for domain in self.domains:
        #     print(self.domains[domain])

        for v in self.crossword.variables:
            # print(v)
            for domain in self.domains[v].copy():
                if v.length != len(domain):
                    # print(domain)
                    self.domains[v].remove(domain)
            # print("--------------------------")


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        if self.crossword.overlaps[(x, y)]:
            (i, j) = self.crossword.overlaps[(x, y)]
            # print(i, j)
            for x_domain in self.domains[x].copy():
                delete = True
                for y_domain in self.domains[y].copy():
                    if y_domain[j] == x_domain[i]:
                        delete = False
                if delete == True:
                    # print (x, y)
                    # print(x_domain)
                    self.domains[x].remove(x_domain)
                    revised = True
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        q = deque()

        if arcs is None:
            for v1 in self.crossword.variables:
                for v2 in self.crossword.neighbors(v1):
                    q.append((v1, v2))
        else:
            for arc in arcs:
                q.append(arc)

        while q:
            (x, y) = q.popleft()
            if self.revise(x, y):
                # print(x)
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    # print(2)
                    q.append((z, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = set()
        for (key, value) in assignment.items():
            # print(value)
            if key.length != len(value):
                 return False
            if value in values:
                return False
            values.add(value)

            for v in self.crossword.neighbors(key):
                if v in assignment:
                    overlap = (self.crossword.overlaps.get((key, v)))
                    if overlap:
                        i, j = overlap
                        if assignment[key][i] != assignment[v][j]:
                            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domains = list(self.domains[var])
        count = 0
        key = list()
        for d in domains:
            for v in self.crossword.neighbors(var):
                if v not in assignment:
                    overlap = self.crossword.overlaps.get((var, v))
                    if overlap:
                        i, j = overlap
                        for dom in self.domains[v]:
                            if d[i] != dom[j]:
                                count += 1
            key.append(count)
            count = 0

        domains = [items for key, items in sorted(zip(key, domains))]
        return domains


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables = set()
        for (var, value) in assignment.items():
            variables.add(var)
        v = list(self.crossword.variables - variables)
        m = float('inf')
        mini = list()
        for var in v:
            length = len(list(self.domains[var]))
            if length < m:
                mini.clear()
                mini.append(var)
                m = length
            elif length == m:
                mini.append(var)

        degree = list()
        m = 0
        for var in mini:
            length = len(list(self.crossword.neighbors(var)))
            if length > m:
                degree.clear()
                degree.append(var)
                m = length
            elif length == m:
                degree.append(var)

        return degree[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for values in self.order_domain_values(var, assignment):
            assign = assignment.copy()
            assign[var] = values
            if self.consistent(assign):
                inferences = self.inferences(assign, var)
                if inferences is not None:
                    assign.update(inferences)

                    result = self.backtrack(assign)
                    if result is not None:
                        return result
        return None


    def inferences(self, assignment, var):
        domain_copy = {
            v: self.domains[v].copy()
            for v in self.crossword.variables
        }
        original_domains = self.domains
        self.domains = domain_copy

        res = {}
        arcs = list()
        value = assignment[var]
        neighbors = list(self.crossword.neighbors(var))
        for v in neighbors:
            arcs.append((v, var))

        if self.ac3(arcs) is False:
            self.domains = original_domains
            return None

        for v in self.crossword.variables:
            if v not in assignment and len(self.domains[v]) == 1:
                res[v] = list(self.domains[v])[0]

        self.domains = original_domains
        return res

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
