#!/usr/bin/env python3
"""
Setup script for THPT Analysis 2025
Chuẩn bị môi trường để chạy notebook và phân tích
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_requirements():
    """Cài đặt các dependencies cần thiết"""
    print("📦 Cài đặt dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Đã cài đặt thành công dependencies!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt dependencies: {e}")
        return False
    
    return True

def create_directories():
    """Tạo các thư mục cần thiết"""
    print("📁 Tạo thư mục...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "output/tables",
        "output/charts",
        "output/reports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("✅ Đã tạo tất cả thư mục!")

def check_python_version():
    """Kiểm tra phiên bản Python"""
    print("🐍 Kiểm tra phiên bản Python...")
    
    if sys.version_info < (3, 9):
        print("❌ Cần Python 3.9 trở lên!")
        print(f"   Phiên bản hiện tại: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} OK!")
    return True

def run_initial_analysis():
    """Chạy phân tích ban đầu để tạo dữ liệu mẫu"""
    print("🚀 Chạy phân tích ban đầu...")
    
    try:
        # Chạy scraper để tạo dữ liệu mẫu
        from src.data_scraper import THPTDataScraper
        scraper = THPTDataScraper()
        data = scraper.run_full_scrape(year_range=(2020, 2024))
        print("✅ Đã tạo dữ liệu mẫu!")
        
        # Chạy analyzer để tạo kết quả phân tích
        from src.data_analyzer import THPTDataAnalyzer
        analyzer = THPTDataAnalyzer()
        results, report = analyzer.run_full_analysis()
        print("✅ Đã tạo kết quả phân tích!")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi chạy phân tích: {e}")
        print("💡 Bạn có thể chạy thủ công: python src/main.py --mode full")
        return False

def open_jupyter():
    """Mở Jupyter Notebook"""
    print("📓 Mở Jupyter Notebook...")
    
    notebook_path = "notebooks/thpt_analysis_demo.ipynb"
    
    try:
        subprocess.Popen([
            sys.executable, "-m", "jupyter", "notebook", 
            notebook_path, "--no-browser"
        ])
        print("✅ Jupyter Notebook đã được khởi động!")
        print("🌐 Mở browser và truy cập: http://localhost:8888")
        
    except Exception as e:
        print(f"❌ Lỗi khi mở Jupyter: {e}")
        print("💡 Chạy thủ công: jupyter notebook")

def main():
    """Hàm chính"""
    parser = argparse.ArgumentParser(description="Setup THPT Analysis 2025")
    parser.add_argument("--skip-install", action="store_true", 
                       help="Bỏ qua cài đặt dependencies")
    parser.add_argument("--skip-analysis", action="store_true", 
                       help="Bỏ qua phân tích ban đầu")
    parser.add_argument("--no-jupyter", action="store_true", 
                       help="Không mở Jupyter Notebook")
    
    args = parser.parse_args()
    
    print("🎓 THPT Analysis 2025 - Setup")
    print("=" * 40)
    
    # Kiểm tra Python version
    if not check_python_version():
        sys.exit(1)
    
    # Tạo thư mục
    create_directories()
    
    # Cài đặt dependencies
    if not args.skip_install:
        if not install_requirements():
            sys.exit(1)
    else:
        print("⏭️ Bỏ qua cài đặt dependencies")
    
    # Chạy phân tích ban đầu
    if not args.skip_analysis:
        run_initial_analysis()
    else:
        print("⏭️ Bỏ qua phân tích ban đầu")
    
    # Mở Jupyter
    if not args.no_jupyter:
        open_jupyter()
    else:
        print("⏭️ Không mở Jupyter Notebook")
    
    print("\n🎉 Setup hoàn thành!")
    print("\n📋 Các bước tiếp theo:")
    print("   1. Mở http://localhost:8888 trong browser")
    print("   2. Chạy notebook: notebooks/thpt_analysis_demo.ipynb")
    print("   3. Hoặc chạy CLI: python src/main.py --mode full")
    print("\n📚 Tài liệu: https://github.com/Noiceboi/THPT_ANALYSIS_2025")

if __name__ == "__main__":
    main()
