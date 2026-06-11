All Men's SA20 match data in CSV format
=======================================

The background
--------------

As an experiment, after being asked by a user of the site, I started
converting the IPL data from YAML into this CSV format. This then expanded
to include international T20s, for both women and men, before, finally,
expanding again to cover all matches we provide.

This particular zip folder contains the CSV data for...
  All Men's SA20 matches
...for which we have data, and is loosely based on the format that Retrosheet
uses for baseball, with some suitable hacks built in.

How you can help
----------------

Providing feedback on the data would be the most helpful. Tell me what you
like and what you don't. Is there anything that is in the JSON data that
you'd like to be included in the CSV? Could something be included in a better
format? General views and comments help, as well as incredibly detailed
feedback. All information is of use to me at this stage. I can only improve
the data if people tell me what does works and what doesn't. I'd like to make
the data as useful as possible but I need your help to do it. Also, which of
the 2 CSV formats do you prefer, this one or the newer "Ashwin" format?
Ideally I'd like to settle on a single CSV format so what should be kept
from each?

Finally, any feedback as to the licence the data should be released under
would be greatly appreciated. Licensing is a strange little world and I'd
like to choose the "right" licence. My basic criteria may be that:

  * the data should be free,
  * corrections are encouraged/required to be reported to the project,
  * derivative works are allowed,
  * you can't just take data and sell it.

Feedback, pointers, comments, etc on licensing are welcome.

The format of the data
----------------------

Full documentation of this CSV format can be found at:
  https://cricsheet.org/format/csv_original/
but the following is a brief summary of the details...

Each file has a 'version', multiple 'info' lines, and multiple 'ball' lines.
'version' is just 1.6.0, or 1.7.0 for now, and will change as I make changes.
The 'info' entries should be fairly self-explanatory but feel free to ask on
Mastodon (@cricsheet@deeden.co.uk) if you're unsure. If you look carefully
you may see some slight hints as to some data we'll be including in the full
data files in the future.

Each 'ball' line has the following fields:

  * The word 'ball' to identify it as such
  * Innings number, starting from 1
  * Over and ball
  * Batting team name
  * Batsman
  * Non-striker
  * Bowler
  * Runs-off-bat
  * Extras
  * Wides
  * No-balls
  * Byes
  * Leg-byes
  * Penalty
  * Kind of wicket, if any
  * Dismissed played, if there was a wicket

Matches included in this archive
--------------------------------

