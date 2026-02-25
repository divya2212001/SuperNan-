"""
Translation module for SuperNan project.
Translates text between languages using NLLB model.
"""

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class TranslationService:
    """Service for translating text between languages."""
    
    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M"):
        """
        Initialize the translation service.
        
        Args:
            model_name: Hugging Face model name for translation
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    def translate(self, text: str, source_lang: str = "eng_Latn", target_lang: str = "hin_Deva") -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code (NLLB format)
            target_lang: Target language code (NLLB format)
            
        Returns:
            Translated text
        """
        self.tokenizer.src_lang = source_lang
        
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            generated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(target_lang),
                max_length=512
            )
        
        translated_text = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translated_text
    
    def translate_to_hindi(self, text: str) -> str:
        """
        Translate English text to Hindi.
        
        Args:
            text: English text to translate
            
        Returns:
            Hindi translation
        """
        return self.translate(text, source_lang="eng_Latn", target_lang="hin_Deva")
    
    def translate_to_english(self, text: str, source_lang: str = "hin_Deva") -> str:
        """
        Translate text to English.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            
        Returns:
            English translation
        """
        return self.translate(text, source_lang=source_lang, target_lang="eng_Latn")


# Supported language codes
SUPPORTED_LANGUAGES = {
    "eng_Latn": "English",
    "hin_Deva": "Hindi",
    "spa_Latn": "Spanish",
    "fra_Latn": "French",
    "deu_Latn": "German",
    "ita_Latn": "Italian",
    "por_Latn": "Portuguese",
    "jpn_Jpan": "Japanese",
    "kor_Kore": "Korean",
    "chi_Simp": "Chinese (Simplified)",
}


def translate_to_hindi(text: str) -> str:
    """
    Convenience function to translate English to Hindi.
    
    Args:
        text: English text
        
    Returns:
        Hindi translation
    """
    service = TranslationService()
    return service.translate_to_hindi(text)

