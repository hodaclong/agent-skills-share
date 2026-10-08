---
name: dsh-mobile-private-access
description: "Thiết lập, kiểm tra và khắc phục truy cập DeepSeek Harness Web từ iPhone/điện thoại hoặc máy cá nhân qua Tailscale Serve riêng tư; dùng khi người dùng muốn tiếp tục workspace, session và job từ xa. Không dùng cho DeepSeek chat app, triển khai công khai hay di chuyển job lên cloud."
version: "1.0.0"
---

# DeepSeek Harness trên mobile qua mạng riêng

## Kết quả và giới hạn

Giúp người dùng không chuyên mở **cùng một DSH Web đang chạy trên máy chủ** từ trình duyệt mobile, xem workspace/session, gửi việc và tiếp tục công việc. Không giả định job ở profile/runtime khác cũng xuất hiện. Máy chủ phải bật, có mạng và không ngủ; điện thoại là client, không mang dữ liệu workspace sang máy mới.

Trước khi thay đổi, kiểm tra thực trạng và xác nhận đây là máy/DSH mà người dùng muốn truy cập. Không tự dừng hay khởi động lại tiến trình đang giữ job. Chỉ dùng Tailscale **Serve (tailnet only)**, không dùng Funnel, không bind `0.0.0.0`, mở port router hay tắt xác thực để xử lý lỗi. Bất kỳ thay đổi liên quan tài khoản, quyền tailnet, cert, đăng nhập đều cần người dùng tự cho phép; không nhận mật khẩu hay mã xác thực.

## Quy trình

1. **Khảo sát không lộ bí mật.** Kiểm tra `tailscale version`, `tailscale status`, `tailscale serve status`, cổng DSH đang nghe bằng `lsof -nP -iTCP:<port> -sTCP:LISTEN`. Xác định DSH Web trên `127.0.0.1:<port>` và thiết bị mobile thuộc cùng tailnet. Không in `dsh web` URL có token hoặc trạng thái cấu hình có secrets vào chat/log chia sẻ. Dùng cổng thực tế, không mặc định luôn là 3080.
2. **Kết nối máy chủ.** Nếu Tailscale đã cài nhưng `Stopped`, có thể `tailscale up` cho tài khoản đang có, rồi xác minh `Running`; nếu cần đăng nhập/đổi tài khoản, yêu cầu người dùng tự làm. Hướng dẫn mobile bật Tailscale và xác nhận nhìn thấy đúng máy chủ. Trạng thái peer có thể `idle` dù người dùng đã kết nối; kiểm chứng bằng thử nghiệm thật.
3. **Tạo đường riêng.** Khi người dùng đã yêu cầu truy cập từ xa, dùng `tailscale serve --bg --https=443 http://127.0.0.1:<port>` và kiểm tra `tailscale serve status` ghi `tailnet only`, proxy đúng loopback. Nếu CLI yêu cầu bật Serve/cert ở trang Tailscale, để chủ tài khoản tự phê duyệt và thử lại. Không dùng `--yes` để vượt qua bước này. Ghi nhớ cách gỡ riêng proxy đã tạo: `tailscale serve --https=443 off` (chỉ làm khi người dùng muốn).
4. **Kiểm tra tuyến và xác thực.** Thử `curl -sS -o /dev/null -w '%{http_code}\n' https://<dns-tailnet>/` và với `Origin: https://<dns-tailnet>` / `Sec-Fetch-Site: same-origin` trên `/api/`. `401` khi chưa có cookie là dấu hiệu mạng/proxy tới DSH đã thông, **không phải đăng nhập thành công**; `403` gợi ý Host/Origin hoặc policy; timeout/TLS error là tầng kết nối. DSH có xác thực bằng process launch token và cookie theo authority (host/port); không suy diễn cookie của localhost hoặc Safari áp dụng cho Brave.
5. **Đăng nhập an toàn trên điện thoại.** Chủ máy lấy link `dsh web:` của *đúng tiến trình hiện tại* qua kênh riêng, sửa **chỉ origin** `http://127.0.0.1:<port>/` thành `https://<dns-tailnet>/`, giữ nguyên `?token=<mã thật>`; mở trong tab thường của trình duyệt sẽ dùng (Brave hoặc Safari). Tránh dán link này vào hội thoại, log, screenshot, notes chia sẻ hay công cụ rút gọn URL. DSH trả 303 và cookie, rồi xóa token khỏi thanh địa chỉ. Về sau lưu dấu trang URL sạch không token. Không dùng `?token=...` ba dấu chấm như token thật. Nếu không còn link khởi động, nghiên cứu cách tạo đường đăng nhập mới không gây gián đoạn job; không đoán hay trích xuất secret từ tệp/process một cách ngầm định.
6. **Nghiệm thu trên mobile.** Người dùng xác nhận thấy workspace, mở session cũ, gửi thử yêu cầu đọc-only, chuyển workspace rồi quay lại kiểm tra kết quả; nếu cần chứng minh điều khiển job đang chạy, dùng một việc thử không quan trọng và xác nhận trạng thái sau khi ngắt/kết nối lại. Chỉ khẳng định đúng những phép thử đã thực hiện. Nhắc máy chủ bật, online và không ngủ; VPN mobile phải Connected.

## Xử lý lỗi ngắn gọn

- `dsh web authentication required; reopen the URL printed by dsh web`: hỏi **không lộ token** liệu thanh địa chỉ sau khi mở còn `?token=` hay đã chuyển về URL sạch. Nếu còn token, kiểm tra origin, đường `/`, token của đúng process và tab thường; nếu URL sạch rồi nhưng vẫn 401, kiểm tra cookie trong chính trình duyệt đó và Host/Origin ở tuyến proxy. Không gửi lại token vào chat.
- Trang trắng/quay mãi: kiểm tra HTTPS reachability, trình duyệt, stream/WebSocket và trạng thái DSH; đừng sửa mạng khi chưa xác định tầng lỗi.
- Có giao diện nhưng không thấy workspace: phân biệt DSH instance/profile/home khác, sidebar lọc/thu gọn, lỗi đồng bộ hay thiếu cookie; không coi đây là bằng chứng dữ liệu mất.
- `403`: kiểm tra tên Host/Origin thực tế và trusted-host config hiện tại trước khi cân nhắc thay đổi; cấu hình có thể cần restart, phải có kế hoạch không làm gián đoạn job.
- Token bị chia sẻ: coi là credential đã lộ; giới hạn phân phối, chọn thời điểm an toàn để xoay process launch token (restart có thể ngắt job). Không tuyên bố token đã vô hiệu chỉ vì người dùng đóng tab.

## Bằng chứng và bàn giao

Phiên áp dụng ban đầu: macOS DSH Web loopback + Tailscale Serve HTTPS tailnet-only + Brave iPhone đã hiển thị workspace và gửi tin từ mobile. Chưa xác nhận tất cả job/background behavior hoặc quy trình xoay token. Đây là ví dụ, **không hardcode hostname, cổng hay tài khoản của phiên đó**. Sau thay đổi tuyến vận hành, cập nhật hướng dẫn dự án tương ứng nếu được phép; không ghi token/cookie/khóa vào tài liệu.
