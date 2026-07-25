#!/usr/bin/env bash
set -euxo pipefail

TARGETPLATFORM="${TARGETPLATFORM:-linux/arm64}"
JUST_VERSION="${JUST_VERSION:-1.46.0}"

mkdir -p /tmp/setup-ctx
pushd /tmp/setup-ctx >/dev/null
trap 'popd && rm -rf "/tmp/setup-ctx"' EXIT

: "TARGETPLATFORM=${TARGETPLATFORM}"
just_url="https://github.com/casey/just/releases/download/${JUST_VERSION}/just-${JUST_VERSION}-aarch64-unknown-linux-musl.tar.gz"

if [[ "${TARGETPLATFORM}" == "linux/arm64" ]]; then
  : ARM is default
elif [[ "${TARGETPLATFORM}" == "linux/amd64" ]]; then
  : x86_64/amd64 - update defaults...
  just_url="https://github.com/casey/just/releases/download/${JUST_VERSION}/just-${JUST_VERSION}-x86_64-unknown-linux-musl.tar.gz"
else
  echo "Unsupported TARGETPLATFORM: ${TARGETPLATFORM}"
  exit 1
fi

: just
curl -sL "${just_url}" -o just.tar.gz
tar -xzf just.tar.gz
install -m 0755 -v -D -o 1000 -g 1000 just /usr/local/bin
