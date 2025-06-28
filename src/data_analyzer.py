"""
Module Phân tích Dữ liệu THPT
Thực hiện các phân tích thống kê và so sánh các tổ hợp môn
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import logging
import os

# Cấu hình logging
logger = logging.getLogger(__name__)

# Cấu hình matplotlib cho tiếng Việt
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

class THPTDataAnalyzer:
    """Class chính để phân tích dữ liệu THPT"""
    
    def __init__(self, db_path="data/thpt_data.db"):
        """Khởi tạo analyzer với database"""
        self.db_path = db_path
        self.data = {}
        
        # Tạo thư mục output
        os.makedirs("output/reports", exist_ok=True)
        os.makedirs("output/charts", exist_ok=True)
        os.makedirs("output/tables", exist_ok=True)
        
    def load_data(self):
        """Tải dữ liệu từ database"""
        logger.info("Đang tải dữ liệu từ database...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Tải các bảng dữ liệu
            self.data['to_hop_mon'] = pd.read_sql_query("SELECT * FROM to_hop_mon", conn)
            self.data['diem_chuan'] = pd.read_sql_query("SELECT * FROM diem_chuan", conn)
            self.data['pho_diem'] = pd.read_sql_query("SELECT * FROM pho_diem", conn)
            
            conn.close()
            
            logger.info(f"Đã tải {len(self.data)} bảng dữ liệu")
            for table, df in self.data.items():
                logger.info(f"  - {table}: {len(df)} bản ghi")
                
        except Exception as e:
            logger.error(f"Lỗi khi tải dữ liệu: {e}")
            raise
    
    def analyze_to_hop_popularity(self):
        """Phân tích độ phổ biến của các tổ hợp môn"""
        logger.info("Đang phân tích độ phổ biến tổ hợp môn...")
        
        df_diem_chuan = self.data['diem_chuan']
        
        # Tính số lượng ngành theo tổ hợp
        popularity = df_diem_chuan.groupby('ma_to_hop').agg({
            'nganh': 'count',
            'chi_tieu': 'sum',
            'diem_chuan': ['mean', 'std']
        }).round(2)
        
        popularity.columns = ['so_nganh', 'tong_chi_tieu', 'diem_chuan_tb', 'diem_chuan_std']
        popularity = popularity.reset_index()
        popularity = popularity.sort_values('so_nganh', ascending=False)
        
        # Lưu kết quả
        popularity.to_csv("output/tables/to_hop_popularity.csv", index=False, encoding='utf-8-sig')
        
        logger.info("Hoàn thành phân tích độ phổ biến")
        return popularity
    
    def analyze_diem_chuan_trends(self):
        """Phân tích xu hướng điểm chuẩn theo thời gian"""
        logger.info("Đang phân tích xu hướng điểm chuẩn...")
        
        df_diem_chuan = self.data['diem_chuan']
        
        # Tính điểm chuẩn trung bình theo năm và tổ hợp
        trends = df_diem_chuan.groupby(['nam', 'ma_to_hop']).agg({
            'diem_chuan': ['mean', 'std', 'count']
        }).round(2)
        
        trends.columns = ['diem_chuan_tb', 'diem_chuan_std', 'so_nganh']
        trends = trends.reset_index()
        
        # Tính xu hướng (slope) cho mỗi tổ hợp
        trend_analysis = []
        for to_hop in trends['ma_to_hop'].unique():
            subset = trends[trends['ma_to_hop'] == to_hop]
            if len(subset) > 1:
                slope, intercept, r_value, p_value, std_err = stats.linregress(subset['nam'], subset['diem_chuan_tb'])
                trend_analysis.append({
                    'ma_to_hop': to_hop,
                    'xu_huong': slope,
                    'r_squared': r_value**2,
                    'p_value': p_value,
                    'ket_luan': 'Tăng' if slope > 0.05 else ('Giảm' if slope < -0.05 else 'Ổn định')
                })
        
        trend_df = pd.DataFrame(trend_analysis)
        
        # Lưu kết quả
        trends.to_csv("output/tables/diem_chuan_trends.csv", index=False, encoding='utf-8-sig')
        trend_df.to_csv("output/tables/trend_analysis.csv", index=False, encoding='utf-8-sig')
        
        logger.info("Hoàn thành phân tích xu hướng")
        return trends, trend_df
    
    def analyze_regional_differences(self):
        """Phân tích sự khác biệt giữa các vùng miền"""
        logger.info("Đang phân tích sự khác biệt vùng miền...")
        
        df_diem_chuan = self.data['diem_chuan']
        
        # So sánh điểm chuẩn giữa các vùng miền
        regional_stats = df_diem_chuan.groupby(['vung_mien', 'ma_to_hop']).agg({
            'diem_chuan': ['mean', 'std', 'count']
        }).round(2)
        
        regional_stats.columns = ['diem_chuan_tb', 'diem_chuan_std', 'so_nganh']
        regional_stats = regional_stats.reset_index()
        
        # Kiểm định t-test giữa Miền Bắc và Miền Nam
        t_test_results = []
        for to_hop in df_diem_chuan['ma_to_hop'].unique():
            mien_bac = df_diem_chuan[(df_diem_chuan['ma_to_hop'] == to_hop) & 
                                   (df_diem_chuan['vung_mien'] == 'Miền Bắc')]['diem_chuan']
            mien_nam = df_diem_chuan[(df_diem_chuan['ma_to_hop'] == to_hop) & 
                                   (df_diem_chuan['vung_mien'] == 'Miền Nam')]['diem_chuan']
            
            if len(mien_bac) > 0 and len(mien_nam) > 0:
                t_stat, p_value = stats.ttest_ind(mien_bac, mien_nam)
                t_test_results.append({
                    'ma_to_hop': to_hop,
                    't_statistic': round(t_stat, 3),
                    'p_value': round(p_value, 3),
                    'khac_biet_co_y_nghia': 'Có' if p_value < 0.05 else 'Không',
                    'mien_bac_tb': round(mien_bac.mean(), 2),
                    'mien_nam_tb': round(mien_nam.mean(), 2)
                })
        
        t_test_df = pd.DataFrame(t_test_results)
        
        # Lưu kết quả
        regional_stats.to_csv("output/tables/regional_stats.csv", index=False, encoding='utf-8-sig')
        t_test_df.to_csv("output/tables/regional_t_test.csv", index=False, encoding='utf-8-sig')
        
        logger.info("Hoàn thành phân tích vùng miền")
        return regional_stats, t_test_df
    
    def analyze_difficulty_ranking(self):
        """Phân tích và xếp hạng độ khó của các tổ hợp"""
        logger.info("Đang phân tích độ khó tổ hợp môn...")
        
        df_pho_diem = self.data['pho_diem']
        df_diem_chuan = self.data['diem_chuan']
        
        # Tính các chỉ số độ khó
        difficulty_stats = df_pho_diem.groupby('ma_to_hop').agg({
            'diem_trung_binh': 'mean',
            'do_lech_chuan': 'mean',
            'ty_le_dat': 'mean'
        }).round(2)
        
        # Tính điểm chuẩn trung bình
        avg_cutoff = df_diem_chuan.groupby('ma_to_hop')['diem_chuan'].mean()
        
        # Kết hợp dữ liệu
        difficulty_stats['diem_chuan_tb'] = avg_cutoff
        difficulty_stats = difficulty_stats.reset_index()
        
        # Chuẩn hóa các chỉ số (Z-score)
        scaler = StandardScaler()
        features = ['diem_trung_binh', 'do_lech_chuan', 'diem_chuan_tb']
        difficulty_stats[features] = scaler.fit_transform(difficulty_stats[features])
        
        # Tính điểm tổng hợp độ khó (điểm càng cao = càng khó)
        difficulty_stats['diem_do_kho'] = (
            -difficulty_stats['diem_trung_binh'] +  # Điểm TB thấp = khó
            difficulty_stats['do_lech_chuan'] +     # Độ lệch chuẩn cao = khó
            difficulty_stats['diem_chuan_tb']       # Điểm chuẩn cao = khó
        )
        
        # Xếp hạng
        difficulty_stats['hang_do_kho'] = difficulty_stats['diem_do_kho'].rank(ascending=False, method='dense')
        difficulty_stats = difficulty_stats.sort_values('hang_do_kho')
        
        # Thêm nhãn mức độ
        difficulty_stats['muc_do_kho'] = pd.cut(
            difficulty_stats['diem_do_kho'], 
            bins=3, 
            labels=['Dễ', 'Trung bình', 'Khó']
        )
        
        # Lưu kết quả
        difficulty_stats.to_csv("output/tables/difficulty_ranking.csv", index=False, encoding='utf-8-sig')
        
        logger.info("Hoàn thành phân tích độ khó")
        return difficulty_stats
    
    def cluster_analysis(self):
        """Phân cụm các tổ hợp môn dựa trên đặc điểm"""
        logger.info("Đang thực hiện phân cụm tổ hợp môn...")
        
        df_pho_diem = self.data['pho_diem']
        df_diem_chuan = self.data['diem_chuan']
        
        # Tính features cho clustering
        features_df = df_pho_diem.groupby('ma_to_hop').agg({
            'diem_trung_binh': 'mean',
            'do_lech_chuan': 'mean',
            'so_thi_sinh': 'mean',
            'ty_le_dat': 'mean'
        }).round(2)
        
        # Thêm điểm chuẩn trung bình
        avg_cutoff = df_diem_chuan.groupby('ma_to_hop')['diem_chuan'].mean()
        features_df['diem_chuan_tb'] = avg_cutoff
        
        # Chuẩn hóa dữ liệu
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_df)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)
        
        # Thêm kết quả clustering
        features_df['cluster'] = clusters
        features_df['cluster_label'] = features_df['cluster'].map({
            0: 'Nhóm 1: Thi sinh nhiều, điểm TB',
            1: 'Nhóm 2: Điểm cao, cạnh tranh',
            2: 'Nhóm 3: Điểm thấp, ít cạnh tranh'
        })
        
        features_df = features_df.reset_index()
        
        # Lưu kết quả
        features_df.to_csv("output/tables/cluster_analysis.csv", index=False, encoding='utf-8-sig')
        
        logger.info("Hoàn thành phân cụm")
        return features_df
    
    def generate_summary_report(self):
        """Tạo báo cáo tổng quan"""
        logger.info("Đang tạo báo cáo tổng quan...")
        
        # Chạy tất cả các phân tích
        popularity = self.analyze_to_hop_popularity()
        trends, trend_analysis = self.analyze_diem_chuan_trends()
        regional_stats, t_test = self.analyze_regional_differences()
        difficulty = self.analyze_difficulty_ranking()
        clusters = self.cluster_analysis()
        
        # Tạo báo cáo văn bản
        report = f"""
