# MCP: Model Context Protocol

# 🪜 Stage: AI Workflows

The "USB-C port" that lets AI tools plug into your design files and apps.

# 👋 Context

On its own, an AI model only knows what you paste into the chat. The **Model Context Protocol (MCP)** is an open standard, introduced by Anthropic in 2024 and now supported across the industry, that lets AI applications connect to other tools and data in a consistent way. Anthropic describes it as a USB-C port for AI: one standard plug, many devices.

An **MCP server** exposes a tool or a source of data (Figma, Notion, GitHub, a database). An **MCP client** (Claude, Claude Code, an IDE) connects to it. Once connected, the AI can read real context, such as the frames, components and variables in your Figma file, instead of guessing from a screenshot.

For designers, the most important example is Figma's **MCP server**: it lets Claude Code read your selected frames, styles and variables and turn them into code that uses your real design system. It also works the other way: well-named layers, components and variables give the AI much better context, so tidy files produce better results.

MCP gives AI access, and access needs care. Connect only what the task needs, check what each server can read and do, and approve actions yourself.

# 🎯 Goal / Learning Outcome

- Explain what MCP is: servers, clients and the context they share.
- Connect an AI tool to Figma (or another app) through MCP.
- See how well-structured design files give AI better context.
- Keep control: limit access and review what the AI does with it.

# 🛠️ Main Exercise

1. **Read the guide.** Open Figma's guide to its MCP server (in Resources) and note what it can read: frames, components, variables, styles.
2. **Prepare a frame.** Take one screen from your sprint. Name every layer, use Auto Layout and apply your styles and variables.
3. **Connect.** With your mentor, enable the Figma MCP server and connect it to Claude Code (or Claude Desktop).
4. **Ask for context, not magic.** Select the frame and ask: "Describe the structure, components and variables of the selected frame."
5. **Generate.** Ask for a simple HTML/CSS version of the frame that uses your variables.
6. **Compare.** Put the result next to your design. What did it get right? Where did messy layers or missing variables cause mistakes?
7. **Tidy and repeat.** Fix one problem in the Figma file and run it again. Note what improved.

# ⏱️ Estimated Duration

- ~1 hour (with your mentor for setup)

# 🏞️ Template

- 🔌 **MCP server:** Figma
- 🤖 **MCP client:** Claude Code / Claude Desktop
- 📥 **Context it read:** …
- ✅ **What it got right:** …
- ❌ **What went wrong, and why:** …
- 🧹 **What I fixed in the file:** …

# ⚡ Tips

- Garbage in, garbage out: Auto Layout, named layers, components and variables are what the AI reads.
- Start with read-only tasks ("describe", "list") before asking it to create anything.
- Only connect the servers you need for the task, and remove the ones you don't use.
- Never let an AI publish, send or delete without you reviewing it first.

# 🎥 Media

[https://www.youtube.com/watch?v=CQywdSdi5iA](https://www.youtube.com/watch?v=CQywdSdi5iA)

[https://www.youtube.com/watch?v=_gdtY2V3Zx8](https://www.youtube.com/watch?v=_gdtY2V3Zx8)

# 📚 Resources

[Introducing the Model Context Protocol – Anthropic](https://www.anthropic.com/news/model-context-protocol)

[Model Context Protocol – official site](https://modelcontextprotocol.io/)

[Guide to the Figma MCP Server – Figma Help](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server)

# ✅ Checklist

☐ Can explain MCP servers and clients in one sentence each

☐ Prepared a clean, well-named frame

☐ Connected an AI tool to Figma through MCP

☐ Compared the output with the design and fixed one problem in the file

# 📝 Summary

**MCP** is an open standard that connects AI tools to apps and data. For designers it means Claude can read your real Figma frames, components and variables, so the cleaner your file, the better the result. Give it only the access it needs, and review everything it does.
