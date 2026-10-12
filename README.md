# Redstone Tweaks, archival mirror

**This is an archive, not a place to get the pack.** Download Redstone Tweaks
from its author's page on Modrinth:

**https://modrinth.com/resourcepack/redstone-tweaks**

Redstone Tweaks is a Java Edition resource pack by **RexxStone** that makes
redstone easier to read. This repository is not affiliated with RexxStone and is
not maintained by them. Questions and bug reports about the pack belong on
Modrinth or on RexxStone's Discord, https://discord.gg/XaU2wkEtVu, not here.

## Why it exists

[Scaffold](https://github.com/EvilSlimeLabs/Scaffold) converts some of Redstone
Tweaks' textures for its Clearer Redstone options, and includes this repository
as a git submodule so the conversion can be run again. The mirror keeps every
release it has seen, so that work does not depend on any one download staying
available.

## What is here

- Each release exactly as published on Modrinth, unpacked, checked against the
  SHA-512 Modrinth gives for it, and committed once, tagged with its version
  number (`2.5.6`).
- `VERSION`, the release held, and `SOURCE.json`, where it came from and its
  checksum.
- `.github/`, a weekly workflow that adds new releases. Nothing in the pack is
  edited.

## Licence and credit

Redstone Tweaks is licensed under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), whose
text is in `LICENSE`: anything using it must credit RexxStone, may not be sold,
and must be shared under the same licence. The pack's own `credits.txt` names
the creators whose work it builds on.

The workflow and `.github/mirror.py` are the mirror's own, and may be used under
the MIT licence.
