All Women's Premier League match data in CSV format
===================================================

The background
--------------

As an experiment, after being asked by a user of the site, I started
converting the IPL data from YAML into this CSV format. This then expanded
to include international T20s, for both women and men, before, finally,
expanding again to cover all matches we provide.

This particular zip folder contains the CSV data for...
  All Women's Premier League matches
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

2026-02-05 - club - WPL - female - 1513703 - Delhi Capitals vs Royal Challengers Bengaluru
2026-02-03 - club - WPL - female - 1513702 - Gujarat Giants vs Delhi Capitals
2026-02-01 - club - WPL - female - 1513701 - UP Warriorz vs Delhi Capitals
2026-01-30 - club - WPL - female - 1513700 - Gujarat Giants vs Mumbai Indians
2026-01-29 - club - WPL - female - 1513699 - UP Warriorz vs Royal Challengers Bengaluru
2026-01-27 - club - WPL - female - 1513698 - Gujarat Giants vs Delhi Capitals
2026-01-26 - club - WPL - female - 1513697 - Mumbai Indians vs Royal Challengers Bengaluru
2026-01-24 - club - WPL - female - 1513696 - Royal Challengers Bengaluru vs Delhi Capitals
2026-01-22 - club - WPL - female - 1513695 - Gujarat Giants vs UP Warriorz
2026-01-20 - club - WPL - female - 1513694 - Mumbai Indians vs Delhi Capitals
2026-01-19 - club - WPL - female - 1513693 - Royal Challengers Bengaluru vs Gujarat Giants
2026-01-17 - club - WPL - female - 1513692 - Delhi Capitals vs Royal Challengers Bengaluru
2026-01-17 - club - WPL - female - 1513691 - UP Warriorz vs Mumbai Indians
2026-01-16 - club - WPL - female - 1513690 - Royal Challengers Bengaluru vs Gujarat Giants
2026-01-15 - club - WPL - female - 1513689 - Mumbai Indians vs UP Warriorz
2026-01-14 - club - WPL - female - 1513688 - UP Warriorz vs Delhi Capitals
2026-01-13 - club - WPL - female - 1513687 - Gujarat Giants vs Mumbai Indians
2026-01-12 - club - WPL - female - 1513686 - UP Warriorz vs Royal Challengers Bengaluru
2026-01-11 - club - WPL - female - 1513685 - Gujarat Giants vs Delhi Capitals
2026-01-10 - club - WPL - female - 1513684 - Mumbai Indians vs Delhi Capitals
2026-01-10 - club - WPL - female - 1513683 - Gujarat Giants vs UP Warriorz
2026-01-09 - club - WPL - female - 1513682 - Mumbai Indians vs Royal Challengers Bengaluru
2025-03-15 - club - WPL - female - 1469319 - Mumbai Indians vs Delhi Capitals
2025-03-13 - club - WPL - female - 1469318 - Mumbai Indians vs Gujarat Giants
2025-03-11 - club - WPL - female - 1469317 - Royal Challengers Bengaluru vs Mumbai Indians
2025-03-10 - club - WPL - female - 1469316 - Mumbai Indians vs Gujarat Giants
2025-03-08 - club - WPL - female - 1469315 - UP Warriorz vs Royal Challengers Bengaluru
2025-03-07 - club - WPL - female - 1469314 - Delhi Capitals vs Gujarat Giants
2025-03-06 - club - WPL - female - 1469313 - UP Warriorz vs Mumbai Indians
2025-03-03 - club - WPL - female - 1469312 - Gujarat Giants vs UP Warriorz
2025-03-01 - club - WPL - female - 1469311 - Royal Challengers Bengaluru vs Delhi Capitals
2025-02-28 - club - WPL - female - 1469310 - Mumbai Indians vs Delhi Capitals
2025-02-27 - club - WPL - female - 1469309 - Royal Challengers Bengaluru vs Gujarat Giants
2025-02-26 - club - WPL - female - 1469308 - UP Warriorz vs Mumbai Indians
2025-02-25 - club - WPL - female - 1469307 - Gujarat Giants vs Delhi Capitals
2025-02-24 - club - WPL - female - 1469306 - Royal Challengers Bengaluru vs UP Warriorz
2025-02-22 - club - WPL - female - 1469305 - UP Warriorz vs Delhi Capitals
2025-02-21 - club - WPL - female - 1469304 - Royal Challengers Bengaluru vs Mumbai Indians
2025-02-19 - club - WPL - female - 1469303 - UP Warriorz vs Delhi Capitals
2025-02-18 - club - WPL - female - 1469302 - Gujarat Giants vs Mumbai Indians
2025-02-17 - club - WPL - female - 1469301 - Delhi Capitals vs Royal Challengers Bengaluru
2025-02-16 - club - WPL - female - 1469300 - UP Warriorz vs Gujarat Giants
2025-02-15 - club - WPL - female - 1469299 - Mumbai Indians vs Delhi Capitals
2025-02-14 - club - WPL - female - 1469298 - Gujarat Giants vs Royal Challengers Bengaluru
2024-03-17 - club - WPL - female - 1417737 - Delhi Capitals vs Royal Challengers Bangalore
2024-03-15 - club - WPL - female - 1417736 - Royal Challengers Bangalore vs Mumbai Indians
2024-03-13 - club - WPL - female - 1417735 - Gujarat Giants vs Delhi Capitals
2024-03-12 - club - WPL - female - 1417734 - Mumbai Indians vs Royal Challengers Bangalore
2024-03-11 - club - WPL - female - 1417733 - Gujarat Giants vs UP Warriorz
2024-03-10 - club - WPL - female - 1417732 - Delhi Capitals vs Royal Challengers Bangalore
2024-03-09 - club - WPL - female - 1417731 - Gujarat Giants vs Mumbai Indians
2024-03-08 - club - WPL - female - 1417730 - UP Warriorz vs Delhi Capitals
2024-03-07 - club - WPL - female - 1417729 - Mumbai Indians vs UP Warriorz
2024-03-06 - club - WPL - female - 1417728 - Gujarat Giants vs Royal Challengers Bangalore
2024-03-05 - club - WPL - female - 1417727 - Delhi Capitals vs Mumbai Indians
2024-03-04 - club - WPL - female - 1417726 - Royal Challengers Bangalore vs UP Warriorz
2024-03-03 - club - WPL - female - 1417725 - Delhi Capitals vs Gujarat Giants
2024-03-02 - club - WPL - female - 1417724 - Royal Challengers Bangalore vs Mumbai Indians
2024-03-01 - club - WPL - female - 1417723 - Gujarat Giants vs UP Warriorz
2024-02-29 - club - WPL - female - 1417722 - Delhi Capitals vs Royal Challengers Bangalore
2024-02-28 - club - WPL - female - 1417721 - Mumbai Indians vs UP Warriorz
2024-02-27 - club - WPL - female - 1417720 - Gujarat Giants vs Royal Challengers Bangalore
2024-02-26 - club - WPL - female - 1417719 - UP Warriorz vs Delhi Capitals
2024-02-25 - club - WPL - female - 1417718 - Gujarat Giants vs Mumbai Indians
2024-02-24 - club - WPL - female - 1417717 - Royal Challengers Bangalore vs UP Warriorz
2024-02-23 - club - WPL - female - 1417716 - Delhi Capitals vs Mumbai Indians
2023-03-26 - club - WPL - female - 1358950 - Delhi Capitals vs Mumbai Indians
2023-03-24 - club - WPL - female - 1358949 - Mumbai Indians vs UP Warriorz
2023-03-21 - club - WPL - female - 1358948 - UP Warriorz vs Delhi Capitals
2023-03-21 - club - WPL - female - 1358947 - Royal Challengers Bangalore vs Mumbai Indians
2023-03-20 - club - WPL - female - 1358946 - Mumbai Indians vs Delhi Capitals
2023-03-20 - club - WPL - female - 1358945 - Gujarat Giants vs UP Warriorz
2023-03-18 - club - WPL - female - 1358944 - Gujarat Giants vs Royal Challengers Bangalore
2023-03-18 - club - WPL - female - 1358943 - Mumbai Indians vs UP Warriorz
2023-03-16 - club - WPL - female - 1358942 - Gujarat Giants vs Delhi Capitals
2023-03-15 - club - WPL - female - 1358941 - UP Warriorz vs Royal Challengers Bangalore
2023-03-14 - club - WPL - female - 1358940 - Mumbai Indians vs Gujarat Giants
2023-03-13 - club - WPL - female - 1358939 - Royal Challengers Bangalore vs Delhi Capitals
2023-03-12 - club - WPL - female - 1358938 - UP Warriorz vs Mumbai Indians
2023-03-11 - club - WPL - female - 1358937 - Gujarat Giants vs Delhi Capitals
2023-03-10 - club - WPL - female - 1358936 - Royal Challengers Bangalore vs UP Warriorz
2023-03-09 - club - WPL - female - 1358935 - Delhi Capitals vs Mumbai Indians
2023-03-08 - club - WPL - female - 1358934 - Gujarat Giants vs Royal Challengers Bangalore
2023-03-07 - club - WPL - female - 1358933 - Delhi Capitals vs UP Warriorz
2023-03-06 - club - WPL - female - 1358932 - Royal Challengers Bangalore vs Mumbai Indians
2023-03-05 - club - WPL - female - 1358931 - Gujarat Giants vs UP Warriorz
2023-03-05 - club - WPL - female - 1358930 - Delhi Capitals vs Royal Challengers Bangalore
2023-03-04 - club - WPL - female - 1358929 - Mumbai Indians vs Gujarat Giants

Further information
-------------------

You can find all of our currently available data at https://cricsheet.org/

You can contact me via the following methods:
  Email   : stephen@cricsheet.org
  Mastodon: @cricsheet@deeden.co.uk
