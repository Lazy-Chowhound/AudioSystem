from Util.AudioUtil import name_to_pattern, suffix_to_pattern_type


def get_pattern_info_from_name(pattern_tag):
    """
    从名称后缀解析出扰动大类和具体类型
    :param pattern_tag: animal_wild_animals
    :return: animal,wild animals
    """
    if "gaussian_white_noise" in pattern_tag:
        return name_to_pattern["gaussian_white_noise"], suffix_to_pattern_type("gaussian_white_noise")
    else:
        for key, value in name_to_pattern.items():
            if key in pattern_tag:
                return name_to_pattern[key], suffix_to_pattern_type(pattern_tag.replace(key + "_", ""))