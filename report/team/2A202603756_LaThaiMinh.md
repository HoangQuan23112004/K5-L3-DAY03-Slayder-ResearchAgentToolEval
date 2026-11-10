# Báo cáo cá nhân — Lã Thái Minh-2A202603756

## 1. Thông tin thành viên

- Họ tên: Lã Thái Minh
- MSSV: 2A202603756
- Email: 26ai.minhlt4@vinuni.edu.vn

## 2. Phần việc phụ trách

- Thực hiện Checkpoint 5 (CP5): làm UI để demo Research Agent, chuẩn bị Phần A của báo cáo nhóm và tạo transcript hội thoại thử nghiệm.

## 3. Đóng góp cụ thể

- Tạo giao diện Streamlit trong [app.py](../../starter_v0/app.py), dùng vòng gọi agent và cách lưu transcript từ [chat.py](../../starter_v0/chat.py).
- Bổ sung dependency Streamlit vào [requirements.txt](../../starter_v0/requirements.txt).
- Viết Phần A trong [group_report.md](group_report.md): giới thiệu agent, các tool, lệnh chạy UI và câu hỏi mẫu.
- Chuẩn bị câu hỏi thử và lưu các lượt chat thực tế tại [transcripts/](../../starter_v0/transcripts/).

## 4. Bằng chứng

- File/commit/PR: [app.py](../../starter_v0/app.py), [requirements.txt](../../starter_v0/requirements.txt), [group_report.md](group_report.md) mục 2 và B4, [v3_openrouter_20261111T011751683948.transcript.json](../../starter_v0/transcripts/v3_openrouter_20261111T011751683948.transcript.json).
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Dùng Codex hỗ trợ viết UI và báo cáo; tự kiểm tra bằng cách mở UI tại `http://localhost:8501` và đối chiếu 4 lượt chat với transcript. Agent hỏi URL còn thiếu, gọi `fetch` sau khi được cung cấp URL, gọi `lookup` để tìm tin và gọi `clarify` để xin xác nhận gửi.

## 5. Tự đánh giá

- Đã hoàn thành UI, Phần A và lưu transcript 4 lượt gồm yêu cầu thiếu URL, bổ sung URL, tìm tin và xin xác nhận gửi Telegram. Phiên chat dừng ở bước hỏi xác nhận.
