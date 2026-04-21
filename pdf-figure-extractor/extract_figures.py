#!/usr/bin/env python3
"""
PDF Figure Extractor
Extracts figures from academic PDFs and saves them for Obsidian.

Usage:
    python3 extract_figures.py <pdf_path> <vault_dir> [--out figures] [--dpi 2.0] [--page 0]

Examples:
    # Extract all figures from a PDF into Obsidian vault
    python3 extract_figures.py paper.pdf /path/to/Obsidian/vault

    # Custom output subdirectory
    python3 extract_figures.py paper.pdf /path/to/Obsidian/vault --out paper_figures

    # Extract from specific page only (0-indexed)
    python3 extract_figures.py paper.pdf /path/to/Obsidian/vault --page 5

    # Preview first (dry run, no files written)
    python3 extract_figures.py paper.pdf /path/to/Obsidian/vault --dry-run
"""
import sys, os, shutil, fitz, re, argparse
from pathlib import Path


def find_captions(page):
    """Return list of (fig_num: int, cap_y: float, label: str) for Figure captions."""
    captions = []
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b["type"] != 0:
            continue
        all_text = "".join(sp["text"] for ln in b["lines"] for sp in ln["spans"])
        # Match "Figure N:" where N is digit(s)
        m = re.search(r"Figure\s+(\d+)", all_text)
        if m and ":" in all_text:
            fig_num = int(m.group(1))
            cap_y = b["bbox"][1]
            # Skip "see Figure N" references (caption is usually above y=100)
            if cap_y > 60:
                captions.append((fig_num, cap_y, all_text[:80].strip()))
    return captions


def extract_figures(pdf_path, vault_dir, out_subdir="figures", dpi=2.0, page_idx=None, dry_run=False):
    """
    Extract figures from PDF and save to Obsidian vault.

    Args:
        pdf_path:   Path to input PDF
        vault_dir:  Obsidian Vault root directory
        out_subdir: Subdirectory under vault/images/ (default: "figures")
        dpi:        Zoom factor for rendering (2.0 = 2x, high quality)
        page_idx:   If set, only process this page (0-indexed)
        dry_run:    If True, scan and print layout without saving files
    """
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(dpi, dpi)
    img_dir = Path(vault_dir) / "images" / out_subdir

    if not dry_run:
        img_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output: {img_dir}")
    else:
        print(f"[DRY RUN] Would output to: {img_dir}")

    # Determine page range
    page_range = [page_idx] if page_idx is not None else range(len(doc))

    for pn in page_range:
        if pn >= len(doc):
            print(f"  Page {pn+1}: out of range (total {len(doc)} pages)")
            continue

        page = doc[pn]
        captions = find_captions(page)

        if not captions:
            print(f"  Page {pn+1}: no figure captions found")
            continue

        print(f"\n  Page {pn+1}: {len(captions)} figure(s) detected")

        # Add sentinel with large y so last figure clips to page height
        bounds = [(n, y, t) for n, y, t in captions]
        bounds.append((None, float("inf"), None))  # sentinel

        for i, (fig_num, cap_y, label) in enumerate(bounds[:-1]):
            next_cap_y = bounds[i + 1][1]

            # Skip if gap < 30pt (likely same caption split across spans)
            if i < len(bounds) - 2 and next_cap_y - cap_y < 30:
                continue

            # Clip to page height for the last figure (sentinel has y=inf)
            y1 = min(next_cap_y - 5, page.rect.height)
            if y1 < 30:  # figure too small
                continue

            rect = fitz.Rect(0, 0, page.rect.width, y1)
            pix = page.get_pixmap(matrix=mat, clip=rect)

            name = f"fig{fig_num}.png"
            out_path = img_dir / name

            if dry_run:
                clipped = min(next_cap_y - 5, page.rect.height)
                print(f"    {name}: page={pn+1} y0=0 y1={clipped:.0f} → {pix.width}x{pix.height}")
            else:
                pix.save(str(out_path))
                print(f"    {name}: {pix.width}x{pix.height} → {out_path}")

    doc.close()

    if dry_run:
        print(f"\n[DRY RUN] No files written.")
        print(f"Run without --dry-run to extract.")


def main():
    ap = argparse.ArgumentParser(
        description="Extract figures from academic PDFs for Obsidian",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    ap.add_argument("pdf_path", help="Path to input PDF")
    ap.add_argument("vault_dir", help="Obsidian Vault root directory")
    ap.add_argument("--out", default="figures",
                    help="Subdirectory under vault/images/ (default: figures)")
    ap.add_argument("--dpi", type=float, default=2.0,
                    help="Render zoom factor, 2.0=high quality (default: 2.0)")
    ap.add_argument("--page", type=int, default=None,
                    help="Process only this page (0-indexed)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Scan and print layout without writing files")

    args = ap.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF not found: {args.pdf_path}")
        sys.exit(1)

    extract_figures(
        args.pdf_path, args.vault_dir,
        out_subdir=args.out, dpi=args.dpi,
        page_idx=args.page, dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
