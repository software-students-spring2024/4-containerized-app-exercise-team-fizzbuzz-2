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
        if idef:
            self.idef = idef
        else:
            Prompt.prompts.insert_one(self.to_bson())

    def update_db(self):
        """
        update database
        """
        Prompt.prompts.replace_one({"_id": self.idef}, self.to_bson())

    def get_id(self):
        """
        get id
        """
        return str(self.idef)

    def to_bson(self) -> Dict:
        """
        convert object to bson
        """
        bson_dict = {}
        if hasattr(self, "id"):
            bson_dict["_id"] = self.idef
            bson_dict["input"] = self.input
            bson_dict["solution"] = self.solution
            bson_dict["cookie"] = self.cookie
        return bson_dict

    def from_bson(self, bson_dict: Dict) -> Prompt:
        """
        initialize and return object from bson
        """
        if not bson_dict:
            return None
        return Prompt(
            prompt=bson_dict["prompt"],
            difficulty=bson_dict["difficulty"],
            number_of_attempts=bson_dict["number_of_attempts"],
            idef=bson_dict["_id"],
        )
