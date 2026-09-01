# FATHER UI Brand Standard

Status: ACTIVE / mandatory for all FATHER sites and web applications.

## Global rule

Every FATHER site must have a visible brand mark/icon in the upper part of the interface. The preferred position is the upper-left corner.

The mark is not decorative only: it is the persistent visual identity anchor of the product family.

## Mandatory behavior

- the brand mark is visible on desktop and mobile;
- the brand mark appears before the primary page content;
- clicking the mark returns the user to the product home/root view;
- the mark has an accessible name/label;
- product name or module name may be shown next to it;
- plain text product naming without a visual mark does not satisfy this rule;
- public/showcase builds also provide a browser favicon derived from the approved brand mark;
- new sites/templates must implement this rule from the first screen, not as later polish.

## Minimum acceptance

- desktop visual mark: at least 32 px;
- mobile visual mark: at least 28 px;
- preferred click target: `/`;
- no FATHER showcase page is accepted if the top brand mark is missing.

## Current OSINT implementation

`osint_web/static/index.html` uses the FATHER `F` sigil as the top-left brand mark and links it to `/`.

When a final corporate icon/logo is approved later, the asset may change, but this placement and behavior contract remains stable.
