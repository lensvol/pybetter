import hypothesmith
import pytest
from hypothesis import given, settings, HealthCheck

from pybetter.cli import process_file, ALL_IMPROVEMENTS


settings.register_profile(
    "slow_example_generation",
    suppress_health_check=list(HealthCheck),
)
settings.load_profile("slow_example_generation")


@pytest.mark.slow
@given(generated_source=hypothesmith.from_grammar())
def test_no_crashes_on_valid_input(generated_source):
    process_file(generated_source, ALL_IMPROVEMENTS)
