import subprocess


def run_bandit() -> None:
    # bandit -c bandit.yaml -r . -f html -o bandit_report.html
    format_output = "html"
    configfile_name = "bandit.yaml"
    command = [
        "bandit",
        "-c",
        configfile_name,
        "-r",
        ".",
        "-f",
        format_output,
        "-o",
        f"bandit_report.{format_output}",
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(
            f"Bandit scan completed successfully. "
            f"Report saved to 'report_bandit.{format_output}'."
        )
    except subprocess.CalledProcessError as e:
        print(f"Error during Bandit scan:\n{e.stderr}")


def run_safety_check() -> None:
    # safety scan --output html --save-html output.html
    command = [
        "safety",
        "scan",
        "--output",
        "html",
        "--save-html",
        "output.html",
    ]

    print("Running safety scan...")
    with open("report_safety.html", "w") as f:
        subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

    print(
        "Safety scan completed successfully. "
        "Report saved to 'report_safety.html'."
    )


if __name__ == "__main__":
    run_bandit()
    run_safety_check()
