#!/usr/bin/env python3
"""
MAIN - Hệ thống Thu thập và Phân tích Dữ liệu THPT
Điều phối các module thu thập, phân tích và tạo báo cáo

Sử dụng:
    python src/main.py --mode scrape --years 2020-2024
    python src/main.py --mode analyze
    python src/main.py --mode report
    python src/main.py --mode full
"""

import argparse
import logging
import sys
import os
from datetime import datetime

# Import các module
from data_scraper import THPTDataScraper
from data_analyzer import THPTDataAnalyzer

# Cấu hình logging
def setup_logging():
    """Cấu hình logging cho toàn bộ hệ thống"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Tạo thư mục logs
    os.makedirs("logs", exist_ok=True)
    
    # Cấu hình file log
    log_filename = f"logs/thpt_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Khởi động hệ thống THPT Analysis")
    logger.info(f"Log file: {log_filename}")
    
    return logger

def parse_arguments():
    """Phân tích tham số dòng lệnh"""
    parser = argparse.ArgumentParser(
        description="Hệ thống Thu thập và Phân tích Dữ liệu THPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python src/main.py --mode scrape --years 2020-2024
  python src/main.py --mode analyze  
  python src/main.py --mode report
  python src/main.py --mode full --years 2018-2024
  python src/main.py --mode visualize --charts all
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['scrape', 'analyze', 'report', 'visualize', 'full'],
        required=True,
        help='Chế độ hoạt động của hệ thống'
    )
    
    parser.add_argument(
        '--years',
        type=str,
        default='2020-2024',
        help='Khoảng năm thu thập dữ liệu (format: 2020-2024)'
    )
    
    parser.add_argument(
        '--charts',
        type=str,
        choices=['trends', 'comparison', 'distribution', 'all'],
        default='all',
        help='Loại biểu đồ cần tạo'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='output',
        help='Thư mục đầu ra'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/settings.json',
        help='File cấu hình'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Hiển thị thông tin chi tiết'
    )
    
    return parser.parse_args()

def parse_year_range(year_str):
    """Phân tích chuỗi năm thành tuple"""
    try:
        if '-' in year_str:
            start, end = map(int, year_str.split('-'))
            return (start, end)
        else:
            year = int(year_str)
            return (year, year)
    except ValueError:
        raise ValueError(f"Format năm không hợp lệ: {year_str}. Sử dụng format: 2020-2024 hoặc 2024")

def run_scrape_mode(args, logger):
    """Chạy chế độ thu thập dữ liệu"""
    logger.info("=== CHẠY CHỂ ĐỘ THU THẬP DỮ LIỆU ===")
    
    year_range = parse_year_range(args.years)
    logger.info(f"Thu thập dữ liệu từ năm {year_range[0]} đến {year_range[1]}")
    
    # Khởi tạo scraper
    scraper = THPTDataScraper()
    
    # Thu thập dữ liệu
    data = scraper.run_full_scrape(year_range=year_range)
    
    # In kết quả
    print(f"\n✅ Hoàn thành thu thập dữ liệu!")
    print(f"📊 Tổ hợp môn: {len(data['to_hop_mon'])} bản ghi")
    print(f"📈 Điểm chuẩn: {len(data['diem_chuan'])} bản ghi")
    print(f"📉 Phổ điểm: {len(data['pho_diem'])} bản ghi")
    print(f"💾 Dữ liệu đã lưu trong thư mục data/")
    
    return data

def run_analyze_mode(args, logger):
    """Chạy chế độ phân tích dữ liệu"""
    logger.info("=== CHẠY CHỂ ĐỘ PHÂN TÍCH DỮ LIỆU ===")
    
    # Kiểm tra file database
    db_path = "data/thpt_data.db"
    if not os.path.exists(db_path):
        logger.error(f"Không tìm thấy file database: {db_path}")
        print("❌ Lỗi: Chưa có dữ liệu để phân tích!")
        print("💡 Chạy lệnh: python src/main.py --mode scrape trước")
        return None
    
    # Khởi tạo analyzer
    analyzer = THPTDataAnalyzer(db_path=db_path)
    
    # Chạy phân tích
    results, report = analyzer.run_full_analysis()
    
    # In kết quả
    print(f"\n✅ Hoàn thành phân tích dữ liệu!")
    print(f"📋 Số phân tích: {len(results)}")
    print(f"📁 Kết quả lưu trong: output/")
    print(f"📑 Báo cáo tổng quan: output/reports/summary_report.md")
    
    return results, report

def run_report_mode(args, logger):
    """Chạy chế độ tạo báo cáo chi tiết"""
    logger.info("=== CHẠY CHỂ ĐỘ TẠO BÁO CÁO ===")
    
    # Kiểm tra các file phân tích
    required_files = [
        "output/tables/to_hop_popularity.csv",
        "output/tables/diem_chuan_trends.csv",
        "output/tables/difficulty_ranking.csv"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        logger.error(f"Thiếu file phân tích: {missing_files}")
        print("❌ Lỗi: Chưa có kết quả phân tích!")
        print("💡 Chạy lệnh: python src/main.py --mode analyze trước")
        return None
    
    # Tạo báo cáo chi tiết
    logger.info("Tạo báo cáo chi tiết...")
    
    # Đọc các file kết quả
    import pandas as pd
    
    popularity = pd.read_csv("output/tables/to_hop_popularity.csv")
    trends = pd.read_csv("output/tables/diem_chuan_trends.csv")
    difficulty = pd.read_csv("output/tables/difficulty_ranking.csv")
    
    # Tạo báo cáo HTML
    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Báo cáo Phân tích THPT</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .highlight {{ background-color: #fff3cd; }}
        </style>
    </head>
    <body>
        <h1>📊 Báo cáo Phân tích Dữ liệu THPT</h1>
        <p><strong>Ngày tạo:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        
        <h2>🎯 Độ phổ biến tổ hợp môn</h2>
        {popularity.to_html(index=False, table_id="popularity")}
        
        <h2>📈 Xếp hạng độ khó</h2>
        {difficulty[['ma_to_hop', 'muc_do_kho', 'hang_do_kho']].to_html(index=False, table_id="difficulty")}
        
        <h2>🔍 Phân tích chi tiết</h2>
        <p>Các file phân tích chi tiết đã được lưu trong thư mục <code>output/tables/</code></p>
        
        <hr>
        <p><em>Báo cáo được tạo bởi THPT Analysis System</em></p>
    </body>
    </html>
    """
    
    # Lưu báo cáo HTML
    with open("output/reports/detailed_report.html", "w", encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"\n✅ Hoàn thành tạo báo cáo!")
    print(f"📄 Báo cáo HTML: output/reports/detailed_report.html")
    print(f"📋 Báo cáo Markdown: output/reports/summary_report.md")
    
    return html_report

