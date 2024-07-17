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
        pass

    # display and normalize methods
    @staticmethod
    def normalize_bin(bin: str) -> str:
        seperators = [" ", ".", "-"]
        for seperator in seperators:
            bin = bin.replace(seperator, "")
        return bin

    @staticmethod
    def fill_up_bits(bin: str, bits: int) -> str:
        bin = bin[::-1]
        bin += "0"*(bits-len(bin))
        return bin

    @staticmethod
    def space_bin_num(bin: str) -> str:
        idx = len(bin) % 4
        prefix = "" if idx == 0 else f"{bin[:idx]} "
        suffix = bin[idx:]
        suffix = ' '.join([suffix[i:i+4] for i in range(0, len(suffix), 4)])
        return f'{prefix}{suffix}'


    # Normal binary conversion
    @staticmethod
    def bin_to_dec(bin: str) -> str:
        bin = Converter.normalize_bin(bin)
        dec = 0
        for idx, num in enumerate(bin[::-1]):
            if num=="0": continue
            dec += 2**idx
        return dec

    @staticmethod
    def dec_to_bin(dec: str, bits=32) -> str:
        dec = int(dec)
        if dec < 0: return

        ans, rest = dec//2, dec%2
        bin = f"{rest}"
        while True:
            if ans == 0: break
            ans, num = ans//2, ans%2
            bin += str(num)

        length_bin = len(bin)
        if length_bin < bits:
            bin = Converter.fill_up_bits(bin, bits)
        elif length_bin > bits:
            print(f"Stackoverflow: length of number -> {length_bin}; bitsize -> {bits}")
        return Converter.space_bin_num(bin[::-1])

    # Sign-Magnitude
    @staticmethod
    def sign_magnitude_to_dec(bin: str) -> str:
        pass

    @staticmethod
    def dec_to_sign_magnitude(dec: str, bits=32) -> str:
        pass

if __name__ == "__main__":
    con = Converter()
    print(con.dec_to_bin("0", 10))
