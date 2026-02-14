import itertools
import random


class Minesweeper:
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


class Sentence:
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

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
         Under what circumstances do you know for sure that a sentence’s cells are mines?
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
         under what circumstances do you know for sure that a sentence’s cells are safe?
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

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


class MinesweeperAI:
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
        counter = 0
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        return counter

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        counter = 0
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        return counter

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

        # 1 Mark as a move
        self.moves_made.add(cell)
        # 2 Mark as safe
        self.safes.add(cell)

        # 3
        undetermined_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Dont include current cell
                if (i, j) == cell:
                    continue
                # Dont include known mines
                if (i, j) in self.mines:
                    count -= 1  # if not including the mine reduce the sentance count
                    continue
                # Dont include known safes
                if (i, j) in self.safes:
                    continue
                # Anything else in the gird can be confirmed to be within the sentance
                if 0 <= i < self.height and 0 <= j < self.width:
                    undetermined_cells.add((i, j))

        # New setance - add to knowledge
        new_sentance = Sentence(undetermined_cells, count)

        self.knowledge.append(new_sentance)

        # 4) mark any additional cells as safe or as mines
        #       if it can be concluded based on the AI's knowledge base

        # identify all known mines
        #  each sentance is updated with the known mines + removed

        counter = 1
        while counter:
            counter = 0
            # reviews/rereviews the knowledge base each time until count is 0
            for sentence in self.knowledge:
                s_mines = sentence.known_mines()
                s_safes = sentence.known_safes()
                # if s_mines:
                for cell in s_mines.copy():
                    # marking as a mine - goes into the serntence removes the mine and reduces the count
                    self.mark_mine(cell)
                    counter += 1
                    # And similar for safes
                    # if s_safes:
                for cell in s_safes.copy():
                    self.mark_safe(cell)
                    counter += 1
                for cell in self.safes:
                    counter += self.mark_safe(cell)
                for cell in self.mines:
                    counter += self.mark_mine(cell)

        # Remove empty sentence objects from list using list comprehension
        empty_sentence = Sentence(set(), 0)
        self.knowledge = [
            sentence for sentence in self.knowledge if sentence != empty_sentence
        ]
        #    5) add any new sentences to the AI's knowledge base
        #       if they can be inferred from existing knowledge
        # if all cells in sentence B are in Sentence A = subset and we can make an new setence out of it
        new_sentances = []
        for sub in self.knowledge:
            for super in self.knowledge:
                if sub != super:

                    if sub.cells.issubset(super.cells):
                        # subset_cells = super.cells.difference(sub.cells)
                        subset_cells = super.cells - sub.cells
                        subset_count = super.count - sub.count

                        if len(subset_cells) > 0 and subset_count >= 0:
                            newknowledge = Sentence(subset_cells, subset_count)

                        if newknowledge not in self.knowledge:
                            new_sentances.append(newknowledge)

        for sentence in new_sentances:
            self.knowledge.append(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # not be in self.moves_made,self.mines but be in self.safes

        if len(self.safes) == 0:
            return None
        for safecells in self.safes:
            if safecells not in self.moves_made:
                return safecells
            else:
                return None

        # Get safe moves and ensure its not in

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_cells = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    possible_cells.append(cell)

        if len(possible_cells) == 0:
            return None
        else:
            # Return a random cell chosen from possible moves
            return random.choice(possible_cells)
