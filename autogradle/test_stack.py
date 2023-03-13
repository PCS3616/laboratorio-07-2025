from pathlib import Path
from tempfile import NamedTemporaryFile

from utils import executable, run_mvn, SUBMISSION_PATH


MAIN_BASE = """
    < EMPI
    < DEMP
    < VALOR
            @ /0
            JP TMAIN

            @ /F00

    NINE    K  =9
    SPACES  K /2020
    USPACE  K /2000
    M       $ =1
    M2ASCII $ =1
            LD NINE
            SB M       ; If 9 - M < 0 => M > 9 => M >= 10
            JN AZ      ; so it should be encoded as a letter;
            LV /30     ; Otherwise, it should be encoded as a digit
            JP TOASCII
    AZ      LV /37     ; "A" - 10
    TOASCII AD M       ; Codify M as ASCII as hex digit
            AD USPACE  ; Add /20 to upper byte to avoid printing \0
            RS M2ASCII

    TMAIN   LV /0      ; Placeholder which cannot be zero, since zero is JP
"""

def push(value: int) -> str:
    return f"""
        LV /{value}
        MM VALOR
        SC EMPI
        ; Zero VALOR to prevent cheating
        LV /0
        MM VALOR
    """

def pop() -> str:
    return """
        SC DEMP
        LD VALOR
        MM M
        SC M2ASCII
        PD /300
        ; Zero VALOR to prevent cheating
        LV /0
        MM VALOR
    """


def main_file(content: str) -> Path:
    file = NamedTemporaryFile("w", encoding="utf8")
    file.write(content)
    file.flush()
    return file


def _test_commands(output_dir: Path, main_code: str, expected: str | list[str]):
    with NamedTemporaryFile("r") as output_file:
        main = main_file(
            MAIN_BASE
            + main_code
            + "\n HM /0"
        )
        main_filepath = Path(main.name)
        subroutine = SUBMISSION_PATH / "stack.asm"
        executable_filepath = executable(output_dir, main_filepath, subroutine)

        run_mvn("\n".join((
            "s", "a", "3", "00", output_file.name, "e",
            f"p {executable_filepath}",
            "r", "0", "n",
            "x",
        )))

        output = output_file.read().strip().split()
        assert len(output) == len(expected)
        assert all(
            output == expected for output, expected in zip(output, expected)
        )


def test_push_pop_one_element(tmp_path: Path):
    """
    Tests that pushing a single element onto the stack and then popping it
    off returns the same element.
    """
    commands = "\n".join((
        push(1),
        pop(),
    ))
    expected = "1"
    _test_commands(tmp_path, commands, expected)


def test_push_pop_multiple_elements(tmp_path: Path):
    """
    Tests that pushing multiple elements onto the stack and then popping
    them off returns the elements in the correct order.
    """
    commands = "\n".join((
        push(1),
        push(2),
        push(3),
        pop(),
        pop(),
        pop(),
    ))
    expected = ["3", "2", "1"]
    _test_commands(tmp_path, commands, expected)


def test_push_pop_same_element(tmp_path: Path):
    """
    Tests that pushing the same element onto the stack multiple times and
    then popping it off returns the same element every time.
    """
    commands = "\n".join((
        push(1),
        push(1),
        push(1),
        pop(),
        pop(),
        pop(),
    ))
    expected = ["1"] * 3
    _test_commands(tmp_path, commands, expected)
