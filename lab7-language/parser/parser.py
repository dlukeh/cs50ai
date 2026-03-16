import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det AdjP N | NP PP | NP Conj NP
AdjP -> Adj | Adj AdjP
VP -> V | V NP | V PP | V NP PP | Adv VP | VP Adv | VP Conj VP | VP PP
PP -> P NP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Tokenize and normalize a sentence for parsing.

    - Converts all tokens to lowercase.
    - Keeps only tokens containing at least one alphabetic character.
    - Removes punctuation, numbers, and symbols.
    """
    tokens = nltk.word_tokenize(sentence)

    # Keep lowercase tokens that contain at least one alphabetic character
    return [token.lower() for token in tokens if any(c.isalpha() for c in token)]


def np_chunk(tree):
    """
    Return a list of all minimal noun phrase (NP) chunks in the tree.
    A chunk is an NP subtree that contains no other NP subtrees inside it.
    """
    chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == "NP":

            # Check whether this NP contains any other NP inside it
            has_nested_np = any(
                child.label() == "NP"
                for child in subtree.subtrees()
                if child is not subtree
            )

            if not has_nested_np:
                chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
