# Token Economics and Context

# 🪜 Stage: AI Workflows

Why long chats get worse, and how to feed AI only what it needs.

# 👋 Context

AI models don't read words, they read **tokens**: small chunks of text (in English, a token is roughly three-quarters of a word). Images and files are turned into tokens too. Everything in a conversation, your messages, the AI's replies and every file you've attached, takes up space in the model's **context window**, its working memory for that conversation.

Two things follow from that:

- **Tokens cost.** Paid plans and APIs are limited or billed by tokens, and the model's replies (output) usually cost more than what you send (input). Big files and long chats use up your allowance faster.
- **More context isn't always better.** As a conversation grows, the model's accuracy and recall drop, which Anthropic calls **context rot**. A two-hour chat full of old drafts often gives worse answers than a fresh one with a good summary.

**Context engineering** is the skill of curating what goes into that window: the right information, in the right amount, at the right time. For designers, that means clean briefs, short summaries and starting fresh at the right moment.

# 🎯 Goal / Learning Outcome

- Explain tokens, context windows and context rot in plain language.
- Recognise when a conversation has grown too long to be useful.
- Write a hand-over summary and restart with focused context.
- Choose what to include (and leave out) for a design task.

# 🛠️ Main Exercise

1. **Look at a long chat.** Open one of your longest AI conversations from the sprint. Find the point where the answers got worse or started ignoring earlier instructions.
2. **Write a hand-over summary.** In under 200 words: the goal, the decisions made so far, the constraints and what's left to do.
3. **Start fresh.** Open a new conversation with only your summary and the one file you need now.
4. **Compare.** Ask the same question in the old chat and the new one. Which answer is sharper?
5. **Make a context checklist** for your project: what every AI task needs (goal, user, constraints, style guide) and what it never needs (old drafts, whole transcripts when a summary will do).
6. **Use a Project.** Put the stable material (brief, personas, style guide) in a Claude Project's knowledge, so each new chat starts with it.

# ⏱️ Estimated Duration

- 45 minutes

# 🏞️ Template

**Hand-over summary**

- 🎯 **Goal:** …
- ✅ **Decided so far:** …
- 📏 **Constraints:** …
- ⏭️ **Next step:** …
- 📎 **Attached:** only what this step needs

# ⚡ Tips

- New task, new chat. Keep each conversation to one job.
- Summarise, don't paste: a 10-line summary of six interviews beats six full transcripts for most tasks.
- Crop screenshots to what matters; large images use many tokens.
- Put long-lived material in Project knowledge or a Skill, not in every message.
- When the AI starts forgetting your rules, that's your cue to restart with a summary.

# 🎥 Media

[https://www.youtube.com/watch?v=-QVoIxEpFkM](https://www.youtube.com/watch?v=-QVoIxEpFkM)

[https://www.youtube.com/watch?v=TeQDr4DkLYo](https://www.youtube.com/watch?v=TeQDr4DkLYo)

# 📚 Resources

[Context windows – Claude Docs](https://docs.claude.com/en/docs/build-with-claude/context-windows)

[Effective context engineering for AI agents – Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

[Plans and pricing – Anthropic](https://www.anthropic.com/pricing)

# ✅ Checklist

☐ Can explain tokens, context windows and context rot

☐ Wrote a hand-over summary of a long conversation

☐ Restarted with focused context and compared the results

☐ Made a context checklist for your project

# 📝 Summary

Everything in a conversation costs **tokens** and takes space in the **context window**, and too much context makes answers worse (**context rot**). Good **context engineering** means giving AI only what the task needs: one job per chat, short summaries instead of long pastes, and stable material in a Project or a Skill.
