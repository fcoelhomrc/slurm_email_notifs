#!/bin/bash
#
#SBATCH --partition=gpu_min32gb       # Partition where the job will be run. Check with "$ sinfo".
#SBATCH --qos=gpu_min32gb             # QoS level. Must match the partition name. External users must add the suffix "_ext". Check with "$sacctmgr show qos".
#SBATCH --job-name=JobName            # Job name
#SBATCH -o slurm_%x.%j.out            # File containing STDOUT output

# ======== Do not change ========
SLURM_EMAIL_NOTIFS_PATH="$HOME/utils/slurm_email_notifs"

# Email notification setup
notify_cmd="uv run --project $SLURM_EMAIL_NOTIFS_PATH slurm-notify"
# ===============================

# Command to run
application=""

# Options to pass
options=""

SUBMIT_TIME=${SLURM_SUBMIT_TIME:-$(squeue -j $SLURM_JOB_ID -h -o "%V" | xargs -I{} date -d {} +%s 2>/dev/null || date +%s)}
START_TIME=$(date +%s.%N)

# Send start notification
$notify_cmd start \
    --job-id "$SLURM_JOB_ID" \
    --job-name "$SLURM_JOB_NAME" \
    --submit-time "$SUBMIT_TIME" || true

echo "Running command $application $options"
$application $options
EXIT_CODE=$?

# Send finish notification
$notify_cmd finish \
    --job-id "$SLURM_JOB_ID" \
    --job-name "$SLURM_JOB_NAME" \
    --start-time "$START_TIME" \
    --exit-code "$EXIT_CODE" || true

exit $EXIT_CODE
