# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

xxx = """
Int64 hash (String s) {
        Int64 h = 7
        String letters = "acdegilmnoprstuw"
        for(Int32 i = 0; i < s.length; i++) {
            h = (h * 37 + letters.indexOf(s[i]))
        }
        return h
    }
"""

# <codecell>

available_characters = 'acdegilmnoprstuw'
the_hash = 945924806726376

def forward_hash(astring, available_characters):
    """A python version of the original hash algo"""
    h = 7
    for letter in astring:
        h = (h*37 + available_characters.index(letter))
    return h

def reverse_hash(the_hash, available_characters):
    """The reverse of the forward_hash algorithm"""
    the_word = ''    
    
    # When the hash equals the starting value of 7, you're done.
    while the_hash != 7:
        # Iterate through each possible character
        for idx, letter in enumerate(available_characters):
            # Here's the important bit - determine if the algorithm can be reversed
            # and yet still arrive at an integer value. If not, try the next character.
            hashbit = ((the_hash - idx)/37.0)
            if hashbit%1 == 0:
                # Decrement your hash
                the_hash = hashbit
                # Store the correct character
                the_word += letter
                break
            if idx == len(available_characters)-1:
                raise UserWarning, "Either your hash or your algorithm is terrible..."
    # We've found our word. Reverse it (as we reversed the algorithm) and return.
    return the_word[::-1]


    

# <codecell>

%timeit reverse_hash(1317985395604951854, 'acdegilmnoprstuw')

# <codecell>


