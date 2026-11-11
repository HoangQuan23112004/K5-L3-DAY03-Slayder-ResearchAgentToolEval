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

Slayder Research Agent hỗ trợ tìm tin web, bài đăng X/Twitter, paper arXiv và quy định nghiên cứu nội bộ; có thể đọc URL hoặc nội dung paper, loại mục trùng, phân tích sắc thái và xuất nội dung ra file. Agent hỏi lại khi thiếu thông tin và cần xác nhận nội dung cuối trước khi gửi lên Telegram.

**Cách chạy UI:**

Từ `starter_v0/`, cài dependency bằng `python -m pip install -r requirements.txt`, cấu hình `.env` theo [TOOL-SETUP.md](../../docs/TOOL-SETUP.md), rồi chạy `streamlit run app.py`. Mở `http://localhost:8501` trên máy chạy UI. UI dùng cùng vòng chat và định dạng transcript với `chat.py`; mỗi phiên lưu vào `starter_v0/transcripts/*.transcript.json`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL: https://spoke-dod-vsnet-forget.trycloudflare.com/


### A2. Tool agent có

Danh sách dưới đây khớp các tool đang được đăng ký trong `starter_v0/tools/__init__.py` và khai báo trong `starter_v0/artifacts/tools.yaml`.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại khi thiếu thông tin hoặc cần xác nhận | không |
| timeline | Lấy bài đăng gần đây của một tài khoản X/Twitter | không |
| social_search | Tìm bài đăng X/Twitter về một chủ đề | không |
| lookup | Tìm thông tin và tin tức trên web | không |
| fetch | Đọc nội dung từ URL cụ thể | không |
| format | Định dạng dữ liệu đã có thành bản tin hoặc danh sách | không |
| send | Gửi nội dung đã được xác nhận lên Telegram | không |
| policy | Tra cứu tài liệu chính sách nghiên cứu nội bộ | không |
| papers | Tìm paper trên arXiv | không |
| paper_text | Đọc text từ paper arXiv đã xác định | không |
| dedupe | Loại các mục trùng URL hoặc nội dung tương tự | có |
| sentiment | Phân tích sắc thái tích cực, tiêu cực hoặc trung tính của văn bản | có |
| export_file | Xuất nội dung đã thu thập thành file PDF, HTML hoặc JSON cục bộ | có |

### A3. Câu hỏi mẫu để thử

1. Tin tức AI hôm nay có gì nổi bật?
2. Lấy 5 bài đăng mới nhất của Sam Altman trên X.
3. Tìm paper về đánh giá research agent trên arXiv.
4. Tóm tắt bài viết này giúp mình. (Kiểm tra agent có hỏi URL còn thiếu.)
5. Gửi bản tin này lên Telegram. (Kiểm tra agent có hỏi xác nhận trước khi gửi.)

## 3. Giải pháp

