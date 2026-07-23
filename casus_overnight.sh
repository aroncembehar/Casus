#!/bin/bash
# casus_overnight.sh — run now, wait for 4am reset, run again

cd /path/to/Casus   # adjust to your actual repo path

echo "=== SESSION 1: starting now ==="
claude -p "$(cat casus_batch_prompt.md)" \
  --allowedTools "Read,Edit,WebFetch,WebSearch" \
  --permission-mode acceptEdits \
  --output-format json \
  --max-turns 200 \
  > session1_output.json 2>&1

# Pull the session_id out of the JSON result so we can resume it later
SESSION_ID=$(python3 -c "import json; print(json.load(open('session1_output.json'))['session_id'])" 2>/dev/null)
echo "Session 1 ended. Session ID: $SESSION_ID"
echo "Check session1_output.json and PROGRESS.md for what got done."

echo "=== Waiting until 4:00 AM ==="
caffeinate -i bash -c '
  target="04:00:00"
  now=$(date +%H:%M:%S)
  target_epoch=$(date -j -f "%H:%M:%S" "$target" +%s 2>/dev/null || date -d "$target" +%s)
  now_epoch=$(date +%s)
  if [ "$target_epoch" -le "$now_epoch" ]; then
    target_epoch=$((target_epoch + 86400))
  fi
  sleep_seconds=$((target_epoch - now_epoch))
  echo "Sleeping for $sleep_seconds seconds until 4am..."
  sleep "$sleep_seconds"
'

echo "=== SESSION 2: resuming at 4am ==="
claude -p "Continue the batch case-processing job exactly where you left off. Check the tracking file and PROGRESS.md for what's done and what's remaining, and pick up from there." \
  --resume "$SESSION_ID" \
  --allowedTools "Read,Edit,WebFetch,WebSearch" \
  --permission-mode acceptEdits \
  --output-format json \
  --max-turns 200 \
  > session2_output.json 2>&1

echo "=== DONE. Check session2_output.json and PROGRESS.md ==="
