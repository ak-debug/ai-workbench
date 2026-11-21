Fictional example. The files and results below are illustrative.

---

# Why two identical-looking CSV exports had different checksums

Two inventory exports showed the same rows in a spreadsheet, but they had
different SHA-256 digests. I worked with two sample files in a local exercise
to find out what had changed. The answer was in the line endings.

## What the spreadsheet hid

A spreadsheet interprets the file and displays its cells. A checksum is
calculated over the original bytes. Those views can disagree when a difference
changes the file without changing how it looks.

I compared the files as bytes. One used LF after each row. The other used CRLF,
which adds a carriage return before each line feed. That gave me a specific
difference to test, but the first few rows alone couldn't establish whether
there were other changes later in the file.

## Checking the whole file

I converted the line endings in a scratch copy and compared it byte for byte
with the LF export. The files matched after that one change. The originals still
had different checksums, as expected. The match established that line endings
accounted for the difference in these two files.

## Takeaway

A checksum mismatch tells you that the bytes differ. If two files look the same
in an application, check what the application hides. Keep the originals and
test any proposed explanation on a copy.
