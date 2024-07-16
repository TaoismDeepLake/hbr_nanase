def _format_output(self, output, key, keys = None, prompt = None, compressed_kw = False,
                   custom_kw = False, key_kw = None, combine_kw = None,):
    if output is None:
        return output
    if (key is None) and self.format_output:
        # custom key and value to combine
        if custom_kw:
            output_dict = self._combine_output_by_kw(output, key_kw, combine_kw,
                                                     compressed_kw = compressed_kw)
            output = self._construct_output(output_dict, custom_kw = custom_kw)
        # special case where nested compressed info is in the output
        elif compressed_kw:
            output_msg = ''
            lines = output.split(self.nl)
            info = self.kw_info_dict_default.copy()
            for line in lines:
                line_dict = self._simple_output(line, compressed_kw = compressed_kw)
                info_dict = self._get_output_info(line_dict, get_info = True)
                if not (info_dict == self.kw_info_dict_default):
                    for key in info_dict.keys():
                        if info_dict[key] is not None:
                            info[key] = info_dict[key]
                    line_dict = self._remove_output_info(line_dict)
                if not (line_dict == {}):
                    output_msg += self._construct_output(line_dict, keys, prompt)
                    output_msg += self.nl
            if info_dict == self.kw_info_dict_default:
                output = output_msg
            else:
                output = self._get_output_info(info)+output_msg
        else:
            # other: simple outputs
            output_dict = self._simple_output(output)
            output = self._construct_output(output_dict, keys, prompt)
    return output.rstrip(self.nl)

def _simple_output(self, output, compressed_kw = False):
    # transform output to a format dict, must be simple dict-like output
    # can work for single line
    lines = output.split(self.nl)
    output_dict = {}
    for line in lines:
        try:
            if compressed_kw:
                words = line.split(self.colon)
                # fancy way to split words and keep them in place by split signs
                words = [word for line in words for word in line.split(self.split)]
                # now this should be [key, value,... key, value]
                for key, value in zip(words[0::2], words[1::2]):
                    if not (key in output_dict.keys()):
                        output_dict[key] = value
                    else:
                        if (not type(output_dict[key]) == list):
                            output_dict[key] = [output_dict[key],]
                        output_dict[key].append(value)
            else:
                [key, value] = line.split(self.colon)
                output_dict[key] = value
        except:
            continue
    return output_dict

def _combine_output_by_kw(self, output, key_kw, value_kw, compressed_kw = False):
    if compressed_kw:
        output = output.replace(self.split, self.nl)
    # transform output to a format dict
    lines = output.split(self.nl)
    output_dict = {}
    current_kw = ''
    for line in lines:
        if line == '':
            continue
        try:
            words = line.split(self.colon)
        except:
            continue
        # match all keys and combine into dict
        for key, value in zip(words[0::2], words[1::2]):
            if key in self.kw_info_dict_default.keys():
                if not (key in output_dict.keys()):
                    output_dict[key] = value
                    # discard the rest
            elif key == key_kw: # keyword option
                current_kw = value # switch key
                if not current_kw in output_dict.keys():
                    output_dict[current_kw] = [] # create key if not exist
            elif key == value_kw: # value option
                if not (current_kw in output_dict.keys()):
                    pass # value before key is discarded
                else:
                    output_dict[current_kw].append(value) # combine value
            else:
                pass # ignore other keywords
    return output_dict

def _hide_kw_output():
    pass

def _construct_output(self, output_dict, keys = None, prompt = None, custom_kw = False):
    # construct output from a dict
    output = self._get_output_info(output_dict)
    output_dict = self._remove_output_info(output_dict)
    if output_dict == {}:
        return output
    if custom_kw:
        # format output that was generated with custom keys
        # plain output by merging lines
        for key in output_dict.keys():
            output += f'{key}{self.colon}{output_dict[key]}{self.nl}'
        return output.rstrip(self.nl)
    else:
        # output with provided prompt and keys
        output += prompt[0]
        for i in range(len(prompt)-1):
            value = output_dict[keys[i]]
            if value in [None, 'None']:
                output += '缺少数据。'
                break
            elif value == '':
                output += 'N/A'
            elif (value in ['0.0', '0']) and ('Param' in keys[i]):
                # to just skip the terms, and also relative prompt
                # this is mainly for skill params
                # may need some tweaks，ugly but works
                if keys[i] == "RefParamToughness":
                    output += ")。\n"
                continue 
            else:
                output += value
            output += prompt[i+1]
    return output

def _get_output_info(self, output_dict, get_info = False):
    # format output match info
    info_dict = self.kw_info_dict_default.copy()
    info_flag = False
    for key in output_dict.keys():
        if key in self.kw_info_dict_default.keys():
            info_dict[key] = output_dict[key]
            info_flag = True
    if get_info:
        return info_dict # only return this dict
    output = '' # if it does not exist or missing labels
    if info_flag: # if any info kw exists
        # try to convert tag back to char, if any
        try:
            label_char = self.profile(info_dict['匹配标签'], key='CharacterNamezhTW').split(self.colon)[-1]
            if (label_char is not None) and (self.tag(label_char) == info_dict['匹配标签']):
                info_dict['匹配标签'] = label_char
        except:
            pass
        if info_dict['匹配标签'] is None:
            output = '真是的，你在打听谁的消息啊？'
            return output
        # construct info message
        output = f'你是想查询【{info_dict["匹配标签"]}】'
        if info_dict['匹配内容'] is not None:
            output += f'的【{info_dict["匹配内容"]}】'
        # add score
        if info_dict['匹配分数'] is not None:
            output += f'（{info_dict["匹配分数"]}）'
        output += f'吧？：{self.nl}'
    return output

def _remove_output_info(self, output_dict):
    for key in self.kw_info_dict_default.keys():
        output_dict.pop(key, None)
    return output_dict
