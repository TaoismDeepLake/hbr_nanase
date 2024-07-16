def _define_values(self):
    # define default output keys and prompts
    # prompts must follow gaps with list order of keys
    self.skill_keys = ['SkillNamezhTW', 'LabelSkillPart', 'InfozhTW',
                        'ElementList', 'TargetType', 'Sp',
                        'Power', 'MaxPower', 'RefParamDiffForMax',
                        'RefParamPower','RefParamDexterity','RefParamWisdom',
                        'RefParamLuck','RefParamSpirit','RefParamToughness',
                        'HitCount', 'DamageRateRate']
    self.skill_prompt = ['', '(', ')：', '。\n元素：', '，对象：', '，SP：', 
                        '。\n技能强度：', '~', '（差值：', 
                        '，属性倍率：','x力 ','x器 ','x知 ','x运 ','x精 ','x体）。\n',
                        '-hit(若有效)，破坏倍率：', '。']
    
    self.skill_hit_keys = ['SkillNamezhTW', 'PowerRatio',]
    
    self.skill_accessory_keys = ['SkillNamezhTW', 'LabelSkillPart', 'InfozhTW',
                        'TargetType', 'Sp','Power', 'MaxPower', 'RefParamDiffForMax',
                        'RefParamPower','RefParamDexterity','RefParamWisdom',
                        'RefParamLuck','RefParamSpirit','RefParamToughness']
    self.skill_accessory_prompt = ['', '(', ')：', '。\n对象：', '，SP：', 
                        '。\n技能强度：', '~', '（差值：', 
                        '，属性倍率：','x力 ','x器 ','x知 ','x运 ','x精 ','x体）。']
    
    self.skill_name_keys = ['SkillName', 'Label', 'SkillInfo']
    self.skill_name_prompt = ['',' (','):','。']
    
    self.enemy_keys = ['NamezhTW', 'Dp', 'Hp', 'RefParamBorder', 'Attack',
                         'MaxDamageRate', 'DamageRateValue']
    self.enemy_prompt = ['','：DP:','， HP:','。\n属性值','，攻击倍率','，破坏率上限','%（','%）。']
    
    self.passive_keys = ['SkillNamezhTW', 'CardNamezhTW', 'InfozhTW']
    self.passive_prompt = ['',' (','):','。']
    
    self.profile_keys = ['CharacterNameJp', 'CharacterNamezhTW',
                        'CharacterVoiceJp', 'CharacterVoicezhTW', 
                        'TeamJp', 'Height', 'BirthdayzhTW', 'BirthPlacezhTW', 
                        'SeraphimCodeJp', 'SeraphimCodezhTW', ]
    self.profile_prompt = ['', '(',')，CV:','(',')。',
                        '，身高','，出生于','(','）。\n炽天使口令为：','，','。']
    

    self.nl = '\n'  # newline
    self.colon = ': ' # colon used to get attribution
    self.split = '; ' # split for compressed keywords
    self.match_thresh = 50 # fuzzy wuzzy score threshold
    self.match_hard_thresh = 80
    self.match_definite = 100

    # keyword : function
    self.kw_dict = {
        #"角色标签": self.tag,
        #"敌人标签": self.tag_enemy,
        "技能": self.skill,
        "伤害分布": self.skill_hit,
        "宝玉":self.skill_accessory,
        "被动": self.passive,
        "敌人": self.enemy,
        "打分": self.enemy_scoreattack,
        "技能列表": self.skill_name,
        "档案": self.profile,
    }

    # format output settings
    self.kw_info_dict_default = {
        '匹配标签': None,
        '匹配内容': None,
        '匹配分数': None,
        }
    # info prompt is kept in _output._get_output_info