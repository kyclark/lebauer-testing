import io
from finder import find_words


# --------------------------------------------------
def test_find_words() -> None:
    """Test find_words"""

    text = lambda: [io.StringIO('The quick brown fox jumps over the lazy dog.')]
    assert find_words(1, text()) == []
    assert find_words(2, text()) == []
    assert find_words(3, text()) == ['The', 'fox', 'the', 'dog']
    assert find_words(4, text()) == ['over', 'lazy']
    assert find_words(5, text()) == ['quick', 'brown', 'jumps']
    assert find_words(6, text()) == []
