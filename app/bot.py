import json
import logging

from aiogram import Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import dotenv_values
from pydantic import ValidationError

from app.core import aggregator_service as service
from app.core.db import get_db
from app.core.repositories import SampleCollectionRepository
from app.schemas import Request

config = dotenv_values(".env")

db = get_db(config["MONGO_URI"], config["DB_NAME"]).get_db_client()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def rlt_handler(message: types.Message) -> None:
    """
    Handler for aggregation requests.
    """
    sample_collection_repository = SampleCollectionRepository(db["sample_collection"])
    resp = f"Невалидный запрос. Пример запроса:\n{json.dumps(Request.Config.json_schema_extra['example'])}"
    try:
        req_raw = json.loads(message.text)
        req = Request.model_validate(req_raw)
        aggregation_result = await service.aggregate(
            req.dt_from, req.dt_upto, req.group_type.value, sample_collection_repository
        )
        resp = json.dumps(aggregation_result)
    except json.decoder.JSONDecodeError as e:
        logging.log(level=logging.getLevelName("INFO"), msg=f"JSONDecodeError. {e}")
    except ValidationError as e:
        logging.log(level=logging.getLevelName("INFO"), msg=f"Validation error. {e}")
    await message.answer(resp)
