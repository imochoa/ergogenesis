set positional-arguments := true

set shell := ["bash", "-euco", "pipefail"]

setup:
    pnpm import
    pnpm install

build:
    pnpm run ergogen:build

watch:
    pnpm run ergogen:watch

stl-from-jscad:
    fd -ejscad . . -x npx @jscad/cli@1 "{}" -of stla -o "{.}.stl"
