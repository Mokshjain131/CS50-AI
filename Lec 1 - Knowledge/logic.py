def model_check(knowledge, query):
    """Checks if knowledge base entails query"""

    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a model."""

        # if there are no symbols left to assign
        if not symbols:
            if knowledge.evaluate(model): 
                return query.evaluate(model)

        else:
            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false))

    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check if knowledge entails query
    return check_all(knowledge, query, symbols, dict())