#!/usr/bin/env bash
# Cài bộ skill vào máy: Claude Code, Codex, DeepSeek Harness (DSH).
# Dùng: ./install.sh            (cài tất cả agent)
#       ./install.sh claude     (chỉ Claude Code)
#       ./install.sh agents     (chỉ Codex + DSH: ~/.agents/skills)
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/skills"
TARGET="${1:-all}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$HOME/.agent-skills-backup/$STAMP"

[ -d "$SRC" ] || { echo "Không thấy thư mục skills/ cạnh install.sh"; exit 1; }

dests=()
case "$TARGET" in
    all)    dests=("$HOME/.agents/skills" "$HOME/.claude/skills") ;;
    claude) dests=("$HOME/.claude/skills") ;;
    agents|codex|dsh) dests=("$HOME/.agents/skills") ;;
    *) echo "Tham số không hợp lệ: $TARGET (all|claude|agents)"; exit 1 ;;
esac

for dest in "${dests[@]}"; do
    mkdir -p "$dest"
    count=0
    for skill in "$SRC"/*/; do
        name="$(basename "$skill")"
        if [ -e "$dest/$name" ] || [ -L "$dest/$name" ]; then
            mkdir -p "$BACKUP/$(basename "$(dirname "$dest")")"
            mv "$dest/$name" "$BACKUP/$(basename "$(dirname "$dest")")/$name"
        fi
        cp -R "$skill" "$dest/$name"
        count=$((count + 1))
    done
    echo "✓ Đã cài $count skill vào $dest"
done

[ -d "$BACKUP" ] && echo "ℹ Skill cũ trùng tên đã được sao lưu tại: $BACKUP"
echo "Khởi động lại Claude Code / Codex / DSH để nhận skill mới."
