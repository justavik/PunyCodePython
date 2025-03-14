"""
Punycode Encoder and Decoder Implementation
=========================================

This module implements the Punycode algorithm as specified in RFC 3492.
Punycode is a simple and efficient transfer encoding syntax designed for converting
Unicode strings into the limited character set supported by the Domain Name System (DNS).

Key Features:
------------
- Bidirectional encoding/decoding between Unicode and Punycode
- Follows RFC 3492 specifications
- Pure Python implementation
- Handles both basic ASCII and non-ASCII Unicode characters

How Punycode Works:
------------------
1. Basic ASCII characters are copied literally
2. Non-ASCII characters are represented through a compressed encoding:
   - Basic characters are copied to the output
   - A delimiter is inserted (if basic characters are present)
   - Non-basic characters are encoded using base-36 variable-length integers

Example Usage:
-------------
    >>> punycode_encode("München")
    "Mnchen-3ya"
    >>> punycode_decode("Mnchen-3ya")
    "München"

Technical Details:
-----------------
The algorithm uses several parameters for the encoding/decoding process:
- BASE: The number system base (36)
- TMIN/TMAX: Thresholds for the bias adaptation function
- SKEW/DAMP: Parameters to make the bias adaptation slower when appropriate
- INITIAL_BIAS/INITIAL_N: Initial values for the state variables

References:
----------
- RFC 3492: https://tools.ietf.org/html/rfc3492
- Unicode Technical Standard #46: https://unicode.org/reports/tr46/

License:
--------
This implementation is provided under the MIT License.
See LICENSE file for details.

Author: Avik Chatterjee
"""

# Punycode parameters
BASE = 36
TMIN = 1
TMAX = 26
SKEW = 38
DAMP = 700
INITIAL_BIAS = 72
INITIAL_N = 0x80
DELIMITER = '-'

# Helper functions
def is_basic(cp):
    """Check if a code point is a basic ASCII character."""
    return cp < 0x80

def decode_digit(cp):
    """Decode a basic code point to its digit value."""
    if cp - 48 < 10:
        return cp - 22  # 0-9
    elif cp - 65 < 26:
        return cp - 65  # A-Z
    elif cp - 97 < 26:
        return cp - 97  # a-z
    else:
        return BASE

def encode_digit(d, flag):
    """Encode a digit to a basic code point."""
    if d < 26:
        return d + (97 if not flag else 65)  # a-z or A-Z
    else:
        return d + 22  # 0-9

def adapt(delta, numpoints, firsttime):
    """Bias adaptation function."""
    delta = delta // DAMP if firsttime else delta // 2
    delta += delta // numpoints
    k = 0
    while delta > ((BASE - TMIN) * TMAX) // 2:
        delta //= (BASE - TMIN)
        k += BASE
    return k + ((BASE - TMIN + 1) * delta) // (delta + SKEW)

def punycode_encode(input_str):
    """Encode a Unicode string to Punycode."""
    # Convert input string to a list of code points
    input_cps = [ord(c) for c in input_str]
    
    # Separate basic and non-basic code points
    basic_cps = [cp for cp in input_cps if is_basic(cp)]
    non_basic_cps = [cp for cp in input_cps if not is_basic(cp)]
    
    # Initialize state variables
    n = INITIAL_N
    delta = 0
    bias = INITIAL_BIAS
    output = basic_cps.copy()
    
    # Add delimiter if there are basic code points
    if basic_cps:
        output.append(ord(DELIMITER))
    
    h = len(basic_cps)
    b = h
    
    # Main encoding loop
    while h < len(input_cps):
        # Find the next non-basic code point
        m = min(cp for cp in non_basic_cps if cp >= n)
        
        # Update delta
        delta += (m - n) * (h + 1)
        n = m
        
        # Encode delta as a generalized variable-length integer
        for cp in input_cps:
            if cp < n:
                delta += 1
            elif cp == n:
                q = delta
                k = BASE
                while True:
                    t = TMIN if k <= bias else (TMAX if k >= bias + TMAX else k - bias)
                    if q < t:
                        break
                    output.append(encode_digit(t + (q - t) % (BASE - t), 0))
                    q = (q - t) // (BASE - t)
                    k += BASE
                output.append(encode_digit(q, 0))
                bias = adapt(delta, h + 1, h == b)
                delta = 0
                h += 1
        delta += 1
        n += 1
    
    # Convert output code points to a string
    return ''.join(chr(cp) for cp in output)

def punycode_decode(input_str):
    """Decode a Punycode string to Unicode."""
    # Convert input string to a list of code points
    input_cps = [ord(c) for c in input_str]
    
    # Find the last delimiter
    last_delimiter = input_str.rfind(DELIMITER)
    if last_delimiter == -1:
        basic_cps = []
        encoded_cps = input_cps
    else:
        basic_cps = input_cps[:last_delimiter]
        encoded_cps = input_cps[last_delimiter + 1:]
    
    # Initialize state variables
    n = INITIAL_N
    i = 0
    bias = INITIAL_BIAS
    output = basic_cps.copy()
    
    # Main decoding loop
    while encoded_cps:
        oldi = i
        w = 1
        k = BASE
        while True:
            if not encoded_cps:
                raise ValueError("Invalid Punycode input")
            cp = encoded_cps.pop(0)
            digit = decode_digit(cp)
            if digit >= BASE:
                raise ValueError("Invalid Punycode input")
            i += digit * w
            t = TMIN if k <= bias else (TMAX if k >= bias + TMAX else k - bias)
            if digit < t:
                break
            w *= (BASE - t)
            k += BASE
        
        bias = adapt(i - oldi, len(output) + 1, oldi == 0)
        n += i // (len(output) + 1)
        i %= (len(output) + 1)
        
        # Insert the decoded code point
        output.insert(i, n)
        i += 1
    
    # Convert output code points to a string
    return ''.join(chr(cp) for cp in output)

# User interaction
if __name__ == "__main__":
    print("Punycode Encoder/Decoder")
    print("1. Encode Unicode to Punycode")
    print("2. Decode Punycode to Unicode")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        input_str = input("Enter a Unicode string: ")
        punycode_str = punycode_encode(input_str)
        print(f"Punycode: {punycode_str}")
    elif choice == "2":
        input_str = input("Enter a Punycode string: ")
        unicode_str = punycode_decode(input_str)
        print(f"Unicode: {unicode_str}")
    else:
        print("Invalid choice!")