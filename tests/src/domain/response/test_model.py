from func.src.domain.response.model import ResponseModel


def test_assert_init_default_as_none():
    assert ResponseModel.__init__.__defaults__ == (None, None)
