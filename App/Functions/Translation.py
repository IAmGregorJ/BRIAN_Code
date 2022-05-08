'''imports'''
import Communication.Output as out
import Communication.SpeechIn as ind
from translate import Translator
from base_logger import logger

class Translate():
    '''Translate English to other languages'''
    def __init__(self):
        self.languages = {
            'tamil':'ta',
            'greek':'el',
            'ukrainian':'uk',
            'arabic':'ar'
        }

    def get_source(self):
        '''Get the input text to translate'''
        out.Output.say("What would you like to have translated?")
        source = ind.SpeechIn.dictate()
        out.Output.say("Would you like to translate the text to "
                        f"{self.get_key_from_value('ta')}, {self.get_key_from_value('el')}, "
                        f"{self.get_key_from_value('uk')} or {self.get_key_from_value('ar')}")
        lang = ind.SpeechIn.listen()
        try:
            val = self.languages[lang]
        except KeyError as ex:
            logger.error(repr(ex))
            out.Output.say("I'm sorry, that wasn't one of the choices.")
        result = self.get_target(val, source)
        out.Output.say(result, val)

    def get_target(self, lang, text):
        '''the google translate source process'''
        translator = Translator(to_lang = lang)
        translation = translator.translate(text)
        return translation

    def get_key_from_value(self, val):
        '''get the dictionary key from the value'''
        languages = self.languages
        for key, value in languages.items():
            if val == value:
                return key
        out.Output.say(f"I'm sorry, {val} isn't available")
