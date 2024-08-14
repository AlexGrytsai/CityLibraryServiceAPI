import logging
import os
import subprocess

from django.core.management import execute_from_command_line
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("security_checking")

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "CityLibraryServiceAPI.settings"
)
execute_from_command_line(["manage.py", "check"])


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
        logger.info("Running bandit scan...")
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.info(
            "Bandit scan completed successfully. "
            "Report saved to 'report_bandit.{format_output}'."
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during Bandit scan: {e}")


def run_safety_check() -> None:
    # safety --stage production scan --key=<API_KEY> --output html --save-html output.html
    api_key = os.environ.get("SAFETY_API_KEY")
    command = [
        "safety",
        "--stage",
        "production",
        "scan",
        f"--key={api_key}",
        "--output",
        "html",
        "--save-html",
        "output.html",
    ]

    logger.info("Running safety scan...")
    try:
        with open("report_safety.html", "w") as f:
            subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
        logger.info(
            "Safety scan completed successfully. "
            "Report saved to 'report_safety.html'."
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during safety scan: {e}")


if __name__ == "__main__":
    run_bandit()
    run_safety_check()
