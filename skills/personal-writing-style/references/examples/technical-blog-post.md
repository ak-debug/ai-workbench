Fictional example. The file, output and investigation below are illustrative.

---

# Finding a file hidden in a PNG's trailing data

## Overview

An image can open normally and still carry extra data after the picture. PNG
decoders stop at the `IEND` chunk, which marks the end of the image. Bytes after
that point may be ignored by a viewer even though they are still in the file.

In this fictional local forensics exercise, I examine a PNG that displays
normally but is much larger than expected. I use its chunk structure to find
where the image ends, then check the remaining bytes for a second file.

## How a PNG ends

A PNG starts with an eight-byte signature and then stores data in **chunks**.
Each chunk has a four-byte length, a four-byte type, the data itself, and a
four-byte CRC. The length counts only the data, so the whole chunk takes
`length + 12` bytes.

The final chunk is `IEND`. It has no data, so its complete representation is
12 bytes:

```text
00 00 00 00  49 45 4e 44  ae 42 60 82
   length       IEND           CRC
```

Finding those bytes by searching alone is a clue, but it is not enough to prove
where the image ends. The same sequence could occur inside chunk data. Walking
the chunks by their lengths gives us the boundary.

## Finding the boundary

I ran this short script on a copy of the sample. It checks the PNG signature,
walks each chunk and reports the first `IEND` it reaches.

```python
from pathlib import Path
import struct

data = Path("sample.png").read_bytes()
if data[:8] != b"\x89PNG\r\n\x1a\n":
    raise ValueError("Not a PNG signature")

offset = 8
while offset + 12 <= len(data):
    length = struct.unpack_from(">I", data, offset)[0]
    kind = data[offset + 4:offset + 8]
    end = offset + 12 + length
    if end > len(data):
        raise ValueError(f"Truncated chunk at {offset:#x}")
    if kind == b"IEND":
        print(f"IEND ends at {end:#x}; {len(data) - end} trailing bytes")
        break
    offset = end
else:
    raise ValueError("No complete IEND chunk found")
```

For the sample, the output was:

```text
IEND ends at 0x1240; 214 trailing bytes
```

That places 214 bytes beyond the end of the chunk stream. The script checks
boundaries, but it does not validate CRCs or prove that every chunk is valid.
I would use a PNG validator as a separate check.

## Inspecting the trailing bytes

I extracted the bytes after offset `0x1240` into a scratch file and inspected
its beginning:

```text
50 4b 03 04 ...
 P  K
```

`50 4b 03 04` is a ZIP local-file header. That makes a ZIP archive a useful
hypothesis, though a signature alone does not prove the archive is complete.
In the exercise, an archive listing succeeded and showed a single text file. I
read that file from the extracted copy and found the challenge message.

## Takeaways

- A normal-looking image can contain bytes beyond the image data.
- Walk the chunk lengths to locate `IEND`. A raw signature search can match
  bytes inside a chunk.
- Treat a file signature as a lead. Check whether the extracted data is
  structurally readable before concluding what it contains.
