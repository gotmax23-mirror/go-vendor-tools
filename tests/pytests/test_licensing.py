# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import pytest
from license_expression import ExpressionParseError

from go_vendor_tools.exceptions import LicenseParsingError
from go_vendor_tools.licensing import (
    combine_licenses,
    compare_licenses,
    simplify_license,
)


@pytest.mark.parametrize(
    "expression, expected",
    [
        pytest.param("GPL-2.0-only", "GPL-2.0-only"),
        pytest.param("GPL-2.0-only OR GPL-2.0", "GPL-2.0-only"),
        pytest.param(
            "(MIT OR Apache-2.0) AND Apache-2.0",
            "Apache-2.0 AND (Apache-2.0 OR MIT)",
        ),
        pytest.param(
            "(Apache-2.0 OR MIT) AND Apache-2.0",
            "Apache-2.0 AND (Apache-2.0 OR MIT)",
        ),
        pytest.param(
            "(Apache-2.0 AND (MIT OR Apache-2.0)) AND Apache-2.0",
            "Apache-2.0 AND (Apache-2.0 OR MIT)",
        ),
        pytest.param(
            "Licenseref-Scancode-Public-Domain and LicenseRef-Scancode-Public-Domain-Disclaimer",  # noqa: E501
            "LicenseRef-Fedora-Public-Domain",
        ),
        pytest.param(
            "Licenseref-Scancode-Public-Domain AND LicenseRef-Fedora-Public-Domain",
            "LicenseRef-Fedora-Public-Domain",
        ),
    ],
)
def test_simplify_license(expression: str, expected: str) -> None:
    simplified = simplify_license(expression)
    assert str(simplified) == expected
    assert compare_licenses(expected, simplified)


def test_simplify_with_WITH_succeeds() -> None:
    expected = "LicenseRef-Fedora-Public-Domain WITH LicenseRef-scancode-musl-exception"
    simplified = simplify_license(expected)
    assert str(simplified) == expected
    assert compare_licenses(expected, simplified)


def test_simplify_with_strict_throws() -> None:
    """
    license_expression.parse doesn't like an expression containing exception
    unless it is preceded by WITH. scancode can generate a
    LicenseRef-scancode-musl-exception particle, which causes simplify_license to fail.
    """
    expression = "LicenseRef-Fedora-Public-Domain AND LicenseRef-scancode-musl-exception"  # noqa: E501
    with pytest.raises(ExpressionParseError):
        simplify_license(expression)


def test_simplify_not_strict_returns_a_value() -> None:
    expression = "LicenseRef-Fedora-Public-Domain AND LicenseRef-scancode-musl-exception"  # noqa: E501
    assert simplify_license(expression, strict=False) == expression


def test_compare_with_strict_and_no_invalid_throws() -> None:
    expression = "LicenseRef-Fedora-Public-Domain AND LicenseRef-scancode-musl-exception"  # noqa: E501
    with pytest.raises(LicenseParsingError):
        compare_licenses(expression, expression, allow_invalid=False)


def test_compare_with_strict_and_allow_invalid_defaults_to_false() -> None:
    expression = "LicenseRef-Fedora-Public-Domain AND LicenseRef-scancode-musl-exception"  # noqa: E501
    assert not compare_licenses(expression, expression)


def test_compare_not_strict_succeeds() -> None:
    expression = "LicenseRef-Fedora-Public-Domain AND LicenseRef-scancode-musl-exception"  # noqa: E501
    assert compare_licenses(expression, expression, strict=False)


def test_combine_licenses() -> None:
    combined = combine_licenses("Apache-2.0 OR MIT", "ISC")
    assert str(combined) == "ISC AND (Apache-2.0 OR MIT)"
