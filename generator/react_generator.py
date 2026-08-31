def gen_react(llm, system, prd, plan):
    user = f"""Generate a complete React + Vite + Tailwind single page app.

PRD:
{prd}

Task Plan:
{plan}

Return the full code structure as markdown with file paths."""
    return llm.invoke([{"role": "system", "content": system}, {"role": "user", "content": user}]).content
