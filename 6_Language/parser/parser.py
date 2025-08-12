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
NP -> N | Det N | NP PP | ADJP NP | Det ADJP N | NP Conj NP
PP -> P NP
ADJP -> Adj | ADJP Adj | Adj ADJP
VP -> V | V NP | V PP | V Adv | Adv V | Adv V NP | VP Adv | VP Conj VP | V NP PP | V Adv PP
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
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = sentence.lower().split(' ')
    for word in words:
        print(word)
        alpha = False
        for c in word:
            if c.isalpha():
                alpha = True
        if alpha == False:
            words.remove(word)
    for i in range(len(words)):
        words[i] = words[i].replace('.', '').replace('\n', '')
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NPChunk = list()
    parent = False
    for child in tree:
        if isinstance(child, nltk.Tree) and child.label():
            recur = np_chunk(child)
            NPChunk.extend(recur)
            if len(recur) > 0:
                parent = True

    if parent == False and tree.label() == 'NP':
        NPChunk.append(tree)
    return NPChunk


if __name__ == "__main__":
    main()
