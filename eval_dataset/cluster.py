import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from rdkit.DataStructs.cDataStructs import ConvertToNumpyArray

# 读取CSV文件
file_path = 'IRAK4.csv'  # 请替换为你的CSV文件路径
data = pd.read_csv(file_path)

# 将SMILES字符串转化为分子指纹
def smiles_to_fingerprint(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        # Morgan Fingerprint, 2048位
        return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    else:
        return None

# 生成指纹并转化为NumPy数组
fingerprint_list = []
for smiles in data['smiles']:
    fp = smiles_to_fingerprint(smiles)
    if fp is not None:
        arr = np.zeros((2048,))
        ConvertToNumpyArray(fp, arr)
        fingerprint_list.append(arr)

# 转化为二维NumPy数组
fingerprint_array = np.array(fingerprint_list)

# 使用t-SNE降维
tsne = TSNE(n_components=2, random_state=42)
data_tsne = tsne.fit_transform(fingerprint_array)

# K-means聚类（50类）
kmeans = KMeans(n_clusters=50, random_state=42)
data = data.iloc[:len(data_tsne)]  # 确保 data 的长度与 data_tsne 一致
data['Cluster'] = kmeans.fit_predict(data_tsne)

# 保存聚类结果到CSV文件
data.to_csv('clustered_data.csv', index=False)

# 可视化并保存图片
plt.figure(figsize=(12, 8))
scatter = plt.scatter(data_tsne[:, 0], data_tsne[:, 1], c=data['Cluster'], cmap='tab20', s=50, alpha=0.7)
plt.colorbar(scatter, label='Cluster')
plt.title("t-SNE with K-means Clustering (50 clusters)")
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")

# 保存高质量的PNG图片 (300 DPI)
plt.savefig('cluster_visualization.png', dpi=300, format='png')
plt.show()
