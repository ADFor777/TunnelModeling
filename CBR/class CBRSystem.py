import numpy as np

class CBRSystem:
    def __init__(self, case_base, feature_weights, threshold=0.85):
        self.case_base = case_base
        self.feature_weights = feature_weights
        self.threshold = threshold

        # 👇 在初始化时做一次全局统计
        self.feature_mins, self.feature_maxs = self.compute_feature_ranges()

    def compute_feature_ranges(self):
        """
        计算案例库里各个特征的全局 min 和 max
        """
        all_features = np.array([c["features"] for c in self.case_base])
        feature_mins = all_features.min(axis=0)
        feature_maxs = all_features.max(axis=0)
        return feature_mins, feature_maxs

    def normalize(self, features):
        """
        将输入特征按案例库里的全局 min-max 归一化到 [0,1]
        """
        features = np.array(features, dtype=float)
        denom = self.feature_maxs - self.feature_mins
        # 避免除0
        denom = np.where(denom == 0, 1, denom)
        normed = (features - self.feature_mins) / denom
        return normed

    def calculate_similarity(self, target_features, case_features):
        """
        加权欧氏距离 → 相似度
        """
        # 👇 归一化
        norm_target = self.normalize(target_features)
        norm_case = self.normalize(case_features)

        diff = norm_target - norm_case
        weights = np.array(self.feature_weights, dtype=float)
        weighted_squared = weights * diff ** 2
        distance = np.sqrt(weighted_squared.sum())

        similarity = 1 / (1 + distance)
        return similarity

    def retrieve(self, target_case):
        similarities = []
        for case in self.case_base:
            sim = self.calculate_similarity(target_case['features'], case['features'])
            similarities.append((case, sim))
        return sorted(similarities, key=lambda x: x[1], reverse=True)

    def adapt_case(self, source_case, target_case):
        print(f"\n✅ 采用案例【{source_case['label']}】的参数作为推荐方案")
        return source_case

    def reuse(self, retrieved_case, target_case):
        if retrieved_case[1] >= self.threshold:
            print(f"✅ 相似度 {retrieved_case[1]:.3f} ≥ 阈值 {self.threshold}")
            return self.adapt_case(retrieved_case[0], target_case)
        else:
            print(f"⚠️ 相似度 {retrieved_case[1]:.3f} < 阈值 {self.threshold}，需要调用RBR推理。")
            return None

    def revise(self, adapted_case, target_case):
        print("✅ （可选）这里可以对参数做最后的调整")
        return adapted_case

    def retain(self, new_case):
        self.case_base.append(new_case)
        print(f"✅ 新案例【{new_case['label']}】已加入案例库。")

    def print_outputs(self, case):
        print("\n📌 推荐的后续设计参数：")
        for k, v in case["outputs"].items():
            print(f"  - {k}: {v}")


# ================================================
# ✅ 设定：案例库
# ================================================
case_base = [
    {
        "features": [1200, 3, 2, 2, 1, 10.5],
        "label": "MountainTunnelProject_A",
        "outputs": {
            "hasConstructionMethod": "DrillBlast",
            "hasBoltLength": 4.5,
            "hasBoltRowCount": 2,
            "hasBoltColumnCount": 3,
            "hasLiningThickness": 30,
            "hasSteelArchSpacing": 0.8,
            "hasSteelArchCount": 5,
            "hasSteelArchThickness": 12,
            "hasWaterproofLayerThickness": 5
        }
    },
    {
        "features": [800, 2, 1, 1, 2, 9.0],
        "label": "UnderwaterTunnelProject_B",
        "outputs": {
            "hasConstructionMethod": "TBM",
            "hasBoltLength": 3.5,
            "hasBoltRowCount": 1,
            "hasBoltColumnCount": 2,
            "hasLiningThickness": 25,
            "hasSteelArchSpacing": 1.2,
            "hasSteelArchCount": 3,
            "hasSteelArchThickness": 10,
            "hasWaterproofLayerThickness": 8
        }
    }
]

# ================================================
# ✅ 特征权重
# ================================================
feature_weights = [0.2, 0.15, 0.1, 0.1, 0.15, 0.3]

# ================================================
# ✅ 创建CBR系统
# ================================================
cbr = CBRSystem(case_base, feature_weights, threshold=0.85)

# ================================================
# ✅ 用户输入
# ================================================
target_case = {
    "features": [1100, 3, 2, 2, 1, 10.2]
}

# ================================================
# ✅ CBR四步走
# ================================================
retrieved_list = cbr.retrieve(target_case)
best_case, best_similarity = retrieved_list[0]
print("\n✅ 最相似案例:", best_case["label"])
print("✅ 相似度:", round(best_similarity, 3))

adapted_case = cbr.reuse(retrieved_list[0], target_case)

if adapted_case:
    revised_case = cbr.revise(adapted_case, target_case)
    cbr.print_outputs(revised_case)

    new_case = {
        "features": target_case["features"],
        "label": "NewTunnelCase_001",
        "outputs": revised_case["outputs"]
    }
    cbr.retain(new_case)
