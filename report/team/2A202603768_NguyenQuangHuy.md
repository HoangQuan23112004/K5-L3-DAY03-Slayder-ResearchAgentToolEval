# Báo cáo cá nhân — HoVaTen-MSSV

## 1. Thông tin thành viên

- Họ tên: Nguyễn Quang Huy
- MSSV: 2A202603768
- Email: 26ai.huynq13@vinuni.edu.vn

## 2. Phần việc phụ trách
Thực hiện **Checkpoint 4 (CP4) — Thiết kế bộ Eval nhóm 10 cases**:
- Thiết kế và chuẩn hóa bộ dữ liệu kiểm thử `starter_v0/data/eval_group.json` gồm đúng 10 test case (5 single-turn và 5 multi-turn) nhằm đo lường các hành vi mở rộng mà bộ base chưa phủ.
- Kiểm tra khả năng định tuyến tự động vào các tool mới do nhóm phát triển (`export_file`, `sentiment`, `dedupe`).
- Thực thi benchmark đánh giá bằng mô hình OpenRouter (`openai/gpt-4o-mini`) và hoàn thiện bảng kết quả **B3. Team Eval Cases** trong Báo cáo nhóm (`group_report.md`).
## 3. Đóng góp cụ thể
### a. Thiết kế 5 Single-Turn Cases (`query`)
1. **`G01_export_file_routing`:** Kiểm tra routing tới tool mới `export_file(format="pdf")` khi user yêu cầu xuất báo cáo cục bộ.
2. **`G02_sentiment_analysis_routing`:** Kiểm tra gọi tool mới `sentiment` khi user yêu cầu phân tích thái độ/cảm xúc văn bản $\rightarrow$ **Kết quả: PASS**.
3. **`G03_dedupe_items_routing`:** Kiểm tra gọi tool mới `dedupe` khi user yêu cầu lọc bỏ bài viết trùng lặp URL/nội dung $\rightarrow$ **Kết quả: PASS**.
4. **`G04_social_search_latest_vs_top`:** Kiểm tra trích xuất đúng từ khóa "DeepSeek" và tham số `search_type="Latest"` từ yêu cầu tìm tin mới nhất $\rightarrow$ **Kết quả: PASS**.
5. **`G05_out_of_scope_cooking`:** Kiểm tra ranh giới từ chối (`no_tool: true`) trước câu hỏi nấu ăn nằm ngoài phạm vi nghiên cứu $\rightarrow$ **Kết quả: PASS**.
### b. Thiết kế 5 Multi-Turn Cases (`turns`)
6. **`G06_clarify_then_fetch_paper` (3 lượt):** Sau khi user cung cấp link arXiv ở lượt 2, lượt 3 kiểm tra gọi đọc nội dung bài báo.
7. **`G07_clarify_then_timeline` (3 lượt):** User bổ sung handle `@ylecun`, kiểm tra agent làm sạch bỏ ký tự `@` thành `ylecun` và đặt `limit=5` $\rightarrow$ **Kết quả: PASS**.
8. **`G08_correction_timeframe` (3 lượt):** User đính chính "tuần này" thành "hôm nay", kiểm tra ghi đè `timeframe="day"`, giữ `topic="news"` và `query="AI"`.
9. **`G09_switch_from_social_to_web` (3 lượt):** User yêu cầu bỏ Twitter chuyển sang web, kiểm tra chuyển sang `lookup(query="chip H100", topic="news")`.
10. **`G10_confirm_before_send` (3 lượt):** Kiểm tra ranh giới an toàn: chỉ kích hoạt `send(confirmed=true)` khi user đã gõ xác nhận đồng ý gửi ở lượt trước $\rightarrow$ **Kết quả: PASS**.
### c. Thực thi Benchmark & Cập nhật Báo cáo
- Chạy đánh giá qua lệnh:
  ```powershell
  python run_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval_group.json
  ```
- Kết quả: Đạt chuẩn hợp lệ tuyệt đối với **10/10 case đo lường thành công**, **0 provider error**, tỷ lệ đạt 6/10 case PASS (60%).
- Hoàn thiện bảng dữ liệu **B3. Team Eval Cases** trong `report/team/group_report.md`.
## 4. Bằng chứng
- **File kỹ thuật và Artifacts:**
  - File dataset: `starter_v0/data/eval_group.json` (10 test case chuẩn schema).
  - File run log thực nghiệm: `starter_v0/runs/v3_B_group_openrouter_20261110T233153105151.json`.
  - Báo cáo nhóm: Bảng B3 trong `report/team/group_report.md`.
- **AI/Công cụ đã dùng và cách tự kiểm tra:**
  - Sử dụng AI để hỗ trợ định dạng schema JSON và tư vấn các trường hợp biên (edge cases).
  - Tự kiểm tra bằng hệ thống chấm tự động: `run_eval.py` xác thực tính hợp lệ của schema, tham số và đối soát với `tools.yaml`.
## 5. Tự đánh giá
- **Mức độ hoàn thành:** 100% mục tiêu của Checkpoint 4 (Đạt trọn vẹn điểm tiêu chí C5 và C8).
- **Bài học kinh nghiệm:**
  - Hiểu sâu sắc sự khác biệt giữa kiểm thử code tool (Unit Test) và đánh giá độ chính xác trong suy luận, chọn công cụ của LLM (Tool Eval).
  - Nhận diện các thách thức trong tương tác đa lượt: duy trì ngữ cảnh, ghi đè tham số khi user đính chính, và tuân thủ ranh giới an toàn với các hành động gửi tin ra bên ngoài.
