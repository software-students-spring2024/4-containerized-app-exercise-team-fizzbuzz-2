"""
class + tools to interact with transcription
"""

from __future__ import annotations
from typing import Dict, AnyStr
from bson.objectid import ObjectId
from pymongo import collection


class Transcription:
    """
    class implementation for transcriptions
    """

    transcriptions: collection

    def __init__(
        self, inputed: AnyStr, solution: AnyStr, scoring: Scoring, idef: ObjectId = None
    ):
        """
        initialize transcription
        """
        self.inputed = inputed
        self.solution = solution
        self.scoring = scoring
        if not idef:
            Transcription.transcriptions.insert_one(self.to_bson())
            self.idef = Transcription.transcriptions.find_one(
                {"inputed": self.inputed}
            )["_id"]

    def update_db(self):
        """
        update database automatically
        """
        Transcription.transcriptions.replace_one({"_id": self.idef}, self.to_bson())

    def get_idef(self):
        """
        get the id of a transcription object
        """
        return str(self.idef)

    def to_bson(self) -> Dict:
        """
        convert object to BSON
        """
        bson_dict = {}
        if hasattr(self, "idef"):
            bson_dict["_id"] = self.idef
        bson_dict["inputed"] = self.inputed
        bson_dict["solution"] = self.solution
        bson_dict["cookie"] = self.scoring.cookie
        bson_dict["score"] = self.scoring.score
        return bson_dict

    def from_bson(self, bson_dict: Dict) -> Transcription:
        """
        create and return object from BSON
        """
        if not bson_dict:
            return None
        cookie = bson_dict["cookie"]
        score = bson_dict["score"]
        return Transcription(
            inputed=bson_dict["inputed"],
            solution=bson_dict["solution"],
            idef=bson_dict["_id"],
            scoring=Scoring(cookie, score),
        )


class Scoring:
    """
    class implementation for Scoring
    """

    def __init__(self, cookie: ObjectId = None, score: int = 0):
        """
        initialize new scoring object
        """
        self.cookie = cookie
        self.score = score

    def get_cookie(self):
        """
        get cookie value
        """
        return self.cookie

    def get_score(self):
        """
        get score value
        """
        return self.score

    def set_cookie(self, new_cookie):
        """
        set cookie value
        """
        self.cookie = new_cookie

    def set_score(self, new_score):
        """
        set score value
        """
        self.score = new_score
