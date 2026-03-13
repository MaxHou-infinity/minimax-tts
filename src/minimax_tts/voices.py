"""MiniMax system voice definitions."""

VOICES = {
    # ── 中文（普通话）标准音色 ──
    "male-qn-qingse": {"name": "青涩青年", "lang": "zh", "gender": "male", "desc": "青涩清新的年轻男声"},
    "male-qn-qingse-jingpin": {"name": "青涩青年·精品", "lang": "zh", "gender": "male", "desc": "青涩清新的年轻男声（精品版）"},
    "male-qn-jingying": {"name": "精英青年", "lang": "zh", "gender": "male", "desc": "成熟干练的精英男声"},
    "male-qn-jingying-jingpin": {"name": "精英青年·精品", "lang": "zh", "gender": "male", "desc": "成熟干练的精英男声（精品版）"},
    "male-qn-badao": {"name": "霸道青年", "lang": "zh", "gender": "male", "desc": "霸气有力的男声"},
    "male-qn-badao-jingpin": {"name": "霸道青年·精品", "lang": "zh", "gender": "male", "desc": "霸气有力的男声（精品版）"},
    "male-qn-daxuesheng": {"name": "大学生", "lang": "zh", "gender": "male", "desc": "阳光活力的大学生男声"},
    "male-qn-daxuesheng-jingpin": {"name": "大学生·精品", "lang": "zh", "gender": "male", "desc": "阳光活力的大学生男声（精品版）"},
    "female-shaonv": {"name": "少女", "lang": "zh", "gender": "female", "desc": "甜美可爱的少女音"},
    "female-shaonv-jingpin": {"name": "少女·精品", "lang": "zh", "gender": "female", "desc": "甜美可爱的少女音（精品版）"},
    "female-yujie": {"name": "御姐", "lang": "zh", "gender": "female", "desc": "成熟知性的御姐音"},
    "female-yujie-jingpin": {"name": "御姐·精品", "lang": "zh", "gender": "female", "desc": "成熟知性的御姐音（精品版）"},
    "female-chengshu": {"name": "成熟女性", "lang": "zh", "gender": "female", "desc": "沉稳大气的成熟女声"},
    "female-chengshu-jingpin": {"name": "成熟女性·精品", "lang": "zh", "gender": "female", "desc": "沉稳大气的成熟女声（精品版）"},
    "female-tianmei": {"name": "甜美女声", "lang": "zh", "gender": "female", "desc": "甜蜜温柔的女声"},
    "female-tianmei-jingpin": {"name": "甜美女声·精品", "lang": "zh", "gender": "female", "desc": "甜蜜温柔的女声（精品版）"},

    # ── 中文特色音色 ──
    "clever_boy": {"name": "聪明男孩", "lang": "zh", "gender": "male", "desc": "机灵的小男孩"},
    "cute_boy": {"name": "可爱男孩", "lang": "zh", "gender": "male", "desc": "可爱的小男孩"},
    "lovely_girl": {"name": "萌萌女孩", "lang": "zh", "gender": "female", "desc": "萌系小女孩"},
    "cartoon_pig": {"name": "猪小琦", "lang": "zh", "gender": "neutral", "desc": "卡通角色音"},
    "bingjiao_didi": {"name": "病娇弟弟", "lang": "zh", "gender": "male", "desc": "病娇系弟弟"},
    "junlang_nanyou": {"name": "俊朗男友", "lang": "zh", "gender": "male", "desc": "温柔帅气的男友音"},
    "badao_shaoye": {"name": "霸道少爷", "lang": "zh", "gender": "male", "desc": "霸气十足的少爷"},
    "Arrogant_Miss": {"name": "傲娇大小姐", "lang": "zh", "gender": "female", "desc": "傲娇的大小姐"},

    # ── 中文播音/专业 ──
    "audiobook_male_1": {"name": "有声书男声", "lang": "zh", "gender": "male", "desc": "浑厚有磁性的有声书男声"},
    "audiobook_male_2": {"name": "有声书男声2", "lang": "zh", "gender": "male", "desc": "温和沉稳的有声书男声"},
    "audiobook_female_1": {"name": "有声书女声", "lang": "zh", "gender": "female", "desc": "温婉动听的有声书女声"},
    "audiobook_female_2": {"name": "有声书女声2", "lang": "zh", "gender": "female", "desc": "知性优雅的有声书女声"},

    # ── 英文 ──
    "English_Trustworthy_Man": {"name": "Trustworthy Man", "lang": "en", "gender": "male", "desc": "Reliable, confident English male"},
    "English_Graceful_Lady": {"name": "Graceful Lady", "lang": "en", "gender": "female", "desc": "Elegant, refined English female"},
    "English_Whispering_girl": {"name": "Whispering Girl", "lang": "en", "gender": "female", "desc": "Soft whispering English female"},
    "English_Aussie_Bloke": {"name": "Aussie Bloke", "lang": "en", "gender": "male", "desc": "Australian English male"},
    "Santa_Claus": {"name": "Santa Claus", "lang": "en", "gender": "male", "desc": "Jolly Santa Claus"},

    # ── 日文 ──
    "Japanese_IntellectualSenior": {"name": "知性先輩", "lang": "ja", "gender": "female", "desc": "知的なお姉さん"},
    "Japanese_GentleButler": {"name": "優しい執事", "lang": "ja", "gender": "male", "desc": "紳士的な執事"},
    "Japanese_InnocentBoy": {"name": "無邪気少年", "lang": "ja", "gender": "male", "desc": "純真な少年"},
    "Japanese_ColdQueen": {"name": "冷酷女王", "lang": "ja", "gender": "female", "desc": "クールな女王"},

    # ── 韩文 ──
    "Korean_StrictBoss": {"name": "엄격한 상사", "lang": "ko", "gender": "male", "desc": "Strict Korean male boss"},
    "Korean_SassyGirl": {"name": "당돌한 소녀", "lang": "ko", "gender": "female", "desc": "Sassy Korean girl"},

    # ── 粤语 ──
    "Cantonese_ProfessionalHost_F": {"name": "粤语女主持", "lang": "yue", "gender": "female", "desc": "专业粤语女主持人"},
    "Cantonese_ProfessionalHost_M": {"name": "粤语男主持", "lang": "yue", "gender": "male", "desc": "专业粤语男主持人"},
    "Cantonese_GentleLady": {"name": "粤语温柔女", "lang": "yue", "gender": "female", "desc": "温柔粤语女声"},
}

LANGUAGES = {
    "zh": "中文（普通话）",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
    "yue": "粤语",
}

MODELS = {
    "speech-2.8-hd": "精准音调还原，高相似度（推荐）",
    "speech-2.6-hd": "超低延迟，高自然度",
    "speech-2.8-turbo": "精准音调，更快更省",
    "speech-2.6-turbo": "速度优先，适合语音聊天",
    "speech-02-hd": "优秀节奏感，高稳定性",
    "speech-02-turbo": "强节奏感，增强多语言支持",
}
