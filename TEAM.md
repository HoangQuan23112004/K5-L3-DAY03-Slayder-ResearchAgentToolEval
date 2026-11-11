# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |  Hoàng Dương Anh Quân      |   2A202603735   |   26ai.quanhda@vinuni.edu.vn    | HoangQuan23112004      | Thực hiện Checkpoint 1 và checkpoint 2        |
|   2 |  Nguyễn Quang Huy      |   2A202603768   |   26ai.huynq13@vinuni.edu.vn    |   nguyenquanghuy091204     |    Thực hiện Checkpoint 4 (CP4) - Thiết kế bộ Eval nhóm 10 cases     |
|   3 |  Đào Nguyễn Quang Thành      |  2A202603754    | 26ai.thanhdnq@vinuni.edu.vn      | DaoThanh11       | Phụ trách lập tool mới, viết test case tương ứng với tool mới        |
|   4 | Lã Thái Minh       | 2A202603756      | 26ai.minhlt4@vinuni.edu.vn      |  minh17023      | Thực hiện Checkpoint 5 (CP5) - UI, demo và báo cáo |
## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-

## DaoNguyenQuangThanh - 2A202603754

### Phần việc phụ trách

- Thực hiện Checkpoint 3 (CP3): Viết tool mới và lập unit test cho tool mới
- Phụ trách phát triển và tích hợp 3 tool mới cho agent: `dedupe`, `sentiment` và `export_file`.
- Với mỗi tool, lập ra 3 test case với happy path, missing input và failure path tương ứng

### Đóng góp cụ thể

- `dedupe`: triển khai tool loại bỏ URL tracking và các item trùng lặp tương tự bằng cách chuẩn hóa URL, bỏ tham số theo dõi (`utm_`, `fbclid`, ...), so sánh độ tương đồng text bằng Jaccard similarity, và trả về danh sách item đã giữ lại / đã loại bỏ cùng metadata `removed_count`, `skipped_invalid`.
- `sentiment`: triển khai phân loại cảm xúc tiếng Anh và tiếng Việt với từ vựng và quy tắc negation/booster; hỗ trợ đầu vào `items` hoặc `text`, trả về `overall` và nhãn `positive/neutral/negative`.
- `export_file`: triển khai export ra file JSON/HTML/PDF an toàn, chuẩn hóa tên file, tránh overwrite bằng unique path, và có cảnh báo khi thiếu phông chữ Unicode trong PDF.
- Cập nhật `starter_v0/tests/test_tools_todo.py` cho các tool mới với ít nhất 3 testcase theo hướng happy path, bad input, failure path (không raise, trả error dict).
- Đồng bộ khai báo tool trong `starter_v0/artifacts/tools.yaml` và `starter_v0/tools/__init__.py` để model có thể gọi đúng tên tool.

### Bằng chứng

- Commit chính: `e89887e` — `3 new tools: dedupe, sentiment and export_file`
- Declare tool: `starter_v0/tools/__init__.py`,
- Lập tool artifact: `starter_v0/artifacts/tools.yaml`
- TOOL.md và tool.py trong folder tương ứng: `starter_v0/tools/dedupe/tool.py`, `starter_v0/tools/sentiment/tool.py`, `starter_v0/tools/export_file/tool.py`
- 9 unit test tương ứng với 3 tool trên: `starter_v0/tests/test_tools_todo.py`.

## NguyenQuangHuy-2A202603768

### Phần việc phụ trách

- Thực hiện Checkpoint 4 (CP4): Nghiên cứu và thiết kế bộ 10 Eval cases nhóm .
- Thực thi benchmark đánh giá bằng mô hình OpenRouter (`openai/gpt-4o-mini`) qua lệnh `run_eval.py --suite group`.
- Hoàn thiện mục B3 (Team Eval Cases) trong Báo cáo nhóm .

### Đóng góp cụ thể

- Thiết kế 5 single-turn cases: kiểm tra khả năng định tuyến tự động vào các tool mới do nhóm phát triển (`export_file`, `sentiment`, `dedupe`), chuẩn hóa tham số lọc bài mới nhất `search_type="Latest"`, và ranh giới từ chối yêu cầu ngoài phạm vi (`no_tool: true`).
- Thiết kế 5 multi-turn cases: kiểm tra khả năng duy trì ngữ cảnh đa lượt, hỏi lại khi thiếu URL/handle (`clarify`), đính chính tham số (`correction`), chuyển đổi công cụ linh hoạt theo ngữ cảnh, và đảm bảo ranh giới an toàn trước khi gửi tin (`send(confirmed=true)`).
- Chạy đánh giá thực nghiệm: Đo lường thành công 10/10 case, 0 provider error, đạt tỷ lệ 6/10 case PASS (60%) tại file run `v3_B_group_openrouter_20261110T233153105151.json`.
- Tổng hợp và phân tích đầy đủ kết quả thực nghiệm của 10 case vào Bảng B3 trong Báo cáo nhóm.

### Bằng chứng

- File dataset kiểm thử: `starter_v0/data/eval_group.json`
- File run log thực nghiệm: `starter_v0/runs/v3_B_group_openrouter_20261110T233153105151.json`
- Báo cáo nhóm: Bảng B3 trong `report/team/group_report.md`
- Báo cáo cá nhân: `report/team/2A202603768_NguyenQuangHuy.md`

## Lã Thái Minh-2A202603756

### Phần việc phụ trách

- Thực hiện Checkpoint 5 (CP5): làm UI demo Research Agent, chuẩn bị Phần A của báo cáo nhóm và tạo transcript hội thoại thử nghiệm.

### Đóng góp cụ thể

- Tạo giao diện Streamlit trong [app.py](starter_v0/app.py), dùng vòng gọi agent và cách lưu transcript từ [chat.py](starter_v0/chat.py).
- Bổ sung dependency Streamlit vào [requirements.txt](starter_v0/requirements.txt).
- Viết Phần A trong [group_report.md](report/team/group_report.md): giới thiệu agent, các tool, lệnh chạy UI và câu hỏi mẫu.
- Thử hội thoại qua UI và lưu transcript nhiều lượt.

### Bằng chứng

- Mã UI: [app.py](starter_v0/app.py), [requirements.txt](starter_v0/requirements.txt).
- Báo cáo nhóm: Phần A trong [group_report.md](report/team/group_report.md).
- Transcript 4 lượt: [v3_openrouter_20261111T011751683948.transcript.json](starter_v0/transcripts/v3_openrouter_20261111T011751683948.transcript.json).
- Báo cáo cá nhân: [2A202603756_LaThaiMinh.md](report/team/2A202603756_LaThaiMinh.md).
