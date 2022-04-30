'''imports'''
import re
from configparser import ConfigParser
import Communication.Output as out
import Communication.SpeechIn as ind
import wolframalpha


class SearchWolfram():
    '''Query Wolfram Alpha for information'''
    def __init__(self):
        config = ConfigParser()
        # read the api key into memory
        config.read("App/secrets.ini")
        self.__app_id = config.get("wolframalpha", "api_key")
        self.client = wolframalpha.Client(self.__app_id)

    def wolfsearch(self):
        '''the actual search function'''
        out.Output.say("What's your question?")
        question= ind.SpeechIn.listen()
        result = self.get_wolf_results(question)
        # remove everything in parenthesis, because that gave some weird speech
        result = re.sub(r"\([^()]*\)", "", result)
        out.Output.say(result)

    def get_wolf_results(self, question):
        '''the wikipedia query process'''
        client = self.client
        result = client.query(question)
        answer = next(result.results).text
        return answer
    