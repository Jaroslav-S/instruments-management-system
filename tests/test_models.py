# tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from instruments.models import Inventory

@pytest.mark.django_db
def test_inventory_create_and_str():
    """
    Create a simple Inventory object and check its string representation.
    """
    inv = Inventory.objects.create(
        group='žestě',
        subgroup='trumpety',
        subsubgroup='nástroj',
        item='Trumpeta B',
        description='Vincent Bach',
        serial_number='4586321'
    )
    s = str(inv)
    assert 'Trumpeta B' in s
    assert 'žestě' in s or 'trumpety' in s  # check the group/subgroup appear in the str()

@pytest.mark.django_db
def test_inventory_clean_subgroup_mismatch_raises():
    """
    Validation: subgroup not valid for a given group should raise ValidationError on full_clean().
    """
    inv = Inventory(
        group='smyčce',
        subgroup='trumpety',  # invalid for 'smyčce'
        subsubgroup='nástroj',
        item='Bad item',
        description='Desc'
    )
    with pytest.raises(ValidationError):
        inv.full_clean()