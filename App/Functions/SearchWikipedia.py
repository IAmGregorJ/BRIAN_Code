'''imports'''
import warnings
import wikipedia
import Communication.SpeechIn as ind
import Communication.Output as out
from base_logger import logger

warnings.filterwarnings('ignore')

class SearchWikipedia():
    '''Query Wikipedia for items'''
    def __init__(self):
        # limit the number of sentences so the answer is not too long
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
            logger.error(repr(derr))
            # when there's too many results
            result = wikipedia.summary(derr.options[0], sentences = self.sentences)
        except wikipedia.PageError as ex:
            # when there's no results
            logger.error(repr(ex))
            result = f"there were no results for {query}"
        return str(result)
    