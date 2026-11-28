# Pinned west revisions

`config/west.yml` pins ZMK and every module to an exact commit, so a build is
reproducible while the firmware still follows ZMK `main`. The pins are
maintained with [pin-west](https://github.com/urob/pin-west), which edits only
the `revision:` lines and needs no west workspace.

## The tracking comment

```yaml
revision: f84ef436cd8e88f9d1580a9b86bab2fae8d349c6 # main (2026-07-21)
```

The trailing comment is read by pin-west: it names the branch the pin follows
and the commit date. Do not reword it. A pin **without** such a comment is
treated as a release pin, and a bump would move it to the latest release tag
(for the urob modules that is `v0.3.0`, which does not match ZMK `main`).

## Commands

```bash
just firmware west-pin-check        # every pin is a full, existing SHA matching its comment
just firmware west-bump --dry-run   # show what a bump would change
just firmware west-bump             # rewrite the pins
```

After a bump: `just firmware west-update`, a pristine `just firmware
build-firmware`, flash both halves, then commit.

## nanopb

`nanopb` is pinned by hand to the revision in
`zephyr/submanifests/optional.yaml` and is excluded from `west-bump`. When a
ZMK bump moves Zephyr, copy the new revision from that file.

## Adding a module

Pin it with a tracking comment (`pin-west pin -f config/west.yml` writes one),
and add its name to `west_bump_projects` in `firmware/justfile` and to
`PROJECTS` in `.github/workflows/bump-west.yml`.

## Weekly pull request

`.github/workflows/bump-west.yml` runs the same bump every Monday and opens or
updates one draft pull request on the `pin-west/bump` branch. This repository
has no firmware CI, so that pull request is not built: treat it as a reminder
and verify locally before merging.
