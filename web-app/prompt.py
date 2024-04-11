"""
class + tools to interact with prompt
"""

from __future__ import annotations
from typing import Dict, AnyStr
from bson.objectid import ObjectId
from pymongo import collection


class Prompt:
    """
    class for prompt
    """

    prompts: collection = None

    def __init__(
        self,
        prompt: AnyStr,
        difficulty: AnyStr,
        number_of_attempts: int,
        idef: ObjectId = None,
    ):
        """
        initializer
        """
        self.prompt = prompt
        self.difficulty = difficulty
        self.number_of_attempts = number_of_attempts
        self.idef = idef
        if not idef:
            just_inserted = Prompt.prompts.insert_one(self.to_bson())
            self.idef = just_inserted.inserted_id

    def to_bson(self) -> Dict:
        """
        convert object to bson
        """
        bson_dict = {}
        if self.idef:
            bson_dict["_id"] = self.idef
        bson_dict["prompt"] = self.prompt
        return bson_dict

    def get_prompt(self):
        """
        prompt getter function
        """
        return self.prompt
