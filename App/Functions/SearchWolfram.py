'''imports'''
import wolframalpha
import Communication.SpeechIn as ind
import Communication.Output as out

class SearchWolfram():
    '''Query Wolfram Alpha for information'''
    def __init__(self):
        self.__app_id = "LQ7PTH-QRRJ7PGEYJ"
        self.client = wolframalpha.Client(self.__app_id)

    def wolfsearch(self):
        '''the actual search function'''
        out.Output.say("What's your question?")
        question= ind.SpeechIn.listen()
        result = self.get_wolf_results(question)
        out.Output.say(result)

    def get_wolf_results(self, question):
        '''the wikipedia query process'''
        client = self.client
        result = client.query(question)
        answer = next(result.results).text
        return answer
    