# Init for Calli_Utils
"""
印章效果工具包
包含四种带边框的印章效果实现
"""

from .seal_border_simple import add_seal_with_border
from .seal_border_circular import add_circular_seal_with_border
from .seal_border_fancy import add_fancy_seal_with_border
from .seal_border_antique import add_antique_seal_with_border
from .seal_border_fancy_4char import add_four_character_seal, add_seal_with_text_penetration
from .seal_border_circular_4char import add_circular_seal_with_border_4char, add_circular_seal_advanced, add_circular_seal_with_rotation, add_circular_seal_visual_debug, add_circular_seal_with_traditional_layout
from .seal_manipulation import apply_seal_safely, create_realistic_seal, add_formal_seal, add_note_seal
from .paper_texture_basic import add_paper_texture_basic
from .paper_texture_xuan import add_xuan_paper_texture, add_xuan_paper_texture_enhanced
from .paper_texture_rice import add_rice_paper_texture_enhanced
from .paper_texture_parchment import add_parchment_texture_enhanced
from .ink_bleed_effect_xuan import add_ink_bleed_effect, add_ink_bleed_effect_optimized, add_ink_bleed_effect_enhanced
from .ink_bleed_effect_rice import add_subtle_ink_effect
from .ink_bleed_effect_parchment import add_ink_bleed_effect_parchment
from .paper_texture_type import create_authentic_torn_paper, create_realistic_paper_texture, apply_paper_texture, create_authentic_paper_texture, add_realistic_aging
from .poem_to_char_conversion import poem_to_flat_char_list, convert_poem_to_char_matrix, poem_to_char_matrix
from .paper_edge_natural_torn import add_organic_torn_mask, safe_apply_mask
from .seal_texture_type import add_texture_and_aging
from .text_inscription_type import add_upper_inscription, add_vertical_upper_inscription, add_vertical_lower_inscription, add_special_lower_inscription
from .char_type_lishu import get_lishu_spacing
from .seal_border_oval import add_leisure_oval_seal

__all__ = [
    'add_seal_with_border',
    'add_circular_seal_with_border',
    'add_fancy_seal_with_border',
    'add_antique_seal_with_border',
    'add_circular_seal_with_border_4char'
]

print("✅ 印章效果工具包已加载")