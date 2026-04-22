"""
ADD THIS TO YOUR BOT FILE (gamble_match_bot.py)
================================================
1. Add these imports at the top if not already present:
   import secrets
   import json
   from pathlib import Path

2. Add the LOGIN_CODES dict and /login command below anywhere after the bot setup.

3. The website reads from data/login_codes.json to verify codes.
"""

import secrets

# ── Login codes store ──────────────────────────────────────────────
# { user_id_str: { "userId": str, "username": str, "code": str, "expiresAt": int (ms timestamp) } }
# Persisted to data/login_codes.json so the website can read it

def _get_login_codes() -> dict:
    p = DATA_DIR / "login_codes.json"
    if p.exists():
        try:
            with open(p) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def _save_login_codes(codes: dict):
    try:
        with open(DATA_DIR / "login_codes.json", "w") as f:
            json.dump(codes, f, indent=2)
    except Exception as e:
        log.warning(f"Could not save login codes: {e}")

def _clean_expired_codes():
    """Remove expired codes to keep the file clean."""
    codes = _get_login_codes()
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    cleaned = {k: v for k, v in codes.items() if v.get("expiresAt", 0) > now_ms}
    if len(cleaned) != len(codes):
        _save_login_codes(cleaned)

# ── /login slash command ───────────────────────────────────────────
@tree.command(name="login", description="Get a one-time login code for the GambleMatch website")
async def login_cmd(interaction: discord.Interaction):
    uid      = interaction.user.id
    username = interaction.user.display_name

    # Clean up old codes first
    _clean_expired_codes()

    # Generate a 6-character alphanumeric code (uppercase)
    code = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))

    # Expires in 5 minutes
    expires_at_ms = int((datetime.now(timezone.utc).timestamp() + 300) * 1000)

    # Save code
    codes = _get_login_codes()
    codes[str(uid)] = {
        "userId":    str(uid),
        "username":  username,
        "code":      code,
        "expiresAt": expires_at_ms,
    }
    _save_login_codes(codes)

    # DM the code to the user
    try:
        dm = await interaction.user.create_dm()
        e = discord.Embed(
            title="🔐  Your GambleMatch Login Code",
            description=(
                f"Use this code to sign in at the website:\n\n"
                f"## `{code}`\n\n"
                f"⏳ **Expires in 5 minutes** — single use only.\n\n"
                f"**Steps:**\n"
                f"1. Go to **gamblematch.vercel.app/login**\n"
                f"2. Enter your Discord ID: `{uid}`\n"
                f"3. Enter the code above\n\n"
                f"🔒 Never share this code with anyone."
            ),
            color=0x5865F2,
            timestamp=datetime.now(timezone.utc),
        )
        e.set_footer(text="GambleMatch · Code is single-use and expires in 5 minutes")
        await dm.send(embed=e)

        # Confirm in the channel (ephemeral)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="✅  Code Sent!",
                description=(
                    f"A login code has been sent to your DMs!\n"
                    f"Go to **gamblematch.vercel.app/login** and enter:\n"
                    f"• Your Discord ID: `{uid}`\n"
                    f"• The 6-digit code from your DMs\n\n"
                    f"⏳ Code expires in **5 minutes**."
                ),
                color=0x57f287,
            ),
            ephemeral=True,
        )
    except discord.Forbidden:
        # Can't DM — show the code in the ephemeral message instead
        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️  DMs Closed — Here's Your Code",
                description=(
                    f"Enable DMs from server members to receive codes normally.\n\n"
                    f"Your one-time code: **`{code}`**\n"
                    f"Your Discord ID: `{uid}`\n\n"
                    f"Go to **gamblematch.vercel.app/login** and enter these.\n"
                    f"⏳ Expires in **5 minutes**. Don't share this with anyone!"
                ),
                color=0xfee75c,
            ),
            ephemeral=True,
        )
