from openkoreantext import OpenKoreanTextProcessor
import sys
sys.path.insert(0, '/Users/junksound/PycharmProjects/datastructure_make/semantic')


class NLP_korean():
    def __init__(self, text):
        self.text = text
        self.processor = OpenKoreanTextProcessor()
    def standarize_token_lst(self, token_lst):
        useless_lst = ['Space','Josa','Punctuation','Koreanpractical']
        token_st_lst = []
        for token in token_lst:
            if token[1] in useless_lst:
                pass
            else:
                token_st_lst.append(token[0])
        return token_st_lst
    def standarize_phrase_lst(self, phrase_lst):
        phrase_st_lst = []
        for phrase in phrase_lst:
            phrase_st_lst.append(phrase[0])
        return phrase_st_lst
    def nlp_nomal(self):
        normalized_text = self.processor.normalize(self.text)
        return normalized_text
    def nlp_tokenize(self):
        token_lst = self.processor.tokenize(self.text)
        return token_lst
    def nlp_phrase(self):
        phrase_lst = self.processor.extractPhrases(self.text)
        return phrase_lst
    def sum_token_phrase(self, token_st_lst, phrase_st_lst):
        complete_lst = list(set(token_st_lst)|set(phrase_st_lst))
        return complete_lst

if __name__ =='__main__':
    text1 = '미끄럽지 않은 도마'
    text2 = '빨갛지 않은 사과'
    text3 = '100ml 이하의 우유'
    text4 = '미끄럼 방지 도마'
    text5 = '미끄럽지 않은 도마'
    text6 = '균이 없는 도마'
    text7 = '스텐이 아닌 후라이팬'
    text8 = '색깔이 빨갛지 않고,크기가 50cm이상은 되고, 재질이 스텐이 아닌 후라이팬'
    mod1 = NLP_korean(text3)
    token_lst = mod1.nlp_tokenize()
    token_st_lst = mod1.standarize_token_lst(token_lst)
    phrase_lst = mod1.nlp_phrase()
    phrase_st_lst = mod1.standarize_phrase_lst(phrase_lst)
    complete_lst = mod1.sum_token_phrase(token_st_lst,phrase_st_lst)
    print(token_st_lst)
    print(phrase_st_lst)
    print(complete_lst)

