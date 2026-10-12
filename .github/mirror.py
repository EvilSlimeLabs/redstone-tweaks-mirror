"""Bring this mirror up to the newest release of Redstone Tweaks on Modrinth.

    python .github/mirror.py

Asks Modrinth for the project's newest release. When this repository already
holds it, says so and changes nothing. Otherwise downloads its zip, checks it
against the SHA-512 Modrinth publishes, and replaces the pack's files with the
release's, unpacked, so the commit that follows shows exactly what changed.

The version found is written to `$GITHUB_OUTPUT` as `version` when something
changed, which is what the workflow commits and tags by.
"""
import hashlib
import io
import json
import os
import shutil
import sys
import urllib.request
import zipfile

PROJECT = "redstone-tweaks"
API = "https://api.modrinth.com/v2/project/%s/version" % PROJECT
## Modrinth asks every client to name itself
AGENT = "EvilSlimeLabs/redstone-tweaks-mirror (github.com/EvilSlimeLabs/redstone-tweaks-mirror)"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
## what this repository adds beside the pack, and keeps across releases
KEEP = {".git", ".github", ".gitattributes", "README.md", "LICENSE", "VERSION", "SOURCE.json"}


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def newest():
    """The newest release, as Modrinth lists it: newest first."""
    versions = json.loads(fetch(API))
    releases = [v for v in versions if v.get("version_type") == "release"]
    if not releases:
        sys.exit("Modrinth lists no release of %s" % PROJECT)
    return max(releases, key=lambda v: v["date_published"])


def held():
    try:
        with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return None


def unpack(data):
    """Replace the pack's files with the release's.

    A zip that wraps the pack in a folder is unwrapped, so the pack always
    starts at this repository's root, where pack.mcmeta is.
    """
    archive = zipfile.ZipFile(io.BytesIO(data))
    names = [n for n in archive.namelist() if not n.endswith("/")]
    meta = [n for n in names if n.rsplit("/", 1)[-1] == "pack.mcmeta"]
    if not meta:
        sys.exit("the release has no pack.mcmeta; nothing was changed")
    prefix = min(meta, key=len)[:-len("pack.mcmeta")]
    for entry in os.listdir(ROOT):
        if entry in KEEP:
            continue
        path = os.path.join(ROOT, entry)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    root = os.path.realpath(ROOT)
    for name in names:
        if not name.startswith(prefix):
            continue
        target = os.path.realpath(os.path.join(ROOT, name[len(prefix):]))
        ## nothing in an archive may write outside the repository
        if not target.startswith(root + os.sep):
            sys.exit("the release names a path outside the pack: %s" % name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(archive.read(name))


def main():
    version = newest()
    number = version["version_number"]
    if held() == number:
        print("already holding Redstone Tweaks %s" % number)
        return 0
    primary = [f for f in version["files"] if f.get("primary")] or version["files"]
    upload = primary[0]
    print("fetching Redstone Tweaks %s: %s" % (number, upload["url"]))
    data = fetch(upload["url"])
    if hashlib.sha512(data).hexdigest() != upload["hashes"]["sha512"]:
        sys.exit("the download does not match Modrinth's SHA-512; nothing was changed")
    unpack(data)
    with open(os.path.join(ROOT, "VERSION"), "w", encoding="utf-8", newline="\n") as f:
        f.write(number + "\n")
    with open(os.path.join(ROOT, "SOURCE.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"project": PROJECT,
                   "version": number,
                   "version_id": version["id"],
                   "published": version["date_published"],
                   "game_versions": version["game_versions"],
                   "file": upload["filename"],
                   "url": upload["url"],
                   "sha512": upload["hashes"]["sha512"]}, f, indent=2)
        f.write("\n")
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as f:
            f.write("version=%s\n" % number)
    print("now holding Redstone Tweaks %s" % number)
    return 0


if __name__ == "__main__":
    sys.exit(main())
