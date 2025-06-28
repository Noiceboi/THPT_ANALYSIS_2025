# 🤝 Contributing to THPT Analysis 2025

Chúng tôi rất hoan nghênh mọi đóng góp để cải thiện dự án! Đây là hướng dẫn chi tiết về cách bạn có thể đóng góp.

## 📋 Các cách đóng góp

### 🐛 Báo cáo Bug
- Kiểm tra [Issues](https://github.com/Noiceboi/THPT_ANALYSIS_2025/issues) để đảm bảo bug chưa được báo cáo
- Tạo issue mới với template bug report
- Cung cấp thông tin chi tiết về môi trường và cách tái hiện lỗi

### 💡 Đề xuất Feature
- Kiểm tra [Issues](https://github.com/Noiceboi/THPT_ANALYSIS_2025/issues) để tránh trùng lặp
- Tạo issue với template feature request
- Mô tả rõ ràng lý do và lợi ích của feature

### 🔧 Code Contribution
1. Fork repository
2. Tạo branch mới: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.9+
- Jupyter Notebook
- Git

### Setup Environment
```bash
# Clone repository
git clone https://github.com/Noiceboi/THPT_ANALYSIS_2025.git
cd THPT_ANALYSIS_2025

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test
python -m pytest tests/test_data_analyzer.py
```

## 📝 Code Style

### Python Code
- Sử dụng [Black](https://black.readthedocs.io/) để format code
- Tuân thủ [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Viết docstring cho functions và classes
- Type hints cho parameters và return values

### Commit Messages
Sử dụng format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: Feature mới
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

Ví dụ:
```
feat(analyzer): add clustering analysis for subject combinations

- Implement K-means clustering
- Add visualization for clusters
- Update analysis pipeline

Closes #123
```

## 📊 Data Contribution

### Nguồn dữ liệu mới
- Đảm bảo dữ liệu từ nguồn chính thức
- Cung cấp metadata và documentation
- Tuân thủ privacy và copyright

### Data Quality
- Kiểm tra tính toàn vẹn dữ liệu
- Xử lý missing values và outliers
- Validate data schema

## 📋 Pull Request Process

1. **Kiểm tra trước khi submit**:
   - [ ] Code đã được test
   - [ ] Documentation đã được cập nhật
   - [ ] Commit messages rõ ràng
   - [ ] Không có conflicts với main branch

2. **PR Description**:
   - Mô tả ngắn gọn thay đổi
   - Link đến related issues
   - Screenshots nếu có UI changes
   - Testing instructions

3. **Review Process**:
   - Ít nhất 1 reviewer approve
   - Tất cả conversations resolved
   - CI/CD checks pass

## 🧪 Testing Guidelines

### Unit Tests
- Test coverage ≥ 80%
- Test edge cases và error conditions
- Mock external dependencies

### Integration Tests
- Test data pipeline end-to-end
- Validate analysis results
- Check output formats

### Example Test
```python
def test_analyze_popularity():
    """Test popularity analysis functionality."""
    analyzer = THPTDataAnalyzer(db_path="test_data.db")
    result = analyzer.analyze_to_hop_popularity()
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert 'ma_to_hop' in result.columns
    assert 'so_nganh' in result.columns
```

## 📚 Documentation

### README Updates
- Cập nhật features mới
- Thay đổi installation instructions
- Update examples và use cases

### Code Documentation
- Docstrings cho public APIs
- Inline comments cho complex logic
- Type hints cho better IDE support

### Notebooks
- Clear explanations và context
- Well-structured cells
- Meaningful outputs và visualizations

## 🌟 Recognition

Contributors sẽ được ghi nhận trong:
- README.md
- CONTRIBUTORS.md
- Release notes
- Project website

## ❓ Questions?

- Tạo [Discussion](https://github.com/Noiceboi/THPT_ANALYSIS_2025/discussions)
- Email: contact@thptanalysis.com
- Join our Discord: [link]

## 📜 License

Bằng việc đóng góp, bạn đồng ý rằng contributions sẽ được licensed under MIT License.

---

**Cảm ơn bạn đã quan tâm đến dự án! 🎉**
