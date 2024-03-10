### Bottom text get only set code

Remove "EN.*" in a line, where "EN" comes after a space (first space is after the set code)

regex: `(?=\s).*EN.*` (replace with "")
- positive lookahead (?=) matches _after_ this group (so set code isn't deleted)
- \s matches space
- .* before EN as there may be trash characters picked up between the set code and "EN"

NOTE: Not fully accurate, a string like below is still not stripped because of no space

`WOE +EN % NESTOR OSSANDON Lzu. ™ & © 2023 rds of the Coast`



### Bottom text remove garbage between set code and author

regex: `(?=\s).*EN.*?(?=\w)` (replace with "")
- Similar to above, but matches up until (but not including) the next word char, which should be the author.
- - "word char" is alphanumeric or underscore

So from:
- `WOE +EN % NESTOR OSSANDON Lzu. ™ & © 2023 rds of the Coast`
it returns
- `WOE NESTOR OSSANDON Lzu. ™ & © 2023 rds of the Coast`



### Bottom text remove garbage after author
This is assuming the above is already done -- basically that the start of the string _is_ the author.

regex: `^([\w\s\.]+)` (returned match _is_ the author -- do not replace text)
- Match all word characters, spaces, and `.`
- When a character not in this group is hit, regex match finishes.

The following are matched from:
- `NESTOR OSSANDON Lzu. ™ & © 2023 rds of the Coast`
- `BONEFACE ™ & © 2023 Wizards of the Coast`
- `Bone_._Face! ™ & © 2023 Wizards of the Coast`
to:
- `NESTOR OSSANDON Lzu. `
- `BONEFACE `
- `Bone_._Face`
