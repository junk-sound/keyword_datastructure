import excel_to_py as ep
import pickle
import os

class Node(object):

    def __init__ (self, d, n = None):
        self.data = d
        self.next_node = n

    def get_next (self):
        return self.next_node

    def set_next (self, n):
        self.next_node = n

    def get_data (self):
        return self.data

    def set_data (self, d):
        self.data = d

class LinkedList (object):

    def __init__(self, r = None):
        self.root = r
        self.size = 0
        self.tail = None

    def get_size (self):
        return self.size

    def add_first (self, d):
        new_node = Node (d, self.root)
        self.root = new_node
        if self.root.get_next() == None:
            self.tail = self.root
        self.size += 1

    def add_common (self, d, idx):
        if idx == 0:
            self.add_first(d)
        else:
            temp1 = self.check_node(idx-1)
            temp2 = temp1.get_next()
            new_node = Node(d)
            temp1.set_next(new_node)
            new_node.set_next(temp2)
            self.size += 1
            if new_node.get_next() == None:
                self.tail = new_node

    def add_last(self, d):
        new_node = Node (d)
        if self.size == 0:
            self.add_first(d)
        else:
            self.tail.set_next(new_node)
            self.tail = new_node
            self.size += 1

    def remove (self, d):
        this_node = self.root
        prev_node = None

        while this_node:
            if this_node.get_data() == d:
                if prev_node:
                    prev_node.set_next(this_node.get_next())
                else:
                    self.root = this_node.get_next()
                self.size -= 1
                return True		# data removed
            else:
                prev_node = this_node
                this_node = this_node.get_next()
        return False  # data not found

    def find (self, d):
        this_node = self.root
        while this_node:
            if this_node.get_data() == d:
                return d
            else:
                this_node = this_node.get_next()
        return None

    def check_node(self, idx_range):
        temp_node = self.root
        for idx in range(idx_range-1):
            temp_node = temp_node.get_next()
        return temp_node
    def print_result(self):
        if self.root == None:
            return []
        temp = self.root
        result_list = []
        while temp.get_next() != None:
            result_list.append(temp.get_data())
            temp = temp.get_next()
        result_list.append(temp.get_data())
        return result_list

