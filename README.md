# Installation

Simply `git clone` this repo to your remote server and run `uv sync`. 

# Usage 

Create a `.env` file in your `$HOME` directory, with the following:

```
SLURM_EMAIL_SMTP_SERVER=smtp.gmail.com  # or other provider
SLURM_EMAIL_SMTP_PORT=587                          # optional, defaults to 587
SLURM_EMAIL_SMTP_USER=<insert stmp email>
SLURM_EMAIL_SMTP_PASSWORD=<insert stmp token>
SLURM_EMAIL_FROM=$SLURM_EMAIL_STMP_USER            # optional, defaults to SMTP_USER
SLURM_EMAIL_TO=<insert target email>
```

Do youself a favor and DO NOT push your `.env` files to a public repo.
