# Connectors in Claude

# 🪜 Stage: AI Workflows

Let Claude read your research where it lives, safely.

# 👋 Context

Your sprint lives in many places: interview notes in Google Drive, a board in Notion, screens in Figma, messages in Slack. **Connectors** let Claude access those apps directly, search your files and, if you allow it, take actions in them, so you don't have to copy and paste everything into the chat.

Connectors are built on **MCP** (see [MCP: Model Context Protocol](mcp.html)). You add them from the **Connectors Directory** in Claude (from a chat, click **+** → Connectors, or go to Customize → Connectors), sign in to the service and choose what to allow. Claude inherits your permissions: if you can't see a file, Claude can't either.

That access is powerful, so it needs judgement. A connector that can read your whole Drive can also read things that have nothing to do with your sprint, and a connector that can write can change or send things in your name.

# 🎯 Goal / Learning Outcome

- Explain what a connector is and how it relates to MCP.
- Connect one app to Claude and use it in a real sprint task.
- Check what a connector can read and do before you enable it.
- Keep a human in the loop for any action that changes or sends something.

# 🛠️ Main Exercise

1. **Choose one app** your team uses for the sprint, such as Google Drive or Notion.
2. **Read its directory page.** Note what it can read and what it can do (read-only, or write too).
3. **Connect it** and sign in. Limit access where the app lets you (for example, one shared folder).
4. **Do a real task.** Ask Claude: "Find our interview notes from this week and list every pain point mentioned, with the file and participant it came from."
5. **Check the sources.** Open two of the files it cited. Are the findings accurate?
6. **Try one action, carefully.** If the connector can write, ask it to create a draft (not send or publish), and review it yourself.
7. **Disconnect** anything you don't need any more.

# ⏱️ Estimated Duration

- 30–45 minutes

# 🏞️ Template

- 🔗 **Connector:** …
- 👀 **What it can read:** …
- ✍️ **What it can do:** …
- 🧪 **Task I gave it:** …
- ✅ **Sources checked:** …
- 🙋 **Actions I approved myself:** …

# ⚡ Tips

- Connect the minimum: one folder or workspace is safer than your whole account.
- Ask Claude to cite the file for every claim, then spot-check them.
- Prefer drafts: let Claude prepare, and you send, publish or delete.
- Never connect accounts containing participants' personal data without their consent.

# 🎥 Media

[https://www.youtube.com/watch?v=FpRNId-jeTQ](https://www.youtube.com/watch?v=FpRNId-jeTQ)

# 📚 Resources

[Use connectors to extend Claude's capabilities – Claude Help Center](https://support.claude.com/en/articles/11176164-pre-built-web-connectors-using-remote-mcp)

[Claude Connectors Directory](https://claude.com/connectors)

# ✅ Checklist

☐ Read what the connector can read and do before connecting

☐ Limited its access to what the sprint needs

☐ Used it for a real task and checked the sources

☐ Approved every action yourself

# 📝 Summary

**Connectors** let Claude search and act in the apps where your work lives, using MCP and your own permissions. Connect only what you need, ask for sources, and keep every send, publish or delete decision in human hands.
