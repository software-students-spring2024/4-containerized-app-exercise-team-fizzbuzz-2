"""
Inference.py: inference

This module contains functions for performing inference using the Speech2Text Processor.

Author: Firas Darwish
"""

from typing import AnyStr, Optional
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration

def test_test():
    return True

def speech2textpipeline(SOURCE: Optional[AnyStr] = None) -> Optional[AnyStr]:
    # To Do: Must add recorded audio

    model = Speech2TextForConditionalGeneration.from_pretrained(
        "facebook/s2t-small-librispeech-asr"
    )
    processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")

    # add
    inputs = processor(SOURCE, sampling_rate=48000, return_tensors="pt")
    generated_ids = model.generate(
        inputs["input_features"], attention_mask=inputs["attention_mask"]
    )

    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)
    # transcription is now list, for example: transcription =
    # ['mister quilter is the apostle of the middle classes and we are glad to welcome his gospel']

    # To Do: Add code to send data back to website

    # To Do: Add code to save transcription to mongoDB database
