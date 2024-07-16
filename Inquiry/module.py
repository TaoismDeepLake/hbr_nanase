from opencc import OpenCC

class Inquiry:
    from ._define_values import _define_values
    from ._methods import info, tag, tag_enemy, profile, skill, skill_hit, skill_accessory, skill_name
    from ._methods import passive, enemy, enemy_scoreattack
    from ._search  import _match_simple, _match_label, _match_label_name
    from ._util import _read_db, _in_list, _get_value, _get_data, _search_key, _df2str, _wrap_msg
    from ._output import _format_output, _simple_output, _combine_output_by_kw
    from ._output import _construct_output, _get_output_info, _remove_output_info
    
    def __init__(self, db_path = 'HBR_bak.db', format_output = True, enable_all = False, show_match_score = True):
        self.db_path = db_path
        self.format_output = format_output
        self.enable_all = enable_all
        self.show_match_score = show_match_score

        self.t2s = OpenCC('t2s')  # zhtw to zhcn
        self.s2t = OpenCC('s2t')  # zhcn to zhtw

        self._define_values()
        self._read_db()