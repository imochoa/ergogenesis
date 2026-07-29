# TODO (future): convert the ergogenesis shield to a ZMK module

**Status:** not started — deferred on purpose. The build works today; this is
future-proofing / cleanup only. Do NOT do this reactively.

## Context

`just build-all` currently prints:

```
CMake Deprecation Warning at keymap-module/modules/modules.cmake:53 (message):
  The `config/boards` folder is deprecated. Please use a module instead.
```

It fires from `zmk/app/keymap-module/modules/modules.cmake:53`, guarded by
`if(EXISTS ${ZMK_CONFIG}/boards)`. So the warning is triggered purely by the
existence of `config/boards/` — nothing more. It is a **warning, not an error**;
all three `.uf2` targets build fine with it. ZMK is steering everyone off the
in-config `config/boards/` layout toward shipping a shield as a standalone
**Zephyr/ZMK module**.

**Why bother later:** (a) silences the warning; (b) if ZMK ever promotes it to
an error, the build breaks; (c) a module is a reusable, publishable unit if we
ever want to share the shield. **Why not now:** it touches the same
board-discovery / `west` machinery documented as hard-won in `AGENTS.md`, needs
a `west-update` + pristine rebuild to validate, and buys zero functional change.

## Current layout (relevant bits)

```
firmware/
├── config/                         # west manifest root (self.path: config), ZMK_CONFIG
│   ├── west.yml
│   ├── ergogenesis.conf
│   ├── settings_reset.conf
│   ├── ergogenesis.keymap          # keymap OVERRIDE (edited here); includes
│   │                               #   boards/shields/ergogenesis/{36,helper}.h (relative to config/)
│   └── boards/shields/ergogenesis/ # <-- THIS dir triggers the deprecation
│       ├── ergogenesis.zmk.yml  ergogenesis.dtsi  ergogenesis.keymap (fallback)
│       ├── ergogenesis_left.overlay  ergogenesis_right.overlay
│       ├── 36.h  helper.h  ergogenesis.conf
│       └── Kconfig.shield  Kconfig.defconfig
└── .just/in-devc.just              # generic-build: `west build zmk/app -- -DZMK_CONFIG=config -DSHIELD=...`
```

Build invocation (`.just/in-devc.just`, `generic-build`):
`west build … zmk/app -- -DZMK_CONFIG=/workspace/config -DSHIELD=ergogenesis_left …`

## Key fact that makes this cheap

ZMK reads a `ZMK_EXTRA_MODULES` CMake var and appends it to
`ZEPHYR_EXTRA_MODULES` — see `zmk/app/CMakeLists.txt:6`:

```cmake
set(ZEPHYR_EXTRA_MODULES "${ZMK_EXTRA_MODULES};${CMAKE_CURRENT_SOURCE_DIR}/module;…")
```

So an **in-tree** module (same repo, not a separate git remote) can be
registered with `-DZMK_EXTRA_MODULES=<abs path>` — no `west.yml` project entry
and no extra clone needed.

## Target layout

Move the shield out of `config/boards/` into a module dir (suggested name
`firmware/ergogenesis-module/`, flexible — just NOT `modules/`, which is
west-managed/gitignored):

```
firmware/
├── ergogenesis-module/
│   ├── zephyr/module.yml           # board_root: .
│   └── boards/shields/ergogenesis/ # moved verbatim from config/boards/shields/ergogenesis/
└── config/                         # keeps west.yml, *.conf, ergogenesis.keymap (override)
```

`ergogenesis-module/zephyr/module.yml`:

```yaml
build:
  settings:
    board_root: .
```

(Only `board_root` — the shield has no separate `dts/` bindings dir, so no
`dts_root` needed.)

## Steps

1. `mkdir -p firmware/ergogenesis-module/zephyr` and write `module.yml` (above).
2. `git mv config/boards/shields/ergogenesis firmware/ergogenesis-module/boards/shields/ergogenesis`
   (then remove the now-empty `config/boards/`). Use `git mv` to keep history.
3. In `.just/in-devc.just`, `generic-build`, add to the `west build … --` args:
   `-DZMK_EXTRA_MODULES="{{ fw }}/ergogenesis-module"`.
   `-DZMK_CONFIG=config` and `-DSHIELD=ergogenesis_{left,right}` stay as-is.
4. **Fix the override keymap's includes** (the main wrinkle — see below).
5. `just west-update` (registers nothing new but keeps state consistent), then
   `just build-all` **pristine** and confirm the deprecation warning is gone and
   all three `.uf2` still build.

## The one real wrinkle: keymap-override includes

`config/ergogenesis.keymap` currently does (resolved relative to `config/`):

```c
#include "boards/shields/ergogenesis/36.h"
#include "boards/shields/ergogenesis/helper.h"
```

Once `boards/` leaves `config/`, that path no longer resolves. Options, in order
of preference:

- **A (simplest, robust):** point at the module via a relative path from
  `config/`:
  ```c
  #include "../ergogenesis-module/boards/shields/ergogenesis/36.h"
  #include "../ergogenesis-module/boards/shields/ergogenesis/helper.h"
  ```
  Deterministic (quoted include resolves against the including file's dir); a bit
  ugly but zero build-system magic.
- **B (cleaner includes):** add the shield dir to the preprocessor include path
  (e.g. a `zephyr_include_directories()` in a shield `CMakeLists.txt`, or an
  `-I` in the build args) and switch to `#include <36.h>` / `<helper.h>`. Needs
  verifying that the shield `CMakeLists.txt` is picked up for a shield build.

The **fallback** shield keymap (`…/boards/shields/ergogenesis/ergogenesis.keymap`)
keeps its colocated `#include "./36.h"` — it sits next to the headers, so it is
unaffected by the move.

## Verification

- `just build-all` exits 0, produces `ergogenesis_left/right-nice_nano-zmk.uf2`
  + `settings_reset-nice_nano-zmk.uf2`.
- The `config/boards … deprecated` warning no longer appears in the log.
- Build log still shows `Using keymap file: …/config/ergogenesis.keymap` (the
  override is still in effect) — otherwise the keymap-include fix regressed.

## Rollback

All changes are file moves + a build-arg + include-path edits; `git revert` /
`git mv` back restores the working `config/boards` layout. No irreversible steps.

## Also note

`config/dts/` is deprecated by the same mechanism (`modules.cmake:56`) — we don't
use it, so nothing to do, but don't reintroduce it either.
