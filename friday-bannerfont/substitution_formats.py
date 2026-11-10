from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString



def add_gsub(font, feature_text):
    addOpenTypeFeaturesFromString(font, feature_text, ["GSUB"])

def build_fea_file():
    color_list = ["zero","one","two","three","four","five","six","seven","eight","nine","A","B","C","D","E","F"]
    # can't be bothered to find out if color_list works as the name of a "named glyph class", hence making this list
    color_group_list = ["WHITE","LIGHT_GRAY","GRAY","BLACK","YELLOW","ORANGE","RED","BROWN","LIME","GREEN","LIGHT_BLUE","CYAN","BLUE","PINK","MAGENTA","PURPLE"]
    pattern_list = ["period"] + [chr(x) for x in range(ord('G'), ord('Z') + 1)] + [chr(x) for x in range(ord('a'), ord('v') + 1)]

    # ligature: sub 0-F pattern by (0-F pattern)
    lines = [
        f"    sub {color} {pattern} by uniE{color_index:X}{pattern_index:02d};"
        for color_index, color in enumerate(color_list)
        for pattern_index, pattern in enumerate(pattern_list)
    ]
    liga_string = "\n    ".join(lines) + "\n"

    lines = [
        f"    @{color_group} = [{' '.join(f'uniE{color_group_index:X}{pattern_index:02d}' for pattern_index in range(43))}];"
    for color_group_index, color_group in enumerate(color_group_list)
]
    color_string = "\n    ".join(lines) + "\n"

    # calt: sub 0-F pattern by (0-F pattern) (doesn't include period)
    lines = [
        f"    sub @{color_group} {pattern}' by uniE{color_group_index:X}{pattern_index+1:02d};"
        for color_group_index, color_group in enumerate(color_group_list)
        for pattern_index, pattern in enumerate(pattern_list[1:])
    ]
    calt_string = "\n    ".join(lines) + "\n"


    feature_text = f"""
    feature liga {{
        sub h t t p s colon slash slash b a n n e r hyphen w r i t e r period w e b period a p p slash i m a g e slash R by space;
        sub h t t p s colon slash slash b a n n e r hyphen w r i t e r period w e b period a p p slash i m a g e slash L by space;
        sub period p n g by space;
        sub R period by uniE000;
        sub L period by uniE000;
    {liga_string}
    }} liga;

    {color_string}

    feature calt {{
    {calt_string}
    }} calt;
    """
    
    return feature_text

def add_default_gsub(font_path):
    font = TTFont(font_path)
    feature_text = build_fea_file()
    add_gsub(font, feature_text)
    return font

c = add_default_gsub("Combined.ttf")

c.save("BannerFont-Patched.ttf")
