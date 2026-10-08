# Bộ Agent Skills (Marketing + Engineering)

Repo **private**, chỉ dành cho thành viên được mời. Gồm 187 skill dùng chung cho
Claude Code, Codex và DeepSeek Harness (DSH).

> **License:** Các skill `ak-*` thuộc AgentKit và được chia sẻ theo gói team /
> sự đồng ý của AgentKit dành cho chủ repo. **Không** fork công khai, không
> chia sẻ lại ra ngoài nhóm. Các skill bên thứ ba giữ nguyên file LICENSE gốc.

## Cài đặt

Yêu cầu: đã được mời vào repo và đăng nhập GitHub (`gh auth login`).

**macOS / Linux**

```bash
gh repo clone hodaclong/agent-skills-share
cd agent-skills-share
./install.sh            # cài cho tất cả agent
# ./install.sh claude   # chỉ Claude Code  (~/.claude/skills)
# ./install.sh agents   # chỉ Codex + DSH  (~/.agents/skills)
```

**Windows (PowerShell)**

```powershell
gh repo clone hodaclong/agent-skills-share
cd agent-skills-share
powershell -ExecutionPolicy Bypass -File install.ps1
```

Skill trùng tên đã có trên máy sẽ được sao lưu vào `~/.agent-skills-backup/<thời-gian>/`
trước khi ghi đè. Sau khi cài, khởi động lại agent.

## Cập nhật

```bash
cd agent-skills-share && git pull && ./install.sh
```

## Kiểm tra

Mở agent và gõ `/ak-help` (DSH/Codex) hoặc hỏi "liệt kê skill ak đang có".

## Lưu ý

- Một số skill cần API key riêng (Gemini, ElevenLabs, Lark, DataForSEO…). Tự tạo
  key của bạn theo file `.env.example` trong skill tương ứng; **không** commit key.
- Skill `ego-browser` không có trong repo vì đi kèm ứng dụng ego lite.
- Các skill `lark-*` cần cài thêm `lark-cli`; skill `orca-*` cần ứng dụng Orca.
