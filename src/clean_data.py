"""
Module: clean_data.py
Mô tả: Pipeline làm sạch dữ liệu toàn diện với Pandas, xử lý triệt để tất cả các loại lỗi
(Missing values, Duplicates, Typo/Casing, Mixed Data Types, Outliers, Sentinel values, Logic anomalies)
và tạo các cột phái sinh (Feature Engineering) phục vụ trực quan hóa biểu đồ.
"""

import os
import sys
import re
import numpy as np
import pandas as pd

# Fix Windows console utf-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def clean_ecommerce_data(raw_csv_path="data/raw_data.csv", cleaned_csv_path="data/cleaned_data.csv"):
    print("=" * 60)
    print("🚀 BẮT ĐẦU QUY TRÌNH LÀM SẠCH DỮ LIỆU VỚI PANDAS")
    print("=" * 60)

    # 1. ĐỌC DỮ LIỆU THÔ
    df = pd.read_csv(raw_csv_path)
    initial_rows = len(df)
    print(f"📊 Dữ liệu thô ban đầu: {initial_rows} dòng, {len(df.columns)} cột.")
    print("Các cột:", list(df.columns))
    
    # 2. XỬ LÝ TRÙNG LẶP (DUPLICATES)
    # Loại bỏ exact duplicates
    exact_dups = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"\n[Bước 1] Loại bỏ {exact_dups} dòng trùng lặp hoàn toàn (Exact Duplicates).")

    # Xử lý duplicate Order_ID (chỉ giữ lại bản ghi đầu tiên hợp lệ)
    order_dups = df.duplicated(subset=["Order_ID"]).sum()
    df = df.drop_duplicates(subset=["Order_ID"], keep="first").reset_index(drop=True)
    print(f"[Bước 2] Loại bỏ {order_dups} dòng trùng lặp Order_ID.")

    # 3. CHUẨN HÓA VĂN BẢN & XỬ LÝ PLACEHOLDERS (TEXT CLEANING)
    # Định nghĩa các placeholder biểu thị missing value
    null_placeholders = ["N/A", "Unknown", "unknown", "?", "-", "missing", "nan", "None", "", "   "]
    
    # Chuẩn hóa cột Category
    df["Category"] = df["Category"].replace(null_placeholders, np.nan)
    df["Category"] = df["Category"].astype(str).str.strip().str.title()
    df["Category"] = df["Category"].replace({"Nan": np.nan, "Electrnics": "Electronics"})
    
    # Suy luận Category bị thiếu dựa trên Product_Name nếu có
    prod_cat_map = {
        "Smartphone X": "Electronics", "Wireless Headphones": "Electronics",
        "Smart Watch": "Electronics", "Laptop Pro": "Electronics", "Bluetooth Speaker": "Electronics",
        "Men T-Shirt": "Fashion", "Women Dress": "Fashion", "Denim Jeans": "Fashion",
        "Running Shoes": "Fashion", "Leather Jacket": "Fashion",
        "Air Fryer": "Home & Kitchen", "Blender 500W": "Home & Kitchen",
        "Non-Stick Pan": "Home & Kitchen", "Coffee Maker": "Home & Kitchen", "Robot Vacuum": "Home & Kitchen",
        "Face Sunscreen": "Beauty & Care", "Moisturizer Cream": "Beauty & Care",
        "Hair Dryer": "Beauty & Care", "Lipstick Matte": "Beauty & Care", "Perfume 50Ml": "Beauty & Care",
        "Yoga Mat": "Sports & Outdoors", "Dumbbell Set": "Sports & Outdoors",
        "Water Bottle": "Sports & Outdoors", "Bicycle Helmet": "Sports & Outdoors", "Camping Tent": "Sports & Outdoors",
        "Data Science Handbook": "Books", "Python Cookbook": "Books",
        "Business Strategy": "Books", "Psychology Of Money": "Books", "Atomic Habits": "Books"
    }
    
    # Chuẩn hóa Product_Name
    df["Product_Name"] = df["Product_Name"].astype(str).str.strip().str.title()
    
    # Điền Category bị khuyết bằng Mapping từ Product_Name
    inferred_cat = df["Product_Name"].map(prod_cat_map)
    df["Category"] = df["Category"].fillna(inferred_cat)
    # Nếu vẫn còn khuyết, điền bằng Mode của Category
    mode_cat = df["Category"].mode()[0]
    df["Category"] = df["Category"].fillna(mode_cat)
    print(f"[Bước 3] Chuẩn hóa Category & Product_Name (Xóa khoảng trắng, sửa lỗi chính tả, map danh mục thiếu).")

    # Chuẩn hóa cột Region
    df["Region"] = df["Region"].replace(null_placeholders, np.nan)
    df["Region"] = df["Region"].astype(str).str.strip().str.title()
    region_mapping = {
        "Vn-North": "North", "North": "North",
        "Vn-South": "South", "South": "South",
        "Vn-Central": "Central", "Central": "Central",
        "Intl": "International", "Overseas": "International", "Global": "International",
        "Nan": np.nan
    }
    df["Region"] = df["Region"].map(region_mapping)
    mode_region = df["Region"].mode()[0]
    df["Region"] = df["Region"].fillna(mode_region)
    print(f"[Bước 4] Chuẩn hóa Region (Đồng nhất tên gọi North/South/Central/International).")

    # 4. CHUYỂN ĐỔI KIỂU DỮ LIỆU & LÀM SẠCH SỐ LIỆU (TYPE CASTING & REGEX)
    # Chuyển đổi Unit_Price từ chuỗi "$1,250.00" / "45.50 USD" sang số thực float
    df["Unit_Price"] = (
        df["Unit_Price"]
        .astype(str)
        .str.replace(r"[^\d.]", "", regex=True) # Chỉ giữ lại chữ số và dấu chấm thập phân
    )
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    # Điền giá thiếu (nếu có) bằng median theo Category
    df["Unit_Price"] = df.groupby("Category")["Unit_Price"].transform(lambda x: x.fillna(x.median()))
    print(f"[Bước 5] Làm sạch Unit_Price: Chuyển chuỗi tiền tệ ký tự đặc biệt ($ , USD) thành Float.")

    # 5. XỬ LÝ DATE TIME VỚI NHIỀU ĐỊNH DẠNG HỖN HỢP
    # Sử dụng pd.to_datetime với format='mixed'
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce", format="mixed")
    # Với các date bị lỗi (NaT), điền bằng ngày gần nhất hoặc median date
    valid_dates = df["Order_Date"].dropna()
    median_date = valid_dates.iloc[len(valid_dates) // 2]
    df["Order_Date"] = df["Order_Date"].fillna(median_date)
    print(f"[Bước 6] Chuẩn hóa Order_Date: Parse đa định dạng (YYYY-MM-DD, DD/MM/YYYY, Mon DD, YYYY) sang chuẩn datetime.")

    # 6. XỬ LÝ OUTLIERS & SENTINEL VALUES (GIÁ TRỊ NGOẠI LAI & PHI LÝ)
    # A. Customer_Age: loại bỏ sentinel (-999, <= 0, > 100) -> điền bằng median tuổi
    median_age = df.loc[(df["Customer_Age"] > 10) & (df["Customer_Age"] < 100), "Customer_Age"].median()
    df.loc[(df["Customer_Age"] <= 0) | (df["Customer_Age"] > 100) | (df["Customer_Age"].isna()), "Customer_Age"] = median_age
    df["Customer_Age"] = df["Customer_Age"].astype(int)

    # B. Quantity: loại bỏ <= 0 hoặc > 50 -> điền bằng median (hoặc 1)
    df.loc[(df["Quantity"] <= 0) | (df["Quantity"] > 20) | (df["Quantity"].isna()), "Quantity"] = 1
    df["Quantity"] = df["Quantity"].astype(int)

    # C. Customer_Rating: giới hạn từ 1.0 đến 5.0
    mean_rating = df.loc[(df["Customer_Rating"] >= 1.0) & (df["Customer_Rating"] <= 5.0), "Customer_Rating"].mean()
    df.loc[(df["Customer_Rating"] < 1.0) | (df["Customer_Rating"] > 5.0) | (df["Customer_Rating"].isna()), "Customer_Rating"] = round(mean_rating, 1)

    # D. Marketing_Spend: đảm bảo không âm
    df["Marketing_Spend"] = df["Marketing_Spend"].clip(lower=5.0)
    print(f"[Bước 7] Xử lý Outliers & Sentinel Values cho Age, Quantity, Rating, Marketing Spend.")

    # 7. FEATURE ENGINEERING (TẠO BIẾN PHÂN TÍCH MỚI)
    # Tổng tiền = Đơn giá * Số lượng
    df["Total_Amount"] = round(df["Unit_Price"] * df["Quantity"], 2)

    # Tỷ suất lợi nhuận giả định theo Category
    profit_margin_map = {
        "Electronics": 0.18,
        "Fashion": 0.35,
        "Home & Kitchen": 0.28,
        "Beauty & Care": 0.42,
        "Sports & Outdoors": 0.30,
        "Books": 0.25
    }
    df["Profit_Margin"] = df["Category"].map(profit_margin_map).fillna(0.25)
    df["Profit"] = round(df["Total_Amount"] * df["Profit_Margin"], 2)

    # Trích xuất thời gian: Năm-Tháng, Quý, Thứ trong tuần
    df["Order_Year"] = df["Order_Date"].dt.year
    df["Order_Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    df["Order_Quarter"] = df["Order_Date"].dt.to_period("Q").astype(str)
    df["Day_Of_Week"] = df["Order_Date"].dt.day_name()

    # Nhóm tuổi khách hàng (Age Groups)
    bins = [0, 25, 35, 50, 100]
    labels = ["Gen Z (<25)", "Young Adults (25-34)", "Middle-Aged (35-49)", "Seniors (50+)"]
    df["Age_Group"] = pd.cut(df["Customer_Age"], bins=bins, labels=labels, right=False)
    
    print(f"[Bước 8] Feature Engineering: Tạo Total_Amount, Profit, Order_Month, Quarter, Day_Of_Week, Age_Group.")

    # Sắp xếp lại dữ liệu theo ngày
    df = df.sort_values("Order_Date").reset_index(drop=True)

    # 8. XUẤT DỮ LIỆU ĐÃ LÀM SẠCH
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)
    df.to_csv(cleaned_csv_path, index=False, encoding="utf-8")
    
    print("=" * 60)
    print(f"✨ HOÀN TẤT LÀM SẠCH: {len(df)} dòng dữ liệu sạch sẵn sàng phân tích.")
    print(f"📁 Lưu tại: {cleaned_csv_path}")
    print(f"Kiểm tra khuyết thiếu sau khi clean: {df.isna().sum().sum()} nulls.")
    print("=" * 60)
    return df

if __name__ == "__main__":
    clean_ecommerce_data()
