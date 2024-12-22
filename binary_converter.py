from argparse import ArgumentParser, Namespace


class Converter:
    """
    Convert dezimal to binary or the other way around.
    Supported formats are:
        - Normal binary
        - Sign-Magnitude Representation
        - Ones' Complement
        - Two's Complement
        - Fixed point
        - IEEE 754 Floating-Point
    """

    def __init__(self) -> None:
        self.FIXED_VALUES = [[8, 23, 127], [11, 52, 1023]]

    # wrapper
    @staticmethod
    def is_normalized_binary(func):
        """
        A wrapper to make shure that a correctly formated string is passed (binary)
        """

        def wrapper(binary_str, *args):
            # Check if input is a string
            if not isinstance(binary_str, str):
                binary_str = str(binary_str)

            # normalize input
            binary_str = Converter.normalize_bin(binary_str)

            # Check if input is a binary string
            if not all(char in "01" for char in binary_str):
                raise ValueError(
                    "Input must be a binary string containing only '0' and '1'."
                )

            return func(binary_str, *args)

        return wrapper

    @staticmethod
    def is_normalized_decimal(func):
        """
        A wrapper to make shure that a correctly formated string is passed (integers)
        """

        def wrapper(decimal_str, *args):
            # Check if input is a string
            if not isinstance(decimal_str, str):
                decimal_str = str(decimal_str)

            # Check if it is an integer
            try:
                int(decimal_str)
            except Exception as e:
                raise e

            return func(decimal_str, *args)

        return wrapper

    @staticmethod
    def is_normalized_float(func):
        """
        A wrapper to make shure that a correctly formated string is passed (floats)
        """

        def wrapper(decimal_str, *args):
            object_self = None
            # Check if input is a string
            if isinstance(decimal_str, object):
                object_self = decimal_str
                decimal_str = args[0]
            if not isinstance(decimal_str, str):
                decimal_str = str(decimal_str)

            # Check if it is an float
            try:
                decimal_str = decimal_str.replace(",", ".")
                float(decimal_str)
            except Exception as e:
                raise e

            return func(object_self, *args)

        return wrapper

    # display and normalize methods
    @staticmethod
    def normalize_bin(bin: str) -> str:
        seperators = [" ", ".", "-"]
        for seperator in seperators:
            bin = bin.replace(seperator, "")
        return bin

    @staticmethod
    def fill_up_bits(bin: str, bits: int) -> str:
        bin += "0" * (bits - len(bin))
        return bin

    @staticmethod
    @is_normalized_binary
    def space_bin_num(bin: str) -> str:
        bin = bin.replace(" ", "")  # normalize if it was spaced before
        idx = len(bin) % 4
        prefix = "" if idx == 0 else f"{bin[:idx]} "
        suffix = bin[idx:]
        suffix = " ".join([suffix[i : i + 4] for i in range(0, len(suffix), 4)])
        return f"{prefix}{suffix}"

    # Normal binary conversion
    @staticmethod
    @is_normalized_binary
    def bin_to_dec(bin: str) -> str:
        dec = 0
        for idx, num in enumerate(bin[::-1]):
            if num == "0":
                continue
            dec += 2**idx
        return str(dec)

    @staticmethod
    @is_normalized_decimal
    def dec_to_bin(p_dec: str, bits=32) -> str:
        dec: int = int(p_dec)
        if dec < 0:
            return "Can't convert a negative number to a normal bin!"

        ans, rest = dec // 2, dec % 2
        bin = f"{rest}"
        while True:
            if ans == 0:
                break
            ans, num = ans // 2, ans % 2
            bin += str(num)

        length_bin = len(bin)
        if length_bin < bits:
            bin = Converter.fill_up_bits(bin, bits)
        elif length_bin > bits:
            print(f"Stackoverflow: length of number -> {length_bin}; bitsize -> {bits}")
        return bin[::-1]

    # Sign-Magnitude
    @staticmethod
    @is_normalized_binary
    def sign_magnitude_to_dec(bin: str) -> str:
        msb = bin[0]
        sign = "-" if msb == "1" else "(+)"
        num = Converter.bin_to_dec(bin[1:])
        return f"{sign}{num}"

    @staticmethod
    @is_normalized_decimal
    def dec_to_sign_magnitude(p_dec: str, bits=32) -> str:
        dec = int(p_dec)
        msb = "1" if dec < 0 else "0"
        num = Converter.dec_to_bin(str(abs(dec)), bits - 1)
        return f"{msb}{num}"

    # Ones' Complement
    @staticmethod
    @is_normalized_binary
    def ones_complement_to_dec(bin: str) -> str:
        msb = bin[0]
        sign = "-" if msb == "1" else "(+)"
        if msb == "1":
            new_bin = "".join(str(1 - int(i)) for i in bin)
            num = Converter.bin_to_dec(new_bin)
        else:
            num = Converter.bin_to_dec(bin)
        return f"{sign}{num}"

    @staticmethod
    @is_normalized_decimal
    def dec_to_ones_complement(p_dec: str, bits=32) -> str:
        dec = int(p_dec)
        msb = "1" if dec < 0 else "0"
        num = Converter.dec_to_bin(str(abs(dec)), bits - 1)
        if num is None:
            return "Something went wrong"
        if msb == "1":
            num = "".join(str(1 - int(i)) for i in num)
        return f"{msb}{num}"

    # Two's Complement
    @staticmethod
    @is_normalized_binary
    def twos_complement_to_dec(bin: str) -> str:
        ans = Converter.ones_complement_to_dec(bin)
        if ans[0] == "-":
            num = int(ans[1:])
            ans = f"{ans[0]}{num+1}"
        return ans

    @staticmethod
    @is_normalized_decimal
    def dec_to_twos_complement(dec: str, bits=32) -> str:
        ans = Converter.dec_to_ones_complement(dec, bits)
        if ans[0] == "1":
            ans_list = list(ans[1:][::-1])
            for idx in range(len(ans_list)):
                if ans_list[idx] == "0":
                    ans_list[idx] = "1"
                    break
                ans_list[idx] = "0"
            ans = f"1{''.join(ans_list[::-1])}"
        return ans

    # Fixed Point
    @staticmethod
    @is_normalized_binary
    def fixed_point_to_dec(bin: str, k: int, j: int) -> str:
        if len(bin) != k + j + 1:
            return f"Binary number has a length of {len(bin)} but should have a length of {k+j+1}"
        int_part: str = Converter.sign_magnitude_to_dec(bin[: k + 1])
        comma_value: float = 0
        for idx, num in enumerate(bin[k + 1 :]):
            if num == "0":
                continue
            comma_value += 2 ** -(idx + 1)
        return f"{int_part}{str(comma_value)[1:]}"

    @staticmethod
    @is_normalized_float
    def dec_to_fixed_point(p_dec: str, k: int, j: int) -> str:
        dec = float(p_dec)
        if not (k > 0 and isinstance(k, int)) or not (j > 0 and isinstance(j, int)):
            return "`k` and `j` must be integers and can't be 0 or negative."
        int_part: str = Converter.dec_to_sign_magnitude(str(int(dec)), k + 1)
        comma_part: float = abs(dec) % 1
        ans = comma_part * 2
        if ans >= 1:
            ans, rest = ans - 1, 1
        else:
            rest = 0
        comma_value: str = f"{rest}"
        counter = 1
        while True:
            if ans == 0 or counter == j:
                break
            ans = ans * 2
            if ans >= 1:
                ans, num = ans - 1, 1
            else:
                num = 0
            comma_value += str(num)
            counter += 1
        if len(comma_value) < j:
            comma_value = Converter.fill_up_bits(comma_value, j)
        return f"{int_part}{comma_value}"

    @is_normalized_binary
    def ieee_to_dec(self, bin: str, bits=32) -> str:
        """
        An algortihm that converts a binary in IEEE 754 format to a decimal.
        Accuracy gets increasingly worse with more precise values (due to python).
        """
        if bits not in [32, 64]:
            return "IEEE 754 needs to have 32 or 64Bit"
        if len(bin) != bits:
            return f"The provided binary has a size of {len(bin)} Bit but {bits} are needed."

        C, M, B = self.FIXED_VALUES[(bits // 32) - 1]

        msb, int_part, comma_part = bin[0], bin[1 : C + 1], bin[C + 1 :]

        mantisse_all_zero = all(i == "0" for i in comma_part)
        characteristic_all_ones = all(i == "1" for i in int_part)
        characteristic_all_zero = all(i == "0" for i in int_part)

        if mantisse_all_zero and characteristic_all_zero:
            return "+0" if msb == "0" else "-0"
        elif mantisse_all_zero and characteristic_all_ones:
            return "+inf" if msb == "0" else "-inf"
        elif not mantisse_all_zero and characteristic_all_ones:
            return "NaN"

        int_part = Converter.bin_to_dec(int_part)

        E = int(int_part) - B  # calc exponent

        # Convert to fixed point format
        if E < 0:
            comma_part = msb + "0" * abs(E) + "1" + comma_part
            k, j = 1, len(comma_part) - 2
        else:
            comma_part = f"{msb}1" + comma_part
            k, j = E + 1, M - E

        return Converter.fixed_point_to_dec(comma_part, k, j)

    @is_normalized_float
    def dec_to_ieee(self, p_dec: str, bits=32) -> str:
        dec = float(p_dec)
        if bits not in [32, 64]:
            return "IEEE 754 needs to have 32 or 64Bit"

        C, M, B = self.FIXED_VALUES[(bits // 32) - 1]

        msb = "1" if dec < 0 else "0"

        # int_part
        m_dec = abs(int(dec))
        ans, rest = m_dec // 2, m_dec % 2
        int_part = f"{rest}"
        while True:
            if ans == 0:
                break
            ans, num = ans // 2, ans % 2
            int_part += str(num)

        # comma_part
        j = bits - len(int_part) - 1
        comma_part: float = abs(dec) % 1
        ans = comma_part * 2
        if ans >= 1:
            ans, rest = ans - 1, 1
        else:
            rest = 0
        comma_value: str = f"{rest}"
        counter = 1
        while True:
            if ans == 0 or counter == j:
                break
            ans = ans * 2
            if ans >= 1:
                ans, num = ans - 1, 1
            else:
                num = 0
            comma_value += str(num)
            counter += 1
        if len(comma_value) < j:
            comma_value = Converter.fill_up_bits(comma_value, j)
        whole_num, comma_idx = "".join([int_part, comma_value]), len(int_part) - 1
        try:
            idx = whole_num.index("1")
            mantisse = whole_num[idx : idx + M]
            E = idx - comma_idx
        except ValueError:
            return "0" * bits

        charakteristik = Converter.dec_to_bin(str(E + B), C)
        return f"{msb}{charakteristik}{mantisse}"


def main(args: Namespace) -> None:
    num, base, bits = (
        args.number,
        getattr(args, "type of number", None),
        32 if args.bits is None else args.bits,
    )
    output = []
    match base:
        case "bin":
            if args.normal:
                try:
                    output.append(["Normal conversion\n", Converter.bin_to_dec(num)])
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.sign:
                try:
                    output.append(
                        [
                            "Sign-Magnitude-Format conversion\n",
                            Converter.sign_magnitude_to_dec(num),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.ones:
                try:
                    output.append(
                        [
                            "Ones complement conversion\n",
                            Converter.ones_complement_to_dec(num),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.twos:
                try:
                    output.append(
                        [
                            "Twos complement conversion\n",
                            Converter.twos_complement_to_dec(num),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.fixed:
                try:
                    k = int(
                        input(
                            "Please provide how many bits should be reserved for the integer part: "
                        )
                    )
                    j = int(
                        input(
                            "Please provide how many bits should be reserved for the comma part: "
                        )
                    )
                    output.append(
                        [
                            "Fixed point conversion\n",
                            Converter.fixed_point_to_dec(num, k, j),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.ieee:
                try:
                    output.append(
                        ["IEEE 754 conversion\n", Converter.ieee_to_dec(num, str(bits))]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
        case "dec":
            if args.normal:
                try:
                    output.append(
                        ["Normal conversion\n", Converter.dec_to_bin(num, bits)]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.sign:
                try:
                    output.append(
                        [
                            "Sign-Magnitude-Format conversion\n",
                            Converter.dec_to_sign_magnitude(num, bits),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.ones:
                try:
                    output.append(
                        [
                            "Ones complement conversion\n",
                            Converter.dec_to_ones_complement(num, bits),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.twos:
                try:
                    output.append(
                        [
                            "Twos complement conversion\n",
                            Converter.dec_to_twos_complement(num, bits),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.fixed:
                try:
                    k = int(
                        input(
                            "Please provide how many bits should be reserved for the integer part: "
                        )
                    )
                    j = int(
                        input(
                            "Please provide how many bits should be reserved for the comma part: "
                        )
                    )
                    output.append(
                        [
                            "Fixed point conversion\n",
                            Converter.dec_to_fixed_point(num, k, j),
                        ]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")
            if args.ieee:
                try:
                    output.append(
                        ["IEEE 754 conversion\n", Converter.dec_to_ieee(num, str(bits))]
                    )
                except Exception as e:
                    print(f"Something went wrong.\n{e}")

    if output == []:
        print(
            f"The number {num} could not be converted in any format (None was given or the number was not of the {base} format)"
        )
        return

    if args.beautify:
        if base == "dec":
            m_output = []
            for entry in output:
                try:
                    m_output.append([entry[0], Converter.space_bin_num(entry[1])])
                except Exception:
                    m_output.append(entry)
            output = m_output
        elif base == "bin":
            m_output = []
            for entry in output:
                try:
                    t = (
                        entry[1].replace("(", "").replace(")", "")
                        if all(i in entry[1] for i in "()")
                        else entry[1]
                    )
                    entry[1] = float(t) if "." in t else int(t)
                    m_output.append([entry[0], f"{entry[1]:_}"])
                except Exception:
                    m_output.append(entry)
            output = m_output

    print("================ Output ================")
    for format in output:
        print("".join(format) + "\n")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Bin-Dec-Converter",
        description="Convert dezimal to binary or the other way around.",
        epilog="If something isn't working please open an issue or open a pull request on [ https://github.com/Testspieler09/binary_converter ]",
    )

    parser.add_argument("number", type=str, help="The number that should be converted.")
    parser.add_argument(
        "type of number",
        choices=["dec", "bin"],
        help="Specifies the base of the provided number.",
    )
    parser.add_argument(
        "-B",
        "--bits",
        type=int,
        help="Specify the number of bits the number should have (mostly for DEC->BIN)",
    )

    formats = parser.add_argument_group("Formats")
    formats.add_argument(
        "-n", "--normal", action="store_true", help="Convert a positive number."
    )
    formats.add_argument(
        "-s",
        "--sign",
        action="store_true",
        help="Convert a number from or into sign-magnitude-format.",
    )
    formats.add_argument(
        "-o",
        "--ones",
        action="store_true",
        help="Convert a number from or into ones complement.",
    )
    formats.add_argument(
        "-t",
        "--twos",
        action="store_true",
        help="Convert a number from or into twos complement.",
    )
    formats.add_argument(
        "-f",
        "--fixed",
        action="store_true",
        help="Convert a number from or into fixed point format.",
    )
    formats.add_argument(
        "-i",
        "--ieee",
        action="store_true",
        help="Convert a number from or into IEEE 754 format.",
    )
    formats.add_argument(
        "-b", "--beautify", action="store_true", help="Make the output more readable."
    )

    args = parser.parse_args()

    main(args)
