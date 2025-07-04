import pytest
from main import apply_filter

sample_data = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"}
]

def test_filter_equal():
    result = apply_filter(sample_data, "brand=apple")
    assert len(result) == 1
    assert result[0]["name"] == "iphone 15 pro"

def test_filter_greater_than():
    result = apply_filter(sample_data, "rating>4.7")
    assert len(result) == 2

def test_filter_less_than():
    result = apply_filter(sample_data, "price<300")
    assert len(result) == 2

def test_filter_invalid_operator():
    result = apply_filter(sample_data, "rating!4.5")
    assert result == sample_data
