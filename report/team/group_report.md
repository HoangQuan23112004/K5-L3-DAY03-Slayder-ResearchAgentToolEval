# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Slayder
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter / `openai/gpt-4o-mini`.

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo starter trước sửa | — | 70% (14/20) | `starter_v0/runs/v0_B_base_openrouter_20261110T173810231309.json` |
| v1 | system_prompt.md | Thay chỉ dẫn đoán/gửi ngay bằng routing, hỏi lại và xác nhận | 70% | 90% (18/20) | `starter_v0/runs/v1_B_base_openrouter_20261110T183004214366.json` |
| v2 | system_prompt.md + tools.yaml | Làm rõ điều kiện gọi tool và xác nhận để giảm nhầm response_type và gọi thừa nguồn đã hủy | 90% | 95% (19/20) | `starter_v0/runs/v2_B_base_openrouter_20261110T183941086642.json` |
| v3 | system_prompt.md | Ưu tiên xác nhận đăng bài trước hỏi dữ liệu thiếu để sửa R12 | 95% | 90% (18/20) | `starter_v0/runs/v3_B_base_openrouter_20261110T184513703369.json` |

Tất cả các run trên có measured_cases=total_cases=20 và provider_error_cases=0.
Hash và artifact_version được giữ nguyên từ run trong `version_log.csv`.
*File gọi là v1 nhưng metadata version/run_id/artifact_version vẫn ghi v0.
Đây là lượt dùng prompt hash khác baseline, được đối chiếu như vòng tối ưu v1;
cần giải trình nhãn sai hoặc chạy lại snapshot v1 với nhãn đúng, không sửa log cũ.
V1 và v2 gồm nhiều quy tắc nên chưa cô lập được tác động của từng quy tắc riêng lẻ.
V3 giảm 5 điểm phần trăm: R12 đã PASS, nhưng M02/M06 gọi thừa social_search.
V2 là lượt có case_accuracy cao nhất trong bốn lượt, chưa chứng minh ổn định qua nhiều lần chạy.

Sau v3 đã bổ sung điều kiện dùng/không dùng của timeline, fetch, format, policy,
papers, paper_text và convention screenname không có @; đồng bộ 6 TOOL.md.
Chi tiết: `starter_v0/artifacts/post_v3_tools_changes.md`.
Cấu hình YAML hiện tại khác hash v3 và chưa chạy eval; bảng trên chỉ báo cáo các run lịch sử.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope (unexpected_tool_call) | send | Dùng tool gửi cho bài toán ngoài phạm vi | V1: giải thích phạm vi trong chat, không gọi tool; đã PASS ở v1–v3 |
| R10_missing_handle | missing_info (missing_tool_call) | timeline(screenname=sama) | Tự đoán tài khoản khi user chưa nói của ai | V1: clarify(text) khi thiếu tài khoản; đã PASS ở v1–v3 |
| R11_missing_url | missing_info (missing_tool_call) | fetch(url=https://example.com/article) | Tự bịa URL | V1: clarify(text) xin URL; đã PASS ở v1–v3 |
| R12_confirm_before_send | wrong_boundary (missing_tool_call) | send(text=Bản tin này) | Gọi gửi khi chưa xác nhận | V1/v2 hỏi text nên vẫn FAIL; v3 ưu tiên yes_no và đã PASS |
| R13_parallel_web_and_tweets | wrong_tool theo case; observed=wrong_arg_value | lookup(query=AI news), social_search(query=AI) | Đã gọi đủ tool nhưng query lệch AI và thiếu topic=news | V1: tách chủ đề khỏi bộ lọc topic/timeframe; đã PASS ở v1–v3 |
| R14_out_of_scope_coding | out_of_scope (unexpected_tool_call) | send | Dùng tool gửi cho yêu cầu viết code ngoài phạm vi | V1: trả lời phạm vi trong chat; đã PASS ở v1–v3 |

Nguồn bảng B2: `starter_v0/runs/v0_B_base_openrouter_20261110T173810231309.json`.
Failure Type giữ nhãn case từ log và bổ sung observed_mismatch để phân biệt lỗi tham số thực tế.

Lỗi còn lại của v3: M02_carryover_timeframe (case failure_type=wrong_arg_value)
và M06_switch_tool (wrong_tool), đều observed_mismatch=extra_tool_call với social_search.
Nguồn: `starter_v0/runs/v3_B_base_openrouter_20261110T184513703369.json`.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
