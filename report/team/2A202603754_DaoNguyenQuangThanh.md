Báo cáo cá nhân — HoVaTen-MSSV
Đổi tên file theo quy tắc MSSV_HoTen.md.

Ví dụ: 20241234_NguyenVanAn.md.

1. Thông tin thành viên
Họ tên: Đào Nguyễn Quang Thành
MSSV: 2A202603754
Email: 26ai.thanhdnq@vinuni.edu.vn
2. Phần việc phụ trách
Phụ trách phát triển và tích hợp 3 tool mới cho agent: `dedupe`, `sentiment` và `export_file`. Cụ thể: xây dựng logic nghiệp vụ cho từng tool, cập nhật registration trong `starter_v0/tools/__init__.py`, khai báo trong `starter_v0/artifacts/tools.yaml`, và viết test unit để đảm bảo tool trả về error dict thay vì raise exception khi gặp input sai hoặc lỗi runtime.

3. Đóng góp cụ thể
- `dedupe`: triển khai tool loại bỏ URL tracking và các item trùng lặp tương tự bằng cách chuẩn hóa URL, bỏ tham số theo dõi (`utm_`, `fbclid`, ...), so sánh độ tương đồng text bằng Jaccard similarity, và trả về danh sách item đã giữ lại / đã loại bỏ cùng metadata `removed_count`, `skipped_invalid`.
- `sentiment`: triển khai phân loại cảm xúc tiếng Anh và tiếng Việt với từ vựng và quy tắc negation/booster; hỗ trợ đầu vào `items` hoặc `text`, trả về `overall` và nhãn `positive/neutral/negative`.
- `export_file`: triển khai export ra file JSON/HTML/PDF an toàn, chuẩn hóa tên file, tránh overwrite bằng unique path, và có cảnh báo khi thiếu phông chữ Unicode trong PDF.
- Cập nhật `starter_v0/tests/test_tools_todo.py` cho các tool mới với ít nhất 3 testcase theo hướng happy path, bad input, failure path (không raise, trả error dict).
- Đồng bộ khai báo tool trong `starter_v0/artifacts/tools.yaml` và `starter_v0/tools/__init__.py` để model có thể gọi đúng tên tool.

4. Bằng chứng
File/commit/PR:
- Commit chính: `e89887e` — `3 new tools: dedupe, sentiment and export_file`
- Git diff cho thấy các file được cập nhật: `starter_v0/artifacts/tools.yaml`, `starter_v0/tools/__init__.py`, `starter_v0/tools/dedupe/tool.py`, `starter_v0/tools/sentiment/tool.py`, `starter_v0/tools/export_file/tool.py`, `starter_v0/tests/test_tools_todo.py`.

AI/công cụ đã dùng và cách tự kiểm tra kết quả:
- Đã dùng Claude để kiểm tra logic tool theo hướng mô tả trong `starter_v0/tests/test_tools_todo.py`: happy path, invalid input, failure mode đều yêu cầu trả `error` dict thay vì raise exception. Test case được guidance, không copy-paste kết quả gen đầu tiên.

5. Tự đánh giá
Bản thân đã làm việc có hiệu quả khi đề xuất và phát triển 3 tool mới, tuy nhiên bản thân có research về tool mất thời gian và phải có sự giúp đỡ của thành viên để hiểu ra cách AI Agent gọi tool và cách tạo tool.
