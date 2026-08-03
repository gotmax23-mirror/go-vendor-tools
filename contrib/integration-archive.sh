#!/bin/bash -x
# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

# Create an archive for a tests/integration specfile

set -euo pipefail

_path="$(command -v go_vendor_archive 2>/dev/null || :)"
_default_path="pipx run --spec ../../../[specfile] go_vendor_archive"
GO_VENDOR_ARCHIVE="${GO_VENDOR_ARCHIVE:-${_path:-${_default_path}}}"
IFS=" " read -r -a command <<< "${GO_VENDOR_ARCHIVE}"
command+=("create")

if test -f ./download-sources.sh; then
    ./download-sources.sh
else
    spectool -g ./*.spec
fi
ls
if [ -f "go-vendor-tools.toml" ]; then
    command+=("--config" "$(pwd)/go-vendor-tools.toml")
fi
time "${command[@]}" "$@" ./*.spec

echo Test idempotency by checking that running again does not replace the archive.
# TODO(gotmax23): The code to detect the archive name is slop. Rewrite it to be more reasonable.
vendor_archives=(./*-vendor.tar.*)
test "${#vendor_archives[@]}" -eq 1
archive_mtime="$(stat --format=%Y "${vendor_archives[0]}")"
command+=("--idempotent")
"${command[@]}" "$@" ./*.spec | grep 'already exists'
test "$(stat --format=%Y "${vendor_archives[0]}")" -eq "${archive_mtime}"
sha512sum -c CHECKSUMS
