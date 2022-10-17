from fastapi import FastAPI
from starlette.responses import JSONResponse

from moderation_service.core.services.moderate_sentences import has_foul_language
from moderation_service.core.schemas.sentence import Sentence

app = FastAPI()


@app.post("/sentences")
def moderate_sentence_endpoint(sentence: Sentence) -> bool:

    if not sentence.fragment:
        return JSONResponse(content={"hasFoulLanguage": False}, status_code=200)

    return JSONResponse(
        content={"hasFoulLanguage": has_foul_language(sentence.fragment)},
        status_code=200,
    )