class Hash_dic:
    def __init__(self, Hashmap_Pickle_name, Categorykeys_Pickle_name, UpKeys_Pickle_name, KeyDowns_Pickle_name, Antonym_graph_Pickle_name):
        '''
        이전 해시맵 전체, 카테고리 그래프, 상위어 그래프, 하위어 그래프, 반의어 그래프를 불러옵니다. 만약 처음 py파일을 돌리는거라 없으면, 빈 딕셔너리를 불러옵니다.
        :param Hashmap_Pickle_name: 이전 전체 해시맵의 피클 이름입니다.
        :param Categorykeys_Pickle_name: 저장해둔 카테고리 그래프입니다.
        :param UpKeys_Pickle_name: 저장해둔 상위어 그래프입니다.
        :param KeyDowns_Pickle_name: 저장해둔 하위어 그래프입니다.
        '''
        self.Hashmap_Pickle_name = Hashmap_Pickle_name
        if os.path.exists(Hashmap_Pickle_name):
            f = open(Hashmap_Pickle_name, 'rb')
            self.hashmap = pickle.load(f)
            f.close()
        else:
            self.hashmap = {}

        if os.path.exists(Categorykeys_Pickle_name):
            f2 = open(Categorykeys_Pickle_name, 'rb')
            self.category_graph = pickle.load(f2)
            f2.close()
        else:
            self.category_graph = {}

        if os.path.exists(UpKeys_Pickle_name):
            f3 = open(UpKeys_Pickle_name, 'rb')
            self.up_graph = pickle.load(f3)
            f3.close()
        else:
            self.up_graph = {}

        if os.path.exists(KeyDowns_Pickle_name):
            f4 = open(KeyDowns_Pickle_name, 'rb')
            self.down_graph = pickle.load(f4)
            f4.close()
        else:
            self.down_graph = {}

        if os.path.exists(Antonym_graph_Pickle_name):
            f5 = open(Antonym_graph_Pickle_name, 'rb')
            self.antonym_graph = pickle.load(f5)
            f5.close()
        else:
            self.antonym_graph = {}

    def add_or_change(self, dic_categorykey_info = {}, dic_up_uplikes = {}, dic_down_downlikes = {}):
        '''
        키워드, 상위어, 하위어에 대한 판다스 아웃풋 중 첫번째, 즉 수정 추가할 키워드 정보를 수정, 추가합니다.
        :param dic_categorykey_info: 키워드 정보에 대한 판다스 아웃풋 중 첫번째, 수정 추가할 키워드 정보입니다.
        :param dic_up_uplikes: 상위어-상위 유의어에 대한 판다스 아웃풋 중 첫번째, 수정 추가할 상위어입니다.
        :param dic_down_downlikes: 히위어-하위 유의어에 대한 판다스 아웃풋 중 첫번째, 수정 추가할 하위어입니다. 
        :return: 별도의 리턴 없습니다.
        '''

        for category_key_tuple in dic_categorykey_info.keys():
            self.hashmap[category_key_tuple[1]] = (category_key_tuple[1], '키워드', '101')
            for keylike_weight in dic_categorykey_info[category_key_tuple][1]:
                if keylike_weight == '-':
                    pass
                else:
                    keylike = keylike_weight.split('_')[0]
                    weight = keylike_weight.split('_')[1]
                    if keylike in self.hashmap:
                        del self.hashmap[keylike]
                    self.hashmap[keylike] = (category_key_tuple[1], '키워드', weight)
        for up in dic_up_uplikes.keys():
            self.hashmap[up] = (up, '상위어', '101')
            for uplike_weight in dic_up_uplikes[up]:
                if uplike_weight == '-':
                    pass
                else:
                    uplike = uplike_weight.split('_')[0]
                    weight = uplike_weight.split('_')[1]
                    if uplike in self.hashmap:
                        del self.hashmap[uplike]
                    self.hashmap[uplike] = (up, '상위어', weight)
        for down in dic_down_downlikes.keys():
            self.hashmap[down] = (down, '하위어', '101')
            for downlike_weight in dic_down_downlikes[down]:
                if downlike_weight == '-':
                    pass
                else:
                    downlike = downlike_weight.split('_')[0]
                    weight = downlike_weight.split('_')[1]
                    if downlike in self.hashmap:
                        del self.hashmap[downlike]
                    self.hashmap[downlike] = (down, '하위어', weight)
        # self.save_hashmap()

    def delete(self, dic_categorykey_info= {}, dic_up_uplikes = {}, dic_down_downlikes = {}):
        '''
        키워드, 상위어, 하위어에 대한 판다스 아웃풋 중 두번째, 즉 삭제할 단어 정보를 삭제합니다.
        :param dic_categorykey_info: 키워드 정보에 대한 판다스 아웃풋 중 두번째, 삭제할 키워드 정보입니다.
        :param dic_up_uplikes: 상위어-상위 유의어에 대한 판다스 아웃풋 중 두번째, 삭제할 상위어입니다.
        :param dic_down_downlikes: 히위어-하위 유의어에 대한 판다스 아웃풋 중 두번째, 삭제할 하위어입니다.  
        :return: 별도 리턴 없습니다.
        '''
        for category_key_tuple in dic_categorykey_info.keys():
            if category_key_tuple[1] in self.hashmap:
                del self.hashmap[category_key_tuple[1]]
            else:
                print('해당 단어가 해시맵에 존재하지 않습니다. 이유는 아직 모르겠습니다.')
            for keylike_weight in dic_categorykey_info[category_key_tuple][1]:
                if keylike_weight == '-':
                    if keylike_weight in self.hashmap:
                        del self.hashmap[keylike_weight]
                else:
                    keylike = keylike_weight.split('_')[0]
                    if keylike in self.hashmap:
                        del self.hashmap[keylike]
                    else:
                        print('해당 단어가 해시맵에 존재하지 않습니다. 이유는 아직 모르겠습니다.')

        for up in dic_up_uplikes.keys():
            if up in self.hashmap:
                del self.hashmap[up]
            else:
                print('해당 단어가 해시맵에 존재하지 않습니다. 이유는 아직 모르겠습니다.')

            for uplike_weight in dic_up_uplikes[up]:
                if uplike_weight == '-':
                    if uplike_weight in self.hashmap:
                        del self.hashmap[uplike_weight]
                else:
                    uplike = uplike_weight.split('_')[0]
                    if uplike in self.hashmap:
                        del self.hashmap[uplike]
                    else:
                        print('해당 단어가 해시맵에 존재하지 않습니다. 이유는 아직 모르겠습니다.')

        for down in dic_down_downlikes.keys():
            if down in self.hashmap:
                del self.hashmap[down]
            else:
                print('해당 단어가 해시맵에 존재하지 않습니다. 이유는 아직 모르겠습니다.')

            for downlike_weight in dic_down_downlikes[down]:
                if downlike_weight == '-':
                    if downlike_weight in self.hashmap:
                        del self.hashmap[downlike_weight]
                else:
                    downlike = downlike_weight.split('_')[0]
                    if downlike in self.hashmap:
                        del self.hashmap[downlike]
                    else:
                        print('해당 단어가 해시맵에 존재하지 않습니다. 이유는 아직 모르겠습니다.')
        # self.save_hashmap()

    def make_graph(self, dic_categorykey_info_add, dic_categorykey_info_del):
        '''
        키워드에 대한 판다스 아웃풋으로 필요한 그래프들을 완성해줍니다. py파일을 처음으로 돌리는거면 생성해줄 것이고, 두 번째 부터는 수정사항에 대해서만 추가,삭제해줍니다.
        :param dic_categorykey_info_add: 키워드에 대한 판다스 아웃풋 중 추가할 것, 수정할 것
        :return: 별도의 리턴값 없습니다.
        '''
        for category_key_tuple in dic_categorykey_info_add.keys():
            if category_key_tuple[0] == '-':
                print('***주의: 카테고리가 null값입니다. 확인해주십시오.')
            else:
                if category_key_tuple[0] not in self.category_graph:
                    self.category_graph[category_key_tuple[0]] = [category_key_tuple[1]]
                else:
                    self.category_graph[category_key_tuple[0]].append(category_key_tuple[1])
                if category_key_tuple[1] not in self.category_graph:
                    self.category_graph[category_key_tuple[1]] = [category_key_tuple[0]]
                else:
                    self.category_graph[category_key_tuple[1]].append(category_key_tuple[1])



            if dic_categorykey_info_add[category_key_tuple][0] == ['-']:
                pass
            else:
                for up_weight in dic_categorykey_info_add[category_key_tuple][0]:

                    up = up_weight.split('_')[0]
                    weight = up_weight.split('_')[1]
                    if up not in self.up_graph:
                        self.up_graph[up] = [(category_key_tuple[1],weight)]
                    else:
                        self.up_graph[up].append((category_key_tuple[1],weight))



            if dic_categorykey_info_add[category_key_tuple][2] == ['-']:
                pass
            else:
                for down_weight in dic_categorykey_info_add[category_key_tuple][2]:
                    down = down_weight.split('_')[0]
                    weight = down_weight.split('_')[1]

                    if category_key_tuple[1] not in self.down_graph:
                        self.down_graph[category_key_tuple[1]] = [(down,weight)]
                    else:
                        self.down_graph[category_key_tuple[1]].append((down,weight))
                    if down not in self.down_graph:
                        self.down_graph[down] = [(category_key_tuple[1], weight)]
                    else:
                        self.down_graph[down].append((category_key_tuple[1], weight))


            if dic_categorykey_info_add[category_key_tuple][3] == ['-']:
                pass
            else:
                for antonym in dic_categorykey_info_add[category_key_tuple][3]:
                    if category_key_tuple[1] not in self.antonym_graph:
                        self.antonym_graph[category_key_tuple[1]] = [antonym]
                    else:
                        self.antonym_graph[category_key_tuple[1]].append(antonym)

        '''
        삭제 실제로 해봐야합니다.
        '''

        for category_key_tuple in dic_categorykey_info_del.keys():

            if category_key_tuple[0] in self.category_graph and category_key_tuple[1] in self.category_graph[category_key_tuple[0]]:
                self.category_graph[category_key_tuple[0]].remove(category_key_tuple[1])
            else:
                print('***오류: 내가 상상하지 못한 일이 생겼습니다.')
            if category_key_tuple[1] in self.category_graph and category_key_tuple[0] in self.category_graph[category_key_tuple[1]]:
                self.category_graph[category_key_tuple[1]].remove(category_key_tuple[0])
            else:
                print('***오류: 내가 상상하지 못한 일이 생겼습니다.')


            if dic_categorykey_info_del[category_key_tuple][0] == ['-']:
                if '-' in self.up_graph:
                    self.up_graph['-'].remove('-')
            else:
                for up_weight in dic_categorykey_info_del[category_key_tuple][0]:
                    up = up_weight.split('_')[0]
                    weight = up_weight.split('_')[1]
                    if up in self.up_graph and (category_key_tuple[1], weight) in self.up_graph[up]:
                        self.up_graph[up].remove((category_key_tuple[1], weight))
                    else:
                        print('***오류: 내가 상상하지 못한 일이 생겼습니다.')


            if dic_categorykey_info_del[category_key_tuple][2] == ['-']:
                if '-' in self.up_graph:
                    del self.up_graph['-']
            else:
                for down_weight in dic_categorykey_info_del[category_key_tuple][2]:
                    down = down_weight.split('_')[0]
                    weight = down_weight.split('_')[1]
                    if category_key_tuple[1] in self.down_graph and (down, weight) in self.down_graph[category_key_tuple[1]]:
                        self.down_graph[category_key_tuple[1]].remove((down, weight))
                    else:
                        print('***오류: 내가 상상하지 못한 일이 생겼습니다.')
                    if down in self.down_graph and (category_key_tuple[1], weight) in self.down_graph[down]:
                        self.down_graph[down].remove((category_key_tuple[1], weight))
                    else:
                        print('***오류: 내가 상상하지 못한 일이 생겼습니다.')
            if dic_categorykey_info_del[category_key_tuple][3] == ['-']:
                if '-' in self.antonym_graph:
                    del self.antonym_graph['-']
            else:
                for antonym in dic_categorykey_info_del[category_key_tuple][3]:
                    if category_key_tuple[1] in self.antonym_graph and antonym in self.antonym_graph[category_key_tuple[1]]:
                        self.antonym_graph[category_key_tuple[1]].remove(antonym)
                    else:
                        print('***오류: 내가 상상하지 못한 일이 생겼습니다.')

    #     '판다스 아웃풋으로 상위어 하위어 카테고리에 대한 딕셔너리 새로 만들어줌'

    def get(self, key):
        '''
        모듈 1의 아웃풋 중 하나의 단어에 대해, 해시맵에 넣어 찾아줍니다. 아웃풋은 튜플 형식의 (정규화된 단어, 소속)입니다.
        :param key: 하나의 단어입니다. 예를 들어 스텐, 스텡 등
        :return: 해시맵에서 찾아준 값입니다. (정규화된 단어, 소속)
        '''
        return self.hashmap.get(key)

    def save_hashmap(self):
        '''
        전체 해시맵을 저장해줍니다.
        :return: 별도 리턴 없습니다.
        '''
        f = open(self.Hashmap_Pickle_name, 'wb')
        pickle.dump(self.hashmap, f)
        f.close()

    def search_graph(self, hashout):
        '''
        해시맵 아웃풋의 소속이 상위어, 하위어, 반의어인 경우 그래프를 검색합니다.
        :param hashout: 모듈 1의 인풋 중 하나를 해시에 넣은 아웃풋입니다. 형태는 튜플 형식의 ('단어', '소속')입니다. 예를 들어 ('밝은','상위어') 입니다.
        :return: 그래프에 넣은 값입니다. 예를 들어 인풋의 단어가 '밝은'이면 리스트 형식의 ['red',white','yellow']가 나옵니다.
        '''
        if hashout[1] == '반의어':
            if hashout[0] in self.antonym_graph:
                antonym_lst = self.antonym_graph[hashout[0]]
                return antonym_lst

            else:
                else_lst = []
                category_lst = self.category_graph[hashout[0]]
                for category in category_lst:
                    words_in_same_cate = self.category_graph[category]
                    words_except_key = words_in_same_cate.remove(hashout[0])
                    else_lst.extend(words_except_key)
                return else_lst

        elif hashout[1] == '상위어':
            key_lst = self.up_graph[hashout[0]]
            return key_lst

        elif hashout[1] == '하위어':
            down_lst = self.down_graph[hashout[0]]
            return down_lst


    def return_hashmap(self):
        '''
        전체 해시맵을 리턴해줍니다.
        :return: 전체 해시맵
        '''
        return self.hashmap

    def return_keylikes(self):
        '''
        해시맵에서 소속이 키워드인 모든 정규화된 단어(value)들을 리턴해줍니다.
        :return: 소속이 키워드인 모든 단어 리스트 
        '''
        all_keywords_lst = []
        for key in self.hashmap.keys():
            word_belong_tuple = self.hashmap[key]
            if word_belong_tuple[1] == '키워드':
                all_keywords_lst.append(key)
        return all_keywords_lst

    def return_uplikes(self):
        '''
        해시맵에서 소속이 상위어인 모든 정규화된 단어(value)들을 리턴해줍니다.
        :return: 소속이 상위어인 모든 단어 리스트 
        '''
        all_uplikes_lst = []
        for key in self.hashmap.keys():
            word_belong_tuple = self.hashmap[key]
            if word_belong_tuple[1] == '상위어':
                all_uplikes_lst.append(key)
        return all_uplikes_lst

    def return_downlikes(self):
        '''
        해시맵에서 소속이 하위어인 모든 정규화된 단어(value)들을 리턴해줍니다.
        :return: 소속이 상위어인 모든 단어 리스트
        '''
        all_downlikes_lst = []
        for key in self.hashmap.keys():
            word_belong_tuple = self.hashmap[key]
            if word_belong_tuple[1] == '하위어':
                all_downlikes_lst.append(key)
        return all_downlikes_lst

    def print_result(self, *args):
        '''
        괄호 안에 무슨 값을 넣느냐에 따라 해시맵, 키워드, 하위어를 프린트해줍니다.
        :param args: '사전', '관계어 사전', '관계어사전', '관계어', '해시맵', '키워드','상위어','하위어' 등이 들어갈 수 있습니다.
        :return: 따로 없습니다.
        '''

        hash_map = self.return_hashmap()
        keylikes = self.return_keylikes()
        uplikes = self.return_uplikes()
        downlikes = self.return_downlikes()

        if '사전' in args or '관계어 사전' in args or '관계어사전' in args or '관계어' in args or '해시맵' in args:
            print('관계어 사전입니다:', hash_map)
        if '키워드' in args:
            print('키워드입니다:', keylikes)
        if '상위어' in args:
            print('상위어입니다:', uplikes)
        if '하위어' in args:
            print('하위어입니다:', downlikes)

