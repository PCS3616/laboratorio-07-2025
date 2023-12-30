from pathlib import Path
from tempfile import NamedTemporaryFile

from utils import executable, run_mvn, SUBMISSION_PATH

def limpa(string):
    res=string.split(" ")
    res=list(filter(None, res))
    return int(res[1]+res[2],16)

def fatorial(n: int):
  if n <= 1:
    return 1
  return n*fatorial(n-1)

def test(n: int = 0):
    filecode = executable(SUBMISSION_PATH / "fatorial")
    assert filecode.exists(), f"A submissão não contém o arquivo '{filecode.name}'"

    n_str = "{:04X}".format(n)
    input_file = NamedTemporaryFile(mode='w')
    input_file.writelines([
        f"0100	{n_str}\n"
    ])
    input_file.flush()

    output_file = NamedTemporaryFile(mode='r')

    inputs = [
        f"p {filecode.as_posix()}",
        "",
        f"p {input_file.name}",
        "",
        "r",
        "0",
        "n",
        "",
        f"m 0102 0103 {output_file.name}",
        "",
        "x",
        "",
    ]

    run_mvn('\n'.join(inputs))

    fat = limpa(output_file.read())

    assert fat == fatorial(n), \
      f"Seu código não está correto\nConfira seu envio."

def test_1():
  test(0)

def test_2():
  test(1)

def test_3():
  test(4)

def test_4():
  test(5)
