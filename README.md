# PunyCode

A pure Python implementation of the Punycode algorithm (RFC 3492) for encoding and decoding Unicode domain names.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## Overview

PunyCode is a specialized encoding syntax used to convert Unicode strings into the limited character subset of ASCII supported by the Domain Name System (DNS). This implementation provides a clean, efficient, and RFC-compliant way to encode and decode Punycode strings in Python.

## Features

- 🔄 Bidirectional conversion between Unicode and Punycode
- 📜 Full compliance with RFC 3492 specifications
- 🐍 Pure Python implementation with no external dependencies
- 🌐 Support for both basic ASCII and non-ASCII Unicode characters
- 📚 Comprehensive documentation and examples
- ✅ Easy-to-use interface

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/PunyCode.git
cd PunyCode
```

No additional dependencies are required as this is a pure Python implementation.

## Usage

### As a Command Line Tool

```bash
python punycode.py
```

Follow the interactive prompts to encode or decode strings.

### As a Python Module

```python
from punycode import punycode_encode, punycode_decode

# Encoding example
unicode_str = "München"
encoded = punycode_encode(unicode_str)
print(encoded)  # Output: "Mnchen-3ya"

# Decoding example
punycode_str = "Mnchen-3ya"
decoded = punycode_decode(punycode_str)
print(decoded)  # Output: "München"
```

## Technical Details

The implementation uses several parameters as defined in RFC 3492:

- `BASE`: 36 (using digits 0-9 and letters a-z)
- `TMIN`: 1
- `TMAX`: 26
- `SKEW`: 38
- `DAMP`: 700
- `INITIAL_BIAS`: 72
- `INITIAL_N`: 0x80
- `DELIMITER`: '-'

### Algorithm Overview

1. **Encoding Process**:
   - Basic ASCII characters are preserved
   - Non-ASCII characters are encoded using a delta-compression scheme
   - Results are represented using base-36 encoding

2. **Decoding Process**:
   - Splits input at the last delimiter
   - Processes basic and non-basic code points separately
   - Reconstructs the original Unicode string

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

To run tests (when implemented):

```bash
python -m unittest tests/test_punycode.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [RFC 3492 - Punycode](https://tools.ietf.org/html/rfc3492)
- [Unicode Technical Standard #46](https://unicode.org/reports/tr46/)
- [IDNA - Wikipedia](https://en.wikipedia.org/wiki/Internationalized_domain_name#IDNA)

## Author

Avik Chatterjee

## Acknowledgments

- Thanks to the authors of RFC 3492 for the detailed specification
- The Unicode Consortium for their standards and documentation 