## 3. Giải pháp
- **`system_prompt.md`:** Bỏ chỉ dẫn tự đoán thông tin, gửi ngay và ép xử lý một bước. Bổ sung quy tắc chọn tool, hỏi lại khi thiếu tài khoản/URL, xác nhận trước khi gửi và ưu tiên yêu cầu mới nhất khi người dùng chuyển nguồn tìm kiếm.
- **`tools.yaml`:** Làm rõ chức năng, khi nào dùng/không dùng từng tool; quy ước handle không có `@`, `topic=news`, `timeframe`, `search_type=Top|Latest`. Tool `send` chỉ được gọi với `confirmed=true` sau khi người dùng xác nhận nội dung cuối và nơi gửi.
- **Kiểm chứng:** Đồng bộ các file `TOOL.md`, chạy contract tests và base eval; ghi giả thuyết, hash và kết quả từng phiên bản vào `version_log.csv`.

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

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|:---:|
| **G01_export_file_routing** | Yêu cầu lưu tệp báo cáo cục bộ → gọi tool mới `export_file(format="pdf")`, không nhầm sang `send` hay `format`. | `export_file(format="pdf")` | **FAIL**: Model nhận thấy chưa có nội dung văn bản cụ thể nên gọi `clarify` để hỏi nội dung trước khi export. |
| **G02_sentiment_analysis_routing** | Đánh giá thái độ/cảm xúc văn bản → gọi tool mới `sentiment`, không gọi tool tìm kiếm web hay mạng xã hội. | `sentiment()` | **PASS**: Model nhận diện chính xác intent phân tích cảm xúc và truyền đúng đoạn text phản hồi vào `sentiment`. |
| **G03_dedupe_items_routing** | Yêu cầu lọc bỏ các bài viết bị trùng lặp URL và nội dung → gọi tool mới `dedupe`. | `dedupe()` | **PASS**: Model tự động gọi đúng tool `dedupe` để xử lý danh sách item. |
| **G04_social_search_latest_vs_top** | Yêu cầu tìm tin "mới nhất" trên mạng xã hội → truyền `search_type="Latest"` và trích đúng từ khóa "DeepSeek". | `social_search(query="DeepSeek", search_type="Latest")` | **PASS**: Model trích xuất chuẩn xác query và map từ khóa "mới nhất" sang `search_type="Latest"` (không bị nhầm `Top`). |
| **G05_out_of_scope_cooking** | Yêu cầu công thức nấu ăn ngoài phạm vi nghiên cứu → KHÔNG gọi tool (`no_tool`), giải thích phạm vi trong chat. | `no_tool: true` | **PASS**: Model từ chối lịch sự và trả lời trực tiếp mà không gọi bất kỳ tool nào. |
| **G06_clarify_then_fetch_paper** | Hội thoại 3 lượt: Sau khi user cung cấp URL bài báo nghiên cứu → lượt cuối gọi đọc trang theo URL. | `fetch(url="https://arxiv.org/abs/2401.12345")` | **FAIL**: Model phát hiện link arXiv nên thông minh chọn gọi tool chuyên dụng `paper_text` thay vì tool tổng quát `fetch`. |
| **G07_clarify_then_timeline** | Hội thoại 3 lượt: User cung cấp `@ylecun` → agent chuẩn hóa bỏ ký tự `@` thành `ylecun` và lấy `limit=5`. | `timeline(screenname="ylecun", limit=5)` | **PASS**: Model kế thừa đầy đủ ngữ cảnh qua 3 lượt, tự động làm sạch ký tự `@` và đặt đúng `limit=5`. |
| **G08_correction_timeframe** | Hội thoại 3 lượt: User đính chính "tuần này" thành "hôm nay" → ghi đè `timeframe="day"`, giữ `topic="news"` và `query="AI"`. | `lookup(query="AI", topic="news", timeframe="day")` | **FAIL**: Model đã cập nhật đúng `timeframe="day"` cho `lookup`, nhưng gọi thêm cả `social_search` do nghĩ user muốn cả 2 nguồn. |
| **G09_switch_from_social_to_web** | Hội thoại 3 lượt: User yêu cầu bỏ Twitter chuyển sang web → chỉ gọi `lookup(query="chip H100", topic="news")`. | `lookup(query="chip H100", topic="news")` | **FAIL**: Model đã gọi `lookup(topic="news")` nhưng vẫn gọi kèm `social_search` (chưa triệt để ngắt hẳn nguồn Twitter cũ). |
| **G10_confirm_before_send** | Hội thoại 3 lượt: Sau khi user đã gõ xác nhận đồng ý gửi rõ ràng → kích hoạt `send(confirmed=true)`. | `send(confirmed=true)` | **PASS**: Model tuân thủ đúng ranh giới an toàn: khi đã có xác nhận rõ ràng ở lượt 2, lượt 3 kích hoạt `send(confirmed=true)`. |

### B4. Live Chat Evidence

Lấy từ transcript live [v3_openrouter_20261111T011751683948.transcript.json](../../starter_v0/transcripts/v3_openrouter_20261111T011751683948.transcript.json), chạy qua UI với OpenRouter / `openai/gpt-4o-mini`. Cả bốn lượt dùng artifact `v3+pd6e61a2fbd95+tb959bf7a2303`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | “Tóm tắt bài viết này giúp mình.” | Không gọi tool | `v3+pd6e61a2fbd95+tb959bf7a2303` | `answered`: agent hỏi người dùng cung cấp URL. |
| 2 | Cung cấp `https://openai.com/research/` và yêu cầu tóm tắt | `fetch(url="https://openai.com/research/")` | Cùng artifact lượt 1 | `answered`: đọc URL và trả lời. |
| 3 | “Tin tức AI hôm nay có gì nổi bật?” | `lookup(query="AI", topic="news", timeframe="day", max_results=5)` | Cùng artifact lượt 1 | `answered`: trả tin từ kết quả tìm web. |
| 4 | “Hãy gửi bản tin AI vừa tìm lên Telegram.” | `clarify(response_type="yes_no")` | Cùng artifact lượt 1 | `waiting_for_user`: hỏi xác nhận; transcript không có lệnh `send`. |

Các transcript khác có nhãn v0–v3 nhưng dùng cùng hash prompt và tool hiện tại. Chúng không thay thế run JSON ở B1 để so sánh hiệu quả giữa các phiên bản.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) | [app.py](../../starter_v0/app.py), [requirements.txt](../../starter_v0/requirements.txt), lệnh và link ở A1, [transcript 4 lượt](../../starter_v0/transcripts/v3_openrouter_20261111T011751683948.transcript.json) | UI mở được trên máy và qua link tunnel; ghi transcript có lượt hỏi URL, bổ sung URL, tìm tin và xin xác nhận gửi. | Link tunnel tạm thời; UI hiển thị `provider_error` khi lỗi provider và không nhập API key vào chat. |

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
