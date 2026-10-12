# Weekly Dev Summary with n8n + Claude API 📊

An automated n8n workflow that triggers every Friday at 5:00 PM, collects repository commits and closed issues from GitHub, synthesizes a narrative summary using Claude 3.5 Sonnet, and publishes the report to Discord or Slack.

---

## 🚀 Setup in 4 Steps

1. **Import Workflow:** In your n8n dashboard, click **Workflows** ➔ **Import from File** and select `weekly_dev_summary_n8n.json`.
2. **Set Configuration:** Double-click the **Workflow Configuration** node and set:
   - `repo_owner`: Target GitHub organization/owner
   - `repo_name`: Target repository name
   - `language`: `EN` or `FR`
   - `webhook_url`: Your Discord or Slack incoming webhook URL
3. **Configure API Credentials:** Set `ANTHROPIC_API_KEY` in your n8n environment variables or directly in the HTTP Request node header.
4. **Activate:** Toggle the workflow switch to **Active**. It will automatically execute every Friday at 17:00 (or click **Test Workflow** to run immediately).

---

## 📋 Sample Narrative Output Delivered

> 📢 **Weekly Dev Summary: claude-builders-bounty/claude-builders-bounty**
>
> 🚀 **Highlight of the Week:**  
> Shipped 4 core ecosystem modules expanding developer automation, including safety pre-tool hooks, an automated changelog generator, and full Next.js 15 SQLite SaaS scaffolding.
>
> 🛠️ **Shipped Features & Bugfixes:**  
> • `feat(hooks)`: Intercept dangerous bash invocations before execution (#3)  
> • `feat(templates)`: Deliver production-ready Next.js 15 + SQLite CLAUDE.md (#2)  
> • `feat(skills)`: Git history changelog categorizer adhering to Keep a Changelog (#1)  
> • `feat(agents)`: Automated Pull Request reviewer CLI and GitHub Action (#4)  
>
> 📈 **Momentum for Next Sprint:**  
> Core developer tooling is established. Next sprint focuses on community distribution and webhook integrations.
