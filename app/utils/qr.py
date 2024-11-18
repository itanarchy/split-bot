import asyncio
from io import BytesIO

import qrcode
from qrcode.image.base import BaseImage


def make_qr(url: str) -> bytes:
    qr: BaseImage = qrcode.make(data=url)
    qr_io: BytesIO = BytesIO()
    qr.save(qr_io, "PNG")
    qr_io.seek(0)
    return qr_io.read()


async def create_qr_code(url: str) -> bytes:
    return await asyncio.to_thread(make_qr, url=url)
