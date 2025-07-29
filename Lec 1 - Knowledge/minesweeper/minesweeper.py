import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        return hash((frozenset(self.cells), self.count))

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()

        if (len(self.cells) == self.count):
            mines.update(self.cells)

        return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()

        if (self.count == 0):
            safes.update(self.cells)

        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
                based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
                if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
                if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        unknown_neighbors = set()
        adjusted_count = count

        for i in range(max(0, cell[0] - 1), min(self.height, cell[0] + 2)):
            for j in range(max(0, cell[1] - 1), min(self.width, cell[1] + 2)):
                neighbor = (i, j)
                if neighbor == cell:
                    continue

                if neighbor in self.mines:
                    adjusted_count -= 1
                elif neighbor not in self.safes:
                    unknown_neighbors.add(neighbor)

        if len(unknown_neighbors) > 0 and adjusted_count >= 0:
            new_sentence = Sentence(unknown_neighbors, adjusted_count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        something_changed = True
        while something_changed:
            something_changed = False

            sentences_to_process = self.knowledge[:]

            for sentence in sentences_to_process:
                initial_sentence_cells_len = len(sentence.cells)
                initial_sentence_count = sentence.count

                for mine_cell in list(self.mines):
                    if mine_cell in sentence.cells:
                        sentence.mark_mine(mine_cell)

                for safe_cell in list(self.safes):
                    if safe_cell in sentence.cells:
                        sentence.mark_safe(safe_cell)

                if len(sentence.cells) != initial_sentence_cells_len or sentence.count != initial_sentence_count:
                    something_changed = True

            for i in range(len(self.knowledge) - 1, -1, -1):
                if len(self.knowledge[i].cells) == 0:
                    del self.knowledge[i]
                    something_changed = True

            newly_marked_mines = set()
            newly_marked_safes = set()

            for sentence in self.knowledge[:]:
                if len(sentence.cells) == sentence.count and sentence.count > 0:
                    for cell_to_mark in list(sentence.cells):
                        if cell_to_mark not in self.mines:
                            newly_marked_mines.add(cell_to_mark)
                            something_changed = True

                elif sentence.count == 0 and len(sentence.cells) > 0:
                    for cell_to_mark in list(sentence.cells):
                        if cell_to_mark not in self.safes:
                            newly_marked_safes.add(cell_to_mark)
                            something_changed = True

            for cell in newly_marked_mines:
                self.mark_mine(cell)
            for cell in newly_marked_safes:
                self.mark_safe(cell)

            new_sentences_to_add = []

            current_knowledge_snapshot_for_inference = self.knowledge[:]
            for s1 in current_knowledge_snapshot_for_inference:
                for s2 in current_knowledge_snapshot_for_inference:
                    if s1 == s2:
                        continue

                    if s1.cells.issubset(s2.cells):
                        if not s2.cells == s1.cells:
                            inferred_cells = s2.cells - s1.cells
                            inferred_count = s2.count - s1.count

                            if len(inferred_cells) > 0 and inferred_count >= 0:
                                new_inferred_sentence = Sentence(inferred_cells, inferred_count)

                                if new_inferred_sentence not in self.knowledge and new_inferred_sentence not in new_sentences_to_add:
                                    new_sentences_to_add.append(new_inferred_sentence)
                                    something_changed = True

            for new_s in new_sentences_to_add:
                self.knowledge.append(new_s)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        valid_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if ((i,j) not in self.mines) and ((i,j) not in self.moves_made):
                    valid_moves.append((i,j))
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None
