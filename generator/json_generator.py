def gen_json(llm, system, prd, plan):
    user = f"""Generate a structured JSON representation of the website.

PRD:
{prd}

Task Plan:
{plan}

Return ONLY valid JSON."""
    return llm.invoke([{"role": "system", "content": system}, {"role": "user", "content": user}]).content
