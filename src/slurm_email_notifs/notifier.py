"""Email notification utility for SLURM jobs."""

import os
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv


def _format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


class SlurmNotifier:
    """Send email notifications for SLURM jobs."""

    def __init__(self) -> None:
        """Initialize the notifier, loading config from $HOME/.env."""
        env_path = Path.home() / ".env"
        load_dotenv(env_path)

        self.smtp_server = os.environ["SLURM_EMAIL_SMTP_SERVER"]
        self.smtp_port = int(os.environ.get("SLURM_EMAIL_SMTP_PORT", "587"))
        self.smtp_user = os.environ["SLURM_EMAIL_SMTP_USER"]
        self.smtp_password = os.environ["SLURM_EMAIL_SMTP_PASSWORD"]
        self.sender_email = os.environ.get("SLURM_EMAIL_FROM", self.smtp_user)
        self.recipient_email = os.environ["SLURM_EMAIL_TO"]

    def _send_email(self, subject: str, body: str) -> None:
        """Send an email with the given subject and body."""
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = self.recipient_email

        text_part = MIMEText(body, "plain")
        message.attach(text_part)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls(context=context)
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(
                self.sender_email, self.recipient_email, message.as_string()
            )

    def notify_job_start(
        self,
        job_id: str,
        job_name: str,
        submit_time: float,
    ) -> None:
        """Send notification when a job starts.

        Args:
            job_id: SLURM job ID.
            job_name: Name of the job.
            submit_time: Unix timestamp when the job was submitted.
        """
        start_time = datetime.now()
        queue_duration = start_time.timestamp() - submit_time
        queue_str = _format_duration(queue_duration)

        subject = f"[SLURM] Job {job_name} ({job_id}) started (queued {queue_str})"
        body = f"""SLURM Job Started

Job ID: {job_id}
Job Name: {job_name}
Start Time: {start_time.strftime("%Y-%m-%d %H:%M:%S")}
Time in Queue: {queue_str}
"""
        self._send_email(subject, body)

    def notify_job_finish(
        self,
        job_id: str,
        job_name: str,
        start_time: float,
        exit_code: int,
    ) -> None:
        """Send notification when a job finishes.

        Args:
            job_id: SLURM job ID.
            job_name: Name of the job.
            start_time: Unix timestamp when the job started.
            exit_code: Exit code of the job.
        """
        end_time = datetime.now()
        run_duration = end_time.timestamp() - start_time
        run_str = _format_duration(run_duration)
        status = "SUCCESS" if exit_code == 0 else "FAILED"

        subject = f"[SLURM] Job {job_name} ({job_id}) {status} (runtime {run_str})"
        body = f"""SLURM Job Finished

Job ID: {job_id}
Job Name: {job_name}
Status: {status}
Exit Code: {exit_code}
End Time: {end_time.strftime("%Y-%m-%d %H:%M:%S")}
Runtime: {run_str}
"""
        self._send_email(subject, body)
