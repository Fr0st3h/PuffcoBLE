from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class ProductInfo:
    type: str
    product_code: int
    model_codes: tuple[int, ...]
    marketing_name: str


_PRODUCT_INFOS: tuple[ProductInfo, ...] = (
    ProductInfo("pikachu", 21, (0, 21, 0xFFFFFFFF), "OG"),
    ProductInfo("pikachu", 22, (1, 22), "Opal"),
    ProductInfo("pikachu", 25, (2,), "Indiglow"),
    ProductInfo("pikachu", 26, (4,), "Guardian"),
    ProductInfo("raichu",  51, (0, 0xFFFFFFFF), "OG"),
    ProductInfo("peach",   71, (13,), "Onyx"),
    ProductInfo("peach",   72, (12,), "Pearl"),
    ProductInfo("peach",   74, (13, 15), "Desert"),
    ProductInfo("peach",   75, (17,), "Flourish"),
    ProductInfo("peach",   78, (19,), "Storm"),
    ProductInfo("peach",   79, (13,), "Onyx"),
    ProductInfo("peach",   80, (12,), "Pearl"),
    ProductInfo("peach",   81, (23,), "Daybreak"),
)

_BY_PRODUCT_CODE: dict[int, ProductInfo] = {
    p.product_code: p for p in _PRODUCT_INFOS
}

_BY_MODEL_CODE: dict[int, ProductInfo] = {}
for p in _PRODUCT_INFOS:
    for mc in p.model_codes:
        _BY_MODEL_CODE.setdefault(mc, p)


def get_product_info(
    *,
    product_code: int | None = None,
    model_code: int | None = None,
) -> Optional[ProductInfo]:
    if product_code is not None:
        info = _BY_PRODUCT_CODE.get(product_code)
        if info:
            return info

    if model_code is not None:
        return _BY_MODEL_CODE.get(model_code)

    return None
