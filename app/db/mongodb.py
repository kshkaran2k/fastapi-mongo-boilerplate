from bson import json_util
from pymongo import AsyncMongoClient
from typing import Any, Dict, Optional, List, Tuple

from app.config.settings import Config
from app.core.logger import get_logger

logger = get_logger(__name__)


class MongoDB:
    _client: Optional[AsyncMongoClient] = None
    _db = None

    @classmethod
    async def init(cls):
        if not cls._client:
            mongo_uri = Config.MONGO_URI
            cls._client = AsyncMongoClient(mongo_uri)
            cls._db = cls._client.get_default_database()
            logger.info("MongoDB connected successfully.")

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed.")

    @classmethod
    def get_db(cls):
        if cls._db is None:
            raise RuntimeError("MongoDB not initialized. Call init() first.")
        return cls._db


    @classmethod
    async def find_one(cls, collection_name: str, filter_condition: Dict[str, Any], projection: Optional[Dict[str, int]] = None) -> Tuple[bool, Any]:
        try:
            col = cls.get_db()[collection_name]
            doc = await col.find_one(filter_condition, projection)
            if not doc:
                logger.info(f"No document found in {collection_name} for filter {filter_condition}")
                return False, None
            return True, json_util.loads(json_util.dumps(doc))
        except Exception as ex:
            logger.exception(f"find_one failed: {ex}")
            return False, None

    @classmethod
    async def find_all(cls, collection_name: str, filter_condition: Dict[str, Any], skip: int = 0, limit: int = 10, projection: Optional[Dict[str, int]] = None) -> Tuple[bool, List[Any]]:
        try:
            col = cls.get_db()[collection_name]
            cursor = col.find(filter_condition, projection).skip(skip).limit(limit)
            docs = await cursor.to_list(length=limit)
            return True, json_util.loads(json_util.dumps(docs))
        except Exception as ex:
            logger.exception(f"find_all failed: {ex}")
            return False, []

    @classmethod
    async def find_all_without_limit(cls, collection_name: str, filter_condition: Dict[str, Any], projection: Optional[Dict[str, int]] = None) -> Tuple[bool, List[Any]]:
        try:
            col = cls.get_db()[collection_name]
            cursor = col.find(filter_condition, projection)
            docs = await cursor.to_list(length=None)
            return True, json_util.loads(json_util.dumps(docs))
        except Exception as ex:
            logger.exception(f"find_all_without_limit failed: {ex}")
            return False, []

    @classmethod
    async def insert_one(cls, collection_name: str, document: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            col = cls.get_db()[collection_name]
            result = await col.insert_one(document)
            return True, str(result.inserted_id)
        except Exception as ex:
            logger.exception(f"insert_one failed: {ex}")
            return False, None

    @classmethod
    async def increment(cls, collection_name: str, filter_condition: Dict[str, Any], inc_data: Dict[str, Any], set_data: Optional[Dict[str, Any]] = None, upsert: bool = False) -> Tuple[bool, Any]:
        try:
            col = cls.get_db()[collection_name]
            update_doc: Dict[str, Any] = {"$inc": inc_data}
            if set_data:
                update_doc["$set"] = set_data
            result = await col.update_one(filter_condition, update_doc, upsert=upsert)
            return True, result.raw_result
        except Exception as ex:
            logger.exception(f"increment failed: {ex}")
            return False, None

    @classmethod
    async def update_one(cls, collection_name: str, filter_condition: Dict[str, Any], update_data: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            col = cls.get_db()[collection_name]
            result = await col.update_one(filter_condition, {"$set": update_data})
            return True, result.raw_result
        except Exception as ex:
            logger.exception(f"update_one failed: {ex}")
            return False, None

    @classmethod
    async def update_many(cls, collection_name: str, filter_condition: Dict[str, Any], update_data: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            col = cls.get_db()[collection_name]
            result = await col.update_many(filter_condition, {"$set": update_data})
            return True, result.raw_result
        except Exception as ex:
            logger.exception(f"update_many failed: {ex}")
            return False, None

    @classmethod
    async def delete_one(cls, collection_name: str, filter_condition: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            col = cls.get_db()[collection_name]
            result = await col.delete_one(filter_condition)
            return True, result.raw_result
        except Exception as ex:
            logger.exception(f"delete_one failed: {ex}")
            return False, None

    @classmethod
    async def delete_many(cls, collection_name: str, filter_condition: Dict[str, Any]) -> Tuple[bool, Any]:
        try:
            col = cls.get_db()[collection_name]
            result = await col.delete_many(filter_condition)
            return True, result.raw_result
        except Exception as ex:
            logger.exception(f"delete_many failed: {ex}")
            return False, None

    @classmethod
    async def aggregate(cls, collection_name: str, pipeline: List[Dict[str, Any]]) -> Tuple[bool, List[Any]]:
        try:
            col = cls.get_db()[collection_name]
            cursor = await col.aggregate(pipeline)
            docs = await cursor.to_list(length=None)
            return True, json_util.loads(json_util.dumps(docs))
        except Exception as ex:
            logger.exception(f"aggregate failed: {ex}")
            return False, []

