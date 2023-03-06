from pathlib import Path
import subprocess
import tempfile
import re
from typing import List

submission_path = Path("./submission")
mvn_cli_path = "./mvn-cli"

# Based in https://doc.rust-lang.org/std/primitive.slice.html#method.chunks
# https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# monoid are awensome
# https://stackoverflow.com/a/952946
def flatten(lss: List[List]):
    return sum(lss, [])

def bflatten(lls):
    return bytes(flatten(lls))

def clean_memory_dump(btext: bytes):
    text = btext.decode("utf-8") 
    lines = text.split('\n')[:-1]

    result = []

    for l in lines:
        # Line example
        # 0d00:  00  00  00  02  00  04  00  06  00  08  00  0a  00  0c  00  0e
        values = [
            l[7:9],
            l[11:13],
            l[15:17],
            l[19:21],
            l[23:25],
            l[27:29],
            l[31:33],
            l[35:37],
            l[39:41],
            l[43:45],
            l[47:49],
            l[51:53],
            l[55:57],
            l[59:61],
            l[63:65],
            l[67:69],
        ]

        non_empty_values = [int(v, 16) for v in values if v.strip() != '']

        result.extend(non_empty_values)

    return bytes(result)



def run_mvn(input_text: str) -> str:
    p = subprocess.run(
        [
            "python", 
            "-m", 
            "MVN.mvnMonitor"
        ],
        input=input_text,
        capture_output=True, 
        text=True,
    )
    return p.stdout

def run_assemble(input_path: Path) -> str:
    p = subprocess.run(
        [
            f"{mvn_cli_path}", 
            "assemble",
            "-i", 
            input_path.as_posix()
        ],
        capture_output=True, 
        text=True,
    )
    # return generated code
    return p.stdout

def assemble_and_run_mvn(assembly_path: Path, memory_dump_limits: tuple[int, int] = (0, 0),  mvn_extra_input: list[str] = []) -> tuple[str, bytes]:
    absolute = run_assemble(assembly_path)

    absolute_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    absolute_file.write(absolute)

    (dump_down, dump_upper) = memory_dump_limits

    out_file = tempfile.NamedTemporaryFile(mode='rb')

    inputs = [
        # load
        f"p {absolute_file.name}",

        *mvn_extra_input,

        "r",
        "000",
        "", # yes
        "", # no

        # f"m {dump_down:04X} {dump_upper:04X} {out_file.name}",

        "x",
    ]

    mvn_out = run_mvn('\n'.join(inputs))
    return mvn_out, clean_memory_dump(out_file.read())

def test_1():
    absolute_file = submission_path / "op-mnem.asm"
    assert absolute_file.exists(), f"A submissão não contém o arquivo '{absolute_file.name}'"

    regex1="(\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4} 03(\d|a|b|c|d|e|f){2} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4}"
    regex2="(03\d|a|b|c|d|e|f){2} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4} (\d|a|b|c|d|e|f){4}"

    mvn_out, _ = assemble_and_run_mvn(absolute_file) 
    print(mvn_out)

    print("Sua nota será dada de acordo com a saída abaixo, que comtém a execução da sua rotina em 0x300\n")

    for linha in mvn_out.split("\n"):
        if re.search(regex1, linha) or re.search(regex2, linha):
            print(linha)

def test_2():
    absolute_file = submission_path / "stack.asm"
    assert absolute_file.exists(), f"A submissão não contém o arquivo '{absolute_file.name}'"

    mvn_out, _ = assemble_and_run_mvn(absolute_file, mvn_extra_input=[
    'r'
    'f00'
    ''
    ''
    'oi'
    ''
    'x'
        ]) 
    print(mvn_out)
