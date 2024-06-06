from typing import Any, List  # noqa

from fastapi import APIRouter, Depends, File, Response, UploadFile  # noqa
from instances import elevenlab, salutespeech

router = APIRouter()


@router.post("/synthesize")
async def synthesize(text: str = None) -> Any:
    """
    Synthesize text.
    """
    audio = elevenlab.synthesize(text)

    return Response(content=audio, media_type="audio/x-wav")


@router.post("/recognize")
async def recognize(
    data: UploadFile = File(...),
) -> Any:
    """
    Recognize audio.
    """
    transcript = await salutespeech.recognize(data.file.read(), data.content_type)

    return Response(content=transcript)
