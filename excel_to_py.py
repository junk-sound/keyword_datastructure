import pandas as pd
import pickle
import os

class Ex2Py_key():
    def __init__(self, new_excel,Pickle_name):
        try:
            self.df_new = pd.read_excel(new_excel).fillna('-')
        except FileNotFoundError:
            print('*** 오류 : 엑셀 파일을 찾을 수 없습니다. (init) ***')
        try:
            f = open(Pickle_name, 'rb')
            self.old_dic = pickle.load(f)

            f.close()
            self.old_ex = pd.DataFrame.from_items(self.old_dic.items(), orient='index',columns=['상위어', '유의어', '하위어','반의어'])
            self.old_ex = self.old_ex.set_index(pd.MultiIndex.from_tuples(self.old_ex.index,names = ['카테고리','키워드']))
            self.old_ex = self.old_ex.reset_index()
        except FileNotFoundError:
            print('*** 오류 : 피클 파일을 찾을 수 없습니다. (init) ***')
    def comparenchange(self):
        column_lst = ['카테고리','키워드','상위어','유의어','하위어','반의어']
        self.df_join = pd.concat([self.old_ex, self.df_new])
        self.df_join = self.df_join[column_lst]
        self.df_del_same = self.df_join.drop_duplicates(['카테고리', '키워드', '상위어', '유의어', '하위어','반의어'], keep=False)
        self.df_delnadd = self.df_del_same.drop_duplicates(['카테고리','키워드'], keep= 'last')
        self.df_changed = self.df_delnadd[self.df_delnadd['키워드'].isin(self.df_new['키워드'])]
        self.df_deleted = self.df_delnadd[self.df_delnadd['키워드'].isin(self.old_ex['키워드'])]
        self.df_deleted = self.df_deleted[~self.df_deleted['키워드'].isin(self.df_changed['키워드'])]
        return self.df_changed, self.df_deleted
    def save_pickle(self,Pickle_name):
        self.new_dic = self.df_new.set_index(['카테고리','키워드']).T.to_dict('list')
        f = open(Pickle_name,'wb')
        pickle.dump(self.new_dic,f)
        f.close()


class Ex2Py_extra:
    def __init__(self, extra_excel, Pickle_name):
        self.extraexcel_filename = extra_excel.split('/')[-1]
        try:
            self.df_new = pd.read_excel(extra_excel).fillna('-')
        except FileNotFoundError:
            print('*** 오류 : 엑셀 파일을 찾을 수 없습니다. (init) ***')
        try:
            if '상위' in self.extraexcel_filename:
                index_name = '상위어'
                column = '상위유의어'
            elif '하위' in self.extraexcel_filename:
                index_name = '하위어'
                column = '하위유의어'
            elif '반의' in self.extraexcel_filename:
                index_name = '반의어'
                column = '반의유의어'

            f = open(Pickle_name, 'rb')
            self.old_dic = pickle.load(f)
            f.close()
            self.old_ex = pd.DataFrame.from_items(self.old_dic.items(), orient='index', columns=[column])
            self.old_ex.index.name = index_name
            self.old_ex = self.old_ex.reset_index()

        except FileNotFoundError:
            print('*** 오류 : 피클 파일을 찾을 수 없습니다. (init) ***')

    def comparenchange(self):

        if '상위' in self.extraexcel_filename:
            column_lst = ['상위어', '상위유의어']
            column_first = '상위어'
        elif '하위' in self.extraexcel_filename:
            column_lst = ['하위어', '하위유의어']
            column_first = '하위어'
        elif '반의' in self.extraexcel_filename:
            column_lst = ['반의어', '반의유의어']
            column_first = '반의어'
        else:
            column_lst = []
            column_first = ''

        self.df_join = pd.concat([self.old_ex, self.df_new])
        self.df_join = self.df_join[column_lst]
        self.df_del_same = self.df_join.drop_duplicates(column_lst, keep=False)
        self.df_delnadd = self.df_del_same.drop_duplicates([column_first], keep='last')
        self.df_changed = self.df_delnadd[self.df_delnadd[column_first].isin(self.df_new[column_first])]
        self.df_deleted = self.df_delnadd[self.df_delnadd[column_first].isin(self.old_ex[column_first])]
        self.df_deleted = self.df_deleted[~self.df_deleted[column_first].isin(self.df_changed[column_first])]
        return self.df_changed, self.df_deleted

