# Cron Job Provider Mismatch Fix

## Issue
A cron job fails with error:
```
RuntimeError: Provider 'gemini' is set in config.yaml but no API key was found.
Set the GOOGLE_API_KEY environment variable, or switch to a different provider with hermes model.
```
This occurs when the cron job's internal configuration specifies a provider (e.g., `google`) for which no API key is available in the environment, while other providers (e.g., `openrouter`) have valid keys.

## Root Cause
The `hermes cron edit` command does not accept `--model` or `--provider` flags to override a job's model/provider settings. Therefore, changing the job's provider via CLI is not possible.

## Workaround
Use `execute_code` to directly modify the cron jobs JSON file:

1. Locate the cron jobs file: `/opt/data/cron/jobs.json`
2. Find the job by `job_id` (e.g., `755e1b243397`).
3. Set the `model` field to a valid model string with the desired nested provider configurations. **Pitfall Alert:** Do not double-prefix the model ID with `openrouter/google/...` in JSON targets. Setting `"model": "google/gemini-2.0-flash-001"` and `"provider": "openrouter"` is the clean path. Explicitly omit the openrouter prefix from the model string itself, otherwise OpenRouter will return an HTTP 404 No Endpoints Found error.
4. Set the `provider` field to the provider name (e.g., `\"openrouter\"`).
5. Save the file.

Example Python code:
```python
import json

jobs_path = \"/opt/data/cron/jobs.json\"
job_id = \"755e1b243397\"

with open(jobs_path, 'r') as f:
    jobs_data = json.load(f)

for job in jobs_data.get('jobs', []):
    if job.get('job_id') == job_id:
        job['model'] = \"openrouter/google/gemini-2.0-flash-001\"
        job['provider'] = \"openrouter\"
        break

with open(jobs_path, 'w') as f:
    json.dump(jobs_data, f, indent=2)
```

## Prevention
When creating or editing cron jobs, ensure the selected model/provider has a corresponding API key in the environment (`.env`) or credential pool. Use `hermes config check` to verify available keys.

## Related
- `hermes cron list` to view jobs.
- `hermes config check` for API key status.


## Example Fix for Job 755e1b243397 (from session on 2026-06-04)
The following fix was applied to resolve the error for job ID `755e1b243397`:
```python
import json

jobs_path = '/opt/data/cron/jobs.json'
job_id = '755e1b243397'

with open(jobs_path, 'r') as f:
    jobs_data = json.load(f)

for job in jobs_data.get('jobs', []):
    if job.get('job_id') == job_id:
        job['model'] = 'openrouter/google/gemini-2.0-flash-001'
        job['provider'] = 'openrouter'
        break

with open(jobs_path, 'w') as f:
    json.dump(jobs_data, f, indent=2)
```