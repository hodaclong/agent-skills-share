---
name: chung-cat-kien-thuc
description: Use when a URL, local file, folder, or mixed-source collection must become lightweight, source-grounded machine knowledge for chatbot retrieval or content generation.
---

# Chưng cất kiến thức

## Mục tiêu

Tạo một semantic knowledge pack để AI đọc nhanh: claim nguyên tử, thực thể, quan hệ, nguồn bằng chứng, cổng trả lời chatbot và bản đồ nguồn cho content. Đây không phải bài tóm tắt dài cho con người. Nguồn gốc luôn được giữ riêng; dữ liệu chưng cất chỉ trỏ về nguồn bằng ID ổn định.

Kiến trúc mặc định là claim-centric semantic graph kết hợp hybrid retrieval: lọc metadata/từ khóa trước, chỉ dùng semantic embedding khi quy mô và công cụ sẵn có thực sự đáng kể. Mô hình ngôn ngữ chỉ xử lý phần mơ hồ, không đọc lại toàn bộ raw source.

## Bước đầu bắt buộc

Nếu lời gọi chưa có nguồn, câu trả lời đầu tiên chỉ là một câu hỏi:

> Dữ liệu nguồn nào anh muốn chưng cất? Gửi URL, đường dẫn file/thư mục, hoặc đính kèm file.

Sau đó dừng và chờ nguồn. Chỉ hỏi thêm khi nguồn không truy cập/đọc được hoặc cần quyết định quyền, chi phí hay đích lưu. Nếu lời gọi đã kèm nguồn thì không hỏi lại câu này.

## Quy trình

1. Xác định ranh giới nguồn, loại file, ngôn ngữ, quyền truy cập và đích output. Nếu anh chưa chỉ định đích, dùng `data/distilled/<source-slug>/` trong project hiện tại nếu có `data/`, nếu không dùng `distilled/<source-slug>/`; không ghi đè nguồn. Không vượt qua đăng nhập, không in secret/token/PII, không gửi dữ liệu riêng tư ra ngoài.
2. Kiểm kê rẻ trước: tên, MIME, kích thước, hash, URL, thời điểm lấy, số trang/slide/sheet/thời lượng nếu có. Không đọc toàn bộ vào context khi chưa cần.
3. Trích xuất bằng công cụ miễn phí/local đang có; chọn tuyến theo [format-routing.md](references/format-routing.md). Giữ vị trí bằng chứng (trang, heading, slide, sheet-cell, dòng hoặc timecode). File không đọc được phải ghi trạng thái, không đoán nội dung.
4. Chưng cất theo thứ tự: làm sạch cấu trúc → loại boilerplate/near-duplicate → tạo entity/concept/claim/procedure/relation → gắn thời gian, độ chắc chắn, xung đột và nguồn → tạo bản ghi truy hồi ngắn. Không sinh fact không có bằng chứng.
5. Ghi pack theo [output-contract.md](references/output-contract.md). Bắt buộc có `manifest.json`, `sources.jsonl`, `claims.jsonl`, `entities.jsonl`, `relations.jsonl`, `chatbot.jsonl`, `content-map.jsonl`, `quality.json`; chỉ tạo `chunks.jsonl` hoặc embeddings khi thật sự cần.
6. Kiểm tra JSON/JSONL, ID tham chiếu, nguồn, duplicate, claim thiếu bằng chứng và khả năng chạy lại ổn định. Chạy `scripts/validate_pack.py <pack-dir>` nếu pack theo hợp đồng này.

## Chính sách nhẹ và ít token

- Deterministic/local trước, LLM sau: parse, chuẩn hóa, hash, deduplicate và trích số/ngày/liên hệ bằng code hoặc CLI có sẵn.
- Không gửi nguyên file lớn vào model. Chia lô theo section, chỉ gửi metadata và đoạn bằng chứng ngắn cho phần cần phán đoán ngữ nghĩa.
- Không tự tải model lớn, Docker, vector database hoặc gọi API trả phí. Embedding là lớp tùy chọn sau khi đã giảm trùng; chỉ dùng công cụ miễn phí đã có và ghi model/kích thước nếu dùng.
- JSONL một record một dòng; `retrieval_text` ngắn, mặc định không quá 900 ký tự. Dùng `claim_ids`, `source_refs` và `entity_ids` thay cho lặp văn bản.

## Cổng an toàn

Gắn `answerability` cho từng chủ đề/claim: `source_answerable`, `needs_verification`, `conflict`, `human_review_required` hoặc `live_check_required`. Giá, tồn chỗ, chính sách hiện hành, thời hạn và cam kết thương mại không được tự biến thành sự thật cuối cùng. Thiếu hoặc mâu thuẫn dùng `null`/`Cần kiểm tra`, giữ mọi biến thể và nguồn để rà soát.

Bản đồ content phải dùng nhiều nguồn có vai trò khác nhau (fact, hướng dẫn, trải nghiệm, bối cảnh); không biến một nguồn duy nhất thành bài đăng hoàn chỉnh. Khi báo cáo, nêu rõ file output, số record, nguồn chưa đọc được, xung đột và việc cần người duyệt.
