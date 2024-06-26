"""
Inference.py: inference

This module contains functions for performing inference using the Speech2Text Processor.

Author: Firas Darwish
"""

from typing import AnyStr, Optional
from datasets import load_dataset
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration

model = Speech2TextForConditionalGeneration.from_pretrained(
    "facebook/s2t-small-librispeech-asr"
)
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")


def test():
    """
    test
    """
    dso = load_dataset(
        "patrickvonplaten/librispeech_asr_dummy", "clean", split="validation"
    )

    speech2textpipeline(dso[0]["audio"]["array"])


def speech2textpipeline(
    source: Optional[AnyStr] = None, sample_rate: int = 16_000
) -> Optional[AnyStr]:
    """
    Args:
        SOURCE: Audio Input.

    Returns:
        Transcription (string).
    """
    # To Do: Must add recorded audio

    if source is None:
        return None

    # add
    inputs = processor(source, sampling_rate=sample_rate, return_tensors="pt")
    generated_ids = model.generate(
        inputs["input_features"], attention_mask=inputs["attention_mask"]
    )

    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)
    # transcription is now list, for example: transcription =
    # ['mister quilter is the apostle of the middle classes and we are glad to welcome his gospel']

    return transcription
