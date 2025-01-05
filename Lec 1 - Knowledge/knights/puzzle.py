from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

initial_knowledge = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)

A_statement0 = And(AKnight, AKnave)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    initial_knowledge,
    Implication(A_statement0, AKnight),
    Implication(Not(A_statement0), AKnave)
)

A_statement1 = And(
    AKnave, BKnave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    initial_knowledge,
    Implication(A_statement1, AKnight),
    Implication(Not(A_statement1), AKnave)
)

A_statement2 = And(
    Or(And(AKnight, BKnight), And(AKnave, BKnave)), Not(And(And(AKnight, BKnight), And(AKnave, BKnave)))
)

B_statement2 = And(
    Or(And(AKnight, BKnave), And(AKnave, BKnight)), Not(And(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    initial_knowledge,
    Implication(A_statement2, AKnight),
    Implication(Not(A_statement2), AKnave),
    Implication(B_statement2, BKnight),
    Implication(Not(B_statement2), BKnave)
)

A_statement3 = Or(AKnight, AKnave)

B_statement3 = And(AKnave, CKnave)

C_statement3 = AKnight

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    initial_knowledge,
    Implication(A_statement3, AKnight),
    Implication(Not(A_statement3), AKnave),
    Implication(B_statement3, BKnight),
    Implication(Not(B_statement3), BKnave),
    Implication(C_statement3, CKnight),
    Implication(Not(C_statement3), CKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
