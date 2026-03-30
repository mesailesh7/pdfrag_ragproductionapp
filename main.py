import datetime
import logging
import os
import uuid

import inngest
import inngest.fast_api
from dotenv import load_dotenv
from fastapi import FastAPI
from inngest.experimental import ai
from inngest.experimental.mocked import trigger

load_dotenv()

inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer(),
)


# Invoking inngest
@inngest_client.create_function(
    fn_id="RAG: Inngest PDf", trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
async def rag_inngest_pdf(ctx: inngest.Context):
    return {"Hello": "world"}


app = FastAPI()


inngest.fast_api.serve(app, inngest_client, [])
