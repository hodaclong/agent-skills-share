# Định tuyến trích xuất theo định dạng

Mục tiêu là lấy cấu trúc và bằng chứng với chi phí thấp nhất. Kiểm tra lệnh đã có bằng `command -v` trước; không tự cài thêm nếu chưa được phép.

| Nguồn | Tuyến ưu tiên | Vị trí bằng chứng cần giữ | Fallback an toàn |
|---|---|---|---|
| URL HTML/XML/JSON | `curl`/trình đọc URL sẵn có; lọc main content, giữ URL và thời điểm lấy | URL, heading, CSS/JSON path | Ghi `blocked`/`auth_required`, không đoán |
| TXT/MD/CSV/JSONL | Python standard library hoặc CLI nhẹ | dòng, section, key/path | Giữ file nguyên bản và báo lỗi parse |
| PDF có text | `pdfinfo`, `pdftotext -layout` nếu có | trang, heading/bảng | Đọc text có sẵn; không OCR dư thừa |
| PDF scan / ảnh | OCR đã có (`tesseract` hoặc công cụ hiện có) | trang, bounding box nếu có, confidence | Ghi `ocr_unavailable` nếu không có công cụ |
| DOCX/PPTX/XLSX | XML trong ZIP bằng Python stdlib; dùng `pandoc`/LibreOffice chỉ khi đã có | paragraph, table-cell, slide, sheet-cell | Giữ cấu trúc file và báo phần không trích được |
| Audio/video | phụ đề/transcript sẵn có → `ffprobe` để lấy metadata | timecode, track, speaker nếu có | Không tự tải model; ghi `transcript_required` |
| ZIP/7z/tar | kiểm kê member trước; chỉ giải nén vào thư mục tạm an toàn khi cần | member path + hash | Không chạy file bên trong, không đệ quy vô hạn |
| Định dạng khác | đọc metadata, magic bytes và công cụ sẵn có | offset/page/timecode phù hợp | Record `unsupported_format` và dừng phần đó |

Quy tắc chung:

- Giữ bản gốc hoặc con trỏ tới bản gốc; output chưng cất không thay thế raw source.
- Với URL cần lưu HTTP status, canonical URL, capture time và checksum nếu tải được. Không bypass paywall, CAPTCHA, login hoặc robots/policy.
- Không đưa đường dẫn tuyệt đối chứa tên người dùng, query có token hoặc nội dung nhạy cảm vào `retrieval_text`; dùng `path_redacted` và giữ chi tiết ở nơi được phép.
- OCR/transcript là dữ liệu có sai số: giữ confidence/trạng thái và đánh dấu claim cần kiểm tra.
