---
name: pdf-figure-extractor
description: Extract figures from academic PDFs and insert them into Obsidian notes using PyMuPDF. Auto-detects figure captions, crops precisely, and outputs Markdown image links.
metadata:
  requires:
    bins: ["python3", "pymupdf"]
  skills: []
---

# PDF Figure Extractor

## Skill Overview
Extracts figures from academic PDFs and inserts them as Markdown images into Obsidian notes. Uses **PyMuPDF** to:
1. Auto-detect figure caption positions via text-layer cross-referencing
2. Crop each figure region precisely (2x zoom for quality)
3. Save to Obsidian Vault's `images/` directory
4. Output ready-to-use `![](...)` Markdown links

## Execution Steps

### Step 1 — Verify Dependencies
```bash
python3 -c "import fitz; print('pymupdf ok')"
```
If missing: `pip install pymupdf`

### Step 2 — Locate Figure Captions
Inspect the PDF's text layer to find "Figure N:" caption positions:

```python
import fitz

doc = fitz.open("paper.pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b["type"] != 0: continue
        for ln in b["lines"]:
            for sp in ln["spans"]:
                t = sp["text"].strip()
                if t.startswith("Figure") and ":" in t:
                    print(f"Page {page_num+1}: y={b['bbox'][1]:.1f} '{t[:60]}'")
```

### Step 3 — Determine Crop Bounds

| Case | Crop region |
|:---|:---|
| Figure spans **full page width** above caption | `(0, 0, page_width, caption_y - 5)` |
| Figure in **right column** | `(col_x0, 0, page_width, caption_y - 5)` |
| **Multiple figures** on one page | Use each caption's `y` as boundary |

```python
# Single-figure page
cap_y = caption_block["bbox"][1]
clip = fitz.Rect(0, 0, page.rect.width, cap_y - 5)

# Multi-figure page
cap1 = caption1_y
cap2 = caption2_y
fig_a = fitz.Rect(0, 0, page.rect.width, cap1 - 5)
fig_b = fitz.Rect(0, cap1, page.rect.width, cap2 - 5)
```

### Step 4 — Extract Figures

```python
import fitz, os, shutil

pdf_path  = "paper.pdf"          # input PDF
out_dir   = "/tmp/figures"      # temp staging
vault_dir = "Obsidian/vault"     # Obsidian Vault root

mat = fitz.Matrix(2, 2)          # 2x zoom = high quality
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)

# Example: extract figures from pages 1, 2, 4 (0-indexed)
figure_regions = {
    "fig1": (1, 0, 0, page.rect.width, 0, 164),   # (page, x0, y0, x1, y1)
    "fig2": (2, 0, 0, page.rect.width, 0, 191),
    "fig3": (4, 0, 0, page.rect.width, 0, 271),
}

for name, (page_idx, x0, y0, x1, y1) in figure_regions.items():
    page = doc[page_idx]
    rect = fitz.Rect(x0, y0, x1, y1)
    pix  = page.get_pixmap(matrix=mat, clip=rect)
    pix.save(f"{out_dir}/{name}.png")

doc.close()

# Copy to Obsidian
img_dir = f"{vault_dir}/images/figures"
os.makedirs(img_dir, exist_ok=True)
for f in os.listdir(out_dir):
    shutil.copy2(f"{out_dir}/{f}", f"{img_dir}/{f}")
```

### Step 5 — Insert into Obsidian Note

In the target `.md` file, add images using relative paths from Vault root:

```markdown
## Figure 1: Title

![fig1](images/figures/fig1.png)

**Subject**: ...
**Takeaway**: ...
```

## Auto-Detection Script (Full Pipeline)

Save as `extract_figures.py` and run:

```python
#!/usr/bin/env python3
"""
PDF Figure Extractor
Usage: python3 extract_figures.py <pdf_path> <vault_dir> [--dpi 2]
"""
import sys, os, shutil, fitz, argparse

def find_captions(page):
    """Return list of (fig_num, block_y, all_text) for Figure captions."""
    captions = []
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b["type"] != 0: continue
        all_text = "".join(sp["text"] for ln in b["lines"] for sp in ln["spans"])
        if "Figure " in all_text and ":" in all_text:
            # Extract figure number
            import re
            m = re.search(r"Figure\s+(\d+)", all_text)
            if m:
                captions.append((int(m.group(1)), b["bbox"][1], all_text[:80]))
    return captions

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("vault_dir")
    ap.add_argument("--dpi", type=float, default=2.0, help="Zoom factor (default 2.0)")
    ap.add_argument("--out", default="figures", help="Subdir under images/")
    args = ap.parse_args()

    doc     = fitz.open(args.pdf_path)
    img_dir = os.path.join(args.vault_dir, "images", args.out)
    os.makedirs(img_dir, exist_ok=True)
    mat     = fitz.Matrix(args.dpi, args.dpi)

    for page_num in range(len(doc)):
        page     = doc[page_num]
        captions = find_captions(page)
        if not captions:
            continue

        # Add end-of-page sentinel
        bounds = [(n, y, t) for n, y, t in captions]
        bounds.append((None, page.rect.height, None))  # sentinel

        for i, (fig_num, cap_y, cap_text) in enumerate(bounds[:-1]):
            next_cap_y = bounds[i+1][1]
            # Skip small gaps (< 30pt) — likely same caption split
            if i < len(bounds) - 2 and next_cap_y - cap_y < 30:
                continue
            y1 = next_cap_y - 5
            if y1 - 0 < 50:  # figure too small
                continue
            rect = fitz.Rect(0, 0, page.rect.width, y1)
            pix  = page.get_pixmap(matrix=mat, clip=rect)
            name = f"fig{fig_num}.png"
            pix.save(os.path.join(img_dir, name))
            print(f"  {name}: {pix.width}x{pix.height}")

    doc.close()
    print(f"\nSaved to {img_dir}")

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python3 extract_figures.py paper.pdf /path/to/Obsidian/vault
```

## Tips

- **Caption split across spans**: If "Figure 1:" is split into multiple text spans (common in LaTeX PDFs), use `find_captions()` which joins all spans in a block before matching.
- **Right-column figures**: Add a left x-boundary, e.g., `fitz.Rect(350, 0, page.rect.width, cap_y - 5)` for papers with text in left column.
- **Vector figures**: Pages with 0 `get_images()` results are vector-rendered. The full-page or clipped pixmap captures them correctly.
- **Page dimensions**: Standard ACM/IEEE paper is 612×792 pts (8.5"×11" at 72dpi). At 2x zoom → 1224×1584px.
- **Multi-figure pages**: The auto-detection script groups captions and uses next caption's y as the bottom boundary.
