# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |  Hoàng Dương Anh Quân      |   2A202603735   |   26ai.quanhda@vinuni.edu.vn    |        |         |
|   2 |  Nguyễn Quang Huy      |   2A202603768   |   26ai.huynq13@vinuni.edu.vn    |   nguyenquanghuy091204     |    Thực hiện Checkpoint 4 (CP4) - Thiết kế bộ Eval nhóm 10 cases     |
|   3 |  Đào Nguyễn Quang Thành      |  2A202603754    | 26ai.thanhdnq@vinuni.edu.vn      | DaoThanh11       | Phụ trách lập tool mới, viết test case tương ứng với tool mới        |
|   4 |        |      |       |        |         |
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
