# 🎓 THPT Analysis 2025 - Nghiên cứu So sánh các Tổ hợp Môn

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-green.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

## 🌟 Demo Live
👉 **[Xem Demo trực tiếp tại GitHub Pages](https://noiceboi.github.io/THPT_ANALYSIS_2025/)**

## 📊 Tổng quan Dự án

Dự án nghiên cứu **so sánh chuyên sâu các tổ hợp môn** trong kỳ thi THPT quốc gia từ 2018-2024, sử dụng các phương pháp thống kê và machine learning để phân tích:

- 📈 **Độ phổ biến và xu hướng** của 8 tổ hợp môn chính
- 🎯 **Xếp hạng độ khó** dựa trên multiple metrics  
- 🗺️ **So sánh vùng miền** với kiểm định thống kê
- 🔗 **Phân cụm tổ hợp** theo đặc điểm tương tự
- 📊 **Dashboard tương tác** với Plotly

### 🎯 Kết quả Chính

| Tổ hợp | Độ phổ biến | Xu hướng | Độ khó | Nhóm |
|--------|-------------|----------|---------|------|
| **A01** | 🥇 #1 (36 ngành) | ↘️ Giảm | 🔴 Khó | Cạnh tranh cao |
| **A00** | 🥉 #3 (29 ngành) | ↗️ Tăng mạnh | 🟡 TB | Kỹ thuật |
| **B00** | #5 (24 ngành) | ↘️ Giảm mạnh nhất | 🔴 Khó nhất | Y-Dược |
| **D01** | #4 (28 ngành) | ↗️ Tăng | 🟢 Dễ | Kinh tế |

## Cấu trúc dự án

```
THPT_Analysis_Project/
├── src/                    # Mã nguồn chính
│   ├── data_scraper.py     # Thu thập dữ liệu
│   ├── data_analyzer.py    # Phân tích dữ liệu
│   ├── visualizer.py       # Tạo biểu đồ
│   └── main.py            # File chính
├── data/                   # Dữ liệu thu thập
│   ├── raw/               # Dữ liệu thô
│   ├── processed/         # Dữ liệu đã xử lý
│   └── thpt_data.db      # Database SQLite
├── output/                # Kết quả phân tích
│   ├── reports/          # Báo cáo
│   ├── charts/           # Biểu đồ
│   └── tables/           # Bảng số liệu
├── config/                # Cấu hình
│   └── settings.json     # Thiết lập
├── notebooks/             # Jupyter notebooks
│   └── analysis.ipynb    # Notebook phân tích
└── scripts/               # Scripts tiện ích
    └── setup.py          # Script cài đặt
```

## Cài đặt

```bash
# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Cấu hình Python environment
python scripts/setup.py
```

## Sử dụng

```bash
# Chạy thu thập dữ liệu
python src/main.py --mode scrape --years 2018-2024

# Chạy phân tích
python src/main.py --mode analyze

# Tạo báo cáo
python src/main.py --mode report
```

## Các tiêu chí nghiên cứu

### 1. Nguồn dữ liệu
- **Chính thức**: Bộ GD-ĐT, cổng thông tin tuyển sinh
- **Phụ trợ**: Báo chí, trang web các trường ĐH
- **Dữ liệu mở**: Open Data Chính phủ

### 2. Biến phân tích
- `year`: Năm thi
- `block_code`: Mã tổ hợp (A00, A01, B00, C00, D01...)
- `subjects`: Danh sách môn thi
- `avg_score`: Điểm trung bình
- `std_dev`: Độ lệch chuẩn
- `cutoff_score`: Điểm chuẩn
- `applicants`: Số thí sinh đăng ký
- `quota`: Chỉ tiêu tuyển sinh
- `region`: Vùng miền
- `gender_ratio`: Tỷ lệ giới tính

### 3. Phương pháp phân tích
- **Thống kê mô tả**: Mean, median, std, percentiles
- **Kiểm định**: t-test, ANOVA, chi-square
- **Hồi quy**: Linear regression, time series
- **Trực quan hóa**: Matplotlib, Plotly, Seaborn

### 4. Tiêu chí so sánh
- **Theo thời gian**: Xu hướng 2018-2024
- **Theo ngành**: Kỹ thuật, Kinh tế, Y-Dược, Sư phạm
- **Theo địa lý**: Bắc-Trung-Nam, thành thị-nông thôn
- **Theo độ khó**: Phân tích độ lệch chuẩn, tính phân hóa

## Kết quả mong đợi

1. **Báo cáo tổng quan** về bức tranh các tổ hợp môn THPT
2. **Khuyến nghị** cho thí sinh trong việc chọn tổ hợp
3. **Dự báo xu hướng** cho các năm tới
4. **Dataset hoàn chỉnh** để nghiên cứu tiếp

## Tác giả

Dự án nghiên cứu THPT - 2025