class HashMap:
    def __init__(self, size):
        self.size = size
        self.map = [None] * self.size
    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size
    def add(self, key, value):
        key_hash = self._get_hash(key)

        key_value = [key, value]

        if self.map[key_hash] is None:

            self.map[key_hash] = list([key_value])

            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True
    def change_key(self, old_key, new_key):
        value = self.get(old_key)
        if value is not None:
            self.add(new_key, value)
            self.delete(old_key)
    def change_value(self, key, new_value):
        if type(new_value) == tuple:
            key_hash = self._get_hash(key)
            if self.map[key_hash] is None:
                return False
            else:
                for pair in self.map[key_hash]:
                    if pair[0] == key:
                        pair[1] = new_value
                        return True
                return False
        else:
            return False
    def change_key_value(self, old_key, new_key, new_value):
        if type(new_value) == tuple:
            self.delete(old_key)
            self.add(new_key, new_value)
        else:
            return False
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
    def print(self):
        print(self.map)
        for item in self.map:
            if item is not None:
                pass
                # print(str(item))
    def return_all_words(self):
        all_word_lst = []
        for bucket in self.map:
            if bucket is not None:
                for pair in bucket:
                    all_word_lst.append((pair[0],pair[1][1]))
        return all_word_lst
    def return_all_ketwords(self):
        all_key_lst = []
        for bucket in self.map:
            if bucket is not None:
                for pair in bucket:
                    if pair[1][1] == '키워드':
                        all_key_lst.append(pair[0])
        return all_key_lst
    def return_up_keys(self):
        all_up_keys_dic = {}
        for bucket in self.map:
            if bucket is not None:
                for pair in bucket:
                    if pair[1][1] == '상위어':

                        if pair[1][0] in all_up_keys_dic:
                            all_up_keys_dic[pair[1][0]].append(pair[0])
                        else:
                            all_up_keys_dic[pair[1][0]] = [pair[0]]
        return all_up_keys_dic
    def return_down_keys(self):
        all_down_keys_dic = {}
        for bucket in self.map:

            if bucket is not None:
                for pair in bucket:
                    if pair[1][1] == '하위어':
                        if pair[1][0] in all_down_keys_dic:
                            all_down_keys_dic[pair[1][0]].append(pair[0])
                        else:
                            all_down_keys_dic[pair[1][0]] = [pair[0]]
        return all_down_keys_dic
    def return_keys_with_synonym(self):
        all_synonym_keys_dic = {}
        for bucket in self.map:

            if bucket is not None:
                for pair in bucket:
                    if pair[1][1] == '동의어':
                        if pair[1][0] in all_synonym_keys_dic:
                            all_synonym_keys_dic[pair[1][0]].append(pair[0])
                        else:
                            all_synonym_keys_dic[pair[1][0]] = [pair[0]]
        return all_synonym_keys_dic
    def return_keys_with_antonym(self):
        all_antonym_keys_dic = {}
        for bucket in self.map:
            if bucket is not None:
                for pair in bucket:
                    if pair[1][1] == '반의어':
                        if pair[1][0] in all_antonym_keys_dic:
                            all_antonym_keys_dic[pair[1][1]].append(pair[0])
                        else:
                            all_antonym_keys_dic[pair[1][0]] = [pair[0]]
        return all_antonym_keys_dic
    def print_result(self, *args):

        all_keys = self.return_all_ketwords()
        all_words = self.return_all_words()
        all_keys_with_synonym = self.return_keys_with_synonym()
        all_keys_with_antonym = self.return_keys_with_antonym()
        all_up_keys = self.return_up_keys()
        all_down_keys = self.return_down_keys()

        if '키워드' in args:
            print('중심 키워드입니다.:',all_keys)
            print('모든 단어입니다.:', all_words)
        if '동의어' in args:
            print('중심 키워드와 연결된 동의어입니다.:', all_keys_with_synonym)
        if '반의어' in args:
            print('중심 키워드에 연결된 반의어입니다.:', all_keys_with_antonym)
        if '상위어' in args:
            print('상위 키워드에 연결된 중심 키워드입니다.:', all_up_keys)
        if '하위어' in args:
            print('중심 키워드에 연결된 하위 키워드입니다.:', all_down_keys)

