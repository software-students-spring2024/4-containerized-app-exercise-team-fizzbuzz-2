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
        self.idef = idef
        if not idef:
            self.idef = Transcription.transcriptions.insert_one(
                self.to_bson()
            ).inserted_id

    def to_bson(self) -> Dict:
        """
        convert object to BSON
        """
        bson_dict = {}
        if self.idef:
            bson_dict["_id"] = self.idef
        bson_dict["inputed"] = self.inputed
        bson_dict["solution"] = self.solution
        bson_dict["cookie"] = self.scoring.get_cookie()
        bson_dict["score"] = self.scoring.get_score()
        return bson_dict

    def get_inputed(self):
        """
        inputted getter function
        """
        return self.inputed


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