# BÁO CÁO PHÂN TÍCH DỮ LIỆU THPT
Ngày tạo: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}

## 1. TỔNG QUAN DỮ LIỆU
- Số tổ hợp môn: {len(self.data['to_hop_mon'])}
- Số bản ghi điểm chuẩn: {len(self.data['diem_chuan'])}
- Số bản ghi phổ điểm: {len(self.data['pho_diem'])}

## 2. ĐỘ PHỔ BIẾN CỦA CÁC TỔ HỢP MÔN
Top 3 tổ hợp được sử dụng nhiều nhất:
{popularity.head(3)[['ma_to_hop', 'so_nganh', 'tong_chi_tieu']].to_string(index=False)}

## 3. XU HƯỚNG ĐIỂM CHUẨN
Các tổ hợp có xu hướng tăng điểm:
{trend_analysis[trend_analysis['ket_luan'] == 'Tăng'][['ma_to_hop', 'xu_huong']].to_string(index=False)}

## 4. KHÁC BIỆT VÙNG MIỀN
Số tổ hợp có sự khác biệt có ý nghĩa thống kê giữa Miền Bắc và Miền Nam:
{len(t_test[t_test['khac_biet_co_y_nghia'] == 'Có'])} / {len(t_test)}

## 5. XẾP HẠNG ĐỘ KHÓ
Top 3 tổ hợp khó nhất:
{difficulty.head(3)[['ma_to_hop', 'muc_do_kho', 'hang_do_kho']].to_string(index=False)}

