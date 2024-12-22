# Binary to Decimal and Decimal to Binary Converter

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | **Leave a ⭐ if this project helped** | ![GitHub Repo stars](https://img.shields.io/github/stars/testspieler09/binary_converter)

</div>

## Supported formats

- Normal conversion (all binarys positive)
- Sign-Magnitude-Format (MSB -> also negative numbers possible)
- Ones complement
- Twos complement
- Fixed point
- IEEE 754 (with more precision less accuracy due to python)

## Example output

```
py binary_converter.py 1110-1111-0110 bin -n -s -o -t
```

```txt
================ Output ================
Normal conversion
3830

Sign-Magnitude-Format conversion
-1782

Ones complement conversion
-265

Twos complement conversion
-266
```

## Can be used as a library

Even though I wouldn't recommend it I wrote the class so that it is easy to use from a different python file.

The reason I do not recommend it is because it is not that efficient (due to python and the way i wrote the script).

### Not the most efficient way to convert them (probably)

The program uses the string representation of the bin and converts them by manipulating it. It doesn't use bitwise logic, but rather logic that we as humans can understand more easily.

## Help | Usage

**The following message is the output of `py binary_converter.py -h`**

```txt
usage: Bin-Dec-Converter [-h] [-B BITS] [-n] [-s] [-o] [-t] [-f] [-i] [-b] number {dec,bin}

Convert dezimal to binary or the other way around.

positional arguments:
  number                The number that should be converted.
  {dec,bin}             Specifies the base of the provided number.

options:
  -h, --help            show this help message and exit
  -B BITS, --bits BITS  Specify the number of bits the number should have (mostly for DEC->BIN)

Formats:
  -n, --normal          Convert a positive number.
  -s, --sign            Convert a number from or into sign-magnitude-format.
  -o, --ones            Convert a number from or into ones complement.
  -t, --twos            Convert a number from or into twos complement.
  -f, --fixed           Convert a number from or into fixed point format.
  -i, --ieee            Convert a number from or into IEEE 754 format.
  -b, --beautify        Make the output more readable.

If something isn't working please open an issue or open a pull request on [ https://github.com/Testspieler09/binary_converter ]
```
