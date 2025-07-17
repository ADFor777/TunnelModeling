import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import math
import random

class MHPOAlgorithm:
    """
    改进的猎物-捕食者优化算法（Modified Hunter-Prey Optimization）
    用于CBR模型中特征参数的权重分配优化
    """
    
    def __init__(self, population_size=30, max_iterations=500, dim=7):
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.dim = dim  # 权重维度（特征数量）
        self.lb = 0.0   # 权重下界
        self.ub = 1.0   # 权重上界
        
        # 算法参数
        self.C = 2 * random.random()  # 随机参数
        self.Z = 2 * random.random()  # 随机参数
        
    def levy_flight(self, beta=1.5):
        """Levy飞行分布"""
        sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
                (math.gamma((1 + beta) / 2) * beta * (2 ** ((beta - 1) / 2)))) ** (1 / beta)
        
        u = np.random.normal(0, sigma)
        v = np.random.normal(0, 1)
        step = u / (abs(v) ** (1 / beta))
        return step
    
    def initialize_population(self):
        """初始化种群"""
        population = np.random.uniform(self.lb, self.ub, (self.population_size, self.dim))
        
        # 确保权重和为1的约束
        for i in range(self.population_size):
            population[i] = population[i] / np.sum(population[i])
        
        return population
    
    def fitness_function(self, weights, X_train, y_train, X_test, y_test, k=4):
        """
        CBR模型的适应度函数 - 计算MSE
        使用加权欧几里得距离进行相似度计算
        """
        try:
            # 确保权重和为1
            weights = weights / np.sum(weights)
            
            predictions = []
            
            for test_sample in X_test:
                # 计算与所有训练样本的加权距离
                distances = []
                for train_sample in X_train:
                    # 加权欧几里得距离
                    weighted_diff = weights * (test_sample - train_sample) ** 2
                    distance = np.sqrt(np.sum(weighted_diff))
                    distances.append(distance)
                
                # 找到k个最近邻
                distances = np.array(distances)
                k_nearest_indices = np.argsort(distances)[:k]
                
                # 使用k个最近邻的平均值作为预测
                k_nearest_targets = y_train[k_nearest_indices]
                prediction = np.mean(k_nearest_targets)
                predictions.append(prediction)
            
            # 计算MSE
            mse = mean_squared_error(y_test, predictions)
            return mse
            
        except Exception as e:
            return 1e6  # 返回一个很大的值表示错误
    
    def update_position(self, position, best_position, iteration):
        """更新位置的改进机制"""
        new_position = position.copy()
        
        # 自适应变异因子
        f = 0.4 * np.exp(np.exp(1 - self.max_iterations / (self.max_iterations + 1 - iteration)))
        
        # 随机数q决定搜索策略
        q = random.random()
        
        for j in range(self.dim):
            r1, r2, r3 = random.random(), random.random(), random.random()
            
            if q >= 0.5:
                # 策略1：基于最优位置的搜索
                new_position[j] = position[j] + 0.5 * (
                    (2 * self.C * self.Z * best_position[j] - position[j]) +
                    (2 * (1 - self.C) * self.Z * np.mean(best_position) - position[j])
                )
            elif 0.25 <= q < 0.5:
                # 策略2：基于当前最优解的搜索
                new_position[j] = (best_position[j] - np.mean(best_position)) - r2 * (
                    self.lb + r3 * (self.ub - self.lb))
            else:
                # 策略3：Levy飞行随机搜索
                levy_step = self.levy_flight()
                rand_pos = random.uniform(self.lb, self.ub)
                new_position[j] = rand_pos - levy_step * abs(rand_pos - 2 * r1 * position[j])
        
        # 边界处理
        new_position = np.clip(new_position, self.lb, self.ub)
        
        # 差分进化变异
        if random.random() < 0.3:  # 30%概率进行变异
            r1, r2, r3 = np.random.choice(len(new_position), 3, replace=False)
            new_position = new_position + f * (new_position - new_position)
        
        # 确保权重和为1
        new_position = new_position / np.sum(new_position)
        
        return new_position
    
    def optimize(self, X_train, y_train, X_test, y_test):
        """
        主优化循环 - 自动调整权重以最小化MSE
        这是权重自动优化的核心部分
        """
        # 初始化种群（随机权重组合）
        population = self.initialize_population()
        fitness_values = np.zeros(self.population_size)
        
        # 计算初始适应度（每个权重组合的MSE）
        print("🔄 计算初始权重组合的MSE...")
        for i in range(self.population_size):
            fitness_values[i] = self.fitness_function(population[i], X_train, y_train, X_test, y_test)
        
        # 找到最优个体（MSE最小的权重组合）
        best_idx = np.argmin(fitness_values)
        best_position = population[best_idx].copy()  # 当前最优权重
        best_fitness = fitness_values[best_idx]      # 当前最小MSE
        
        # 记录收敛历史
        convergence_history = []
        weight_history = [best_position.copy()]  # 记录权重变化
        
        print(f"📊 初始最优MSE: {best_fitness:.6f}")
        print(f"📊 初始最优权重: {best_position}")
        
        # 🚀 主优化循环 - 自动权重调整过程
        for iteration in range(self.max_iterations):
            improved_count = 0  # 记录本轮改进次数
            
            for i in range(self.population_size):
                # 🎯 关键步骤1: 生成新的权重组合
                new_position = self.update_position(population[i], best_position, iteration)
                
                # 🎯 关键步骤2: 计算新权重组合下的MSE
                new_fitness = self.fitness_function(new_position, X_train, y_train, X_test, y_test)
                
                # 🎯 关键步骤3: 如果新MSE更小，就接受新权重
                if new_fitness < fitness_values[i]:
                    population[i] = new_position
                    fitness_values[i] = new_fitness
                    improved_count += 1
                    
                    # 🎯 关键步骤4: 更新全局最优权重（如果找到更小的MSE）
                    if new_fitness < best_fitness:
                        old_mse = best_fitness
                        best_position = new_position.copy()
                        best_fitness = new_fitness
                        weight_history.append(best_position.copy())
                        
                        print(f"🎉 发现更优权重! 迭代{iteration+1}: MSE {old_mse:.6f} → {best_fitness:.6f}")
            
            # 记录当前最优适应度
            convergence_history.append(best_fitness)
            
            # 打印进度
            if (iteration + 1) % 50 == 0:
                print(f"📈 迭代 {iteration + 1}/{self.max_iterations}: MSE = {best_fitness:.6f}, 本轮改进{improved_count}次")
        
        print(f"\n✅ 权重优化完成!")
        print(f"🎯 最终最优MSE: {best_fitness:.6f}")
        print(f"🎯 权重调整次数: {len(weight_history)}")
        
        return best_position, best_fitness, convergence_history

