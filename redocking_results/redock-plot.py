import matplotlib.pyplot as plt
import pandas as pd

# 数据准备
data = {
    "PDB": ["2NRU", "5UIT", "6EGE", "6N8G", "6O8U", "6O94", "6O95", "6UYA", "8W3W", "8W3X", "8WTF"],
    "XDOCK-RMSD": [1.819, 2.349, 0.266, 0.114, 1.765, 0.081, 0.991, 0.171, 2.165, 0.067, 2.285],
    "Karmadock-RMSD": [6.429, 4.686, 6.273, 6.906, 5.956, 6.556, 5.754, 6.204, 4.173, 4.248, 4.662],
    "Vina-gpu-RMSD": [1.414, 0.563, 0.544, 0.284, 0.251, 0.588, 0.375, 1.003, 0.533, 0.000, 3.943],
    "ledock-RMSD": [0.573, 0.221, 0.520, 0.521, 0.407, 0.484, 0.625, 0.538, 0.476, 0.798, 0.374]
}

df = pd.DataFrame(data)

# 绘制柱状图
fig, ax = plt.subplots(figsize=(14, 8))

# 设置柱宽度和位置
bar_width = 0.2
x = range(len(df["PDB"]))

# 绘制每种 RMSD 方法的柱状图
ax.bar([pos - 1.5 * bar_width for pos in x], df["XDOCK-RMSD"], bar_width, label="XDOCK-RMSD")
ax.bar([pos - 0.5 * bar_width for pos in x], df["Karmadock-RMSD"], bar_width, label="Karmadock-RMSD")
ax.bar([pos + 0.5 * bar_width for pos in x], df["Vina-gpu-RMSD"], bar_width, label="Vina-gpu-RMSD")
ax.bar([pos + 1.5 * bar_width for pos in x], df["ledock-RMSD"], bar_width, label="Ledock-RMSD")

# 添加标题和标签
ax.set_title("RMSD Comparison Across Methods", fontsize=16)
ax.set_xlabel("PDB", fontsize=12)
ax.set_ylabel("RMSD Values", fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(df["PDB"], rotation=45, fontsize=10)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 保存为 PNG 文件
plt.tight_layout()
plt.savefig("RMSD_Comparison.png", dpi=300)

# 显示图表
plt.show()
