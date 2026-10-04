import io, json, urllib.request
from PIL import Image

M = {
    'essence': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_Drop_Draconic_Soul_All_A_u_001a",
    'scale': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_Draconic_Skin_A_r_001",
    'scale2': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_Draconic_Skin_A_r_002",
    'scale3': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_Draconic_Skin_A_r_003",
    'horn': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_Draconic_Horn_A_r_001",
    'mind': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Material_Craft_Draconic_L_lv1_04",
    'will': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Material_Craft_Draconic_L_lv2_04",
    'ego': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Material_Craft_Draconic_L_lv3_04",
    'refstone': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_SmeltStone_Equip_A_e_002",
    'odyle': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Gather_Od_A_u_001",
    'ruby': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Gather_Gemstone_A_u_003",
    'ore': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Gather_Ore_A_u_001",
    'artnl': "/assets/Game/UI/Resource/Texture/Item/Accessory/Icon_ACC_NL_0012",
    'hardener': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_Shop_Draconic_Skin_Additive_A_c_001",
    'hammer': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craftl_Shop_Draconic_Hammer_A_c_001",
    'lessms': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Usable_MagicStone_a_001",
    'powder': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Enchant_Supplement_lv4_01",
    'ink': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Craft_Shop_Ink_A_c_002",
    'intms': "/assets/Game/UI/Resource/Texture/Item/ETC/Icon_Item_Usable_Enchant_MagicStone_A_c_002",
    'nl_true': "/assets/Game/UI/Resource/Texture/Item/Accessory/Icon_ACC_NL_0036",
    'nl_white': "/assets/Game/UI/Resource/Texture/Item/Accessory/Icon_ACC_NL_0035",
    'nl_wise': "/assets/Game/UI/Resource/Texture/Item/Accessory/Icon_ACC_NL_0047",
}
ok = {}
for k, path in M.items():
    url = 'https://cdn.questlog.gg/aion-2' + path + '.webp'
    req = urllib.request.Request(url, headers={'Referer': 'https://questlog.gg/', 'User-Agent': 'Mozilla/5.0'})
    try:
        im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=20).read())).convert('RGBA')
        im.resize((96, 96), Image.LANCZOS).save(f'out/cr_{k}.png'); ok[k] = im.size
    except Exception as e:
        ok[k] = 'ERR ' + str(e)[:60]
print(json.dumps(ok))