2026-01-25 - club - SAT - male - 1494286 - Pretoria Capitals vs Sunrisers Eastern Cape
2026-01-23 - club - SAT - male - 1494285 - Paarl Royals vs Sunrisers Eastern Cape
2026-01-22 - club - SAT - male - 1494284 - Paarl Royals vs Joburg Super Kings
2026-01-21 - club - SAT - male - 1494283 - Sunrisers Eastern Cape vs Pretoria Capitals
2026-01-19 - club - SAT - male - 1494282 - Joburg Super Kings vs Paarl Royals
2026-01-18 - club - SAT - male - 1494281 - MI Cape Town vs Sunrisers Eastern Cape
2026-01-17 - club - SAT - male - 1494280 - Pretoria Capitals vs Joburg Super Kings
2026-01-17 - club - SAT - male - 1494279 - Durban's Super Giants vs Paarl Royals
2026-01-16 - club - SAT - male - 1494278 - Sunrisers Eastern Cape vs MI Cape Town
2026-01-15 - club - SAT - male - 1494277 - Pretoria Capitals vs Paarl Royals
2026-01-14 - club - SAT - male - 1494276 - Sunrisers Eastern Cape vs Joburg Super Kings
2026-01-13 - club - SAT - male - 1494275 - Durban's Super Giants vs Paarl Royals
2026-01-12 - club - SAT - male - 1494274 - Pretoria Capitals vs MI Cape Town
2026-01-11 - club - SAT - male - 1494273 - Sunrisers Eastern Cape vs Durban's Super Giants
2026-01-10 - club - SAT - male - 1494272 - MI Cape Town vs Joburg Super Kings
2026-01-10 - club - SAT - male - 1494271 - Pretoria Capitals vs Paarl Royals
2026-01-08 - club - SAT - male - 1494269 - Joburg Super Kings vs Paarl Royals
2026-01-07 - club - SAT - male - 1494268 - Pretoria Capitals vs Durban's Super Giants
2026-01-06 - club - SAT - male - 1494267 - Joburg Super Kings vs MI Cape Town
2026-01-05 - club - SAT - male - 1494266 - Pretoria Capitals vs Sunrisers Eastern Cape
2026-01-04 - club - SAT - male - 1494265 - MI Cape Town vs Paarl Royals
2026-01-02 - club - SAT - male - 1494262 - Paarl Royals vs MI Cape Town
2026-01-01 - club - SAT - male - 1494261 - Joburg Super Kings vs Durban's Super Giants
2025-12-31 - club - SAT - male - 1494260 - Pretoria Capitals vs MI Cape Town
2025-12-31 - club - SAT - male - 1494259 - Sunrisers Eastern Cape vs Paarl Royals
2025-12-30 - club - SAT - male - 1494258 - Durban's Super Giants vs Joburg Super Kings
2025-12-29 - club - SAT - male - 1494257 - Sunrisers Eastern Cape vs Pretoria Capitals
2025-12-28 - club - SAT - male - 1494256 - Durban's Super Giants vs MI Cape Town
2025-12-27 - club - SAT - male - 1494255 - Sunrisers Eastern Cape vs Paarl Royals
2025-12-27 - club - SAT - male - 1494254 - Joburg Super Kings vs Pretoria Capitals
2025-12-26 - club - SAT - male - 1494253 - Durban's Super Giants vs MI Cape Town
2025-02-08 - club - SAT - male - 1449667 - MI Cape Town vs Sunrisers Eastern Cape
2025-02-06 - club - SAT - male - 1449666 - Paarl Royals vs Sunrisers Eastern Cape
2025-02-05 - club - SAT - male - 1449665 - Sunrisers Eastern Cape vs Joburg Super Kings
2025-02-04 - club - SAT - male - 1449664 - MI Cape Town vs Paarl Royals
2025-02-02 - club - SAT - male - 1449663 - MI Cape Town vs Pretoria Capitals
2025-02-01 - club - SAT - male - 1449662 - Durban's Super Giants vs Joburg Super Kings
2025-02-01 - club - SAT - male - 1449661 - Sunrisers Eastern Cape vs Paarl Royals
2025-01-31 - club - SAT - male - 1449660 - MI Cape Town vs Pretoria Capitals
2025-01-30 - club - SAT - male - 1449659 - Paarl Royals vs Joburg Super Kings
2025-01-29 - club - SAT - male - 1449658 - Sunrisers Eastern Cape vs MI Cape Town
2025-01-28 - club - SAT - male - 1449657 - Joburg Super Kings vs Pretoria Capitals
2025-01-27 - club - SAT - male - 1449656 - Durban's Super Giants vs Paarl Royals
2025-01-26 - club - SAT - male - 1449655 - Sunrisers Eastern Cape vs Joburg Super Kings
2025-01-25 - club - SAT - male - 1449654 - Durban's Super Giants vs MI Cape Town
2025-01-25 - club - SAT - male - 1449653 - Paarl Royals vs Pretoria Capitals
2025-01-24 - club - SAT - male - 1449652 - Sunrisers Eastern Cape vs Joburg Super Kings
2025-01-23 - club - SAT - male - 1449651 - Durban's Super Giants vs Paarl Royals
2025-01-22 - club - SAT - male - 1449650 - Sunrisers Eastern Cape vs Pretoria Capitals
2025-01-21 - club - SAT - male - 1449649 - MI Cape Town vs Durban's Super Giants
2025-01-20 - club - SAT - male - 1449648 - Joburg Super Kings vs Paarl Royals
2025-01-19 - club - SAT - male - 1449647 - Durban's Super Giants vs Sunrisers Eastern Cape
2025-01-18 - club - SAT - male - 1449646 - Joburg Super Kings vs MI Cape Town
2025-01-18 - club - SAT - male - 1449645 - Pretoria Capitals vs Paarl Royals
2025-01-17 - club - SAT - male - 1449644 - Sunrisers Eastern Cape vs Durban's Super Giants
2025-01-16 - club - SAT - male - 1449643 - Pretoria Capitals vs Joburg Super Kings
2025-01-15 - club - SAT - male - 1449642 - MI Cape Town vs Paarl Royals
2025-01-14 - club - SAT - male - 1449641 - Joburg Super Kings vs Durban's Super Giants
2025-01-14 - club - SAT - male - 1449640 - Sunrisers Eastern Cape vs Pretoria Capitals
2025-01-13 - club - SAT - male - 1449639 - MI Cape Town vs Paarl Royals
2025-01-11 - club - SAT - male - 1449637 - MI Cape Town vs Joburg Super Kings
2025-01-11 - club - SAT - male - 1449636 - Sunrisers Eastern Cape vs Paarl Royals
2025-01-10 - club - SAT - male - 1449635 - Durban's Super Giants vs Pretoria Capitals
2025-01-09 - club - SAT - male - 1449634 - MI Cape Town vs Sunrisers Eastern Cape
2024-02-10 - club - SAT - male - 1392685 - Sunrisers Eastern Cape vs Durban's Super Giants
2024-02-08 - club - SAT - male - 1392684 - Durban's Super Giants vs Joburg Super Kings
2024-02-07 - club - SAT - male - 1392683 - Paarl Royals vs Joburg Super Kings
2024-02-06 - club - SAT - male - 1392682 - Sunrisers Eastern Cape vs Durban's Super Giants
2024-02-04 - club - SAT - male - 1392681 - Paarl Royals vs Sunrisers Eastern Cape
2024-02-03 - club - SAT - male - 1392680 - Durban's Super Giants vs Joburg Super Kings
2024-02-03 - club - SAT - male - 1392679 - MI Cape Town vs Pretoria Capitals
2024-02-02 - club - SAT - male - 1392678 - Sunrisers Eastern Cape vs Paarl Royals
2024-02-01 - club - SAT - male - 1392677 - MI Cape Town vs Pretoria Capitals
2024-01-31 - club - SAT - male - 1392676 - Joburg Super Kings vs Sunrisers Eastern Cape
2024-01-30 - club - SAT - male - 1392675 - Durban's Super Giants vs Pretoria Capitals
2024-01-29 - club - SAT - male - 1392674 - MI Cape Town vs Joburg Super Kings
2024-01-28 - club - SAT - male - 1392673 - Durban's Super Giants vs Paarl Royals
2024-01-27 - club - SAT - male - 1392672 - Joburg Super Kings vs Pretoria Capitals
2024-01-27 - club - SAT - male - 1392671 - Sunrisers Eastern Cape vs MI Cape Town
2024-01-26 - club - SAT - male - 1392670 - Durban's Super Giants vs Paarl Royals
2024-01-25 - club - SAT - male - 1392669 - Pretoria Capitals vs Sunrisers Eastern Cape
2024-01-24 - club - SAT - male - 1392668 - Joburg Super Kings vs Paarl Royals
2024-01-23 - club - SAT - male - 1392667 - Durban's Super Giants vs MI Cape Town
2024-01-22 - club - SAT - male - 1392666 - Pretoria Capitals vs Sunrisers Eastern Cape
2024-01-21 - club - SAT - male - 1392665 - Paarl Royals vs MI Cape Town
2024-01-20 - club - SAT - male - 1392664 - Pretoria Capitals vs Joburg Super Kings
2024-01-20 - club - SAT - male - 1392663 - Durban's Super Giants vs Sunrisers Eastern Cape
2024-01-19 - club - SAT - male - 1392662 - Paarl Royals vs MI Cape Town
2024-01-18 - club - SAT - male - 1392661 - Pretoria Capitals vs Durban's Super Giants
2024-01-17 - club - SAT - male - 1392660 - Joburg Super Kings vs Paarl Royals
2024-01-16 - club - SAT - male - 1392659 - Sunrisers Eastern Cape vs MI Cape Town
2024-01-15 - club - SAT - male - 1392658 - Durban's Super Giants vs Joburg Super Kings
2024-01-14 - club - SAT - male - 1392657 - Paarl Royals vs Pretoria Capitals
2024-01-13 - club - SAT - male - 1392656 - Durban's Super Giants vs Sunrisers Eastern Cape
2024-01-13 - club - SAT - male - 1392655 - MI Cape Town vs Joburg Super Kings
2024-01-12 - club - SAT - male - 1392654 - Paarl Royals vs Pretoria Capitals
2024-01-11 - club - SAT - male - 1392653 - MI Cape Town vs Durban's Super Giants
2023-02-11 - club - SAT - male - 1343973 - Pretoria Capitals vs Sunrisers Eastern Cape
2023-02-09 - club - SAT - male - 1343972 - Sunrisers Eastern Cape vs Joburg Super Kings
2023-02-08 - club - SAT - male - 1343971 - Pretoria Capitals vs Paarl Royals
2023-02-07 - club - SAT - male - 1343970 - Pretoria Capitals vs Paarl Royals
2023-02-06 - club - SAT - male - 1343969 - Joburg Super Kings vs MI Cape Town
2023-02-05 - club - SAT - male - 1343968 - Durban's Super Giants vs Pretoria Capitals
2023-02-05 - club - SAT - male - 1343967 - Joburg Super Kings vs Sunrisers Eastern Cape
2023-02-04 - club - SAT - male - 1343966 - MI Cape Town vs Pretoria Capitals
2023-02-03 - club - SAT - male - 1343965 - Sunrisers Eastern Cape vs Durban's Super Giants
2023-02-03 - club - SAT - male - 1343964 - Paarl Royals vs Joburg Super Kings
2023-02-02 - club - SAT - male - 1343963 - MI Cape Town vs Durban's Super Giants
2023-01-24 - club - SAT - male - 1343962 - Durban's Super Giants vs Joburg Super Kings
2023-01-24 - club - SAT - male - 1343961 - Sunrisers Eastern Cape vs Paarl Royals
2023-01-23 - club - SAT - male - 1343960 - Pretoria Capitals vs MI Cape Town
2023-01-22 - club - SAT - male - 1343959 - Sunrisers Eastern Cape vs Durban's Super Giants
2023-01-22 - club - SAT - male - 1343958 - Pretoria Capitals vs Paarl Royals
2023-01-21 - club - SAT - male - 1343957 - Sunrisers Eastern Cape vs Joburg Super Kings
2023-01-21 - club - SAT - male - 1343956 - MI Cape Town vs Paarl Royals
2023-01-20 - club - SAT - male - 1343955 - Durban's Super Giants vs Pretoria Capitals
2023-01-19 - club - SAT - male - 1343954 - Paarl Royals vs Sunrisers Eastern Cape
2023-01-18 - club - SAT - male - 1343953 - Joburg Super Kings vs Pretoria Capitals
2023-01-18 - club - SAT - male - 1343952 - MI Cape Town vs Sunrisers Eastern Cape
2023-01-17 - club - SAT - male - 1343951 - Joburg Super Kings vs Pretoria Capitals
2023-01-17 - club - SAT - male - 1343950 - Paarl Royals vs Durban's Super Giants
2023-01-16 - club - SAT - male - 1343949 - MI Cape Town vs Sunrisers Eastern Cape
2023-01-15 - club - SAT - male - 1343948 - Durban's Super Giants vs Paarl Royals
2023-01-14 - club - SAT - male - 1343947 - Joburg Super Kings vs MI Cape Town
2023-01-14 - club - SAT - male - 1343946 - Pretoria Capitals vs Sunrisers Eastern Cape
2023-01-13 - club - SAT - male - 1343945 - MI Cape Town vs Durban's Super Giants
2023-01-13 - club - SAT - male - 1343944 - Joburg Super Kings vs Paarl Royals
2023-01-12 - club - SAT - male - 1343943 - Pretoria Capitals vs Sunrisers Eastern Cape
2023-01-11 - club - SAT - male - 1343942 - Joburg Super Kings vs Durban's Super Giants
2023-01-10 - club - SAT - male - 1343941 - Paarl Royals vs MI Cape Town

Further information
-------------------

You can find all of our currently available data at https://cricsheet.org/

You can contact me via the following methods:
  Email   : stephen@cricsheet.org
  Mastodon: @cricsheet@deeden.co.uk