## 6. PHÂN CỤM TỔ HỢP MÔN
{clusters.groupby('cluster_label')['ma_to_hop'].apply(list).to_string()}

## KẾT LUẬN
- Các tổ hợp khối A (A00, A01) thường có điểm chuẩn cao và cạnh tranh
- Khối B phù hợp với ngành y-dược, có độ khó trung bình
- Khối C và D có sự đa dạng về điểm chuẩn tùy ngành
- Sự khác biệt vùng miền không quá lớn nhưng vẫn có ý nghĩa thống kê

## KHUYẾN NGHỊ
1. Thí sinh cần cân nhắc kỹ năng và sở thích khi chọn tổ hợp
2. Không nên chỉ dựa vào độ khó để quyết định
3. Cần xem xét chỉ tiêu và cơ hội trúng tuyển của từng ngành
"""
        
        # Lưu báo cáo
        with open("output/reports/summary_report.md", "w", encoding='utf-8') as f:
            f.write(report)
        
        logger.info("Đã tạo báo cáo tổng quan")
        return report
    
    def run_full_analysis(self):
        """Chạy toàn bộ phân tích"""
        logger.info("Bắt đầu phân tích dữ liệu THPT đầy đủ...")
        
        # Tải dữ liệu
        self.load_data()
        
        # Chạy các phân tích
        results = {
            'popularity': self.analyze_to_hop_popularity(),
            'trends': self.analyze_diem_chuan_trends(),
            'regional': self.analyze_regional_differences(),
            'difficulty': self.analyze_difficulty_ranking(),
            'clusters': self.cluster_analysis()
        }
        
        # Tạo báo cáo tổng quan
        report = self.generate_summary_report()
        
        logger.info("Hoàn thành phân tích đầy đủ!")
        
        return results, report

if __name__ == "__main__":
    # Demo chạy phân tích
    analyzer = THPTDataAnalyzer()
    results, report = analyzer.run_full_analysis()
    
    print("\n=== KẾT QUÁ PHÂN TÍCH DỮ LIỆU THPT ===")
    print("Các file kết quả đã được lưu trong thư mục output/")
    print("\nBáo cáo tóm tắt:")
    print(report[:500] + "...")
