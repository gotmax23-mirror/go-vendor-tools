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
GO_VENDOR_ARCHIVE="${archive_command}" \
    bash -x "${repo_root}/contrib/integration-archive.sh"
