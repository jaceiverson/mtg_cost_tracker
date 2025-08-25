import pytest

from mtg_product.tcg import determine_change, get_number_of_arrows


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            [
                {"marketPrice": "12.57"},
                {"marketPrice": "12.57"},
            ],
            "12.57 ➡️ 0.00%",
        ),
        (
            [
                {"marketPrice": "12.57"},
                {"marketPrice": "13.57"},
            ],
            "12.57 ⬇️ -7.37%",
        ),
        (
            [
                {"marketPrice": "12.57"},
                {"marketPrice": "11.57"},
            ],
            "12.57 ⬆️ 8.64%",
        ),
        (
            [
                {"marketPrice": "12.57"},
                {"marketPrice": "1.57"},
            ],
            "12.57 ⬆️⬆️⬆️⬆️⬆️ 700.64%",
        ),
        (
            [
                {"marketPrice": "12.57"},
                {"marketPrice": "24.57"},
            ],
            "12.57 ⬇️⬇️⬇️⬇️⬇️ -48.84%",
        ),
        (
            [
                {"marketPrice": "12.57"},
                {"marketPrice": "9.57"},
            ],
            "12.57 ⬆️⬆️⬆️⬆️ 31.35%",
        ),
        (
            [
                {"marketPrice": "12.57"},
                {"marketPrice": "15.97"},
            ],
            "12.57 ⬇️⬇️⬇️ -21.29%",
        ),
    ],
)
def test_determine_change(inputs, expected):
    result = determine_change(inputs, "marketPrice")
    assert result == expected


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (-1, 5),
        (-0.5, 5),
        (-0.4, 5),
        (-0.3, 4),
        (-0.2, 3),
        (-0.1, 2),
        (-0.05, 1),
        (0, 0),
        (0.05, 1),
        (0.1, 2),
        (0.2, 3),
        (0.3, 4),
        (0.4, 5),
        (0.5, 5),
        (1, 5),
    ],
)
def test_get_number_of_arrows(input_value, expected):
    result = get_number_of_arrows(input_value)
    assert result == expected
