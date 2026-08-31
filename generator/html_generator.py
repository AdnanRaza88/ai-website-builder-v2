def gen_html(llm, system, prd, plan):
    user = f"""Generate a complete single-page website as a single HTML file.

PRD:
{prd}

Task Plan:
{plan}

Return ONLY the full HTML code, no markdown fences."""
    return llm.invoke([{"role": "system", "content": system}, {"role": "user", "content": user}]).content
