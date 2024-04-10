"""
methods to create and delete collections
"""

from dotenv import dotenv_values
from transcription import Transcription
from prompt import Prompt
from default_values import list_of_prompts

# Loading development configurations
config = dotenv_values(".env")


def start_mgd(se4_db):
    """
    set up collectionss
    """

    if "transcriptions" not in se4_db:
        se4_db.add_collection("transcriptions", "SE_PROJECT4_transcriptions")
    Transcription.transcriptions = se4_db["transcriptions"]

    if "prompts" not in se4_db:
        se4_db.add_collection("prompts", "SE_PROJECT4_prompts")
    Prompt.prompts = se4_db["prompts"]

    add_to_prompts()


def add_to_prompts(prompts=None):
    """
    add default prompts, or pass in choice of prompts, to prompts collection in mongodb
    """
    if prompts is None:
        prompts = list_of_prompts
    Prompt.prompts.insert_many(prompts)


def end_mgd(db, se4_db):
    """
    delete all collections created
    """

    try:
        Prompt.prompts.drop()
        Transcription.transcriptions.drop()
    except AttributeError:
        return

    se4_db.remove_collection("transcriptions")
    se4_db.remove_collection("prompts")

    db.nested_collections.drop({"name": "SE_PROJECT4"})

    return
