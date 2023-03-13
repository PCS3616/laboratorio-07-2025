from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from utils import executable, run_mvn, SUBMISSION_PATH


TEST_MAIN_ASSEMBLY = """
    < OP2MNEM
    < MNEM2OP
    < OPCODE
    < MNEM

    @ /300
    MAIN    JP  TMAIN

    @ /700
    TOPCODE K  /{opcode}
    TMNEM   K  "{mnemonic}
    O2M     K  ={run_opcode_to_mnemonic}
    NINE    K  =9
    SPACES  K /2020
    USPACE  K /2000

    ; Reset program variables to prevent cheating
    TMAIN   LV /0
            MM OPCODE
            MM MNEM

            ; Decide which subroutine to execute
            LD O2M
            JZ RM2O

            ; Run OP2MNEM
    RO2M    LD TOPCODE
            MM OPCODE
            SC OP2MNEM
            LD MNEM
            PD /300
            ; Reset program variables to prevent cheating
            LV /0
            MM OPCODE
            MM MNEM
            ; Print spaces to the output file
            LD SPACES
            PD /300
            JP END

            ; Run MNEM2OP
    RM2O    LD TMNEM
            MM MNEM
            SC MNEM2OP
            LD NINE
            SB OPCODE      ; If 9 - OPCODE < 0 => OPCODE > 9 => OPCODE >= 10
            JN AZ          ; so it should be encoded as a letter;
            LV /30         ; Otherwise, it should be encoded as a digit
            JP TOASCII
    AZ      LV /37         ; "A" - 10
    TOASCII AD OPCODE      ; Codify OPCODE as ASCII as hex digit
            AD USPACE
            PD /300

    END     HM /0
    # MAIN
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
    file.write(TEST_MAIN_ASSEMBLY.format(
        run_opcode_to_mnemonic=int(run_opcode and not run_mnemonic),
        mnemonic=mnemonic,
        opcode=opcode
    ))
    file.flush()
    return file


def run_op2mnem(output_dir: Path, opcode: str) -> str:
    with NamedTemporaryFile("r") as output_file:
        main = main_file(False, True, opcode=opcode)
        main_filepath = Path(main.name)
        subroutine = SUBMISSION_PATH / "op-mnem.asm"
        executable_filepath = executable(output_dir, main_filepath, subroutine)

        run_mvn("\n".join((
            "s", "a", "3", "00", output_file.name, "e",
            f"p {executable_filepath}",
            "r", "300", "n",
            "x",
        )))

        return output_file.read()



def run_mnem2op(output_dir: Path, mnemonic: str):
    with NamedTemporaryFile("r") as output_file:
        main = main_file(True, False, mnemonic=mnemonic)
        main_filepath = Path(main.name)
        subroutine = SUBMISSION_PATH / "op-mnem.asm"
        executable_filepath = executable(output_dir, main_filepath, subroutine)

        run_mvn("\n".join((
            "s", "a", "3", "00", output_file.name, "e",
            f"p {executable_filepath}",
            "r", "300", "n",
            "x",
        )))

        return output_file.read()


@pytest.mark.parametrize("mnemonic,opcode", zip(MNEMONICS, OPCODES))
def test_op2mnem(tmp_path: Path, mnemonic: str, opcode: str):
    result = run_op2mnem(tmp_path, opcode)
    result = result.strip().upper()
    assert result == mnemonic


@pytest.mark.parametrize("mnemonic,opcode", zip(MNEMONICS, OPCODES))
def test_mnem2op(tmp_path: Path, mnemonic: str, opcode: str):
    result = run_mnem2op(tmp_path, mnemonic)
    result = result.strip().upper()
    assert result == opcode
