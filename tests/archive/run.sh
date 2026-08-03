#!/bin/bash
# Copyright (C) 2026 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

set -euo pipefail

fixture="${1:?missing integration fixture name}"
archive_command=/usr/bin/go_vendor_archive
repo_root="${TMT_TREE:?TMT_TREE is not set}"

test -x "${archive_command}"
rpm -qf "${archive_command}"

cd "${repo_root}/tests/integration/${fixture}"

shopt -s nullglob
specfiles=(./*.spec)
test "${#specfiles[@]}" -eq 1
specfile="${specfiles[0]}"

spectool_output="$(spectool --sources "${specfile}")"
printf '%s\n' "${spectool_output}"

source0="$(sed -n 's/^Source0:[[:space:]]*//p' <<< "${spectool_output}")"
source1="$(sed -n 's/^Source1:[[:space:]]*//p' <<< "${spectool_output}")"
test -n "${source0}"
test -n "${source1}"
source0="${source0##*/}"

if test -x ./download-sources.sh; then
    ./download-sources.sh
else
    spectool --get-files "${specfile}"
fi
test -f "${source0}"

archive_args=(create --output "${source1}")
if test -f ./go-vendor-tools.toml; then
    archive_args+=(--config "go-vendor-tools.toml")
fi
archive_args+=("${source0}")

"${archive_command}" "${archive_args[@]}"
test -f "${source1}"
sha512sum --check CHECKSUMS
