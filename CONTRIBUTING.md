<!--
Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
SPDX-License-Identifier: MIT
-->

# Contributing

## How do I file an issue?

LLM-assisted issue reports are strongly discouraged in this repository.
All contributions must follow the [Fedora AI-Assisted Contributions Policy](https://docs.fedoraproject.org/en-US/council/policy/ai-contribution-policy/).

Use the [issue tracker] to report bugs or request enhancements.
The default issue template is for bug reports.
A full reproducer is required for bug reports.
**Reports without a full reproducer or with uncompleted sections may be closed.**

For enhancement requests, select **RFE** from GitLab's template selector and
describe the problem or use case and requested behavior.
The **Maintainer** template *may only be used* by the project's authors listed in `pyproject.toml`.

## What issues can I work on?

See the [issue tracker] and issues marked with `help-wanted`, in particular,
for places to start with.
Tickets marked with `idea` are larger changes that may require refinement or
additional discussion.
Feel free to chime in on those issues with any thoughts or if you wish to work
on a solution.
You can also search the code base for `TODO(anyone)`.

## How do I run unit tests?

This project's unit tests, integration tests, and linters are managed by the
`noxfile.py`.
Install `nox` with `dnf install` or `pipx install`.
Run the plain `nox` to run the baseline unit tests and linters.
Run `nox -e all` to additionally run integration tests and check code coverage.

## How do I test the go-vendor-tools main branch locally?

``` bash
sudo dnf copr enable @go-sig/go-vendor-tools-dev
sudo dnf upgrade go-vendor-tools go2rpm
```

## How do I test the go-vendor-tools main branch in mock?

``` bash
copr mock-config @go-sig/go-vendor-tools-dev fedora-rawhide-x86_64 > go-vendor-tools.cfg
fedpkg --release rawhide mockbuild --root go-vendor-tools.cfg
```

[issue tracker]: https://gitlab.com/fedora/sigs/go/go-vendor-tools/-/work_items
