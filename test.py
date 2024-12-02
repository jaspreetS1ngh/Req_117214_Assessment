import pytest
from app.mqtt_client import calculate_supplement  # Ensure this import points to your actual module

# Test data
# Valid input for single person with no children
valid_input_single = {
    "id": "test1",
    "numberOfChildren": 0,
    "familyComposition": "single",
    "familyUnitInPayForDecember": True
}

valid_input_couple = {
    "id": "test2",
    "numberOfChildren": 0,
    "familyComposition": "couple",
    "familyUnitInPayForDecember": True
}

valid_input_single_with_children = {
    "id": "test3",
    "numberOfChildren": 2,
    "familyComposition": "single",
    "familyUnitInPayForDecember": True
}

valid_input_couple_with_children = {
    "id": "test4",
    "numberOfChildren": 3,
    "familyComposition": "couple",
    "familyUnitInPayForDecember": True
}

invalid_input_not_eligible = {
    "id": "test5",
    "numberOfChildren": 2,
    "familyComposition": "single",
    "familyUnitInPayForDecember": False
}

# Expected outputs based on the above input
expected_output_single = {
    "id": "test1",
    "isEligible": True,
    "baseAmount": 60.0,
    "childrenAmount": 0.0,
    "supplementAmount": 60.0
}

expected_output_couple = {
    "id": "test2",
    "isEligible": True,
    "baseAmount": 120.0,
    "childrenAmount": 0.0,
    "supplementAmount": 120.0
}

expected_output_single_with_children = {
    "id": "test3",
    "isEligible": True,
    "baseAmount": 60.0,
    "childrenAmount": 40.0,   # $20 per child for 2 children
    "supplementAmount": 100.0  # 120 + 40
}

expected_output_couple_with_children = {
    "id": "test4",
    "isEligible": True,
    "baseAmount": 120.0,
    "childrenAmount": 60.0,   # $20 per child for 3 children
    "supplementAmount": 180.0  # 120 + 60
}

expected_output_not_eligible = {
    "id": "test5",
    "isEligible": False,
    "baseAmount": 0.0,
    "childrenAmount": 0.0,
    "supplementAmount": 0.0
}



# Tests
def test_calculate_supplement_single():
    result = calculate_supplement(valid_input_single)
    assert result == expected_output_single, f"Expected {expected_output_single}, but got {result}"


def test_calculate_supplement_couple():
    result = calculate_supplement(valid_input_couple)
    assert result == expected_output_couple, f"Expected {expected_output_couple}, but got {result}"


def test_calculate_supplement_single_with_children():
    result = calculate_supplement(valid_input_single_with_children)
    assert result == expected_output_single_with_children, f"Expected {expected_output_single_with_children}, but got {result}"


def test_calculate_supplement_couple_with_children():
    result = calculate_supplement(valid_input_couple_with_children)
    assert result == expected_output_couple_with_children, f"Expected {expected_output_couple_with_children}, but got {result}"


def test_calculate_supplement_not_eligible():
    result = calculate_supplement(invalid_input_not_eligible)
    assert result == expected_output_not_eligible, f"Expected {expected_output_not_eligible}, but got {result}"
