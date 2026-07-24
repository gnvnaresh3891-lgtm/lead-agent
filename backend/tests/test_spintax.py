import pytest
from app.services.personalization.spintax import SpintaxParser

def test_spintax_basic():
    text = "[[Hi|Hello]] there"
    # Testing multiple times to ensure we get both outputs eventually
    outputs = set(SpintaxParser.render(text, {}) for _ in range(20))
    assert "Hi there" in outputs
    assert "Hello there" in outputs
    assert len(outputs) == 2

def test_spintax_with_context():
    text = "[[Hi|Hello]] {first_name}"
    context = {"first_name": "Alex"}
    outputs = set(SpintaxParser.render(text, context) for _ in range(20))
    assert "Hi Alex" in outputs
    assert "Hello Alex" in outputs

def test_spintax_missing_context_safe():
    text = "Hello {missing_var}"
    output = SpintaxParser.render(text, {})
    assert output == "Hello {missing_var}"

def test_spintax_nested():
    text = "[[A|[[B|C]]]]"
    outputs = set(SpintaxParser.render(text, {}) for _ in range(50))
    assert "A" in outputs
    assert "B" in outputs
    assert "C" in outputs
