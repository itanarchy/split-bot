from typing import Any, Self

from aiogram.fsm.context import FSMContext
from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, PrivateAttr


class PydanticModel(_BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        from_attributes=True,
    )

    __updated: dict[str, Any] = PrivateAttr(default_factory=dict)

    @property
    def model_state(self) -> dict[str, Any]:
        return self.__updated

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self.__updated[name] = value

    @classmethod
    async def from_state(cls, state: FSMContext) -> Self:
        # noinspection PyArgumentList
        return cls(**await state.get_data())

    async def update_state(self, state: FSMContext) -> None:
        await state.update_data(self.model_dump())
