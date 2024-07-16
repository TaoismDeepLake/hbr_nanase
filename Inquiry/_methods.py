def info(self):
    """帮助：显示帮助。通用说明：
        若需两个或以上输入，使用空格分隔关键词
        除标签查询外，可于末尾增加自定描述以匹配词条(All词条暂时禁用)
    """
    return None

def tag(self, names, *, get_score = False):
    """角色标签：输入姓名或罗马音，查询角色标签"""
    if not (type(names) == list):
        try:
            names = str(names)
            names = [names,]
        except:
            return None
    # match names
    in_list_keys = ['CharacterNameJp','Label','CharacterNamezhTW',
                    'FirstNameJp', 'LastNameJp', 'FirstNamezhTW', 'LastNamezhTW']
    label_match, score_match = self._match_simple(names, self.profile_list, 'Label',
                                        in_list_keys = in_list_keys, get_score = True)
    # match rubies, basically romaji
    in_list_keys = ['LastNameRuby','FirstNameRuby']
    label_ruby, score_ruby = self._match_simple(names, self.name_ruby_list, 'Label',
                                        in_list_keys = in_list_keys, lang='jp', get_score = True)
    # compare score
    max_score = max(score_ruby, score_match)
    if max_score < self.match_thresh:
        label = None
    else:
        if score_ruby >= score_match:
            label = label_ruby
        else:
            label = label_match
    if get_score:
        return label, max_score
    else:
        return label

def tag_enemy(self, names, get_score = False):
    """敌人标签：输入敌人名，查询所有敌人标签"""
    if not (type(names) == list):
        try:
            names = str(names)
            names = [names,]
        except:
            return None
    in_list_keys = ['Label','NameJp','NamezhTW']
    label, max_score = self._match_simple(names, self.enemy_list, 'Label',
                                        in_list_keys = in_list_keys, get_score = True)
    # no threshold for enemy search
    # if max_score < self.match_thresh:
    #     label = None
    if get_score:
        return label, max_score
    else:
        return label

def profile(self, label, key=None):
    """档案：输入角色，查询角色档案"""
    label = self.tag(label)
    if label is None:
        return None
    output = self._match_label(label, self.profile_list, 'Label', self.profile_keys, key)
    output = self._format_output(output, key, self.profile_keys, self.profile_prompt)
    return output

def skill(self, label, name, key=None):
    """技能：输入角色 空格 技能名，查询数据（只匹配第一个结果）"""
    label = self.tag(label)
    in_list_keys = ['LabelSkill','InfozhTW','SkillNamezhTW','SkillType','BuffCategory','SkillNameJp']
    output = self._match_label_name(label, name, self.skill_list, 'LabelName',
                                    self.skill_keys, key,
                                    in_list_keys=in_list_keys, score_key='InfozhTW')
    output = self._format_output(output, key, self.skill_keys, self.skill_prompt)
    return output

def skill_hit(self, label, name, key=None):
    """伤害分布：输入角色 空格 技能名，查询技能hit分布（只匹配第一个结果）"""
    label = self.tag(label)
    label_char = self.profile(label, key='CharacterNamezhTW').split(self.colon)[-1]
    skill_name = self.skill(label, name, key='SkillNamezhTW').split(self.colon)[-1]
    output = f'匹配内容{self.colon}{skill_name}{self.nl}'
    output += self._match_label_name(label_char, skill_name, self.skill_hit_list, 'CharacterNamezhTW',
                                    self.skill_hit_keys, key, 
                                    in_list_keys=['SkillNamezhTW', ], concat = True)
    output = self._format_output(output, key, compressed_kw = True,
                   custom_kw = True, key_kw = 'SkillNamezhTW', combine_kw = 'PowerRatio')
    return output

def skill_accessory(self, name, key=None):
    """宝玉：输入宝珠名，查询数据"""
    name = str(name)
    in_list_keys = ['InfozhTW','SkillNamezhTW','SkillType','BuffCategory','SkillNameJp']
    output = self._match_label_name('Accessory', name, self.skill_list, 'LabelName',
                                self.skill_accessory_keys, key,
                                in_list_keys=in_list_keys, score_key='InfozhTW', concat = False)
    output = self._format_output(output, key, self.skill_accessory_keys, self.skill_accessory_prompt)
    return output

def skill_name(self, label, key=None):
    """技能列表：输入角色或敌人（匹配的第一个结果），查询相关技能列表"""
    label_char, score = self.tag(label, get_score = True)
    label_enemy = None
    if score < self.match_definite:
        try:
            label_enemy = self.tag_enemy(label)[0]
        except:
            pass
    if label_enemy is not None:
        output = self._match_label(label_enemy, self.skill_name_list, 'Label',
                                   self.skill_name_keys, key, concat = True, label_filter = False)
    elif score >= self.match_thresh:
        output = self._match_label(label_char, self.skill_name_list, 'Label',
                                   self.skill_name_keys, key, concat = True)
    else:
        output = None
    output = self._format_output(output, key, self.skill_name_keys, self.skill_name_prompt,
                                compressed_kw = True)
    return output

def passive(self, label, name='', key=None):
    """被动：输入角色，和卡片或被动名，查询被动列表"""
    label = self.tag(label)
    # modularized output
    in_list_keys = ['CardNamezhTW','CardNameJp','SkillNameJp', 'SkillNamezhTW']
    output = self._match_label_name(label, name, self.passive_list, 'LabelName',
                                    self.passive_keys, key,
                                    in_list_keys=in_list_keys, score_key='CardNamezhTW',
                                    concat = True)
    output = self._format_output(output, key, self.passive_keys, self.passive_prompt,compressed_kw = True)
    return output

def enemy(self, label, label_2=None, label_3 = None, key=None):
    """敌人：输入敌人名字(至多三个关键词)，查询数据"""
    try:
        if label_3 is not None:
            label, score = self.tag_enemy([label, label_2, label_3], get_score = True)
        if label_2 is not None:
            label, score = self.tag_enemy([label, label_2], get_score = True)
        else:
            label, score = self.tag_enemy(label, get_score = True)
    except:
        return None
    if self.show_match_score:
        output = f'匹配分数{self.colon}{score}%'+self.nl
    output += self._match_label(label, self.enemy_list, 'Label', self.enemy_keys, key, label_filter = True)
    output = self._format_output(output, key, self.enemy_keys, self.enemy_prompt)
    return output

def enemy_scoreattack(self, label, level, key=None):
    """打分：输入打分敌人信息和等级，查询数据"""
    if not ('Lv' in level):
        level = 'Lv'+level
    try:
        label, score = self.tag_enemy([label, level], get_score = True)
    except:
        return None    
    if self.show_match_score:
        output = f'匹配分数{self.colon}{score}%'+self.nl
    output += self._match_label(label, self.enemy_list, 'Label', self.enemy_keys, key, label_filter = True)
    output = self._format_output(output, key, self.enemy_keys, self.enemy_prompt)
    return output