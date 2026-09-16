"""Global pytest configuration and fixture plugin registration."""

import os

from hypothesis import settings

pytest_plugins = [
    "tests.support.fixtures.config",
    "tests.support.fixtures.datasets",
]


def pytest_configure() -> None:
    """Register and load Hypothesis profiles for local and CI runs."""
    settings.register_profile("local", max_examples=120, deadline=200)
    settings.register_profile("ci_fast", max_examples=40, deadline=200)
    settings.register_profile("ci_slow", max_examples=240, deadline=None)
    selected = os.getenv("HYPOTHESIS_PROFILE", "local")
    settings.load_profile(selected)
