# MINA identity

MIYAZAKI の MI + NAOYA の NA。点がつながり、私の形になる。

Approved direction: a single angular crown monogram, three large solid circular terminals, no interior white-dot cutouts. Lower terminals share a y=156 baseline and 10-unit horizontal end face, with exact right-angle outer corners. The N diagonal makes the internal structure intentionally asymmetric. The public wordmark remains MIYAZAKINAOYA.

## Source and exports
- Geometry master: `assets/mina-study/crown-master.json` (200-square viewBox).
- Visible regular mark: translate down 5 units for optical centering; icon artwork uses the same silhouette.
- Small-tab variant: 1.17× around the optical center. No invented alternate letterform.
- Maskable variant: 0.82×, wholly within the central 80%-diameter safe circle.
- `tools/build-mark.py`: primary, inverse, adaptive favicon and monochrome pinned-tab SVG.
- `tools/render-assets.py`: PNG/ICO and Apple/Android/maskable exports. Build-time CairoSVG/Pillow only; no runtime dependency.
- `tools/render-share-card.py`: home/profile/404/MINA social cards.
- `mina.html`: point→line→final crown sequence plus the earlier angular 01→03 construction history. No autoplay; keyboard/range controls; reduced-motion and no-JS completion.

## Verification and limits
Inspect 16/32/48/64/180/192px artwork at native size, positive and inverse, and actual desktop/mobile screenshots. At 16px, small counters are not individually letter-legible; the crown silhouette is the primary recognition cue. No claim that all four letters are equally readable. Logo adoption does not rename or recolor the independently branded WORLD sites.
