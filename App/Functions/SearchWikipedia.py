'''imports'''
import warnings
import wikipedia
import Communication.SpeechIn as ind
import Communication.Output as out

warnings.filterwarnings('ignore')

class SearchWikipedia():
    '''Query Wikipedia for items'''
    def __init__(self):
        self.sentences = 2

    def wikisearch(self):
        '''the actual search function'''
        out.Output.say("What keyword would you like to search for?")
        query = ind.SpeechIn.listen()
        result = self.get_wiki_results(query)
        out.Output.say(result)

    def get_wiki_results(self, query):
        '''the wikipedia query process'''
        try:
            result = wikipedia.summary(query, sentences = self.sentences)
        except wikipedia.DisambiguationError as derr:
            result = wikipedia.summary(derr.options[0], sentences = self.sentences)
        except wikipedia.PageError:
            result = f"there were no results for {query}"
        return str(result)
    