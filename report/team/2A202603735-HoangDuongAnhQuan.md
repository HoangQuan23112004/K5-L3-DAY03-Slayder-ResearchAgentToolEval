# Báo cáo cá nhân — Checkpoint 2

## 1. Thông tin thành viên

- Họ tên: Hoàng Dương Anh Quân
- MSSV: 2A202603735

## 2. Phần việc phụ trách

Phụ trách tối ưu system prompt và tool declaration của Research Agent ở CP2 theo vòng lặp: phân tích log → đặt giả thuyết → chỉnh sửa → chạy eval → so sánh kết quả. Phạm vi gồm các phiên bản v1–v3, kiểm tra tính đồng bộ của tool và tổng hợp bằng chứng vào version_log.csv, báo cáo nhóm. Công việc được thực hiện với sự hỗ trợ của Codex; các thay đổi và kết quả dưới đây có thể đối chiếu với file trong repository.

## 3. Đóng góp cụ thể

### Phân tích baseline và tối ưu v1

Đối chiếu run v0 đạt 14/20 case (70%), nhận diện sáu case lỗi: R08, R10, R11, R12, R13 và R14. Các lỗi chính gồm gọi tool cho yêu cầu ngoài phạm vi, tự đoán tài khoản hoặc URL, gửi khi chưa xác nhận và truyền sai tham số tìm tin.

Chỉnh system_prompt.md để bỏ các chỉ dẫn đoán thay vì hỏi, gửi ngay và ép xử lý một bước. Bổ sung routing giữa timeline, social_search, lookup, fetch và clarify; quy tắc hỏi lại khi thiếu thông tin; xác nhận trước gửi; topic=news và bộ lọc thời gian. Run sau sửa đạt 18/20 (90%), tăng 20 điểm phần trăm so với baseline, nhưng còn lỗi xác nhận R12 và gọi thừa social_search ở M06.

### Làm rõ tool declaration ở v2

Bổ sung điều kiện dùng/không dùng cho clarify, send, lookup và social_search; làm rõ response_type, topic, timeframe, search_type và quy tắc ngừng gọi nguồn đã bị người dùng hủy. Đồng bộ prompt và TOOL.md tương ứng để giảm chỉ dẫn mâu thuẫn. Run v2 đạt 19/20 (95%); M06 đã PASS, R12 vẫn chọn text thay vì yes_no. Vì v2 thay cả prompt và YAML, kết quả này không tách riêng được tác động của từng file.

### Điều chỉnh thứ tự ưu tiên ở v3

Đặt quy tắc xác nhận ý định đăng bài trước quy tắc hỏi dữ liệu thiếu, kèm ví dụ câu hỏi yes_no. Vẫn yêu cầu xác nhận nội dung cuối và nơi gửi trước send(confirmed=true). Run v3 sửa được R12 nhưng giảm còn 18/20 (90%) do gọi thừa social_search ở M02 và M06. Ghi nhận đây là hồi quy thay vì kết luận v3 tốt hơn v2.

### Kiểm tra và hoàn thiện tài liệu

Bổ sung mô tả dùng/không dùng cho timeline, fetch, format, policy, papers và paper_text sau v3; ghi rõ screenname không có @; đồng bộ sáu TOOL.md. Giữ nguyên tên tool, tham số và registry. Cấu hình YAML mới chưa chạy eval, nên không gán kết quả v3 cho lần sửa này. Tổng hợp hash, giả thuyết, metric trước/sau và run_file trong version_log.csv; bổ sung bảng B1/B2 và các file changes.

## 4. Bằng chứng

### File/commit/PR

- Cấu hình: starter_v0/artifacts/system_prompt.md; starter_v0/artifacts/tools.yaml; tools/<tên>/TOOL.md trong starter_v0.
- Nhật ký: starter_v0/artifacts/version_log.csv; v1_changes.md, v2_changes.md, v3_changes.md và post_v3_tools_changes.md cùng thư mục.
- Báo cáo: report/team/group_report.md, bảng B1 (version evidence) và B2 (failure analysis).

Kết quả case_accuracy trên base eval:

- v0: 14/20 — 70%; run v0_B_base_openrouter_20261110T173810231309.json.
- v1: 18/20 — 90%; file v1_B_base_openrouter_20261110T183004214366.json.
- v2: 19/20 — 95%; run v2_B_base_openrouter_20261110T183941086642.json.
- v3: 18/20 — 90%; run v3_B_base_openrouter_20261110T184513703369.json.

Các file trên nằm trong starter_v0/runs/, dùng OpenRouter / openai/gpt-4o-mini. Cả bốn lượt đều có measured_cases=total_cases=20 và provider_error_cases=0.

### AI/công cụ đã dùng và cách kiểm tra

Sử dụng Codex để hỗ trợ đọc log, đề xuất prompt/YAML, đồng bộ tài liệu, chạy pytest.

Đối chiếu metric, hash và artifact_version trong CSV với run JSON; đọc actual_tool_calls, failures và observed_mismatch để phân biệt lỗi chọn tool với lỗi tham số. 
## 5. Tự đánh giá

Qua checkpoint 2, em hiểu rõ hơn cách tối ưu agent dựa trên log và kết quả kiểm thử. Với sự hỗ trợ của Codex, em đã phân tích lỗi baseline, chỉnh system prompt và tool declaration, sau đó đối chiếu kết quả giữa các phiên bản. Kết quả tốt nhất là v2 đạt 95%, tăng 25 điểm phần trăm so với baseline 70%.

Điểm em thấy mình làm tốt là theo dõi lỗi cụ thể và ghi nhận cả những thay đổi không đạt kỳ vọng. V3 sửa được lỗi xác nhận đăng bài ở R12 nhưng làm phát sinh lỗi gọi thừa tool ở M02 và M06, khiến điểm giảm còn 90%. Điều này giúp em nhận ra cần kiểm tra lại toàn bộ bộ case sau mỗi lần sửa, thay vì chỉ tập trung vào case đang lỗi.

Em còn hạn chế ở việc thay nhiều quy tắc trong cùng một phiên bản nên khó xác định chính xác thay đổi nào tạo ra cải thiện.