def run_full_mode(args, logger):
    """Chạy toàn bộ quy trình"""
    logger.info("=== CHẠY QUY TRÌNH ĐẦY ĐỦ ===")
    
    print("🚀 Bắt đầu quy trình phân tích THPT đầy đủ...")
    
    # 1. Thu thập dữ liệu
    print("\n📥 Bước 1: Thu thập dữ liệu")
    data = run_scrape_mode(args, logger)
    
    # 2. Phân tích dữ liệu  
    print("\n🔍 Bước 2: Phân tích dữ liệu")
    results, report = run_analyze_mode(args, logger)
    
    # 3. Tạo báo cáo
    print("\n📊 Bước 3: Tạo báo cáo")
    html_report = run_report_mode(args, logger)
    
    print(f"\n🎉 Hoàn thành toàn bộ quy trình!")
    print(f"📁 Tất cả kết quả trong thư mục: output/")
    
    return {
        'data': data,
        'analysis': results,
        'reports': {
            'markdown': report,
            'html': html_report
        }
    }

def main():
    """Hàm chính"""
    # Cấu hình logging
    logger = setup_logging()
    
    try:
        # Phân tích tham số
        args = parse_arguments()
        
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        logger.info(f"Chế độ: {args.mode}")
        logger.info(f"Tham số: {vars(args)}")
        
        # Chạy theo chế độ
        if args.mode == 'scrape':
            result = run_scrape_mode(args, logger)
            
        elif args.mode == 'analyze':
            result = run_analyze_mode(args, logger)
            
        elif args.mode == 'report':
            result = run_report_mode(args, logger)
            
        elif args.mode == 'full':
            result = run_full_mode(args, logger)
            
        else:
            logger.error(f"Chế độ không hợp lệ: {args.mode}")
            return 1
        
        if result is None:
            logger.error("Thực thi thất bại")
            return 1
        
        logger.info("Thực thi thành công")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Người dùng dừng chương trình")
        return 1
        
    except Exception as e:
        logger.error(f"Lỗi không mong muốn: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
