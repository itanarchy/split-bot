from typing import Any

from pytoniq_core import Cell
from tonutils.client import ToncenterClient

from app.models.dto import FullGiftCodeData
from app.utils.ton import from_nano


async def get_giftcode_data(address: str, toncenter: ToncenterClient) -> FullGiftCodeData:
    giftcode_data: dict[str, Any] = await toncenter.run_get_method(
        address=address,
        method_name="get_giftcode_data",
    )

    stack: list[Any] = giftcode_data["stack"]
    return FullGiftCodeData(
        owner_address=(
            Cell.from_boc(data=stack[1]["value"])[0]
            .begin_parse()
            .load_address()
            .to_str(is_user_friendly=False)
        ),
        total_activations=int(stack[4]["value"], 16),
        max_activations=int(stack[5]["value"], 16),
        max_buy_amount=from_nano(int(stack[6]["value"], 16)),
    )
