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

    def __str__(self):
        return f"{self.cells} = {self.count}"
    def known_mines(self):
        """Returns the set of all cells in self.cells known to be mines."""
        if self.count != 0 and len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """Returns the set of all cells in self.cells known to be safe."""
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """Updates the sentence given the fact that a cell is known to be a mine."""
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """Updates the sentence given the fact that a cell is known to be safe."""
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

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) build a new sentence from neighbors of this cell
        neighbors = set()
        i, j = cell

        for di in range(-1, 2):
            for dj in range(-1, 2):
                ni = i + di
                nj = j + dj

                # skip out-of-bounds
                if not (0 <= ni < self.height and 0 <= nj < self.width):
                    continue

                # skip the cell itself
                if (ni, nj) == (i, j):
                    continue

                neighbor = (ni, nj)

                # if already known mine, adjust count
                if neighbor in self.mines:
                    count -= 1
                    continue

                # if still unknown (not safe and not mine), include it
                if neighbor not in self.safes and neighbor not in self.mines:
                    neighbors.add(neighbor)

        # add the new sentence if there's anything to say
        if neighbors:
            new_sentence = Sentence(neighbors, count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        # 4 & 5) repeatedly make inferences until nothing new is learned
        changed = True
        while changed:
            changed = False

            # 4a) mark any new safes/mines from current sentences
            safes_to_mark = set()
            mines_to_mark = set()

            for sentence in self.knowledge:
                safes_to_mark |= sentence.known_safes()
                mines_to_mark |= sentence.known_mines()

            for s in safes_to_mark:
                if s not in self.safes:
                    self.mark_safe(s)
                    changed = True

            for m in mines_to_mark:
                if m not in self.mines:
                    self.mark_mine(m)
                    changed = True

            # remove any empty sentences
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

            # 5) infer new sentences via subset rule
            new_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2:
                        continue
                    if s1.cells and s1.cells.issubset(s2.cells):
                        inferred_cells = s2.cells - s1.cells
                        inferred_count = s2.count - s1.count
                        inferred = Sentence(inferred_cells, inferred_count)

                        if inferred_cells and inferred not in self.knowledge and inferred not in new_sentences:
                            new_sentences.append(inferred)

            if new_sentences:
                self.knowledge.extend(new_sentences)
                changed = True

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
        candidates = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell in self.moves_made:
                    continue
                if cell in self.mines:
                    continue
                candidates.append(cell)

        if not candidates:
            return None

        return random.choice(candidates)
