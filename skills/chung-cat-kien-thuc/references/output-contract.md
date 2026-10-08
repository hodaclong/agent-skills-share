# Hợp đồng semantic knowledge pack

## Cây output tối thiểu

```text
pack/
├── manifest.json
├── sources.jsonl
├── claims.jsonl
├── entities.jsonl
├── relations.jsonl
├── chatbot.jsonl
├── content-map.jsonl
└── quality.json
```

`documents.jsonl` và `chunks.jsonl` là tùy chọn: chỉ thêm khi cần trace sâu hoặc truy hồi đoạn dài. Raw source để ngoài pack hoặc tại `raw/`, không nhân bản vào mọi record. Embeddings là lớp tùy chọn riêng, không phải nguồn sự thật.

## Trường dùng chung

- ID: tiền tố loại record + hash SHA-256 ổn định, ví dụ `src-<hash>`, `claim-<hash>`.
- `schema_version`, `created_at`, `status` và `source_refs` khi record có nội dung suy ra.
- `source_refs`: `{ "source_id": "src-...", "locator": {"page": 3, "heading": "..."}, "excerpt_id": "..." }`. Locator thay đổi theo loại file.
- Không lặp nguyên văn dài giữa các file; tham chiếu ID. UTF-8, JSON hợp lệ, JSONL một object mỗi dòng.

## Record tối thiểu

```json
{"source_id":"src-a1b2","kind":"pdf","uri":"https://example.invalid/a.pdf","sha256":"...","captured_at":"...","status":"extracted"}
{"entity_id":"entity-c3d4","entity_type":"organization","label":"Tên thực thể","aliases":[],"status":"canonical","source_refs":[{"source_id":"src-a1b2","locator":{"page":1}}]}
{"claim_id":"claim-e5f6","subject_id":"entity-c3d4","predicate":"has_contact","value":{"phone":"[redacted]"},"value_type":"object","status":"source_observation","answerability":"source_answerable","source_refs":[{"source_id":"src-a1b2","locator":{"page":1}}]}
{"relation_id":"rel-1122","from_id":"entity-c3d4","relation":"mentions","to_id":"entity-3344","status":"observed","source_refs":[{"source_id":"src-a1b2","locator":{"page":2}}]}
{"knowledge_id":"kb-5566","subject_id":"entity-c3d4","intent":"overview","answerability":"source_answerable","retrieval_text":"Tên thực thể | overview | claim-e5f6","claim_ids":["claim-e5f6"],"source_refs":[{"source_id":"src-a1b2","locator":{"page":1}}]}
{"content_map_id":"content-7788","topic_id":"entity-c3d4","audiences":["general"],"source_roles":{"fact":["src-a1b2"],"context":["src-a1b2"]},"claim_ids":["claim-e5f6"],"review_gates":["check_currentness"]}
```

Ví dụ trên chỉ minh họa hình dạng; không dùng làm dữ liệu thật. Không đưa secret/PII thật vào pack mẫu. `manifest.json` phải nêu `dataset_id`, `schema_version`, nguồn, thời điểm chụp, counts, entrypoints (`chatbot`, `content`), toolchain, limitations và trạng thái kiểm tra. `quality.json` phải nêu lỗi, cảnh báo, record thiếu nguồn, OCR/transcript chưa chắc chắn, xung đột và duplicate.

## Hai lối vào cho AI

- `chatbot.jsonl`: bắt đầu từ intent/subject, đọc `answerability`, rồi lần theo claim/entity và source locator. `live_check_required` hoặc `human_review_required` là cổng chặn, không phải gợi ý.
- `content-map.jsonl`: bắt đầu từ topic/audience/angle, chọn nhiều nguồn có vai trò khác nhau, rồi lần theo claim và bằng chứng. Không dùng map như bài viết đã được duyệt.

## Tối ưu kích thước

1. Loại boilerplate và near-duplicate trước khi tạo record.
2. Chuẩn hóa một lần; dùng ID/hash cho mọi liên kết.
3. Giữ excerpt ngắn và chỉ ở nguồn cần trace; toàn văn ở raw source.
4. Nén file sau khi validate nếu hệ thống đích hỗ trợ, nhưng không làm mất khả năng đọc JSONL hoặc provenance.
