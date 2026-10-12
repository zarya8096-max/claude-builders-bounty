# Next.js 15 + SQLite SaaS Template Blueprint for Claude Code 🚀

An opinionated, production-ready `CLAUDE.md` architecture template designed for rapid SaaS development with Next.js 15 App Router, React 19, SQLite (`better-sqlite3` / Turso), and Drizzle ORM.

---

## 📦 How to Use

Drop `CLAUDE.md` into the root of any new or existing Next.js + SQLite repository:

```bash
curl -sSL https://raw.githubusercontent.com/zarya8096-max/claude-builders-bounty/main/templates/nextjs-sqlite-saas/CLAUDE.md -o CLAUDE.md
```

Claude Code will immediately understand your architecture, directory conventions, and coding rules without asking clarifying questions.

---

## ✨ Key Architectural Highlights

1. **Deterministic SQLite Production Setup:** Enforces WAL journal mode, 5000ms busy timeout, and foreign key integrity.
2. **Modular Architecture:** Clear boundary between Server Components (`app/`), Server Actions (`server/actions/`), and Queries (`server/queries/`).
3. **Opinionated Guardrails:** Eliminates common AI anti-patterns (no unnecessary `'use client'`, no Prisma bloat, no unauthenticated SQL).
