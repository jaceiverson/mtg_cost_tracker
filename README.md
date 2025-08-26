# Track Costs via TCGPlayer API

## cron schedule
5 10 * * * # every day at 10:05am

## example bash file
```
#!/bin/sh
cd {path}/{to}/{project}/text_messages || exit 1
venv/bin/python3 -m mtg_product.tcg -f
```

## example outputs
```
========================================
Processing product: 644286
Pulling fresh data...
Saved product data: outputs/644286/2025-08-26.json
Saved product history: outputs/644286/history/2025-08-26.json
PRODUCT NAME: Icetill Explorer
marketPrice        | TODAY: 13.25  | LAST: 12.67  | %CHANGE: 4.58%    | ARROWS: 1
transactionCount   | TODAY: 134.0  | LAST: 201.0  | %CHANGE: -33.33%  | ARROWS: 4
========================================
========================================
Processing product: 455023
Pulling fresh data...
Saved product data: outputs/455023/2025-08-26.json
Saved product history: outputs/455023/history/2025-08-26.json
PRODUCT NAME: Zask, Skittering Swarmlord
marketPrice        | TODAY: 38.56  | LAST: 38.56  | %CHANGE: 0.00%    | ARROWS: 0
transactionCount   | TODAY: 0.0    | LAST: 5.0    | %CHANGE: -100.00% | ARROWS: 5
========================================
========================================
Processing product: 170800
Pulling fresh data...
Saved product data: outputs/170800/2025-08-26.json
Saved product history: outputs/170800/history/2025-08-26.json
PRODUCT NAME: Lord Windgrace
marketPrice        | TODAY: 21.26  | LAST: 21.26  | %CHANGE: 0.00%    | ARROWS: 0
transactionCount   | TODAY: 0.0    | LAST: 3.0    | %CHANGE: -100.00% | ARROWS: 5
========================================
========================================
Processing product: 101347
Pulling fresh data...
Saved product data: outputs/101347/2025-08-26.json
Saved product history: outputs/101347/history/2025-08-26.json
PRODUCT NAME: Jace, Vryn's Prodigy (SDCC 2015 Exclusive)
marketPrice        | TODAY: 106.94 | LAST: 106.94 | %CHANGE: 0.00%    | ARROWS: 0
transactionCount   | TODAY: 0.0    | LAST: 0.0    | %CHANGE: 0.00%    | ARROWS: 0
========================================
========================================
Processing product: 619672
Pulling fresh data...
Saved product data: outputs/619672/2025-08-26.json
Saved product history: outputs/619672/history/2025-08-26.json
PRODUCT NAME: Edge of Eternities - Collector Booster Display
marketPrice        | TODAY: 373.85 | LAST: 372.85 | %CHANGE: 0.27%    | ARROWS: 1
transactionCount   | TODAY: 47.0   | LAST: 69.0   | %CHANGE: -31.88%  | ARROWS: 4
========================================
========================================
Processing product: 619649
Pulling fresh data...
Saved product data: outputs/619649/2025-08-26.json
Saved product history: outputs/619649/history/2025-08-26.json
PRODUCT NAME: Tarkir: Dragonstorm - Collector Booster Display
marketPrice        | TODAY: 318.27 | LAST: 320.56 | %CHANGE: -0.71%   | ARROWS: 1
transactionCount   | TODAY: 21.0   | LAST: 21.0   | %CHANGE: 0.00%    | ARROWS: 0
========================================
Message to be sent:
MTG - Market Price Update
2025-08-26
----------
Icetill Explorer
• C: $13.25 ⬆️ 4.58%
• T: 134.0 ⬇️⬇️⬇️⬇️ -33.33%
https://www.tcgplayer.com/product/644286

Zask, Skittering Swarmlord
• C: $38.56 ➡️ 0.00%
• T: 0.0 ⬇️⬇️⬇️⬇️⬇️ -100.00%
https://www.tcgplayer.com/product/455023

Lord Windgrace
• C: $21.26 ➡️ 0.00%
• T: 0.0 ⬇️⬇️⬇️⬇️⬇️ -100.00%
https://www.tcgplayer.com/product/170800

Jace, Vryn's Prodigy (SDCC 2015 Exclusive)
• C: $106.94 ➡️ 0.00%
• T: 0.0 ➡️ 0.00%
https://www.tcgplayer.com/product/101347

Edge of Eternities - Collector Booster Display
• C: $373.85 ⬆️ 0.27%
• T: 47.0 ⬇️⬇️⬇️⬇️ -31.88%
https://www.tcgplayer.com/product/619672

Tarkir: Dragonstorm - Collector Booster Display
• C: $318.27 ⬇️ -0.71%
• T: 21.0 ➡️ 0.00%
https://www.tcgplayer.com/product/619649


Message sent: 123456789
```
