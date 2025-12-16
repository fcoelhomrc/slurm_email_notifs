"""CLI entry point for SLURM email notifications."""

import argparse
import sys
import time

from .notifier import SlurmNotifier


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Send email notifications for SLURM jobs",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Start command
    start_parser = subparsers.add_parser("start", help="Notify job start")
    start_parser.add_argument("--job-id", required=True, help="SLURM job ID")
    start_parser.add_argument("--job-name", required=True, help="Job name")
    start_parser.add_argument(
        "--submit-time",
        type=float,
        required=True,
        help="Unix timestamp when job was submitted",
    )

    # Finish command
    finish_parser = subparsers.add_parser("finish", help="Notify job finish")
    finish_parser.add_argument("--job-id", required=True, help="SLURM job ID")
    finish_parser.add_argument("--job-name", required=True, help="Job name")
    finish_parser.add_argument(
        "--start-time",
        type=float,
        required=True,
        help="Unix timestamp when job started",
    )
    finish_parser.add_argument(
        "--exit-code",
        type=int,
        required=True,
        help="Exit code of the job",
    )

    # Get-time command (utility to get current timestamp)
    subparsers.add_parser("get-time", help="Print current Unix timestamp")

    args = parser.parse_args()

    if args.command == "get-time":
        print(time.time())
        return

    notifier = SlurmNotifier()

    if args.command == "start":
        notifier.notify_job_start(
            job_id=args.job_id,
            job_name=args.job_name,
            submit_time=args.submit_time,
        )
    elif args.command == "finish":
        notifier.notify_job_finish(
            job_id=args.job_id,
            job_name=args.job_name,
            start_time=args.start_time,
            exit_code=args.exit_code,
        )


if __name__ == "__main__":
    main()
