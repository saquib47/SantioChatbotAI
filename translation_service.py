from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang):
    """Translate text to the target language"""
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

# Note: In a production environment, you might want to use a more robust
# translation API like Google Cloud Translation or Microsoft Translator