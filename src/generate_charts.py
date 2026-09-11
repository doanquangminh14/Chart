"""
Module: generate_charts.py
Mô tả: Bộ công cụ trực quan hóa dữ liệu toàn diện với 16 loại biểu đồ chuẩn chuyên nghiệp,
sử dụng Matplotlib, Seaborn và Squarify.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify

# Thiết lập encoding UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình phong cách đồ thị hiện đại
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e0e0e0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv("data/cleaned_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

# ==============================================================================
# CHART 1: LINE CHART (Biểu đồ đường - Xu hướng theo thời gian)
# ==============================================================================
def chart_01_line(df):
    monthly = df.groupby("Order_Month")[["Total_Amount", "Profit"]].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.plot(monthly["Order_Month"], monthly["Total_Amount"], marker='o', linewidth=2.5, 
            color='#1f77b4', label='Doanh thu (Revenue)', markersize=7)
    ax.plot(monthly["Order_Month"], monthly["Profit"], marker='s', linewidth=2.2, 
            color='#2ca02c', linestyle='--', label='Lợi nhuận (Profit)', markersize=6)
    
    # Fill between
    ax.fill_between(monthly["Order_Month"], monthly["Profit"], monthly["Total_Amount"], 
                    color='#1f77b4', alpha=0.08)
    
    # Annotate max revenue point
    max_rev_idx = monthly["Total_Amount"].idxmax()
    max_rev_val = monthly.loc[max_rev_idx, "Total_Amount"]
    max_rev_month = monthly.loc[max_rev_idx, "Order_Month"]
    ax.annotate(f'Đỉnh: ${max_rev_val:,.0f}', 
                xy=(max_rev_month, max_rev_val), 
                xytext=(0, 15), textcoords="offset points",
                arrowprops=dict(facecolor='#d62728', shrink=0.05, width=1, headwidth=6),
                ha='center', fontweight='bold', color='#d62728')

    ax.set_title("01. Xu Hướng Doanh Thu & Lợi Nhuận Theo Tháng (Monthly Trend)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Tháng Đặt Hàng (Year-Month)", fontsize=11, labelpad=10)
    ax.set_ylabel("Giá Trị ($ USD)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.xticks(rotation=45)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "01_line_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 2: BAR / COLUMN CHART (Biểu đồ cột - So sánh định lượng danh mục)
# ==============================================================================
def chart_02_bar(df):
    cat_sales = df.groupby("Category")["Total_Amount"].sum().sort_values(ascending=False).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    colors = sns.color_palette("Blues_r", len(cat_sales))
    bars = ax.bar(cat_sales["Category"], cat_sales["Total_Amount"], color=colors, edgecolor='#333333', linewidth=0.6, width=0.6)
    
    # Data labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + (yval * 0.015), f"${yval:,.0f}", 
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#222222')

    ax.set_title("02. Tổng Doanh Thu Theo Danh Mục Sản Phẩm (Category Revenue)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Danh Mục Sản Phẩm (Category)", fontsize=11, labelpad=10)
    ax.set_ylabel("Tổng Doanh Thu ($ USD)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter('${x:,.0f}')
    ax.set_ylim(0, cat_sales["Total_Amount"].max() * 1.15)
    plt.xticks(rotation=20)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "02_bar_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 3: GROUPED BAR CHART (Biểu đồ cột nhóm - So sánh đa chiều 2 phân loại)
# ==============================================================================
def chart_03_grouped_bar(df):
    pivot_df = df.groupby(["Category", "Region"])["Total_Amount"].sum().unstack().fillna(0)
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    pivot_df.plot(kind='bar', ax=ax, width=0.8, colormap='Spectral', edgecolor='#444444', linewidth=0.5)
    
    ax.set_title("03. Doanh Thu Từng Danh Mục Phân Bổ Theo Khu Vực Địa Lý (Grouped Bar)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Danh Mục Sản Phẩm", fontsize=11, labelpad=10)
    ax.set_ylabel("Doanh Thu ($ USD)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.xticks(rotation=15)
    ax.legend(title="Khu Vực (Region)", frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "03_grouped_bar_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 4: STACKED BAR CHART (Biểu đồ cột chồng - Tỷ trọng phương thức thanh toán)
# ==============================================================================
def chart_04_stacked_bar(df):
    pivot_norm = pd.crosstab(df["Category"], df["Payment_Method"], normalize='index') * 100
    
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    colors = ['#2b5c8f', '#4682b4', '#87ceeb', '#f4a460']
    pivot_norm.plot(kind='barh', stacked=True, ax=ax, color=colors, edgecolor='#ffffff', linewidth=1)
    
    # Add percentage text in center of segments
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', label_type='center', fontsize=9, fontweight='bold', color='black')

    ax.set_title("04. Cơ Cấu Phương Thức Thanh Toán Theo Từng Danh Mục (Stacked Bar 100%)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Tỷ Lệ Phần Trăm (%)", fontsize=11, labelpad=10)
    ax.set_ylabel("Danh Mục Sản Phẩm", fontsize=11, labelpad=10)
    ax.legend(title="Phương Thức Thanh Toán", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "04_stacked_bar_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 5: HISTOGRAM (Biểu đồ phân phối tần suất - Biến liên tục Age)
# ==============================================================================
def chart_05_histogram(df):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    sns.histplot(df["Customer_Age"], bins=15, kde=True, color='#0288d1', edgecolor='#ffffff', linewidth=1.2, ax=ax)
    
    mean_val = df["Customer_Age"].mean()
    median_val = df["Customer_Age"].median()
    
    ax.axvline(mean_val, color='#d32f2f', linestyle='--', linewidth=2, label=f'Mean (Trung bình): {mean_val:.1f}')
    ax.axvline(median_val, color='#388e3c', linestyle='-', linewidth=2, label=f'Median (Trung vị): {median_val:.1f}')

    ax.set_title("05. Phân Phối Độ Tuổi Khách Hàng (Customer Age Distribution)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Độ Tuổi (Age)", fontsize=11, labelpad=10)
    ax.set_ylabel("Số Lượng Khách Hàng (Tần Suất)", fontsize=11, labelpad=10)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "05_histogram.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 6: KDE / DENSITY PLOT (Biểu đồ mật độ xác suất)
# ==============================================================================
def chart_06_kde_density(df):
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    
    for channel in df["Sales_Channel"].unique():
        subset = df[df["Sales_Channel"] == channel]
        sns.kdeplot(subset["Total_Amount"], label=channel, fill=True, alpha=0.25, linewidth=2, ax=ax)

    ax.set_title("06. Mật Độ Phân Phối Giá Trị Đơn Hàng Theo Kênh Bán Hàng (KDE Density)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Giá Trị Đơn Hàng ($ USD)", fontsize=11, labelpad=10)
    ax.set_ylabel("Mật Độ Xác Suất (Density)", fontsize=11, labelpad=10)
    ax.set_xlim(0, 3500)
    ax.legend(title="Kênh Bán (Sales Channel)", frameon=True, facecolor='white')
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "06_kde_density_plot.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 7: BOX PLOT (Biểu đồ hộp - Phát hiện ngoại lai và tứ phân vị)
# ==============================================================================
def chart_07_box_plot(df):
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    
    sns.boxplot(x="Category", y="Unit_Price", data=df, hue="Category", legend=False, palette="Set2", 
                fliersize=5, flierprops=dict(marker='o', markerfacecolor='crimson', markersize=6),
                width=0.5, ax=ax)

    ax.set_title("07. Phân Bố & Phát Hiện Ngoại Lai Đơn Giá Theo Danh Mục (Box Plot)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Danh Mục Sản Phẩm", fontsize=11, labelpad=10)
    ax.set_ylabel("Đơn Giá Sản Phẩm ($ USD)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.xticks(rotation=15)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "07_box_plot.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 8: VIOLIN PLOT (Biểu đồ vĩ cầm - Kết hợp Box Plot & KDE)
# ==============================================================================
def chart_08_violin_plot(df):
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    
    sns.violinplot(x="Category", y="Customer_Rating", data=df, hue="Category", legend=False, palette="Pastel1", 
                   inner="quartile", cut=0, ax=ax)

    ax.set_title("08. Phân Bố Điểm Đánh Giá Khách Hàng Theo Danh Mục (Violin Plot)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Danh Mục Sản Phẩm", fontsize=11, labelpad=10)
    ax.set_ylabel("Điểm Đánh Giá (Rating 1.0 - 5.0)", fontsize=11, labelpad=10)
    ax.set_ylim(2.5, 5.2)
    plt.xticks(rotation=15)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "08_violin_plot.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 9: SCATTER PLOT (Biểu đồ phân tán - Tương quan 2 biến & Hồi quy)
# ==============================================================================
def chart_09_scatter(df):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    sns.regplot(x="Marketing_Spend", y="Total_Amount", data=df, 
                scatter_kws={'alpha': 0.6, 'color': '#3f51b5', 's': 40},
                line_kws={'color': '#f44336', 'linewidth': 2, 'label': 'Đường xu hướng (Trendline)'},
                ax=ax)

    ax.set_title("09. Tương Quan Giữa Chi Phí Marketing và Doanh Thu Đơn Hàng (Scatter Plot)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Chi Phí Marketing ($ USD)", fontsize=11, labelpad=10)
    ax.set_ylabel("Doanh Thu Đơn Hàng ($ USD)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter('${x:,.0f}')
    ax.xaxis.set_major_formatter('${x:,.0f}')
    ax.legend(frameon=True, facecolor='white')
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "09_scatter_plot.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 10: BUBBLE CHART (Biểu đồ bong bóng - Đa biến 4 chiều)
# ==============================================================================
def chart_10_bubble(df):
    prod_agg = df.groupby(["Product_Name", "Category"]).agg({
        "Total_Amount": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Customer_Rating": "mean"
    }).reset_index()

    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    
    categories = prod_agg["Category"].unique()
    colors = sns.color_palette("tab10", len(categories))
    cat_color_map = dict(zip(categories, colors))
    
    for cat in categories:
        sub = prod_agg[prod_agg["Category"] == cat]
        scatter = ax.scatter(
            sub["Total_Amount"], sub["Profit"],
            s=sub["Quantity"] * 8, # Kích thước bong bóng theo số lượng bán
            color=cat_color_map[cat], alpha=0.7, edgecolors='black', linewidth=0.8,
            label=cat
        )
        # Ghi tên một số sản phẩm nổi bật
        for _, row in sub.iterrows():
            if row["Total_Amount"] > prod_agg["Total_Amount"].quantile(0.7):
                ax.annotate(row["Product_Name"], (row["Total_Amount"], row["Profit"]),
                            fontsize=8, fontweight='bold', xytext=(5, 5), textcoords='offset points')

    ax.set_title("10. Ma Trận Hiệu Suất Sản Phẩm (Bubble Chart: Doanh thu vs Lợi nhuận vs Số lượng)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Tổng Doanh Thu ($ USD)", fontsize=11, labelpad=10)
    ax.set_ylabel("Tổng Lợi Nhuận ($ USD)", fontsize=11, labelpad=10)
    ax.xaxis.set_major_formatter('${x:,.0f}')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    ax.legend(title="Danh Mục (Category)\n*Size = Số lượng bán", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "10_bubble_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 11: HEATMAP CORRELATION (Bản đồ nhiệt ma trận tương quan)
# ==============================================================================
def chart_11_heatmap(df):
    num_cols = ["Customer_Age", "Unit_Price", "Quantity", "Total_Amount", "Profit", "Customer_Rating", "Marketing_Spend"]
    corr_matrix = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', 
                vmin=-1, vmax=1, square=True, linewidths=1, linecolor='white',
                cbar_kws={"shrink": 0.8, "label": "Hệ số tương quan Pearson"}, ax=ax)

    ax.set_title("11. Ma Trận Hệ Số Tương Quan Giữa Các Chỉ Số (Heatmap)", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "11_heatmap_correlation.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 12: DONUT CHART (Biểu đồ bánh Donut - Tỷ phần thị trường khu vực)
# ==============================================================================
def chart_12_donut(df):
    reg_sales = df.groupby("Region")["Total_Amount"].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    colors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2']
    
    wedges, texts, autotexts = ax.pie(
        reg_sales["Total_Amount"], 
        labels=reg_sales["Region"], 
        autopct='%1.1f%%',
        startangle=140, 
        colors=colors, 
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
        pctdistance=0.75,
        textprops=dict(fontsize=11)
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    total_rev = reg_sales["Total_Amount"].sum()
    ax.text(0, 0, f"Tổng Doanh Thu\n${total_rev:,.0f}", ha='center', va='center', fontsize=12, fontweight='bold', color='#333333')

    ax.set_title("12. Tỷ Phần Doanh Thu Theo Khu Vực Địa Lý (Donut Chart)", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "12_donut_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 13: TREEMAP (Bản đồ cây phân cấp)
# ==============================================================================
def chart_13_treemap(df):
    cat_sales = df.groupby("Category").agg({"Total_Amount": "sum", "Quantity": "sum"}).reset_index()
    cat_sales["Label"] = cat_sales.apply(lambda r: f"{r['Category']}\n${r['Total_Amount']:,.0f}\n({r['Quantity']} sp)", axis=1)

    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    colors = sns.color_palette("Spectral", len(cat_sales))
    
    squarify.plot(sizes=cat_sales["Total_Amount"], label=cat_sales["Label"], 
                  color=colors, alpha=0.85, edgecolor="white", linewidth=2.5,
                  text_kwargs={'fontsize': 11, 'weight': 'bold', 'color': '#222222'}, ax=ax)
    
    ax.set_title("13. Cơ Cấu Doanh Thu & Số Lượng Theo Danh Mục (Treemap)", fontsize=14, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "13_treemap.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 14: STACKED AREA CHART (Biểu đồ miền chồng - Tăng trưởng lũy kế)
# ==============================================================================
def chart_14_stacked_area(df):
    monthly_channel = df.groupby(["Order_Month", "Sales_Channel"])["Total_Amount"].sum().unstack().fillna(0)
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78']
    
    ax.stackplot(monthly_channel.index, monthly_channel.T, labels=monthly_channel.columns, colors=colors, alpha=0.85)

    ax.set_title("14. Tăng Trưởng Doanh Số Tích Lũy Qua Các Kênh Bán Hàng (Stacked Area)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Tháng Đặt Hàng", fontsize=11, labelpad=10)
    ax.set_ylabel("Tổng Doanh Thu Tích Lũy ($ USD)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.xticks(rotation=45)
    ax.legend(title="Kênh Bán", loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "14_stacked_area_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 15: RADAR / SPIDER CHART (Biểu đồ mạng nhện - Đánh giá đa chiều)
# ==============================================================================
def chart_15_radar(df):
    metrics = df.groupby("Sales_Channel").agg({
        "Total_Amount": "mean",
        "Profit": "mean",
        "Customer_Rating": "mean",
        "Marketing_Spend": "mean",
        "Quantity": "mean"
    })
    
    # Min-max scale metrics to 0-100 for standard radar comparison
    scaled = (metrics - metrics.min()) / (metrics.max() - metrics.min()) * 80 + 20
    labels = ["Doanh thu TB", "Lợi nhuận TB", "Đánh giá sao", "Chi phí Mkt", "Số lượng TB"]
    num_vars = len(labels)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True), dpi=300)
    
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
    for idx, (channel, row) in enumerate(scaled.iterrows()):
        values = row.values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, color=colors[idx], linewidth=2, label=channel)
        ax.fill(angles, values, color=colors[idx], alpha=0.15)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.set_title("15. Đánh Giá Toàn Diện Hiệu Suất Kênh Bán Hàng (Radar / Spider Chart)", fontsize=14, fontweight='bold', pad=25)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), title="Kênh Bán")
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "15_radar_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# CHART 16: PAIRPLOT (Ma trận biểu đồ cặp - Phân tích đa biến toàn diện)
# ==============================================================================
def chart_16_pairplot(df):
    subset_df = df[["Category", "Unit_Price", "Quantity", "Total_Amount", "Profit", "Customer_Rating"]]
    
    g = sns.pairplot(subset_df, hue="Category", palette="tab10", 
                     diag_kind="kde", plot_kws={'alpha': 0.6, 's': 25},
                     height=2.2, aspect=1.1)
    g.fig.suptitle("16. Ma Trận Tương Quan & Phân Phối Đa Biến (Pairplot)", y=1.02, fontsize=16, fontweight='bold')
    
    filepath = os.path.join(CHARTS_DIR, "16_pairplot.png")
    g.savefig(filepath, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"✅ Generated: {filepath}")
    return filepath

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
ALL_CHARTS = [
    ("01_line_chart", chart_01_line, "Biểu đồ đường (Line Chart)"),
    ("02_bar_chart", chart_02_bar, "Biểu đồ cột (Bar Chart)"),
    ("03_grouped_bar_chart", chart_03_grouped_bar, "Biểu đồ cột nhóm (Grouped Bar Chart)"),
    ("04_stacked_bar_chart", chart_04_stacked_bar, "Biểu đồ cột chồng (Stacked Bar Chart)"),
    ("05_histogram", chart_05_histogram, "Biểu đồ tần số (Histogram)"),
    ("06_kde_density_plot", chart_06_kde_density, "Biểu đồ mật độ xác suất (KDE Plot)"),
    ("07_box_plot", chart_07_box_plot, "Biểu đồ hộp phát hiện ngoại lai (Box Plot)"),
    ("08_violin_plot", chart_08_violin_plot, "Biểu đồ vĩ cầm (Violin Plot)"),
    ("09_scatter_plot", chart_09_scatter, "Biểu đồ phân tán & Hồi quy (Scatter Plot)"),
    ("10_bubble_chart", chart_10_bubble, "Biểu đồ bong bóng đa biến (Bubble Chart)"),
    ("11_heatmap_correlation", chart_11_heatmap, "Bản đồ nhiệt ma trận tương quan (Heatmap)"),
    ("12_donut_chart", chart_12_donut, "Biểu đồ tròn bánh Donut (Donut Chart)"),
    ("13_treemap", chart_13_treemap, "Bản đồ cây phân cấp (Treemap)"),
    ("14_stacked_area_chart", chart_14_stacked_area, "Biểu đồ miền chồng (Stacked Area Chart)"),
    ("15_radar_chart", chart_15_radar, "Biểu đồ mạng nhện (Radar / Spider Chart)"),
    ("16_pairplot", chart_16_pairplot, "Ma trận phân tích đa biến (Pairplot)")
]

if __name__ == "__main__":
    df = load_data()
    print("🚀 BẮT ĐẦU TẠO TOÀN BỘ 16 BIỂU ĐỒ CHUYÊN NGHIỆP...")
    for name, func, desc in ALL_CHARTS:
        print(f"-> Đang vẽ: {desc}...")
        func(df)
    print("✨ TẤT CẢ 16 BIỂU ĐỒ ĐÃ ĐƯỢC TẠO THÀNH CÔNG TRONG THƯ MỤC 'charts/'!")
