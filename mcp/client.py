from mcp.registry import registry
from mcp.connectors import github, vercel, figma, railway, render, gcp, google_console, google_analytics, slack, discord, notion, airtable, supabase, firebase, aws, stripe, twilio, resend, pinecone, brave

def auto_register():
    """Auto-register all 20 MCP connectors."""
    modules = [github, vercel, figma, railway, render, gcp, google_console, google_analytics, slack, discord, notion, airtable, supabase, firebase, aws, stripe, twilio, resend, pinecone, brave]
    for mod in modules:
        if hasattr(mod, "register"):
            mod.register(registry)

auto_register()
