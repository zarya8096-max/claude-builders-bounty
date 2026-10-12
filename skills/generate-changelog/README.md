# Generate Changelog Skill for Claude Code 📝

An automated changelog generator that inspects your git repository history, categorizes commits following the [Keep a Changelog](https://keepachangelog.com) standard, and writes a clean, versioned `CHANGELOG.md`.

---

## 🚀 Setup in 2 Steps

### Step 1: Install to your repository or global skills
```bash
mkdir -p skills/generate-changelog && curl -sSL https://raw.githubusercontent.com/zarya8096-max/claude-builders-bounty/main/skills/generate-changelog/changelog.sh -o skills/generate-changelog/changelog.sh && chmod +x skills/generate-changelog/changelog.sh
```

### Step 2: Generate CHANGELOG
```bash
bash skills/generate-changelog/changelog.sh "v1.0.0"
```

---

## 📋 Sample Output Generated on Real Git History

```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v1.0.0] - 2026-10-12 (initial release)

### Added
- Add initial README with bounty board ([`1aeae2a`] - claudebounty)
- Add opinionated Next.js 15 + SQLite SaaS template ([`6c506c0`] - zarya8096-max)
- Add pre-tool-use hook blocking destructive bash commands ([`5976eaf`] - zarya8096-max)

### Fixed
- Resolve unhandled edge cases in regex parser ([`d4e8a1b`] - zarya8096-max)
```

---

## 🧪 Testing

Run unit tests directly:
```bash
python3 test_changelog.py
```
