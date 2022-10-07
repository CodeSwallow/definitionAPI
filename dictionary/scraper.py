import traceback
import requests
from bs4 import BeautifulSoup


class DictionaryScraper:
    url = 'https://www.vocabulary.com/dictionary/'

    def get_word(self, word):
        word = word.strip().lower()
        response = requests.get(self.url+word)

        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, 'lxml')
                word_searched = {'word': soup.select_one('h1#hdr-word-area').text.strip(), 'definitions': []}
                word_definitions = soup.select('li.sense')
                for item in word_definitions:
                    part_of_speech, definition = self.get_definition(item)
                    synonyms, antonyms, examples = self.get_synonyms_antonyms(item)
                    word_searched['definitions'].append({
                        'part_of_speech': part_of_speech,
                        'definition': definition,
                        'synonyms': synonyms,
                        'antonyms': antonyms,
                        'examples': examples
                    })
                return word_searched
            except AttributeError as e:
                print(traceback.format_exc())
                return {'error': e}
        return {'error': f'Status code: {response.status_code}'}

    @staticmethod
    def get_definition(body):
        main_definition = body.select_one('div.definition')
        part_of_speech, word_definition = main_definition.text.strip().split(' ', 1)
        return part_of_speech.strip(), word_definition.strip()

    @staticmethod
    def get_synonyms_antonyms(body):
        usage_examples = body.select('div.example')
        syn_ant = body.select('dl.instances')
        synonyms = []
        antonyms = []
        examples = []
        type_of = ''
        for item in syn_ant:
            syn_ant = item.select_one('span.detail')
            if syn_ant.text.strip().lower() == 'synonyms:':
                type_of = 'synonyms'
            elif syn_ant.text.strip().lower() == 'antonyms:':
                type_of = 'antonyms'
            elif syn_ant.text.strip().lower() != '':
                type_of = ''
            syn_ant_1 = item.select('span.detail ~ dd > a.word')
            syn_ant_2 = item.select('span.detail + span > a.word')
            syn_ant_1.extend(syn_ant_2)
            if type_of == 'synonyms':
                for i in syn_ant_1:
                    synonyms.append(i.text.strip())
            if type_of == 'antonyms':
                for i in syn_ant_1:
                    antonyms.append(i.text.strip())

        chars_to_replace = {
            '\n': '',
            '“': '',
            '”': '',
        }
        for example in usage_examples:
            examples.append(example.text.strip().translate(str.maketrans(chars_to_replace)))

        return synonyms, antonyms, examples


