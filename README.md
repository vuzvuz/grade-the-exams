# Hệ thống Chấm điểm Tự động

## Giới thiệu Dự án
Dự án này là một chương trình Python tự động hóa việc phân tích và chấm điểm các bài thi trắc nghiệm. Thay vì sử dụng các vòng lặp truyền thống, phiên bản này ứng dụng sức mạnh của thư viện **Pandas** và **NumPy** để xử lý dữ liệu thông qua kỹ thuật **Vector hóa**, cho phép tính toán điểm số của hàng ngàn sinh viên một cách cực kỳ nhanh chóng và chính xác. 

Mã nguồn được thiết kế tuân thủ nghiêm ngặt các tiêu chuẩn mã hóa của **PEP 8** và **Udacity Python Style Guide**.

## Các tính năng chính
- **Bẫy lỗi thông minh:** Tự động phát hiện và bỏ qua các dòng dữ liệu bị thiếu đáp án hoặc sai định dạng ID sinh viên thông qua Regular Expressions (Regex).
- **Chấm điểm siêu tốc:** Áp dụng thuật toán đối chiếu ma trận để chấm điểm toàn bộ danh sách lớp học cùng lúc mà không cần vòng lặp `for`.
- **Thống kê chuyên sâu:** Tự động tính toán các chỉ số thống kê tiêu chuẩn (Mean, Max, Min, Range, Median) và phân tích sâu các câu hỏi bị bỏ qua hoặc trả lời sai nhiều nhất.
- **Xuất dữ liệu tự động:** Tự động tạo tệp `_grades.txt` chứa điểm số của từng sinh viên hợp lệ.

---

## Yêu cầu Hệ thống
Để chạy được ứng dụng này, máy tính của bạn cần cài đặt sẵn:
1. **Python 3.8** trở lên.
2. Các thư viện phân tích dữ liệu: `pandas` và `numpy`.

Bạn có thể cài đặt các thư viện cần thiết bằng lệnh sau trong Terminal hoặc Command Prompt:
```bash
pip install pandas numpy
```

---

## Hướng dẫn Cài đặt và Sử dụng
### Bước 1: Chuẩn bị tệp dữ liệu
Đảm bảo rằng file mã nguồn (ví dụ: `lai_vu_grade_the_exams.py` và các file dữ liệu lớp học định dạng text (ví dụ: `class1.txt`, `class2.txt`, ...) được đặt chung trong cùng một thư mục.

### Bước 2: Khởi chạy chương trình
Mở Terminal hoặc Command Prompt, sử dụng lệnh `cd` để điều hướng đến thư mục chứa dự án và chạy lệnh sau:

```bash
python lai_vu_grade_the_exams.py
```

*(Lưu ý: Thay `lai_vu_grade_the_exams.py` bằng tên file mã nguồn thực tế của bạn).*

### Bước 3: Tương tác với hệ thống
1. Khi chương trình yêu cầu: `Enter a class file to grade (i.e. class1.txt):`, hãy nhập chính xác tên tệp dữ liệu bạn muốn chấm (bao gồm cả phần mở rộng `.txt`) và nhấn `Enter`.

2. Nếu nhập sai tên tệp, hệ thống sẽ báo lỗi `File cannot be found.` và tiếp tục yêu cầu bạn nhập lại (không làm sập chương trình).

3. Nếu tệp hợp lệ, hệ thống sẽ tự động quét, phân tích và in Báo cáo Thống kê trực tiếp ra màn hình.

4. Kiểm tra thư mục hiện tại, bạn sẽ thấy một tệp kết quả mới được tạo ra (ví dụ: `class1_grades.txt`) chứa ID và điểm của sinh viên.

---

## Phụ lục: Luồng thuật toán Vector hóa
Điểm nhấn kỹ thuật lớn nhất của dự án này là việc loại bỏ hoàn toàn các vòng lặp lồng nhau khi chấm điểm, thay bằng phép toán ma trận:

1. **Broadcasting**: Hệ thống chuyển toàn bộ đáp án của lớp thành một ma trận 2 chiều (N dòng x 25 cột) và so sánh trực tiếp với mảng `ANSWER_KEY` 1 chiều. Pandas tự động "nhân bản" (broadcast) mảng đáp án chuẩn để đối chiếu với từng sinh viên cùng lúc.

```python
is_correct = (answers.values == ANSWER_KEY)
```
2. **Tính điểm khối**: Bằng cách gán giá trị True/False thành các phép tính toán học, điểm số của toàn bộ danh sách lớp được tính ra chỉ bằng một phép tổng (`sum`) theo trục ngang (`axis=1`).
