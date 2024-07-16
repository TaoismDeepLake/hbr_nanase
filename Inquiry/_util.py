import sqlite3
import jaconv
import pandas as pd

def _read_db(self):
    print('Reading database...'+self.db_path)
    self.db = sqlite3.connect(self.db_path)
    # full tables
    self.profile_list = pd.read_sql_query('SELECT * FROM MiddleCharaProfile', self.db)
    self.skill_list = pd.read_sql_query('SELECT * FROM MiddleSkillList', self.db)
    self.passive_list = pd.read_sql_query('SELECT * FROM MiddlePassiveSkillList', self.db)
    self.enemy_list = pd.read_sql_query('SELECT * FROM MiddleEnemyList', self.db)
    self.skill_name_list = pd.read_sql_query('SELECT * FROM MiddleSkillNamezhTW', self.db)
    self.skill_hit_list = pd.read_sql_query('SELECT * FROM MiddleSkillHit', self.db)
    # full tables (raw data)
    
    # partial tables
    self.MasterCharacter = pd.read_sql_query('SELECT * FROM MasterCharacter', self.db)
    self.name_ruby_list = self.MasterCharacter[['Label', 'LastNameRuby','FirstNameRuby']]

def _in_list(self, name, df, key, i, lang = None):
    value = self._get_value(df, key, i, convert=False)
    # match name with entry for various languages
    try:
        if name in value:
            return True
    except:
        pass
    try:
        # lower case matches
        if (name.lower() in value.lower()) or (
            name.lower() in value.replace(' ','').lower()) or (
            name.lower() in value.replace('_','').lower()
            ):
            return True
    except:
        pass
    if ('zhtw' in key.lower()) or (lang == 'zhtw'):
        try:
            # chinese matches
            if (name in self.t2s.convert(value)) or (
                name in self.t2s.convert(value.replace(' ',''))) or (
                name in self.t2s.convert(value.replace('_',''))
                ):
                return True
        except:
            pass
    if ('jp' in key.lower()) or (lang == 'jp'):
        try:
            # kana matches
            if (name.lower() in jaconv.kana2alphabet(value.lower())) or (
                name.lower() in jaconv.kana2alphabet(value.replace(' ','').lower())) or (
                name.lower() in jaconv.kana2alphabet(value.replace('_','').lower())
                ):
                return True
        except:
            pass
        try:
            # kata matches
            if (name.lower() in jaconv.kata2alphabet(value.lower())) or (
                name.lower() in jaconv.kata2alphabet(value.replace(' ','').lower())) or (
                name.lower() in jaconv.kata2alphabet(value.replace('_','').lower())
                ):
                return True
        except:
            pass
    # no match
    return False

def _get_value(self, df, key, i=None, convert = True, lang = None):
    try:
        value = df[key].iloc[i]
    except:
        value = df[key]
    try:
        if (('zhtw' in key.lower()) or (lang == 'zhtw')) and convert:
            value = self.t2s.convert(value)
    except:
        pass
    # do not convert for jp unless specified
    try:
        if lang == 'jp' and convert:
            value = jaconv.kana2alphabet(value) # hiragana is fine
    except:
        pass
    return value

def _get_data(self, df, i, default_keys, key=None):
    # get data through dataframe by keys
    if key == 'All' and self.enable_all:
        try:
            data = df.iloc[i]
        except:
            data = df
    elif key is None:
        # default keys
        try:
            data = df[default_keys].iloc[i]
        except:
            data = df[default_keys]
    else:
        data = self._search_key(df, i, key)
    return data

def _search_key(self, df, i, key):
    # return certain skill data by custom keys
    try:
        keys = []
        for element in list(df.keys()):
            if key in element or key.lower() in element.lower():
                keys.append(element)
        data = df[keys].iloc[i]
    except:
        data = None
    return data

def _df2str(self, df):
    # use .to_string directly will give wide results (not good)
    output = ''
    for i, key in enumerate(df.keys()):
        try:
            output += f'{key}: {df[key].to_string(index=False).replace(self.nl,"")}{self.nl}'
        except:
            output += f'{key}: {str(df[key]).replace(self.nl,"")}{self.nl}'
    return output

def _wrap_msg(self, kws):
    len_kws = len(kws)
    msg = '解析失败，请检查输入格式。'
    for keyword in self.kw_dict.keys():
        n_kwargs = self.kw_dict[keyword].__code__.co_argcount -1
        n_args = n_kwargs-len(self.kw_dict[keyword].__defaults__ or '') 
        try:
            if kws[0] == keyword:
                print(len_kws, n_kwargs, n_args)
                if (n_args == 4) or (len_kws-1 >= 4 and n_kwargs >= 4): # just in case...
                    result = self.kw_dict[keyword](kws[1], kws[2], kws[3], kws[4])
                if (n_args == 3) or (len_kws-1 >= 3 and n_kwargs >= 3):
                    result = self.kw_dict[keyword](kws[1], kws[2], kws[3])
                elif (n_args == 2) or (len_kws-1 >= 2 and n_kwargs >= 2):
                    result = self.kw_dict[keyword](kws[1], kws[2])
                elif n_args == 1:
                    result = self.kw_dict[keyword](kws[1])
            if result:
                msg = str(result)
                continue
            else:
                msg = '未查到相关数据'
        except NameError:
            pass
    # warnings
    if kws[-1] == 'All' and not self.enable_all:
        msg = '已禁用ALL功能。'
    return msg