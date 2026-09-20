#!/bin/bash
# ==============================================================================
# ⚡ Agent Skills Quick Installer
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/ilovefiniki/agent-skills/main/scripts/install.sh | bash -s -- init-project
#   curl -fsSL https://raw.githubusercontent.com/ilovefiniki/agent-skills/main/scripts/install.sh | bash -s -- all
# ==============================================================================

set -e

SKILL_NAME="${1:-all}"
REPO_URL="https://raw.githubusercontent.com/ilovefiniki/agent-skills/main"

echo "📦 Installing Agent Skill(s): $SKILL_NAME"

install_skill() {
    local target_skill="$1"
    echo "⬇️  Downloading skill: $target_skill..."

    # Support universal directory structure: .agents/skills/<skill> and .claude/skills/<skill>
    mkdir -p ".agents/skills/$target_skill"
    mkdir -p ".claude/skills/$target_skill" 2>/dev/null || true

    curl -fsSL "$REPO_URL/skills/$target_skill/SKILL.md" -o ".agents/skills/$target_skill/SKILL.md"
    cp ".agents/skills/$target_skill/SKILL.md" ".claude/skills/$target_skill/SKILL.md" 2>/dev/null || true

    # Download templates if any
    if [ "$target_skill" = "init-project" ]; then
        mkdir -p ".agents/skills/init-project/templates"
        curl -fsSL "$REPO_URL/skills/init-project/templates/post-commit.sh" -o ".agents/skills/init-project/templates/post-commit.sh"
        chmod +x ".agents/skills/init-project/templates/post-commit.sh"
    fi

    echo "✅ Successfully installed $target_skill into .agents/skills/$target_skill"
}

if [ "$SKILL_NAME" = "all" ]; then
    install_skill "init-project"
    install_skill "prod-readiness-audit"
else
    install_skill "$SKILL_NAME"
fi

echo ""
echo "🎉 Installation complete! The skills are now available to Claude Code, Antigravity, Gemini, and Cursor."
