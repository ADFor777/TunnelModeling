#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成的隧道工程SWRL规则模块
包含149个推理规则的Python实现
"""

from typing import Dict, Any, Optional
import math

# 规则数据结构
TUNNEL_RULES = {
    "1": {
        "label": "S09-0",
        "comment": "深埋 + RockGrade I + 干燥 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "2": {
        "label": "S14-0",
        "comment": "深埋隧道 + RockGrade_I + 干燥 → 钢拱架间距 1.2m// 深埋稳定围岩，干燥条件支护要求相对宽松",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.2},
        ]
    },
    "3": {
        "label": "S09-2",
        "comment": "深埋 + RockGrade II + 干燥 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "4": {
        "label": "S14-2",
        "comment": "深埋隧道 + RockGrade_II + 干燥 → 钢拱架间距 1.0m",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "5": {
        "label": "S09-4",
        "comment": "深埋 + RockGrade III + 干燥 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "6": {
        "label": "S14-4",
        "comment": "深埋隧道 + RockGrade_III + 干燥 → 钢拱架间距 0.8m // III类围岩深埋下稳定性下降，适当加密支护",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "7": {
        "label": "S14-6",
        "comment": "深埋隧道 + RockGrade_IV + 干燥 → 钢拱架间距 0.6m// 差围岩即便干燥也需密支护防止变形",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "8": {
        "label": "S09-9",
        "comment": "深埋 + RockGrade V + 干燥 → 35.0 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 35.0},
        ]
    },
    "9": {
        "label": "S14-8",
        "comment": "深埋隧道 + RockGrade_V + 干燥 → 钢拱架间距 0.5m // 极差围岩，深埋段必须加强支护",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "10": {
        "label": "S09-1",
        "comment": "深埋 + RockGrade I + 富水 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "11": {
        "label": "S14-1",
        "comment": "深埋隧道 + RockGrade_I + 富水 → 钢拱架间距 1.0m// 深埋富水提高支护密度，防止突水及渗压破坏",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "12": {
        "label": "S09-3",
        "comment": "深埋 + RockGrade II + 富水 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "13": {
        "label": "S14-3",
        "comment": "深埋隧道 + RockGrade_II + 富水 → 钢拱架间距// 深部富水 II 级围岩支护需加密，保障开挖安全",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "14": {
        "label": "S09-5",
        "comment": "深埋 + RockGrade III + 富水 → 32.5 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "15": {
        "label": "S14-5",
        "comment": "深埋隧道 + RockGrade_III + 富水 → 钢拱架间距 0.6m // 深埋+富水+中差围岩，需增强支护强度",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "16": {
        "label": "S09-6",
        "comment": "深埋 + RockGrade IV + 富水 → 35.0 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 35.0},
        ]
    },
    "17": {
        "label": "S09-7",
        "comment": "深埋 + RockGrade IV + 富水 → 35.0 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 35.0},
        ]
    },
    "18": {
        "label": "S14-7",
        "comment": "深埋隧道 + RockGrade_IV + 富水 → 钢拱架间距 0.5m// 富水条件下 IV 类围岩稳定性差，最小间距",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "19": {
        "label": "S09-8",
        "comment": "深埋 + RockGrade V + 富水 → 37.5 cm",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 37.5},
        ]
    },
    "20": {
        "label": "S14-9",
        "comment": "深埋隧道 + RockGrade_V + 富水 → 钢拱架间距0.5m // 极端条件最小间距，参考规范不建议再减小",
        "body": [
            {"type": "class", "class_name": "DeepTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "21": {
        "label": "S06-0",
        "comment": "山岭 + RockGrade I + 干燥 → 20.0 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 20.0},
        ]
    },
    "22": {
        "label": "S11-0",
        "comment": "山岭隧道 + RockGrade_I + 干燥 → 钢拱架间距 1.4m（ 山岭隧道常规稳定段，间距可适当放宽）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.4},
        ]
    },
    "23": {
        "label": "S06-2",
        "comment": "山岭 + RockGrade II + 干燥 → 22.5 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 22.5},
        ]
    },
    "24": {
        "label": "S11-2",
        "comment": "山岭隧道 + RockGrade_II + 干燥 → 钢拱架间距 1.2m（II类围岩结构稳定性好，常用间距）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.2},
        ]
    },
    "25": {
        "label": "S06-4",
        "comment": "山岭 + RockGrade III + 干燥 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "26": {
        "label": "S11-4",
        "comment": "山岭隧道 + RockGrade_III + 干燥 → 钢拱架间距 1.0m（软弱围岩标准支护配置）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "27": {
        "label": "S06-6",
        "comment": "山岭 + RockGrade IV + 干燥 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "28": {
        "label": "S11-6",
        "comment": "山岭隧道 + RockGrade_IV + 干燥 → 钢拱架间距 0.8m（不稳定段标准支护布置）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "29": {
        "label": "S06-8",
        "comment": "山岭 + RockGrade V + 干燥 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "30": {
        "label": "S11-8",
        "comment": "山岭隧道 + RockGrade_V + 干燥 → 钢拱架间距 0.6m（极破碎区干燥，仍需密集支护 ）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "31": {
        "label": "S11-1",
        "comment": "山岭隧道 + RockGrade_I + 富水 → 钢拱架间距 1.2m（富水条件下适当加密以控制初期变形）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
        ]
    },
    "32": {
        "label": "S06-1",
        "comment": "山岭 + RockGrade I + 富水 → 22.5 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 22.5},
        ]
    },
    "33": {
        "label": "S06-3",
        "comment": "山岭 + RockGrade II + 富水 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "34": {
        "label": "S11-3",
        "comment": "山岭隧道 + RockGrade_II + 富水 → 钢拱架间距 1.0m（富水加大支护密度）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "35": {
        "label": "S06-5",
        "comment": "山岭 + RockGrade III + 富水 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "36": {
        "label": "S11-5",
        "comment": "山岭隧道 + RockGrade_III + 富水 → 钢拱架间距 0.8m（围岩软+富水，支护需加密 ）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "37": {
        "label": "S06-7",
        "comment": "山岭 + RockGrade IV + 富水 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "38": {
        "label": "S11-7",
        "comment": "山岭隧道 + RockGrade_IV + 富水 → 钢拱架间距 0.6m（水扰动显著，适当加密）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "39": {
        "label": "S06-9",
        "comment": "山岭 + RockGrade V + 富水 → 32.5 cm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "40": {
        "label": "S11-9",
        "comment": "山岭隧道 + RockGrade_V + 富水 → 钢拱架间距 0.5m（极差围岩 + 富水，按规范推荐极限支护密度）",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "41": {
        "label": "W02-0",
        "comment": "mediumSoil + Dry + MountainTunnelProject → 3.5mm// 山岭隧道多穿岩体，厚度略高",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3.5},
        ]
    },
    "42": {
        "label": "W02-2",
        "comment": "strongSoil + Dry + MountainTunnelProject → 3mm// 岩性强，防水压力小，厚度适中",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3},
        ]
    },
    "43": {
        "label": "W02-4",
        "comment": "weakSoil + Dry + MountainTunnelProject → 4.5mm // 弱土山区段落风险高，厚度适度提高",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4.5},
        ]
    },
    "44": {
        "label": "W02-1",
        "comment": "mediumSoil + WaterRich + MountainTunnelProject → 4.5mm",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4.5},
        ]
    },
    "45": {
        "label": "W02-3",
        "comment": "strongSoil + WaterRich + MountainTunnelProject → 4mm// 富水情况下仍需提升厚度",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4},
        ]
    },
    "46": {
        "label": "W02-5",
        "comment": "weakSoil + WaterRich + MountainTunnelProject → 5mm// 极端地质水文条件下应设最高标准防水层",
        "body": [
            {"type": "class", "class_name": "MountainTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 5},
        ]
    },
    "47": {
        "label": "S08-0",
        "comment": "浅埋 + RockGrade I + 干燥 → 22.5 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 22.5},
        ]
    },
    "48": {
        "label": "S13-0",
        "comment": "浅埋隧道 + RockGrade_I + 干燥 → 钢拱架间距 1.2m(浅埋、稳定围岩、干燥环境下支护强度可适度降低)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.2},
        ]
    },
    "49": {
        "label": "S08-2",
        "comment": "浅埋 + RockGrade II + 干燥 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "50": {
        "label": "S13-2",
        "comment": "浅埋隧道 + RockGrade_II + 干燥 → 钢拱架间距 1.0m (II类围岩常规支护密度即可满足)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "51": {
        "label": "S08-4",
        "comment": "浅埋 + RockGrade III + 干燥 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "52": {
        "label": "S13-4",
        "comment": "浅埋隧道 + RockGrade_III + 干燥 → 钢拱架间距 0.8m(III类围岩稳定性差，应加密支护)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "53": {
        "label": "S08-6",
        "comment": "浅埋 + RockGrade IV + 干燥 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "54": {
        "label": "S13-6",
        "comment": "浅埋隧道 + RockGrade_IV + 干燥 → 钢拱架间距 0.6m (IV类围岩浅埋段应确保施工安全)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "55": {
        "label": "S08-8",
        "comment": "浅埋 + RockGrade V + 干燥 → 32.5 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "56": {
        "label": "S13-8",
        "comment": "浅埋隧道 + RockGrade_V + 干燥 → 钢拱架间距 0.5m(极差围岩，即便干燥也需强支护)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "57": {
        "label": "S08-1",
        "comment": "浅埋 + RockGrade I + 富水 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "58": {
        "label": "S13-1",
        "comment": "浅埋隧道 + RockGrade_I + 富水 → 钢拱架间距 1.0m(富水条件支护加密，防止地表渗水导致坍塌)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "59": {
        "label": "S08-3",
        "comment": "浅埋 + RockGrade II + 富水 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "60": {
        "label": "S13-3",
        "comment": "浅埋隧道 + RockGrade_II + 富水 → 钢拱架间距 0.8m (增强防水及支护稳定性，防止浅覆土滑移)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "61": {
        "label": "S08-5",
        "comment": "浅埋 + RockGrade III + 富水 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "62": {
        "label": "S13-5",
        "comment": "浅埋隧道 + RockGrade_III + 富水 → 钢拱架间距 0.6m(浅埋富水极易涌水塌方，应加大支护强度)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "63": {
        "label": "S08-7",
        "comment": "浅埋 + RockGrade IV + 富水 → 32.5 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "64": {
        "label": "S13-7",
        "comment": "浅埋隧道 + RockGrade_IV + 富水 → 钢拱架间距 0.5m(范建议最小间距，防治浅层地表水渗漏)",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "65": {
        "label": "S08-9",
        "comment": "浅埋 + RockGrade V + 富水 → 35.0 cm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 35.0},
        ]
    },
    "66": {
        "label": "S13-9",
        "comment": "浅埋隧道 + RockGrade_V + 富水 → 钢拱架间距 0.5m// 极端条件下不宜小于 0.5m，施工受限",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "67": {
        "label": "W04-0",
        "comment": "mediumSoil + Dry + ShallowTunnelProject → 3.5mm // 浅埋段施工扰动大，适度提高防水厚度",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3.5},
        ]
    },
    "68": {
        "label": "W05-0",
        "comment": "mediumSoil + Dry + ShallowTunnelProject → 3.5mm// 浅埋段施工扰动大，适度提高防水厚度",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3.5},
        ]
    },
    "69": {
        "label": "W04-2",
        "comment": "strongSoil + Dry + ShallowTunnelProject → 3mm // 自稳能力较强，标准厚度",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3},
        ]
    },
    "70": {
        "label": "W05-2",
        "comment": "strongSoil + Dry + ShallowTunnelProject → 3mm// 自稳能力较强，标准厚度",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3},
        ]
    },
    "71": {
        "label": "W04-4",
        "comment": "weakSoil + Dry + ShallowTunnelProject → 4.5mm  // 弱土层抗渗差，浅埋更易渗透",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4.5},
        ]
    },
    "72": {
        "label": "W05-4",
        "comment": "weakSoil + Dry + ShallowTunnelProject → 4.5mm// 弱土层抗渗差，浅埋更易渗透",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4.5},
        ]
    },
    "73": {
        "label": "W04-1",
        "comment": "mediumSoil + WaterRich + ShallowTunnelProject → 4.5mm // 富水浅埋，需重点加强防水",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4.5},
        ]
    },
    "74": {
        "label": "W05-1",
        "comment": "mediumSoil + WaterRich + ShallowTunnelProject → 4.5mm // 富水浅埋，需重点加强防水",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4.5},
        ]
    },
    "75": {
        "label": "W04-3",
        "comment": "strongSoil + WaterRich + ShallowTunnelProject → 4mm // 强土抗水性好，但富水仍需提升防水层",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4},
        ]
    },
    "76": {
        "label": "W05-3",
        "comment": "strongSoil + WaterRich + ShallowTunnelProject → 4mm// 强土抗水性好，但富水仍需提升防水层",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4},
        ]
    },
    "77": {
        "label": "W05-5",
        "comment": "weakSoil + WaterRich + ShallowTunnelProject → 5.5mm",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 5.5},
        ]
    },
    "78": {
        "label": "W04-5",
        "comment": "weakSoil + WaterRich + ShallowTunnelProject → 5.5mm// 弱土+富水+浅埋为最高风险组合，最大厚度",
        "body": [
            {"type": "class", "class_name": "ShallowTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 5.5},
        ]
    },
    "79": {
        "label": "S16--0",
        "comment": "RockGrade_I + 干燥 → 厚度 6mm// 稳定围岩且干燥，钢拱架厚度需求最低",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 6},
        ]
    },
    "80": {
        "label": "S16-2",
        "comment": "TunnelProject + RockGrade_II + 干燥 → 厚度 8mm // 稳定围岩支护刚度适中，常规厚度",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 8},
        ]
    },
    "81": {
        "label": "S16-4",
        "comment": "TunnelProject + RockGrade_III + 干燥 → 厚度 10mm // 中等围岩需适当提升钢拱架厚度以保证结构安全",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 10},
        ]
    },
    "82": {
        "label": "S16-6",
        "comment": "TunnelProject + RockGrade_IV + 干燥→ 厚度 12mm",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 12},
        ]
    },
    "83": {
        "label": "S16-8",
        "comment": "TunnelProject + RockGrade_V + 干燥 → 厚度 14mm",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 14},
        ]
    },
    "84": {
        "label": "S16--1",
        "comment": "TunnelProject + RockGrade_I + 富水 → 厚度 8mm // 富水导致锈蚀风险提高，适度增加钢拱架厚度",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 8},
        ]
    },
    "85": {
        "label": "S16-3",
        "comment": "TunnelProject + RockGrade_II + 富水 → 厚度 10mm// 富水环境钢拱架需增强耐久性和刚度",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 10},
        ]
    },
    "86": {
        "label": "S16-5",
        "comment": "TunnelProject + RockGrade_III + 富水 → 厚度 12mm // 富水+III类围岩，钢拱架厚度需加强应对双重不利因素",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 12},
        ]
    },
    "87": {
        "label": "S16-7",
        "comment": "TunnelProject + RockGrade_IV + 富水 → 厚度 14mm// 富水+差围岩，拱架厚度进一步加强以提高稳定性",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 14},
        ]
    },
    "88": {
        "label": "S16-9",
        "comment": "TunnelProject + RockGrade_V + 富水 → 厚度 16mm",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchThickness", "subject": ":t", "value": 16},
        ]
    },
    "89": {
        "label": "S05-0",
        "comment": "任意隧道 + RockGrade V + 弱土 + 富水 → 厚度 45mm",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":gc", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 45.0},
        ]
    },
    "90": {
        "label": "S03-1",
        "comment": "优秀围岩（I级）：L = 0.25 × D",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": "RockGrade_I"},
            {"type": "builtin", "function_name": "multiply", "variables": [':len', ':d', '0.25']},
        ],
        "head": [
        ]
    },
    "91": {
        "label": "S03-2",
        "comment": "较好围岩（II级）：L = 0.3 × D",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": "RockGrade_II"},
            {"type": "builtin", "function_name": "multiply", "variables": [':len', ':d', '0.3']},
        ],
        "head": [
        ]
    },
    "92": {
        "label": "S03-3",
        "comment": "中等岩体（III级）：锚杆长度 约为洞身宽度的三分之一（L = 0.33 × B）",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": "RockGrade_III"},
            {"type": "builtin", "function_name": "divide", "variables": [':len', ':w', '3']},
        ],
        "head": [
        ]
    },
    "93": {
        "label": "S03-4",
        "comment": "较差岩体（IV级）：L = 0.45 × D",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": "RockGrade_IV"},
            {"type": "builtin", "function_name": "multiply", "variables": [':len', ':d', '0.45']},
        ],
        "head": [
        ]
    },
    "94": {
        "label": "S03-5",
        "comment": "软弱围岩（V级）：锚杆长度 约为洞身宽度的一半（L = 0.5 × B）",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": "RockGrade_V"},
            {"type": "builtin", "function_name": "divide", "variables": [':len', ':d', '2']},
        ],
        "head": [
        ]
    },
    "95": {
        "label": "S04-0",
        "comment": "锚杆间距与岩石等级的关系，结合岩体质量和长度推荐: 锚杆间距 =锚杆长度/2，规范建议锚杆间距应为锚杆长度的一半或更密集(IS 15026规则)",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "builtin", "function_name": "divide", "variables": [':spacing', ':len', '2']},
        ],
        "head": [
        ]
    },
    "96": {
        "label": "S04-2",
        "comment": "计算列数（圆弧长度 / 间距）",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "builtin", "function_name": "multiply", "variables": [':arcLength', ':D', '3.1416']},
            {"type": "builtin", "function_name": "divide", "variables": [':colCountRaw', ':arcLength', ':S']},
            {"type": "builtin", "function_name": "floor", "variables": [':colCount', ':colCountRaw']},
        ],
        "head": [
        ]
    },
    "97": {
        "label": "S04-1",
        "comment": "计算行数（隧道长度 / 锚杆间距）《岩土锚杆技术规程》（JGJ 120）",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "builtin", "function_name": "divide", "variables": [':rowCountRaw', ':L', ':S']},
            {"type": "builtin", "function_name": "floor", "variables": [':rowCount', ':rowCountRaw']},
        ],
        "head": [
        ]
    },
    "98": {
        "label": "S15-0",
        "comment": "钢拱架数量 = 长度 / 间距，四舍五入",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "builtin", "function_name": "divide", "variables": [':rawCount', ':len', ':spacing']},
            {"type": "builtin", "function_name": "round", "variables": [':count', ':rawCount']},
        ],
        "head": [
        ]
    },
    "99": {
        "label": "S01",
        "comment": "隧道长度大于3000m选择钻爆法",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "builtin", "function_name": "greaterThan", "variables": [':len', '3000']},
        ],
        "head": [
            {"type": "object_property", "property_name": "hasConstructionMethod", "subject": ":t", "object": "DrillAndBlast_001"},
        ]
    },
    "100": {
        "label": "S02",
        "comment": "隧道长度 ≤ 3000 → 使用盾构法（TBM_001）",
        "body": [
            {"type": "class", "class_name": "TunnelProject", "individual": ":t"},
            {"type": "builtin", "function_name": "lessThanOrEqual", "variables": [':len', '3000']},
        ],
        "head": [
            {"type": "object_property", "property_name": "hasConstructionMethod", "subject": ":t", "object": "TBM_001"},
        ]
    },
    "101": {
        "label": "S07-0",
        "comment": "水下 + RockGrade I + 干燥 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "102": {
        "label": "S12-0",
        "comment": "水下隧道 + RockGrade_I + 干燥 → 钢拱架间距 1.2m（水下但地质好且干燥，常规支护即可）",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.2},
        ]
    },
    "103": {
        "label": "S07-2",
        "comment": "水下 + RockGrade II + 干燥 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "104": {
        "label": "S12-2",
        "comment": "水下隧道 + RockGrade_II + 干燥 → 钢拱架间距 1.0m（ II类围岩下常规布置）",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "105": {
        "label": "S07-4",
        "comment": "水下 + RockGrade III + 干燥 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "106": {
        "label": "S12-4",
        "comment": "水下隧道 + RockGrade_III + 干燥 → 钢拱架间距 0.8m(III类围岩较差但干燥，常规支护密度)",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "107": {
        "label": "S07-6",
        "comment": "水下 + RockGrade IV + 干燥 → 32.5 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "108": {
        "label": "S12-6",
        "comment": "水下隧道 + RockGrade_IV + 干燥 → 钢拱架间距 0.6m( IV类围岩稳定性差，建议加密支护)",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "109": {
        "label": "S07-8",
        "comment": "水下 + RockGrade V + 干燥 → 35.0 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 35.0},
        ]
    },
    "110": {
        "label": "S12-8",
        "comment": "水下隧道 + RockGrade_V + 干燥 → 钢拱架间距 0.5m(极差围岩，需密集钢拱架支护)",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "111": {
        "label": "S07-1",
        "comment": "水下 + RockGrade I + 富水 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "112": {
        "label": "S12-1",
        "comment": "水下隧道 + RockGrade_I + 富水 → 钢拱架间距 1.0m（富水条件下增加支护稳定性）",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "113": {
        "label": "S07-3",
        "comment": "水下 + RockGrade II + 富水 → 30.0 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "114": {
        "label": "S12-3",
        "comment": "水下隧道 + RockGrade_II + 富水 → 钢拱架间距 0.8m（富水段支护加密防止掉块涌水）",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "115": {
        "label": "S07-5",
        "comment": "水下 + RockGrade III + 富水 → 32.5 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "116": {
        "label": "S12-5",
        "comment": "水下隧道 + RockGrade_III + 富水 → 钢拱架间距 0.6m",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "117": {
        "label": "S07-7",
        "comment": "水下 + RockGrade IV + 富水 → 35.0 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 35.0},
        ]
    },
    "118": {
        "label": "S12-7",
        "comment": "水下隧道 + RockGrade_IV + 富水 → 钢拱架间距 0.5m(富水破碎区，支护接近极限密度)",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "119": {
        "label": "S07-9",
        "comment": "水下 + RockGrade V + 富水 → 37.5 cm",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 37.5},
        ]
    },
    "120": {
        "label": "S12-9",
        "comment": "水下隧道 + RockGrade_V + 富水 → 钢拱架间距 0.5m(最差工况，采用最密支护方案)",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "121": {
        "label": "W03-0",
        "comment": "mediumSoil + WaterRich + UnderwaterTunnelProject → 5.5mm// 中等土体水压大，需加厚防水层",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 5.5},
        ]
    },
    "122": {
        "label": "W03-1",
        "comment": "strongSoil + WaterRich + UnderwaterTunnelProject → 5mm // 强土抗渗性好，但水压大仍需增强防护",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 5},
        ]
    },
    "123": {
        "label": "W03-2",
        "comment": "weakSoil + WaterRich + UnderwaterTunnelProject → 6mm // 弱土+水下工况最为恶劣，设定最大厚度",
        "body": [
            {"type": "class", "class_name": "UnderwaterTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 6},
        ]
    },
    "124": {
        "label": "S05-1",
        "comment": "城市 + RockGrade I + 干燥 → 22.5 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 22.5},
        ]
    },
    "125": {
        "label": "S10-0",
        "comment": "城市隧道 + RockGrade_I + 干燥 → 钢拱架间距 1.2m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.2},
        ]
    },
    "126": {
        "label": "S05-3",
        "comment": "城市 + RockGrade II + 干燥 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "127": {
        "label": "S10-2",
        "comment": "城市隧道 + RockGrade_II + 干燥 → 钢拱架间距 1.0m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "128": {
        "label": "S05-5",
        "comment": "城市 + RockGrade III + 干燥 -&gt; 27.5 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "129": {
        "label": "S10-4",
        "comment": "城市隧道 + RockGrade_III + 干燥 → 钢拱架间距 0.8m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "130": {
        "label": "S05-7",
        "comment": "城市 + RockGrade IV + 干燥 -&gt; 30.0 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "131": {
        "label": "S10-6",
        "comment": "城市隧道 + RockGrade_IV + 干燥 → 钢拱架间距 0.5m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "132": {
        "label": "S10-8",
        "comment": "城市隧道 + RockGrade_V + 干燥 → 钢拱架间距 0.5m（按规范 TB 10003 调整）",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
        ]
    },
    "133": {
        "label": "S05-9",
        "comment": "城市 + RockGrade V + 干燥 -&gt; 32.5 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "134": {
        "label": "S05-2",
        "comment": "城市 + RockGrade I + 富水 → 25.0 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 25.0},
        ]
    },
    "135": {
        "label": "S10-1",
        "comment": "城市隧道 + RockGrade_I + 富水 → 钢拱架间距 1.0m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_I"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 1.0},
        ]
    },
    "136": {
        "label": "S05-4",
        "comment": "城市 + RockGrade II + 富水 → 27.5 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 27.5},
        ]
    },
    "137": {
        "label": "S10-3",
        "comment": "城市隧道 + RockGrade_II + 富水 → 钢拱架间距 0.8m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_II"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.8},
        ]
    },
    "138": {
        "label": "S05-6",
        "comment": "城市 + RockGrade III + 富水 -&gt; 30.0 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 30.0},
        ]
    },
    "139": {
        "label": "S10-5",
        "comment": "城市隧道 + RockGrade_III + 富水 → 钢拱架间距 0.6m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_III"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.6},
        ]
    },
    "140": {
        "label": "S05-8",
        "comment": "城市 + RockGrade IV + 富水 -&gt; 32.5 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 32.5},
        ]
    },
    "141": {
        "label": "S10-7",
        "comment": "城市隧道 + RockGrade_IV + 富水 → 钢拱架间距 0.5m（按规范 TB 10003 调整）",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_IV"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "142": {
        "label": "S05-91",
        "comment": "城市 + RockGrade V + 富水 -&gt; 35.0 cm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasLiningThickness", "subject": ":t", "value": 35.0},
        ]
    },
    "143": {
        "label": "S10-9",
        "comment": "城市隧道 + RockGrade_V + 富水 → 钢拱架间距  0.5m（按规范调整，不推荐小于 0.5m）过密支护施工困难，依规范 TB 10003 不推荐低于 0.5m",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasGeologicalCondition", "subject": ":t", "object": ":gc"},
            {"type": "object_property", "property_name": "hasRockGrade", "subject": ":gc", "object": "RockGrade_V"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":gc", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasSteelArchSpacing", "subject": ":t", "value": 0.5},
        ]
    },
    "144": {
        "label": "W01-0",
        "comment": "mediumSoil + Dry + UrbanTunnelProject → 3mm// 中等土质，干燥环境，采用常规防水层厚度",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3},
        ]
    },
    "145": {
        "label": "W01-2",
        "comment": "strongSoil + Dry + UrbanTunnelProject → 2.5mm // 强土体具有较强自防水能力，厚度可控",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 2.5},
        ]
    },
    "146": {
        "label": "W01-4",
        "comment": "weakSoil + Dry + UrbanTunnelProject → 4mm// 弱土体易渗水，即便干燥亦应提高防护",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "Dry"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4},
        ]
    },
    "147": {
        "label": "W01-1",
        "comment": "mediumSoil + WaterRich + UrbanTunnelProject → 4mm// 富水环境需提高防水层厚度",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "MediumSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 4},
        ]
    },
    "148": {
        "label": "W01-3",
        "comment": "strongSoil + WaterRich + UrbanTunnelProject → 3.5mm",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "StrongSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 3.5},
        ]
    },
    "149": {
        "label": "W01-5",
        "comment": "weakSoil + WaterRich + UrbanTunnelProject → 5mm// 弱土+富水，采取最大厚度加强防渗安全",
        "body": [
            {"type": "class", "class_name": "UrbanTunnelProject", "individual": ":t"},
            {"type": "object_property", "property_name": "hasSoilType", "subject": ":t", "object": "WeakSoil"},
            {"type": "object_property", "property_name": "hasHydroCondition", "subject": ":t", "object": "WaterRich"},
        ],
        "head": [
            {"type": "data_property", "property_name": "hasWaterproofLayerThickness", "subject": ":t", "value": 5},
        ]
    },
}

def infer_lining_thickness(tunnel_type: str, rock_grade: str, hydro_condition: str) -> Optional[float]:
    """快速推断衬砌厚度"""
    rules_map = {
        ("DeepTunnelProject", "RockGrade_I", "Dry"): 25.0,
        ("DeepTunnelProject", "RockGrade_II", "Dry"): 27.5,
        ("DeepTunnelProject", "RockGrade_III", "Dry"): 30.0,
        ("DeepTunnelProject", "RockGrade_V", "Dry"): 35.0,
        ("DeepTunnelProject", "RockGrade_I", "WaterRich"): 27.5,
        ("DeepTunnelProject", "RockGrade_II", "WaterRich"): 30.0,
        ("DeepTunnelProject", "RockGrade_III", "WaterRich"): 32.5,
        ("DeepTunnelProject", "RockGrade_IV", "WaterRich"): 35.0,
        ("DeepTunnelProject", "RockGrade_IV", "WaterRich"): 35.0,
        ("DeepTunnelProject", "RockGrade_V", "WaterRich"): 37.5,
        ("MountainTunnelProject", "RockGrade_I", "Dry"): 20.0,
        ("MountainTunnelProject", "RockGrade_II", "Dry"): 22.5,
        ("MountainTunnelProject", "RockGrade_III", "Dry"): 25.0,
        ("MountainTunnelProject", "RockGrade_IV", "Dry"): 27.5,
        ("MountainTunnelProject", "RockGrade_V", "Dry"): 30.0,
        ("MountainTunnelProject", "RockGrade_I", "WaterRich"): 22.5,
        ("MountainTunnelProject", "RockGrade_II", "WaterRich"): 25.0,
        ("MountainTunnelProject", "RockGrade_III", "WaterRich"): 27.5,
        ("MountainTunnelProject", "RockGrade_IV", "WaterRich"): 30.0,
        ("MountainTunnelProject", "RockGrade_V", "WaterRich"): 32.5,
        ("ShallowTunnelProject", "RockGrade_I", "Dry"): 22.5,
        ("ShallowTunnelProject", "RockGrade_II", "Dry"): 25.0,
        ("ShallowTunnelProject", "RockGrade_III", "Dry"): 27.5,
        ("ShallowTunnelProject", "RockGrade_IV", "Dry"): 30.0,
        ("ShallowTunnelProject", "RockGrade_V", "Dry"): 32.5,
        ("ShallowTunnelProject", "RockGrade_I", "WaterRich"): 25.0,
        ("ShallowTunnelProject", "RockGrade_II", "WaterRich"): 27.5,
        ("ShallowTunnelProject", "RockGrade_III", "WaterRich"): 30.0,
        ("ShallowTunnelProject", "RockGrade_IV", "WaterRich"): 32.5,
        ("ShallowTunnelProject", "RockGrade_V", "WaterRich"): 35.0,
        ("TunnelProject", "RockGrade_V", "WaterRich"): 45.0,
        ("UnderwaterTunnelProject", "RockGrade_I", "Dry"): 25.0,
        ("UnderwaterTunnelProject", "RockGrade_II", "Dry"): 27.5,
        ("UnderwaterTunnelProject", "RockGrade_III", "Dry"): 30.0,
        ("UnderwaterTunnelProject", "RockGrade_IV", "Dry"): 32.5,
        ("UnderwaterTunnelProject", "RockGrade_V", "Dry"): 35.0,
        ("UnderwaterTunnelProject", "RockGrade_I", "WaterRich"): 27.5,
        ("UnderwaterTunnelProject", "RockGrade_II", "WaterRich"): 30.0,
        ("UnderwaterTunnelProject", "RockGrade_III", "WaterRich"): 32.5,
        ("UnderwaterTunnelProject", "RockGrade_IV", "WaterRich"): 35.0,
        ("UnderwaterTunnelProject", "RockGrade_V", "WaterRich"): 37.5,
        ("UrbanTunnelProject", "RockGrade_I", "Dry"): 22.5,
        ("UrbanTunnelProject", "RockGrade_II", "Dry"): 25.0,
        ("UrbanTunnelProject", "RockGrade_III", "Dry"): 27.5,
        ("UrbanTunnelProject", "RockGrade_IV", "Dry"): 30.0,
        ("UrbanTunnelProject", "RockGrade_V", "Dry"): 32.5,
        ("UrbanTunnelProject", "RockGrade_I", "WaterRich"): 25.0,
        ("UrbanTunnelProject", "RockGrade_II", "WaterRich"): 27.5,
        ("UrbanTunnelProject", "RockGrade_III", "WaterRich"): 30.0,
        ("UrbanTunnelProject", "RockGrade_IV", "WaterRich"): 32.5,
        ("UrbanTunnelProject", "RockGrade_V", "WaterRich"): 35.0,
    }
    return rules_map.get((tunnel_type, rock_grade, hydro_condition))

def infer_steel_arch_spacing(tunnel_type: str, rock_grade: str, hydro_condition: str) -> Optional[float]:
    """快速推断钢拱架间距"""
    rules_map = {
        ("DeepTunnelProject", "RockGrade_I", "Dry"): 1.2,
        ("DeepTunnelProject", "RockGrade_II", "Dry"): 1.0,
        ("DeepTunnelProject", "RockGrade_III", "Dry"): 0.8,
        ("DeepTunnelProject", "RockGrade_IV", "Dry"): 0.6,
        ("DeepTunnelProject", "RockGrade_V", "Dry"): 0.5,
        ("DeepTunnelProject", "RockGrade_I", "WaterRich"): 1.0,
        ("DeepTunnelProject", "RockGrade_II", "WaterRich"): 0.8,
        ("DeepTunnelProject", "RockGrade_III", "WaterRich"): 0.6,
        ("DeepTunnelProject", "RockGrade_IV", "WaterRich"): 0.5,
        ("DeepTunnelProject", "RockGrade_V", "WaterRich"): 0.5,
        ("MountainTunnelProject", "RockGrade_I", "Dry"): 1.4,
        ("MountainTunnelProject", "RockGrade_II", "Dry"): 1.2,
        ("MountainTunnelProject", "RockGrade_III", "Dry"): 1.0,
        ("MountainTunnelProject", "RockGrade_IV", "Dry"): 0.8,
        ("MountainTunnelProject", "RockGrade_V", "Dry"): 0.6,
        ("MountainTunnelProject", "RockGrade_II", "WaterRich"): 1.0,
        ("MountainTunnelProject", "RockGrade_III", "WaterRich"): 0.8,
        ("MountainTunnelProject", "RockGrade_IV", "WaterRich"): 0.6,
        ("MountainTunnelProject", "RockGrade_V", "WaterRich"): 0.5,
        ("ShallowTunnelProject", "RockGrade_I", "Dry"): 1.2,
        ("ShallowTunnelProject", "RockGrade_II", "Dry"): 1.0,
        ("ShallowTunnelProject", "RockGrade_III", "Dry"): 0.8,
        ("ShallowTunnelProject", "RockGrade_IV", "Dry"): 0.6,
        ("ShallowTunnelProject", "RockGrade_V", "Dry"): 0.5,
        ("ShallowTunnelProject", "RockGrade_I", "WaterRich"): 1.0,
        ("ShallowTunnelProject", "RockGrade_II", "WaterRich"): 0.8,
        ("ShallowTunnelProject", "RockGrade_III", "WaterRich"): 0.6,
        ("ShallowTunnelProject", "RockGrade_IV", "WaterRich"): 0.5,
        ("ShallowTunnelProject", "RockGrade_V", "WaterRich"): 0.5,
        ("UnderwaterTunnelProject", "RockGrade_I", "Dry"): 1.2,
        ("UnderwaterTunnelProject", "RockGrade_II", "Dry"): 1.0,
        ("UnderwaterTunnelProject", "RockGrade_III", "Dry"): 0.8,
        ("UnderwaterTunnelProject", "RockGrade_IV", "Dry"): 0.6,
        ("UnderwaterTunnelProject", "RockGrade_V", "Dry"): 0.5,
        ("UnderwaterTunnelProject", "RockGrade_I", "WaterRich"): 1.0,
        ("UnderwaterTunnelProject", "RockGrade_II", "WaterRich"): 0.8,
        ("UnderwaterTunnelProject", "RockGrade_III", "WaterRich"): 0.6,
        ("UnderwaterTunnelProject", "RockGrade_IV", "WaterRich"): 0.5,
        ("UnderwaterTunnelProject", "RockGrade_V", "WaterRich"): 0.5,
        ("UrbanTunnelProject", "RockGrade_I", "Dry"): 1.2,
        ("UrbanTunnelProject", "RockGrade_II", "Dry"): 1.0,
        ("UrbanTunnelProject", "RockGrade_III", "Dry"): 0.8,
        ("UrbanTunnelProject", "RockGrade_IV", "Dry"): 0.5,
        ("UrbanTunnelProject", "RockGrade_I", "WaterRich"): 1.0,
        ("UrbanTunnelProject", "RockGrade_II", "WaterRich"): 0.8,
        ("UrbanTunnelProject", "RockGrade_III", "WaterRich"): 0.6,
        ("UrbanTunnelProject", "RockGrade_IV", "WaterRich"): 0.5,
        ("UrbanTunnelProject", "RockGrade_V", "WaterRich"): 0.5,
    }
    return rules_map.get((tunnel_type, rock_grade, hydro_condition))

def infer_waterproof_thickness(tunnel_type: str, soil_type: str, hydro_condition: str) -> Optional[float]:
    """快速推断防水层厚度"""
    rules_map = {
        ("MountainTunnelProject", "MediumSoil", "Dry"): 3.5,
        ("MountainTunnelProject", "StrongSoil", "Dry"): 3,
        ("MountainTunnelProject", "WeakSoil", "Dry"): 4.5,
        ("MountainTunnelProject", "MediumSoil", "WaterRich"): 4.5,
        ("MountainTunnelProject", "StrongSoil", "WaterRich"): 4,
        ("MountainTunnelProject", "WeakSoil", "WaterRich"): 5,
        ("ShallowTunnelProject", "MediumSoil", "Dry"): 3.5,
        ("ShallowTunnelProject", "MediumSoil", "Dry"): 3.5,
        ("ShallowTunnelProject", "StrongSoil", "Dry"): 3,
        ("ShallowTunnelProject", "StrongSoil", "Dry"): 3,
        ("ShallowTunnelProject", "WeakSoil", "Dry"): 4.5,
        ("ShallowTunnelProject", "WeakSoil", "Dry"): 4.5,
        ("ShallowTunnelProject", "MediumSoil", "WaterRich"): 4.5,
        ("ShallowTunnelProject", "MediumSoil", "WaterRich"): 4.5,
        ("ShallowTunnelProject", "StrongSoil", "WaterRich"): 4,
        ("ShallowTunnelProject", "StrongSoil", "WaterRich"): 4,
        ("ShallowTunnelProject", "WeakSoil", "WaterRich"): 5.5,
        ("ShallowTunnelProject", "WeakSoil", "WaterRich"): 5.5,
        ("UnderwaterTunnelProject", "MediumSoil", "WaterRich"): 5.5,
        ("UnderwaterTunnelProject", "StrongSoil", "WaterRich"): 5,
        ("UnderwaterTunnelProject", "WeakSoil", "WaterRich"): 6,
        ("UrbanTunnelProject", "MediumSoil", "Dry"): 3,
        ("UrbanTunnelProject", "StrongSoil", "Dry"): 2.5,
        ("UrbanTunnelProject", "WeakSoil", "Dry"): 4,
        ("UrbanTunnelProject", "MediumSoil", "WaterRich"): 4,
        ("UrbanTunnelProject", "StrongSoil", "WaterRich"): 3.5,
        ("UrbanTunnelProject", "WeakSoil", "WaterRich"): 5,
    }
    return rules_map.get((tunnel_type, soil_type, hydro_condition))

def apply_construction_method_rules(tunnel_length: float) -> str:
    """根据隧道长度确定施工方法"""
    if tunnel_length > 3000:
        return "DrillAndBlast_001"
    else:
        return "TBM_001"

def calculate_bolt_length(tunnel_diameter: float, rock_grade: str) -> float:
    """计算锚杆长度"""
    multipliers = {
        "RockGrade_I": 0.25,
        "RockGrade_II": 0.3,
        "RockGrade_III": 0.33,
        "RockGrade_IV": 0.45,
        "RockGrade_V": 0.5
    }
    return tunnel_diameter * multipliers.get(rock_grade, 0.3)

def calculate_steel_arch_count(tunnel_length: float, spacing: float) -> int:
    """计算钢拱架数量"""
    if spacing > 0:
        return round(tunnel_length / spacing)
    return 0

def comprehensive_tunnel_design(tunnel_type: str, tunnel_length: float, tunnel_diameter: float,
                                rock_grade: str, hydro_condition: str, 
                                soil_type: str = "MediumSoil") -> Dict[str, Any]:
    """综合隧道设计计算"""
    result = {}
    
    # 基本参数
    result["tunnel_type"] = tunnel_type
    result["tunnel_length"] = tunnel_length
    result["tunnel_diameter"] = tunnel_diameter
    
    # 衬砌厚度
    result["lining_thickness"] = infer_lining_thickness(tunnel_type, rock_grade, hydro_condition)
    
    # 钢拱架间距
    result["steel_arch_spacing"] = infer_steel_arch_spacing(tunnel_type, rock_grade, hydro_condition)
    
    # 防水层厚度
    result["waterproof_thickness"] = infer_waterproof_thickness(tunnel_type, soil_type, hydro_condition)
    
    # 施工方法
    result["construction_method"] = apply_construction_method_rules(tunnel_length)
    
    # 锚杆长度
    result["bolt_length"] = calculate_bolt_length(tunnel_diameter, rock_grade)
    
    # 钢拱架数量
    if result["steel_arch_spacing"]:
        result["steel_arch_count"] = calculate_steel_arch_count(tunnel_length, result["steel_arch_spacing"])
    
    return result

