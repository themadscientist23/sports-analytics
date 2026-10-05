#!/bin/zsh

echo "Script started"

cd ${0:A:h}/..
source venv/bin/activate

LOG=scripts/daily_updater.log

for sport in nba nfl mlb; do
  python -m app.provider.daily $sport >> $LOG 2>&1
  python -m app.sports.process_games $sport >> $LOG 2>&1
done

echo "Script finished"
