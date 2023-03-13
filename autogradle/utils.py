from pathlib import Path
import subprocess


SUBMISSION_PATH = Path('./submission')


def mvn_cli(arguments: list[str], output_filepath: str | Path):
    command = ["./mvn-cli"] + arguments
    with open(output_filepath, "w", encoding="utf8") as output_file:
        subprocess.run(command, check=True, stdout=output_file)


def executable(output_dir: Path, main: Path, *subroutines: Path) -> Path:
    main_filename = output_dir / main.stem

    for subroutine in subroutines:
        mvn_cli(f"assemble -i {subroutine}".split(), f"{output_dir / subroutine.stem}.int")
    mvn_cli(f"assemble -i {main}".split(), f"{main_filename}.int")

    link_arguments = []
    for subroutine in subroutines + (main,):
        link_arguments.append("-i")
        link_arguments.append(f"{output_dir / subroutine.stem}.int")
    link_arguments.insert(0, "link")
    link_arguments.append("--complete")

    mvn_cli(link_arguments, f"{main_filename}.lig")

    executable_filepath = Path(f"{main_filename}.mvn")
    mvn_cli(f"relocate -i {main_filename}.lig --base 0".split(), executable_filepath)

    return executable_filepath


def run_mvn(input_text: str):
    p = subprocess.run(
        [
            "python",
            "-m",
            "MVN.mvnMonitor"
        ],
        input=input_text,
        capture_output=True,
        text=True,
        check=True,
    )
    return p.stdout
