# Analysis

## Layer 4, Head 12

This layer gives attention to the verb in the sentence.

Example Sentences:
- He likes to [MASK] with everyone.

    in this case the layer is paying attention to the verb "likes"

    generated sentences:
        He likes to talk with everyone.
        He likes to be with everyone.
        He likes to chat with everyone.
    
- I love pizza with [MASK] toppings.

    in this case the layer is paying attention to the verb "love"

    generated sentences:
        I love pizza with different toppings.
        I love pizza with various toppings.
        I love pizza with pizza toppings.

## Layer 8, Head 11

This layer is responsible for giving attention to the subject that the mask is describing.

Example Sentences:
- He likes to [MASK] with everyone.

    in this case the layer focuses majorly on "everyone" and also bit on the "with".

    generated sentences:
        He likes to talk with everyone.
        He likes to be with everyone.
        He likes to chat with everyone.
    
- I love pizza with [MASK] toppings.

    in this case the layer pays attention to "topping" which the masked token describing.

    generated sentences:
        I love pizza with different toppings.
        I love pizza with various toppings.
        I love pizza with pizza toppings.

