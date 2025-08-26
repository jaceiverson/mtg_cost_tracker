# Scheduled Reminder for whatever

## cron schedule
5 10 * * * # every day at 10:05am

## example bash file
```
#!/bin/sh
cd {path}/{to}/{project}/text_messages || exit 1
venv/bin/python3 -m mtg_product.tcg -f
```