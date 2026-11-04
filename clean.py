"""Delete image files that are not referenced by a LaTeX file.

For each TeX file, every image under its image folder (``img/`` next to the
TeX file) that is not referenced in the (uncommented) TeX source is removed.
Edit the INPUTS section below, then run the script.
"""

import glob
import os
import re

############ INPUTS ###############
# TeX file(s) to clean; glob patterns are allowed, e.g. r"src\**\_*.tex"
texPathList = [
    r"src\T02_ml_basics\S1\_linear_regression.tex",
    r"src\T02_ml_basics\S2\_classification.tex",
]

# image folder, relative to each TeX file
imgFolder = "img"

# if True, only list the files that would be deleted (nothing is removed)
bDryRun = False

# extensions considered to be images
extensions = [".png", ".jpg", ".jpeg", ".pdf", ".eps", ".svg"]
###################################

# a % that is not escaped (\%) starts a comment
COMMENT_RE = re.compile(r"(?<!\\)%.*")
# anything inside braces ending with an image extension, e.g. {img/foo.png}
REF_RE = re.compile(
    r"\{([^{}]+?(?:" + "|".join(re.escape(e) for e in extensions) + r"))\}",
    re.IGNORECASE,
)


def norm(path):
    return os.path.normcase(os.path.normpath(path))


def referenced_images(tex_path):
    """Return the set of absolute, normalized image paths used in tex_path."""
    with open(tex_path, "r", encoding="utf-8", errors="replace") as f:
        text = "".join(COMMENT_RE.sub("", line) for line in f)
    tex_dir = os.path.dirname(os.path.abspath(tex_path))
    return {norm(os.path.join(tex_dir, ref.strip())) for ref in REF_RE.findall(text)}


def clean(tex_path):
    tex_dir = os.path.dirname(os.path.abspath(tex_path))
    img_dir = os.path.join(tex_dir, imgFolder)
    print(f"\n== {tex_path}")
    if not os.path.isdir(img_dir):
        print(f"   no image folder '{img_dir}', skipping")
        return

    used = referenced_images(tex_path)
    removed = 0
    for root, _, files in os.walk(img_dir):
        for name in sorted(files):
            if os.path.splitext(name)[1].lower() not in extensions:
                continue
            full = os.path.join(root, name)
            if norm(full) in used:
                continue
            print(
                f"   {'would delete' if bDryRun else 'deleting'}: "
                f"{os.path.relpath(full, tex_dir)}"
            )
            if not bDryRun:
                os.remove(full)
            removed += 1

    # sanity check: references that point to missing files
    for path in sorted(used):
        if not os.path.exists(path):
            print(
                f"   WARNING: referenced but missing: {os.path.relpath(path, tex_dir)}"
            )

    print(
        f"   {len(used)} referenced, {removed} unused "
        f"{'found' if bDryRun else 'deleted'}"
    )


# run relative to this script's folder so the paths above work from anywhere
os.chdir(os.path.dirname(os.path.abspath(__file__)))

for pattern in texPathList:
    for tex in glob.glob(pattern, recursive=True) or [pattern]:
        clean(tex)
