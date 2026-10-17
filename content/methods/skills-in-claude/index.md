# Skills in Claude (SKILL.md)

# 🪜 Stage: AI Workflows

Write your process down once, so Claude follows it every time.

# 👋 Context

How many times have you typed the same instructions into a chat? "Use our brand colours. Write in British English. Always cite the interview." A **Skill** saves you from that.

A Skill is a folder with a file called **SKILL.md** inside it. The file starts with a short header (a **name** and a **description** of when to use it), followed by your instructions in plain Markdown. A Skill can also include templates, examples or scripts.

Skills use **progressive context disclosure**: Claude first reads only each Skill's name and description. When your request matches, it loads the full instructions, and only opens extra files if it needs them. So you can have many Skills without filling up the conversation.

Skills work in the Claude apps, Claude Code and the API. Anthropic provides ready-made ones (for example for Word, PowerPoint, Excel and PDF files), and you can write your own. In Claude Code, a **CLAUDE.md** file does a similar job for a whole project: instructions Claude reads at the start of every session.

For a design team, a Skill is a way to share a standard: your UX writing rules, your persona format, your design-review checklist.

# 🎯 Goal / Learning Outcome

- Explain what a Skill is, and how progressive disclosure keeps it light.
- Write a SKILL.md with a clear name, description and instructions.
- Test the Skill and improve it from the results.
- Know when a Skill helps, and when a one-off prompt is enough.

# 🛠️ Main Exercise

1. **Pick a repeated task** from your sprint, such as writing interview summaries, UX microcopy or a persona.
2. **Write the rules down.** List what a great result always has, and what it must never have.
3. **Create the file.** A folder named after the Skill, with a `SKILL.md` inside (see the template).
4. **Write the description carefully.** It decides when Claude uses the Skill: say what it does *and* when to use it.
5. **Add an example** of a great result, in the file or as a separate file in the folder.
6. **Install and test.** Upload the folder as a zip in Claude's settings under **Skills**, or put it in your project's `.claude/skills` folder for Claude Code. Run the same task three times.
7. **Improve.** Fix any rule Claude misread or ignored, and test again.

# ⏱️ Estimated Duration

- ~1 hour

# 🏞️ Template

```markdown
---
name: interview-summary
description: Summarises a UX interview transcript into key findings with quotes. Use when the user shares an interview transcript or notes and asks for a summary.
---

# Interview summary

## Always
- Start with the participant's goal, in one sentence.
- List 3–5 findings, each with a direct quote and a timestamp.
- Separate what they said from what they did.

## Never
- Invent quotes or fill gaps with assumptions.
- Suggest solutions; this is a summary, not ideation.

## Format
See example.md for a finished summary.
```

# ⚡ Tips

- One Skill, one job. Several small Skills beat one giant one.
- The description is the trigger: if Claude doesn't use your Skill, rewrite the description first.
- Write rules as specific instructions, not vague wishes: "Max 5 findings", not "keep it short".
- Keep personal data out of Skills; they're meant to be shared.
- You're still in the loop: a Skill makes output more consistent, not automatically correct.

# 🎥 Media

[https://www.youtube.com/watch?v=bjdBVZa66oU](https://www.youtube.com/watch?v=bjdBVZa66oU)

[https://www.youtube.com/watch?v=fOxC44g8vig](https://www.youtube.com/watch?v=fOxC44g8vig)

# 📚 Resources

[Agent Skills overview – Claude Docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

[Equipping agents for the real world with Agent Skills – Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

[Example Skills – Anthropic on GitHub](https://github.com/anthropics/skills)

# ✅ Checklist

☐ Chose one repeated task

☐ Wrote a SKILL.md with a name, a clear description and specific rules

☐ Added an example of a great result

☐ Tested it three times and improved it

# 📝 Summary

A **Skill** is a folder with a **SKILL.md** file: a name, a description of when to use it, and your instructions. Claude reads the description first and loads the rest only when it's needed. Skills turn your team's standards into something Claude follows every time, while you still check the result.
