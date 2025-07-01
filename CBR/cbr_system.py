import numpy as np

class CBRSystem:
    def __init__(self, case_base, feature_weights, threshold=0.85):
        self.case_base = case_base
        self.feature_weights = feature_weights
        self.threshold = threshold
        self.feature_mins, self.feature_maxs = self.compute_feature_ranges()

    def compute_feature_ranges(self):
        all_features = np.array([case["features"] for case in self.case_base])
        feature_mins = all_features.min(axis=0)
        feature_maxs = all_features.max(axis=0)
        return feature_mins, feature_maxs

    def normalize(self, features):
        features = np.array(features, dtype=float)
        denom = self.feature_maxs - self.feature_mins
        denom = np.where(denom == 0, 1, denom)
        return (features - self.feature_mins) / denom

    def calculate_similarity(self, target_features, case_features):
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
