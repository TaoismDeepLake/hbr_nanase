from fuzzywuzzy.fuzz import token_sort_ratio as fw_score_strict
from fuzzywuzzy.fuzz import partial_token_sort_ratio as fw_score
from fuzzywuzzy.process import extractOne as fw_match

def _match_simple(self, name, df, column, in_list_keys = [], lang = None, get_score = False, strict = True):
    """simple match mode, input name, output only one label"""
    max_score = 0
    label_match = None
    for i, label in enumerate(df[column]):
        for in_list_key in in_list_keys:
            # direct match is disabled
            # fuzzy match, use strict scoring for name (can work for list)
            if strict:
                score = fw_score_strict(name, self._get_value(df, in_list_key, i, lang = lang))
            else:
                score = fw_score(name, self._get_value(df, in_list_key, i, lang = lang))
            if score > max_score:
                max_score = score
                label_match = label
                if score >= self.match_definite:
                    break
    if get_score:
        return label_match, max_score
    else:
        return label_match

def _match_label(self, label, df, column, default_keys, key, concat = False, label_filter = True):
    """input label or name, output match
    as label is built in, match label for score should be careful"""
    output = f'匹配标签{self.colon}{label}{self.nl}'
    if label_filter:
        df = df.loc[df[column].str.contains(label)]
    #data = self._get_data(df_match, 0, default_keys, key)
    for i, row_name in enumerate(df[column]):
        if fw_score(label, row_name) >= self.match_hard_thresh:
            data = self._get_data(df, i, default_keys, key)
        else:
            continue
        if concat:
            output += self._df2str(data).replace(self.nl,self.split)+self.nl
        else:
            output += self._df2str(data)
            break
    return output.rstrip(self.nl)

def _match_label_name(self, label, name, df, column, default_keys, key,
                        in_list_keys = [], score_key = None, concat = False, get_score = False):
    """input label and description, output match
    column: main column description that matches the label
    in_list_keys: keys to search for direct match
    score_key: key to search for score match
    """
    if label is None:
        return None
    name = str(name)
    output = f'匹配标签{self.colon}{label}{self.nl}'
    max_score = 0
    df_match = df.loc[df[column].str.contains(label)]
    flag_match_concat = False # if nothing outputs for concat, still pick one base on score
    for i, row_name in enumerate(df_match[column]):
        # direct match
        if name in row_name:
            max_score = self.match_definite
            data = self._get_data(df_match, i, default_keys, key)
            if concat:
                output += self._df2str(data).replace(self.nl,self.split)+self.nl # match and continue
                flag_match_concat = True
                continue
            else:
                break # match and stop
        for in_list_key in in_list_keys:
            if self._in_list(name, df_match, in_list_key, i):
                max_score = self.match_definite
                data = self._get_data(df_match, i, default_keys, key)
                if concat:
                    output += self._df2str(data).replace(self.nl,self.split)+self.nl
                    flag_match_concat = True
                break # limit to only 1 match for in list keys
        if max_score == self.match_definite and (not concat):
            break # match and stop
        # fuzzy match, which does not have effect on concat
        if score_key:
            score = fw_score(name, self._get_value(df_match,score_key,i))
        else:
            score = 0 # do not match if score key is none
        if score > max_score:
            max_score = score
            data = self._get_data(df_match, i, default_keys, key)
            if score >= self.match_definite and (not concat):
                break
    if self.show_match_score:
        output += f'匹配分数{self.colon}{max_score}%{self.nl}'
    if max_score >= self.match_thresh and (not concat):
        output += self._df2str(data) # add data, not for concat since it is already there
    elif max_score >= self.match_thresh and concat and (not flag_match_concat):
        # add data for concat by match but not output yet
        output += self._df2str(data).replace(self.nl,self.split)+self.nl
    if get_score:
        return output.rstrip(self.nl), max_score
    else:
        return output.rstrip(self.nl)