def load_and_prepare_data(file_path='normalized_case_vectors.csv'):
    """加载和准备数据"""
    try:
        # 读取归一化数据
        df = pd.read_csv(file_path)
        print(f"数据形状: {df.shape}")
        print(f"列名: {df.columns.tolist()}")
        
        # 假设最后一列是目标变量（如论文中的总面积）
        # 如果没有目标列，我们可以创建一个合成的目标
        if 'target' in df.columns:
            X = df.drop('target', axis=1).values
            y = df['target'].values
        else:
            # 使用前n-1列作为特征，最后一列作为目标
            X = df.iloc[:, :-1].values
            y = df.iloc[:, -1].values
        
        print(f"特征矩阵形状: {X.shape}")
        print(f"目标向量形状: {y.shape}")
        
        return X, y
        
    except Exception as e:
        print(f"数据加载错误: {e}")
        # 生成示例数据用于测试
        print("使用示例数据进行测试...")
        np.random.seed(42)
        X = np.random.rand(102, 7)  # 102个样本，7个特征
        y = np.random.rand(102) * 1000  # 目标值
        return X, y

def main():
    """主函数"""
    print("=== MHPO算法用于CBR权重优化 ===\n")
    
    # 加载数据
    X, y = load_and_prepare_data('normalized_case_vectors.csv')
    
    # 划分训练和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"训练集大小: {X_train.shape[0]}")
    print(f"测试集大小: {X_test.shape[0]}")
    print(f"特征维度: {X_train.shape[1]}\n")
    
    # 创建MHPO算法实例
    mhpo = MHPOAlgorithm(
        population_size=30,
        max_iterations=500,
        dim=X_train.shape[1]
    )
    
    print("开始优化...")
    
    # 运行优化
    best_weights, best_mse, convergence_history = mhpo.optimize(
        X_train, y_train, X_test, y_test
    )
    
    print(f"\n=== 优化结果 ===")
    print(f"最优MSE: {best_mse:.6f}")
    print(f"最优权重:")
    for i, weight in enumerate(best_weights):
        print(f"  特征 {i+1}: {weight:.4f}")
    print(f"权重和: {np.sum(best_weights):.6f}")
    
    # 绘制收敛曲线
    plt.figure(figsize=(10, 6))
    plt.plot(convergence_history)
    plt.title('MHPO算法收敛曲线')
    plt.xlabel('迭代次数')
    plt.ylabel('最优适应度 (MSE)')
    plt.grid(True)
    plt.show()
    
    # 分析权重重要性
    print(f"\n=== 特征重要性分析 ===")
    feature_importance = [(i+1, weight) for i, weight in enumerate(best_weights)]
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    for rank, (feature_idx, weight) in enumerate(feature_importance, 1):
        print(f"排名 {rank}: 特征 {feature_idx} (权重: {weight:.4f})")
    
    return best_weights, best_mse, convergence_history

if __name__ == "__main__":
    best_weights, best_mse, convergence_history = main()