class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
    def add_neighbor(self, vertex):
        if vertex not in self.neighbors:
            self.neighbors.append(vertex)

    def del_neighbor(self, vertex):
        if vertex in self.neighbors:
            self.neighbors.remove(vertex)
    def change_name(self,new_name):
        self.name = new_name

class Graph_practice:
    def __init__(self):
        self.vertices = {}
        self.map = {}
        for key in sorted(self.vertices.keys()):

            self.map[key] = self.vertices[key].neighbors

            print('tt',self.vertices[key].neighbors)

    def construct_map(self):
        for key in sorted(self.vertices.keys()):
            self.map[key] = self.vertices[key].neighbors

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    def del_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name in self.vertices:
            self.vertices.pop(vertex.name)
            return True
        else:
            return False

    def revise_vertex(self, vertex, new_name):
        if isinstance(vertex, Vertex) and vertex.name in self.vertices:
            self.vertices[new_name] = self.vertices.pop(vertex.name)
            vertex.change_name(new_name)

    def add_edge(self, vertex1_name, vertex2_name):
        if vertex1_name in self.vertices and vertex2_name in self.vertices:
            for key, value in self.vertices.items():
                if key == vertex1_name:
                    value.add_neighbor(vertex2_name)
                if key == vertex2_name:
                    value.add_neighbor(vertex1_name)
            return True
        else:
            return False

    def del_edge(self, vertex1_name, vertex2_name):
        if vertex1_name in self.vertices and vertex2_name in self.vertices:
            for key, value in self.vertices.items():
                if key == vertex1_name:
                    value.del_neighbor(vertex2_name)
                if key == vertex2_name:
                    value.del_neighbor(vertex1_name)
            return True
        else:
            return False

    def revise_edge(self, vertex_standard_name, vertex_old_name, vertex_new_name):
        if vertex_standard_name in self.vertices and vertex_old_name in self.vertices and vertex_new_name in self.vertices:
            self.del_edge(vertex_standard_name, vertex_old_name)
            self.add_edge(vertex_standard_name, vertex_new_name)
            return True
        else:
            return False

    def return_map_structure(self):
        if self.map:
            pass
        else:
            self.construct_map()
        return self.map


    def return_all_keys(self):
        if self.map:
            pass
        else:
            self.construct_map()
        return list(self.map.keys())

    def return_result(self,input):
        return self.vertices[input].neighbors
        #
        # for key in sorted(self.vertices.keys()):
        #     print(key + str(self.vertices[key].neighbors))

    # def return_all_words(self):



