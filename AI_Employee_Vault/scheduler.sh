#!/bin/bash
# AI Employee Scheduler — Silver Tier
# Sets up cron jobs for automated tasks

VAULT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Setting up AI Employee cron schedules..."
echo "Vault directory: $VAULT_DIR"

# Create the cron entries
CRON_JOBS="
# AI Employee — Daily Dashboard Update at 8:00 AM
0 8 * * * cd $VAULT_DIR && python3 orchestrator.py --once >> $VAULT_DIR/cron.log 2>&1

# AI Employee — Check Needs_Action every 30 minutes
*/30 * * * * cd $VAULT_DIR && python3 orchestrator.py --once >> $VAULT_DIR/cron.log 2>&1
"

echo "To install these cron jobs, run: crontab -e"
echo "Then paste the following:"
echo ""
echo "$CRON_JOBS"
echo ""
echo "Or run this command to install automatically:"
echo "(crontab -l 2>/dev/null; echo \"$CRON_JOBS\") | crontab -"
