# Open fzf picker
[no-cd]
default:
    @just --choose

setup:
    pnpm import
    pnpm install

pnpm-build:
    pnpm run ergogen:build

pnpm-watch:
    pnpm run ergogen:watch

zmk-update:
    pnpm run zmk:update

zmk-build:
    pnpm run zmk:build

zmk-down:
    pnpm run zmk:down