if __name__ == '__main__':
    keyExcel_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹데이터베이스.xlsx'
    keyPickle_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_피클/keyword_structure5.pkl'
    cnd = ep.ChecknDo(keyExcel_name)
    dic_catekey =cnd.return_keydic(keyPickle_name)
    print('키워드와 관련된 딕셔너리입니다:\n',dic_catekey)
    upExcel_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_상위유의어.xlsx'
    upPickle_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_상위유의어_피클.pkl'
    cnd_up = ep.ChecknDo(upExcel_name)
    dic_up = cnd_up.return_extradic(upPickle_name)
    print('상위어와 관련된 키워드입니다.:\n',dic_up)
    downExcel_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_하위유의어.xlsx'
    downPickle_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_하위유의어_피클.pkl'
    cnd_down = ep.ChecknDo(downExcel_name)
    dic_down = cnd_down.return_extradic(downPickle_name)
    print('하위어와 관련된 키워드입니다:\n',dic_down)
    Hash_name = 'hash'
    Category_graph_pkl_name = 'category'
    Up_graph_pkl_name = 'up'
    down_graph_pkl_name = 'down'
    antonym_graph_pkl_name = 'antonym'
    hash_ins = Hash_dic(Hash_name, Category_graph_pkl_name, Up_graph_pkl_name,down_graph_pkl_name, antonym_graph_pkl_name)
    hash_ins.add_or_change(dic_catekey[0],dic_up[0],dic_down[0])
    hash_ins.make_graph(dic_catekey[0], {})
    print('해시맵입니다:\n',hash_ins.hashmap)
    print('카테고리그래프입니다:\n',hash_ins.category_graph)
    print('상위어그래프입니다:\n',hash_ins.up_graph)
    print('하위어그래프입니다:\n',hash_ins.down_graph)
    print('반의어그래프입니다:\n',hash_ins.antonym_graph)
    print('get입니다:\n',hash_ins.get('거친'))










