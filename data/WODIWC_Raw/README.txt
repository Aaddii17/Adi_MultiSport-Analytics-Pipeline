All ICC Women's Cricket World Cup match data in CSV format
==========================================================

The background
--------------

As an experiment, after being asked by a user of the site, I started
converting the IPL data from YAML into this CSV format. This then expanded
to include international T20s, for both women and men, before, finally,
expanding again to cover all matches we provide.

This particular zip folder contains the CSV data for...
  All ICC Women's Cricket World Cup matches
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

2025-11-02 - international - ODI - female - 1490443 - India vs South Africa
2025-10-30 - international - ODI - female - 1490442 - Australia vs India
2025-10-29 - international - ODI - female - 1490441 - South Africa vs England
2025-10-26 - international - ODI - female - 1490440 - Bangladesh vs India
2025-10-26 - international - ODI - female - 1490439 - New Zealand vs England
2025-10-25 - international - ODI - female - 1490438 - South Africa vs Australia
2025-10-24 - international - ODI - female - 1490437 - Pakistan vs Sri Lanka
2025-10-23 - international - ODI - female - 1490436 - India vs New Zealand
2025-10-22 - international - ODI - female - 1490435 - England vs Australia
2025-10-21 - international - ODI - female - 1490434 - South Africa vs Pakistan
2025-10-20 - international - ODI - female - 1490433 - Sri Lanka vs Bangladesh
2025-10-19 - international - ODI - female - 1490432 - England vs India
2025-10-18 - international - ODI - female - 1490431 - Pakistan vs New Zealand
2025-10-17 - international - ODI - female - 1490430 - Sri Lanka vs South Africa
2025-10-16 - international - ODI - female - 1490429 - Bangladesh vs Australia
2025-10-15 - international - ODI - female - 1490428 - England vs Pakistan
2025-10-14 - international - ODI - female - 1490427 - Sri Lanka vs New Zealand
2025-10-13 - international - ODI - female - 1490426 - Bangladesh vs South Africa
2025-10-12 - international - ODI - female - 1490425 - India vs Australia
2025-10-11 - international - ODI - female - 1490424 - England vs Sri Lanka
2025-10-10 - international - ODI - female - 1490423 - New Zealand vs Bangladesh
2025-10-09 - international - ODI - female - 1490422 - India vs South Africa
2025-10-08 - international - ODI - female - 1490421 - Australia vs Pakistan
2025-10-07 - international - ODI - female - 1490420 - Bangladesh vs England
2025-10-06 - international - ODI - female - 1490419 - New Zealand vs South Africa
2025-10-05 - international - ODI - female - 1490418 - India vs Pakistan
2025-10-03 - international - ODI - female - 1490416 - South Africa vs England
2025-10-02 - international - ODI - female - 1490415 - Pakistan vs Bangladesh
2025-10-01 - international - ODI - female - 1490414 - Australia vs New Zealand
2025-09-30 - international - ODI - female - 1490413 - India vs Sri Lanka
2022-04-03 - international - ODI - female - 1243938 - Australia vs England
2022-03-31 - international - ODI - female - 1243937 - England vs South Africa
2022-03-30 - international - ODI - female - 1243936 - Australia vs West Indies
2022-03-27 - international - ODI - female - 1243935 - India vs South Africa
2022-03-27 - international - ODI - female - 1243934 - England vs Bangladesh
2022-03-26 - international - ODI - female - 1243933 - New Zealand vs Pakistan
2022-03-25 - international - ODI - female - 1243932 - Bangladesh vs Australia
2022-03-24 - international - ODI - female - 1243931 - Pakistan vs England
2022-03-24 - international - ODI - female - 1243930 - South Africa vs West Indies
2022-03-22 - international - ODI - female - 1243929 - India vs Bangladesh
2022-03-22 - international - ODI - female - 1243928 - South Africa vs Australia
2022-03-21 - international - ODI - female - 1243927 - West Indies vs Pakistan
2022-03-20 - international - ODI - female - 1243926 - New Zealand vs England
2022-03-19 - international - ODI - female - 1243925 - India vs Australia
2022-03-18 - international - ODI - female - 1243924 - West Indies vs Bangladesh
2022-03-17 - international - ODI - female - 1243923 - New Zealand vs South Africa
2022-03-16 - international - ODI - female - 1243922 - India vs England
2022-03-15 - international - ODI - female - 1243921 - West Indies vs Australia
2022-03-14 - international - ODI - female - 1243920 - Bangladesh vs Pakistan
2022-03-14 - international - ODI - female - 1243919 - England vs South Africa
2022-03-13 - international - ODI - female - 1243918 - Australia vs New Zealand
2022-03-12 - international - ODI - female - 1243917 - India vs West Indies
2022-03-11 - international - ODI - female - 1243916 - South Africa vs Pakistan
2022-03-10 - international - ODI - female - 1243915 - New Zealand vs India
2022-03-09 - international - ODI - female - 1243914 - West Indies vs England
2022-03-08 - international - ODI - female - 1243913 - Pakistan vs Australia
2022-03-07 - international - ODI - female - 1243912 - Bangladesh vs New Zealand
2022-03-06 - international - ODI - female - 1243911 - India vs Pakistan
2022-03-05 - international - ODI - female - 1243910 - Australia vs England
2022-03-05 - international - ODI - female - 1243909 - South Africa vs Bangladesh
2022-03-04 - international - ODI - female - 1243908 - West Indies vs New Zealand
2017-07-23 - international - ODI - female - 1085975 - England vs India
2017-07-20 - international - ODI - female - 1085974 - India vs Australia
2017-07-18 - international - ODI - female - 1085973 - South Africa vs England
2017-07-15 - international - ODI - female - 1085972 - Pakistan vs Sri Lanka
2017-07-15 - international - ODI - female - 1085971 - India vs New Zealand
2017-07-15 - international - ODI - female - 1085970 - England vs West Indies
2017-07-15 - international - ODI - female - 1085969 - Australia vs South Africa
2017-07-12 - international - ODI - female - 1085968 - England vs New Zealand
2017-07-12 - international - ODI - female - 1085967 - Australia vs India
2017-07-12 - international - ODI - female - 1085966 - South Africa vs Sri Lanka
2017-07-11 - international - ODI - female - 1085965 - Pakistan vs West Indies
2017-07-09 - international - ODI - female - 1085964 - Sri Lanka vs West Indies
2017-07-09 - international - ODI - female - 1085963 - England vs Australia
2017-07-08 - international - ODI - female - 1085962 - India vs South Africa
2017-07-08 - international - ODI - female - 1085961 - New Zealand vs Pakistan
2017-07-06 - international - ODI - female - 1085960 - New Zealand vs West Indies
2017-07-05 - international - ODI - female - 1085959 - Australia vs Pakistan
2017-07-05 - international - ODI - female - 1085958 - India vs Sri Lanka
2017-07-05 - international - ODI - female - 1085957 - England vs South Africa
2017-07-02 - international - ODI - female - 1085956 - South Africa vs West Indies
2017-07-02 - international - ODI - female - 1085955 - India vs Pakistan
2017-07-02 - international - ODI - female - 1085954 - Australia vs New Zealand
2017-07-02 - international - ODI - female - 1085953 - England vs Sri Lanka
2017-06-29 - international - ODI - female - 1085952 - Australia vs Sri Lanka
2017-06-29 - international - ODI - female - 1085951 - India vs West Indies
2017-06-27 - international - ODI - female - 1085949 - England vs Pakistan
2017-06-26 - international - ODI - female - 1085948 - Australia vs West Indies
2017-06-25 - international - ODI - female - 1085947 - Pakistan vs South Africa
2017-06-24 - international - ODI - female - 1085946 - England vs India
2017-06-24 - international - ODI - female - 1085945 - New Zealand vs Sri Lanka
2013-02-17 - international - ODI - female - 594915 - Australia vs West Indies
2013-02-15 - international - ODI - female - 594914 - England vs New Zealand
2013-02-13 - international - ODI - female - 594912 - England vs New Zealand
2013-02-11 - international - ODI - female - 594909 - New Zealand vs West Indies
2013-02-10 - international - ODI - female - 594907 - Australia vs Sri Lanka
2013-02-08 - international - ODI - female - 594904 - Australia vs England
2013-02-05 - international - ODI - female - 594901 - India vs Sri Lanka
2013-02-03 - international - ODI - female - 594897 - India vs England
2013-02-01 - international - ODI - female - 594894 - England vs Sri Lanka
2013-01-31 - international - ODI - female - 594891 - India vs West Indies
2009-03-10 - international - ODI - female - 357962 - England vs India

Further information
-------------------

You can find all of our currently available data at https://cricsheet.org/

You can contact me via the following methods:
  Email   : stephen@cricsheet.org
  Mastodon: @cricsheet@deeden.co.uk