class Frame2Frame():
    def __init__(self, Excel_name):
        self.Excel_name = Excel_name
        if '데이터베이스' in self.Excel_name:
            self.index = ['카테고리','키워드']
        elif '상위' in self.Excel_name:
            self.index = ['상위어']
        elif '하위' in self.Excel_name:
            self.index = ['하위어']

    def ex2dicstr(self):
        excel_file = pd.read_excel(self.Excel_name).set_index(self.index).fillna('-')
        dic_str = excel_file.T.to_dict('list')
        return dic_str

    def df2dic(self, df):
        dic_lst = {}
        if '데이터베이스' in self.Excel_name:
            dic_str = df.set_index(self.index).T.to_dict('list')
            for category_key_tuple in dic_str.keys():
                if category_key_tuple[1] == '-':
                    continue
                '''카테고리가 빈 값일 때, 처리를 아직 하지 않았습니다.'''
                # if type(category_key_tuple[0]) == float or type(category_key_tuple[0]) == np.float64:
                dic_lst[category_key_tuple] = []
                for idx , content in enumerate(dic_str[category_key_tuple]):

                    dic_lst[category_key_tuple].append(content.split(','))

            return dic_lst
        else:
            dic_str = df.set_index(self.index).T.to_dict('list')
            for key in dic_str.keys():
                if key == '-':
                    continue
                '''카테고리가 빈 값일 때, 처리를 아직 하지 않았습니다.'''
                # if type(category_key_tuple[0]) == float or type(category_key_tuple[0]) == np.float64:
                dic_lst[key] = []
                for idx , content in enumerate(dic_str[key]):
                    dic_lst[key].extend(content.split(','))
            return dic_lst

    def dic2dic(self, dic_str):
        dic_lst = {}

        for keyword in dic_str.keys():
            dic_lst[keyword] = []
            for content in dic_str[keyword]:

                if content == '-':
                    dic_lst[keyword].append([content])
                else:
                    dic_lst[keyword].append(content.split(','))
        return dic_lst

class ChecknDo():
    def __init__(self, Excel_name):
        if os.path.exists(Excel_name):
            self.excel_name = Excel_name
        else:
            print('*** 엑셀 파일을 찾을 수 없어, 데이터베이스를 초기화합니다.***')

    def return_keydic(self, Pickle_name):
        if os.path.exists(Pickle_name):
            ex2py_key = Ex2Py_key(self.excel_name, Pickle_name)
            df_changed = ex2py_key.comparenchange()[0]
            df_deleted = ex2py_key.comparenchange()[1]
            dic_changed_lst = Frame2Frame(self.excel_name).df2dic(df_changed)
            dic_del_lst = Frame2Frame(self.excel_name).df2dic(df_deleted)
            # ex2py_key.save_pickle(Pickle_name)
            return dic_changed_lst, dic_del_lst

        else:
            dic_str = Frame2Frame(self.excel_name).ex2dicstr()
            dic_lst = Frame2Frame(self.excel_name).dic2dic(dic_str)
            # f = open(Pickle_name, 'wb')
            # pickle.dump(dic_str, f)
            # f.close()
            return dic_lst, {}

    def return_extradic(self, Pickle_name):
        if os.path.exists(Pickle_name):
            ex2py_extra = Ex2Py_extra(self.excel_name, Pickle_name)
            df_changed = ex2py_extra.comparenchange()[0]
            df_deleted = ex2py_extra.comparenchange()[1]
            dic_changed_lst = Frame2Frame(self.excel_name).df2dic(df_changed)
            dic_del_lst = Frame2Frame(self.excel_name).df2dic(df_deleted)
            # save_pickle
            return dic_changed_lst, dic_del_lst
        else:
            dic_str = Frame2Frame(self.excel_name).ex2dicstr()
            dic_lst = Frame2Frame(self.excel_name).dic2dic(dic_str)
            # f = open(Pickle_name, 'wb')
            # pickle.dump(dic_str, f)
            # f.close()
            return dic_lst, {}

if __name__ == '__main__' :
    keyExcel_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹데이터베이스.xlsx'
    keyPickle_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_피클/keyword_structure5.pkl'
    cnd = ChecknDo(keyExcel_name)
    print(cnd.return_keydic(keyPickle_name))

    upExcel_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_상위유의어.xlsx'
    upPickle_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_상위유의어_피클.pkl'
    cnd_up = ChecknDo(upExcel_name)
    print(cnd_up.return_extradic(upPickle_name))

    downExcel_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_하위유의어.xlsx'
    downPickle_name = '/Users/junksound/PycharmProjects/datastructure_make/키워드사전_엑셀/마인드그룹_하위유의어_피클.pkl'
    cnd = ChecknDo(downExcel_name)
    print(cnd.return_extradic(downPickle_name))








