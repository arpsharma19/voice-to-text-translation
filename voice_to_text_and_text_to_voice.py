import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# Supported Indian Languages and their Language Codes
LANGUAGES = {
    "1": ("English", "en"),
    "2": ("Hindi", "hi"),
    "3": ("Bengali", "bn"),
    "4": ("Punjabi", "pa"),
    "5": ("Tamil", "ta"),
    "6": ("Telugu", "te"),
}

# Initialize Translator
translator = Translator()

# Function for Voice-to-Text
def voice_to_text(language_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"\nListening... (Language: {language_code})")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language=language_code)
            print(f"You said: {text}")
            # Optionally save the text to a file
            with open("recognized_text.txt", "w", encoding="utf-8") as file:
                file.write(text)
            print("Text saved to 'recognized_text.txt'.")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand your speech. Try again.")
        except sr.RequestError:
            print("Request error. Please check your internet connection.")
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
    return None

# Function for Text-to-Voice
def text_to_voice(text, language_code):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Set the voice based on the language (modify for your system configuration)
    if "hi" in language_code:
        engine.setProperty('voice', voices[1].id)  # Example: Hindi voice
    else:
        engine.setProperty('voice', voices[0].id)  # Default voice for other languages
    engine.say(text)
    engine.runAndWait()

# Function for Translating Text
def translate_text(text, source_lang, target_lang):
    try:
        translated = translator.translate(text, src=source_lang, dest=target_lang)
        print(f"\nTranslated Text: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

# Main Menu
def main():
    while True:
        print("\n=== Voice-to-Text, Text-to-Voice, and Translation ===")
        print("Supported Languages:")
        for key, (name, code) in LANGUAGES.items():
            print(f"{key}. {name} ({code})")
        print("7. Exit")
        
        choice = input("\nChoose your language (1-6) or Exit (7): ")
        
        if choice in LANGUAGES:
            language_name, language_code = LANGUAGES[choice]
            print(f"\nYou selected: {language_name} ({language_code})")
            print("\nOptions:")
            print("1. Voice to Text")
            print("2. Text to Voice")
            print("3. Translate Text")
            sub_choice = input("Enter your choice (1/2/3): ")
            
            if sub_choice == '1':
                text = voice_to_text(language_code)
                if text:
                    print(f"Recognized Text: {text}")
            elif sub_choice == '2':
                text = input(f"Enter text in {language_name} to convert to voice: ")
                text_to_voice(text, language_code)
            elif sub_choice == '3':
                source_lang = input("Enter source language code (e.g., en for English): ")
                target_lang = input("Enter target language code (e.g., bn for Bengali): ")
                text = input("Enter text to translate: ")
                translated_text = translate_text(text, source_lang, target_lang)
                if translated_text:
                    print("Translation successful.")
                    text_to_voice(translated_text, target_lang)
            else:
                print("Invalid choice. Returning to main menu.")
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
