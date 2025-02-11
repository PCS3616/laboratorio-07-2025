from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from utils import executable, run_mvn, SUBMISSION_PATH

TEST_MAIN_ASSEMBLY = """
  0000 0300 ;  Desvio para MAIN
  0002 000F ;  Variável OPCODE
  0004 0000 ;  Variável MNEM

  0300 070C ; Desvio para a outra main

  0700 {opcode}
  0702 {mnemonic}
  0704 {run_opcode_to_mnemonic}
  0706 0009
  0708 2020
  070A 2000

  ; Reset program variables to prevent cheating
  070C 3000
  070E 9002
  0710 9004

  ; Decide which subroutine to execute
  0712 8704
  0714 172C

  ; Run OP2MNEM
  0716 8700
  0718 9002
  071A A100
  071C 8004
  071E E300
  ; Reset program variables to prevent cheating
  0720 3000
  0722 9002
  0724 9004
  ; Print spaces to the output file
  0726 8708
  0728 E300
  072A 0744

  072C 8702
  072E 9004
  0730 A200
  0732 8706
  0734 5002  ; If 9 - OPCODE < 0 => OPCODE > 9 => OPCODE >= 10
  0736 273C  ; so it should be encoded as a letter;
  0738 3030  ; Otherwise, it should be encoded as a digit
  073A 073E
  073C 3037  ; "A" - 10
  073E 4002  ; Codify OPCODE as ASCII as hex digit
  0740 470A
  0742 E300

  ; END -> HALT
  0744 C000
"""

MNEMONICS = [
    "JP",
    "JZ",
    "JN",
    "LV",
    "AD",
    "SB",
    "ML",
    "DV",
    "LD",
    "MM",
    "SC",
    "RS",
    "HM",
    "GD",
    "PD",
    "OS",
]

OPCODES = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]


def main_file(
        run_mnemonic: bool,
        run_opcode: bool,
        mnemonic: str = "XX",
        opcode: str = "0",
) -> Path:
    file = NamedTemporaryFile("w", encoding="utf8")
    opcode = "000" + opcode
    mnemonic = str(hex(ord(mnemonic[0])*256 + ord(mnemonic[1])))
    run_opcode_to_mnemonic = "{:04X}".format(run_opcode and not run_mnemonic)
    file.write(TEST_MAIN_ASSEMBLY.format(
        run_opcode_to_mnemonic=run_opcode_to_mnemonic,
        mnemonic=mnemonic,
        opcode=opcode
    ))
    file.flush()
    return file


def run_op2mnem(opcode: str) -> str:
    with NamedTemporaryFile("r") as output_file:
        main = main_file(False, True, opcode=opcode)
        main_filepath = Path(main.name)
        subroutine = SUBMISSION_PATH / "op-mnem"
        subroutine_filepath = executable(subroutine)

        run_mvn("\n".join((
            "s", "a", "3", "00", output_file.name, "e",
            f"p {subroutine_filepath}",
            "1", "23",
            f"p {main_filepath}",
            "r", "300", "n",
            "x",
        )))

        return output_file.read()


def run_mnem2op(mnemonic: str):
    with NamedTemporaryFile("r") as output_file:
        main = main_file(True, False, mnemonic=mnemonic)
        main_filepath = Path(main.name)
        subroutine = SUBMISSION_PATH / "op-mnem"
        subroutine_filepath = executable(subroutine)
        run_mvn("\n".join((
            "s", "a", "3", "00", output_file.name, "e",
            f"p {subroutine_filepath}",
            "1", "23",
            f"p {main_filepath}",
            "r", "300", "n",
            "x",
        )))

        return output_file.read()


@pytest.mark.parametrize("mnemonic,opcode", zip(MNEMONICS, OPCODES))
def test_op2mnem(tmp_path: Path, mnemonic: str, opcode: str):
    result = run_op2mnem(opcode)
    result = result.strip().upper()
    assert result == mnemonic


@pytest.mark.parametrize("mnemonic,opcode", zip(MNEMONICS, OPCODES))
def test_mnem2op(tmp_path: Path, mnemonic: str, opcode: str):
    result = run_mnem2op(mnemonic)
    result = result.strip().upper()
    assert result == opcode
