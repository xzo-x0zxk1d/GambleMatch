"""
GambleMatch Discord Bot — Ultimate Edition + Website Sync
==========================================================
pip install discord.py aiohttp
python gamble_match_bot.py

All data is persisted to JSON files in ./data/
Shop + richlist is pushed to your Vercel website every 60 seconds.
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands, ui
import asyncio, random, string, logging, json, os, aiohttp
from datetime import datetime, timezone
from typing import Optional
from pathlib import Path
import sys
import secrets

# ══════════════════════════════════════════════════════════════════
#  CONFIG  — loaded from bot.env (never hardcode secrets in source)
# ══════════════════════════════════════════════════════════════════
def _load_env(filepath: str = "bot.env"):
    """Load key=value pairs from a .env file into os.environ."""
    p = Path(filepath)
    if p.exists():
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                if "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())

_load_env()

BOT_TOKEN   = os.environ.get("BOT_TOKEN", "")
WEBSITE_URL = os.environ.get("WEBSITE_URL", "https://gamblematch.vercel.app")
SYNC_SECRET = os.environ.get("SYNC_SECRET", "")
GUILD_ID    = 1492847247124070520

if not BOT_TOKEN:
    print("\u274c  BOT_TOKEN is not set. Add it to bot.env or set the environment variable.")
    sys.exit(1)

if not SYNC_SECRET:
    print("\u26a0\ufe0f  SYNC_SECRET is not set \u2014 website sync will fail authentication.")

MATCHES_CHANNEL      = "matchs🎰"
FINDG_CHANNEL_ID     = 1492935616462328050
POINTS_CHANNEL_ID    = 1493245892533293096
SUPPLIER_ROLE_ID     = 1493245480367423609
CODE_MAKER_ROLE_ID   = 1494658741520433222
CHANGELOG_CHANNEL_ID = 1493247133661401228
WEBHOOK_URL          = "https://discord.com/api/webhooks/1493247363010007242/kU0lsQtIvcGZUUMA77J4WjvaIOHa_e7lXLxyTawPT2p94XIfk3w3hjd0Ifv_gAmztxU6"
WELCOME_CHANNEL_ID   = 1493245892533293096

EMOJI_WALLET   = "<:GW:1495092237250461718>"
EMOJI_GEM      = "<:GambleGem:1495092299640738004> "

MATCH_TIMEOUT        = 120
COOLDOWN_SECONDS     = 15
POINTS_WIN_MULT      = 2.0
MAX_POINTS_WALLET    = 50_000_000_000
LEADERBOARD_SIZE     = 10

DAILY_BASE           = 500
DAILY_STREAK_BONUS   = 150
DAILY_MAX            = 5_000

MSG_REWARD_EVERY     = 500
MSG_REWARD_AMOUNT    = 2_000

INVITE_REWARD_PTS    = 5_000

ROOM_HOURLY_REWARD = {
    "bronze":   50,
    "silver":   150,
    "gold":     300,
    "platinum": 600,
    "ruby":     1_200,
    "emerald":  2_500,
    "lithium":  5_000,
}

DATA_DIR             = Path("./data")
BOT_VERSION          = "5.1.0"

ROOM_REGISTER_CHANNEL_ID = 1494667681796980897
ROOMS_CATEGORY_NAME      = "🏠 Rooms"

INVITE_LUCK_TABLE = [
    (1,  4,  0.1),
    (5,  9,  0.25),
    (10, 19, 0.5),
    (20, 34, 0.75),
    (35, 49, 1.0),
    (50, 74, 1.25),
    (75, 99, 1.5),
    (100, 149, 1.75),
    (150, 199, 2.0),
    (200, 999, 2.5),
]
MAX_INVITE_LUCK_BONUS = 2.5

VIP_TIERS = {
    "vip":   {"name": "VIP",   "emoji": "💎", "price": 100_000_000,   "luck_bonus": 1.5, "hourly_reward": 10_000},
    "vvip":  {"name": "VVIP",  "emoji": "👑", "price": 500_000_000,   "luck_bonus": 2.5, "hourly_reward": 50_000},
    "vvvip": {"name": "VVVIP", "emoji": "🌟", "price": 2_000_000_000, "luck_bonus": 4.0, "hourly_reward": 150_000},
}

PROMO_MESSAGES = [
    "use /value to exchange your brainrots for gems 💎",
    "buy vip, vvip, vvvip channels from tickets! <#1492937175690383431>",
]

TIPS = [
    "💡 Use `/daily` every day to stack up free points!",
    "💡 `/bomb` has a Cash Out button — don't be greedy!",
    "💡 Higher room tier = better luck multiplier on casino games.",
    "💡 Invite friends to earn permanent luck bonuses.",
    "💡 `/blackjack` pays 2× — stand on 17+ against dealer.",
    "💡 `/slots` — three 7️⃣s pays 10× your wager. Jackpot!",
    "💡 Rep matters — players with more ⭐ are more trusted.",
    "💡 Challenge a specific player with `/challenge @user`.",
    "💡 Your room is visible to everyone — flex that tier!",
    "💡 Streaks boost your rank faster — keep winning!",
    "💡 `/mines` is lower risk than `/bomb` — great for grinding.",
    "💡 Cross-trade in `/findg` lets you match with different games.",
    "💡 Best of 3/5/7 is drawn randomly — adapt your strategy!",
    "💡 Shop items are limited — buy before stock runs out!",
    "💡 Use `/give` to transfer points to friends.",
]

# ══════════════════════════════════════════════════════════════════
#  LOGGING
# ══════════════════════════════════════════════════════════════════
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("GambleMatch")

# ══════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════
GAME_EMOJIS  = {"sab":"🗡️","bloxfruit":"🍎","gag":"🃏","mm2":"🔪","robux":"💎","other":"🎲"}
MODE_EMOJIS  = {"roll":"🎲","coinflip":"🪙","rps":"✊"}
RANK_TIERS   = [
    (0,   "🪨 Unranked",  0x8a8a8a),
    (5,   "🥉 Bronze",    0xcd7f32),
    (15,  "🥈 Silver",    0xc0c0c0),
    (30,  "🥇 Gold",      0xffd700),
    (50,  "💠 Platinum",  0x00bcd4),
    (75,  "💎 Diamond",   0x1e88e5),
    (100, "👑 Legendary", 0xff6f00),
]
GAMES = ["sab","bloxfruit","gag","mm2","robux","other"]

BOMB_GRID_SIZE   = 12
BOMB_COUNT       = 3
BOMB_LOSS_PCT    = 0.2
DIAMOND_GAIN_PCT = 0.08
NOTHING_CELLS    = 5

MINES_GRID_SIZE  = 9
MINES_GEMS       = 7
MINES_GAIN_PCT   = 0.05

SLOTS_SYMBOLS = ["🍒","🍋","🍊","⭐","💎","7️⃣"]
SLOTS_WEIGHTS = [30,  25,  20,  15,   8,    2  ]
SLOTS_PAYOUTS = {
    "7️⃣7️⃣7️⃣": 5.0,
    "💎💎💎":  2.5,
    "⭐⭐⭐":    1.5,
    "🍊🍊🍊":   1.0,
    "🍋🍋🍋":   0.8,
    "🍒🍒🍒":   0.6,
}
SLOTS_TWO_PAYOUT = 0.25

BJ_PAYOUT = 1.2

# ══════════════════════════════════════════════════════════════════
#  JSON PERSISTENCE
# ══════════════════════════════════════════════════════════════════
DATA_DIR.mkdir(exist_ok=True)

def _path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"

def load_json(name: str, default):
    p = _path(name)
    if p.exists():
        try:
            with open(p, "r") as f:
                return json.load(f)
        except Exception as e:
            log.warning(f"Failed to load {name}.json: {e}")
    return default

def save_json(name: str, data):
    try:
        with open(_path(name), "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log.error(f"Failed to save {name}.json: {e}")

# ── Load all state ─────────────────────────────────────────────────
_stats_raw      = load_json("stats",         {})
_points_raw     = load_json("points",        {})
_rep_raw        = load_json("reputation",    {})
_daily_raw      = load_json("daily",         {})
_history_raw    = load_json("history",       [])
_shop_raw       = load_json("shop",          {"items": [], "counter": 1})
_purchase_raw   = load_json("purchases",     [])
_tickets_raw    = load_json("tickets",       [])
_value_subs_raw = load_json("value_submissions", [])

stats:         dict = {int(k): v for k, v in _stats_raw.items()}
points:        dict = {int(k): v for k, v in _points_raw.items()}
reputation:    dict = {int(k): v for k, v in _rep_raw.items()}
daily_claimed: dict = {int(k): v for k, v in _daily_raw.items()}
match_history: list = _history_raw
shop_items:    list = _shop_raw.get("items", [])
shop_id_counter: int = _shop_raw.get("counter", 1)
purchase_log:  list = _purchase_raw
tickets:       list = _tickets_raw
value_submissions: list = _value_subs_raw

LAST_CHANGELOG_VER: str = load_json("meta", {}).get("last_changelog_ver", "")

_rooms_raw      = load_json("rooms", {"rooms": {}, "register_msg_id": None})
rooms:          dict = _rooms_raw.get("rooms", {})
register_msg_id: Optional[int] = _rooms_raw.get("register_msg_id")

_bank_raw       = load_json("bank", {})
bank:           dict = {int(k): v for k, v in _bank_raw.items()}

_msg_raw        = load_json("msg_counts", {})
msg_counts:     dict = {int(k): v for k, v in _msg_raw.items()}

_streak_raw     = load_json("daily_streak", {})
daily_streak:   dict = {int(k): v for k, v in _streak_raw.items()}

_codes_raw      = load_json("redeem_codes", {})
redeem_codes:   dict = _codes_raw

_inv_raw        = load_json("invite_counts", {})
invite_counts:  dict = {int(k): v for k, v in _inv_raw.items()}

_vip_raw        = load_json("vip_rooms", {})
vip_rooms:      dict = {int(k): v for k, v in _vip_raw.items()}

promo_cooldowns: dict = {}

queue:          list = []
active_matches: dict = {}
cooldowns:      dict = {}
game_cooldowns: dict = {}
invite_cache:   dict = {}

def save_all():
    save_json("stats",         {str(k): v for k, v in stats.items()})
    save_json("points",        {str(k): v for k, v in points.items()})
    save_json("reputation",    {str(k): v for k, v in reputation.items()})
    save_json("daily",         {str(k): v for k, v in daily_claimed.items()})
    save_json("history",       match_history)
    save_json("shop",          {"items": shop_items, "counter": shop_id_counter})
    save_json("purchases",     purchase_log)
    save_json("tickets",       tickets)
    save_json("value_submissions", value_submissions)
    save_json("rooms",         {"rooms": rooms, "register_msg_id": register_msg_id})
    save_json("bank",          {str(k): v for k, v in bank.items()})
    save_json("msg_counts",    {str(k): v for k, v in msg_counts.items()})
    save_json("daily_streak",  {str(k): v for k, v in daily_streak.items()})
    save_json("redeem_codes",  redeem_codes)
    save_json("invite_counts", {str(k): v for k, v in invite_counts.items()})
    save_json("vip_rooms",     {str(k): v for k, v in vip_rooms.items()})

# ══════════════════════════════════════════════════════════════════
#  WEBSITE SYNC  — pushes shop + richlist to Vercel every 60s
# ══════════════════════════════════════════════════════════════════
async def push_to_website(guild: discord.Guild):
    """
    Builds the shop payload and richlist payload then POSTs them to
    POST /api/sync on the website.  The website stores them in memory
    and serves them via GET /api/shop and GET /api/richlist.
    """
    # ── Build shop payload ────────────────────────────────────────
    shop_payload = []
    for item in shop_items:
        shop_payload.append({
            "id":          item["id"],
            "name":        item["name"],
            "description": item["description"],
            "price":       item["price"],
            "stock":       item["stock"],
            "emoji":       item.get("emoji") or _game_to_emoji(item["name"]),
            "game":        item.get("game")  or _guess_game(item["name"]),
            "image_url":   item.get("image_url"),
        })

    # ── Build richlist payload ────────────────────────────────────
    # Sort all users by wallet+bank total descending, take top 10
    combined = {}
    for uid, bal in points.items():
        combined[uid] = bal + bank.get(uid, 0)
    sorted_rich = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:10]

    richlist_payload = []
    for rank, (uid, bal) in enumerate(sorted_rich, 1):
        member = guild.get_member(uid)
        if not member:
            continue
        avatar_hash = member.avatar.key if member.avatar else None
        richlist_payload.append({
            "id":         str(uid),
            "username":   member.name,
            "globalName": member.display_name,
            "avatar":     avatar_hash,
            "balance":    bal,
            "rank":       rank,
        })

    # ── POST to website ───────────────────────────────────────────
    url = f"{WEBSITE_URL}/api/sync"
    payload = {"shop": shop_payload, "richlist": richlist_payload}
    headers = {
        "Content-Type":  "application/json",
        "x-sync-secret": SYNC_SECRET,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    log.info(f"[SYNC] Pushed {len(shop_payload)} items + {len(richlist_payload)} players to website")
                else:
                    text = await resp.text()
                    log.warning(f"[SYNC] Website returned {resp.status}: {text}")
    except Exception as e:
        log.warning(f"[SYNC] Failed to push to website: {e}")


def _game_to_emoji(name: str) -> str:
    n = name.lower()
    if any(x in n for x in ["fruit", "blox"]): return "🍎"
    if any(x in n for x in ["knife", "mm2", "murder"]): return "🔪"
    if any(x in n for x in ["pet", "sim"]): return "🐾"
    if "robux" in n: return "💎"
    if "luck" in n: return "🍀"
    if any(x in n for x in ["halo", "gag", "garden"]): return "🌈"
    if any(x in n for x in ["sab", "blade", "sword"]): return "⚔️"
    return "🎮"


def _guess_game(name: str) -> str:
    n = name.lower()
    if any(x in n for x in ["fruit", "blox", "dragon", "soul guitar"]): return "Blox Fruits"
    if any(x in n for x in ["knife", "mm2", "murder", "godly"]): return "MM2"
    if any(x in n for x in ["pet", "huge", "sim"]): return "Pet Sim X"
    if "robux" in n: return "Robux"
    if any(x in n for x in ["sab", "super animal"]): return "SAB"
    if any(x in n for x in ["halo", "gag", "grow", "garden"]): return "GAG"
    if "luck" in n or "multiplier" in n: return "GambleMatch"
    return "Other"

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def gen_id(n=6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))

def get_stats(uid: int) -> dict:
    if uid not in stats:
        stats[uid] = {"wins":0,"losses":0,"games_played":0,"rounds_won":0,"rounds_lost":0,"streak":0,"best_streak":0}
    return stats[uid]

def get_rep(uid: int) -> int:
    return reputation.get(uid, 0)

def add_rep(uid: int, d: int):
    reputation[uid] = reputation.get(uid, 0) + d
    save_json("reputation", {str(k): v for k, v in reputation.items()})

def get_points(uid: int) -> int:
    return points.get(uid, 0)

def add_points(uid: int, amount: int):
    current = points.get(uid, 0)
    new_total = current + amount
    if new_total > 1_000_000_000:
        tax = int(amount * 0.05)
        new_total -= tax
    if new_total > MAX_POINTS_WALLET:
        points[uid] = MAX_POINTS_WALLET
    else:
        points[uid] = new_total
    save_json("points", {str(k): v for k, v in points.items()})

def spend_points(uid: int, amount: int) -> bool:
    if points.get(uid, 0) < amount:
        return False
    points[uid] -= amount
    save_json("points", {str(k): v for k, v in points.items()})
    return True

def get_bank(uid: int) -> int:
    return bank.get(uid, 0)

def deposit_bank(uid: int, amount: int) -> bool:
    if points.get(uid, 0) < amount:
        return False
    points[uid] = points.get(uid, 0) - amount
    bank[uid]   = bank.get(uid, 0) + amount
    save_json("points", {str(k): v for k, v in points.items()})
    save_json("bank",   {str(k): v for k, v in bank.items()})
    return True

def withdraw_bank(uid: int, amount: int) -> bool:
    if bank.get(uid, 0) < amount:
        return False
    bank[uid]   = bank.get(uid, 0) - amount
    points[uid] = points.get(uid, 0) + amount
    save_json("bank",   {str(k): v for k, v in bank.items()})
    save_json("points", {str(k): v for k, v in points.items()})
    return True

def is_room_channel(channel_id: int) -> bool:
    return str(channel_id) in rooms

def get_room_owner_id(channel_id: int) -> Optional[int]:
    r = rooms.get(str(channel_id))
    return r["owner_id"] if r else None

def fmt_bal(amount: int) -> str:
    return f"{EMOJI_GEM} **{amount:,}**"

def fmt_wallet(amount: int) -> str:
    return f"{EMOJI_WALLET} {EMOJI_GEM} **{amount:,}**"

def is_code_maker(member: discord.Member) -> bool:
    return any(r.id == CODE_MAKER_ROLE_ID for r in member.roles)

def get_rank(wins: int) -> tuple:
    r = (RANK_TIERS[0][1], RANK_TIERS[0][2])
    for t, n, c in RANK_TIERS:
        if wins >= t: r = (n, c)
    return r

def rand_best_of() -> int:
    return random.choice([3, 5, 7])

def rounds_needed(bo: int) -> int:
    return (bo // 2) + 1

def find_opponent(user, game, cross_trade):
    for e in queue:
        if e["user"].id == user.id: continue
        if e["game"] == game: return e
        if cross_trade and e["cross_trade"]: return e
    return None

def build_score_bar(match: dict) -> str:
    p1, p2 = match["p1"], match["p2"]
    need = rounds_needed(match["best_of"])
    s1, s2 = match["score"][p1.id], match["score"][p2.id]
    return f"{'🟩'*s1}{'⬛'*(need-s1)} **{p1.display_name}** `{s1}–{s2}` **{p2.display_name}** {'🟩'*s2}{'⬛'*(need-s2)}"

def is_supplier(member: discord.Member) -> bool:
    return any(r.id == SUPPLIER_ROLE_ID for r in member.roles)

def get_shop_item(item_id: int) -> Optional[dict]:
    return next((i for i in shop_items if i["id"] == item_id), None)

def check_game_cooldown(uid: int, seconds: int = 5) -> Optional[int]:
    now = datetime.now(timezone.utc)
    if uid in game_cooldowns:
        elapsed = (now - game_cooldowns[uid]).total_seconds()
        if elapsed < seconds:
            return int(seconds - elapsed)
    game_cooldowns[uid] = now
    return None

# ══════════════════════════════════════════════════════════════════
#  BOT INIT
# ══════════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.invites = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ══════════════════════════════════════════════════════════════════
#  LOGIN COMMAND
# ══════════════════════════════════════════════════════════════════
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
    codes = _get_login_codes()
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    cleaned = {k: v for k, v in codes.items() if v.get("expiresAt", 0) > now_ms}
    if len(cleaned) != len(codes):
        _save_login_codes(cleaned)

@tree.command(name="login", description="Get a one-time login code for the GambleMatch website")
async def login_cmd(interaction: discord.Interaction):
    uid      = interaction.user.id
    username = interaction.user.display_name
    _clean_expired_codes()
    code = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))
    expires_at_ms = int((datetime.now(timezone.utc).timestamp() + 300) * 1000)
    codes = _get_login_codes()
    codes[str(uid)] = {
        "userId":    str(uid),
        "username":  username,
        "code":      code,
        "expiresAt": expires_at_ms,
    }
    _save_login_codes(codes)
    try:
        dm = await interaction.user.create_dm()
        e = discord.Embed(
            title="🔐  Your GambleMatch Login Code",
            description=(
                f"Use this code to sign in at the website:\n\n"
                f"## `{code}`\n\n"
                f"⏳ **Expires in 5 minutes** — single use only.\n\n"
                f"**Steps:**\n"
                f"1. Go to **{WEBSITE_URL}/login**\n"
                f"2. Enter your Discord ID: `{uid}`\n"
                f"3. Enter the code above\n\n"
                f"🔒 Never share this code with anyone."
            ),
            color=0x5865F2,
            timestamp=datetime.now(timezone.utc),
        )
        e.set_footer(text="GambleMatch · Code is single-use and expires in 5 minutes")
        await dm.send(embed=e)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="✅  Code Sent!",
                description=(
                    f"A login code has been sent to your DMs!\n"
                    f"Go to **{WEBSITE_URL}/login** and enter:\n"
                    f"• Your Discord ID: `{uid}`\n"
                    f"• The 6-digit code from your DMs\n\n"
                    f"⏳ Code expires in **5 minutes**."
                ),
                color=0x57f287,
            ),
            ephemeral=True,
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️  DMs Closed — Here's Your Code",
                description=(
                    f"Enable DMs from server members to receive codes normally.\n\n"
                    f"Your one-time code: **`{code}`**\n"
                    f"Your Discord ID: `{uid}`\n\n"
                    f"Go to **{WEBSITE_URL}/login** and enter these.\n"
                    f"⏳ Expires in **5 minutes**. Don't share this!"
                ),
                color=0xfee75c,
            ),
            ephemeral=True,
        )

# ══════════════════════════════════════════════════════════════════
#  WEBHOOK
# ══════════════════════════════════════════════════════════════════
async def send_changelog(title: str, description: str, color: int = 0x5865F2, fields: list = None):
    payload = {
        "embeds": [{
            "title": f"📢  {title}",
            "description": description,
            "color": color,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "footer": {"text": f"GambleMatch v{BOT_VERSION}"},
            "fields": fields or [],
        }]
    }
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        log.warning(f"Webhook failed: {e}")

# ══════════════════════════════════════════════════════════════════
#  CHANNEL GUARDS
# ══════════════════════════════════════════════════════════════════
def E(title="", desc="", color=0x5865F2, **kw) -> discord.Embed:
    return discord.Embed(title=title, description=desc, color=color, **kw)

def findg_only():
    async def predicate(i: discord.Interaction) -> bool:
        if i.channel_id != FINDG_CHANNEL_ID:
            await i.response.send_message(embed=E("❌  Wrong Channel",f"Use /findg in <#{FINDG_CHANNEL_ID}>.",0xed4245),ephemeral=True); return False
        return True
    return app_commands.check(predicate)

def casino_only():
    async def predicate(i: discord.Interaction) -> bool:
        if i.channel_id == POINTS_CHANNEL_ID or is_room_channel(i.channel_id):
            return True
        await i.response.send_message(embed=E(
            "❌  Wrong Channel",
            f"Casino commands only work in <#{POINTS_CHANNEL_ID}> or inside your room channel.",
            0xed4245,
        ), ephemeral=True)
        return False
    return app_commands.check(predicate)

# ══════════════════════════════════════════════════════════════════
#  EMBED BUILDERS
# ══════════════════════════════════════════════════════════════════
def embed_match_intro(m: dict) -> discord.Embed:
    p1, p2 = m["p1"], m["p2"]
    rn1, rc1 = get_rank(get_stats(p1.id)["wins"])
    rn2, _   = get_rank(get_stats(p2.id)["wins"])
    bo, need = m["best_of"], rounds_needed(m["best_of"])
    e = discord.Embed(
        title=f"⚔️ {GAME_EMOJIS.get(m['game'],'🎲')} Epic Duel — `{m['match_id']}`",
        description=f"🎯 **Best of {bo}** randomly selected!\n🏆 First to **{need}** victories claims glory.\n🔄 Cross-trade: {'✅ Enabled' if m['cross_trade'] else '❌ Disabled'}",
        color=rc1, timestamp=datetime.now(timezone.utc))
    e.add_field(name=f"🔵 Challenger {p1.display_name}", value=f"🎁 Offering: `{m['offer1']}`\n{rn1}", inline=True)
    e.add_field(name="⚔️", value="\u200b", inline=True)
    e.add_field(name=f"🔴 Defender {p2.display_name}", value=f"🎁 Offering: `{m['offer2']}`\n{rn2}", inline=True)
    e.set_footer(text=f"GambleMatch Match ID: {m['match_id']} — May the best strategist win!")
    return e

def embed_round_result(m: dict, winner: discord.Member, mode: str, detail: str) -> discord.Embed:
    p1, p2 = m["p1"], m["p2"]
    need   = rounds_needed(m["best_of"])
    s1, s2 = m["score"][p1.id], m["score"][p2.id]
    e = discord.Embed(title=f"{MODE_EMOJIS.get(mode,'🎲')} Round {m['round']-1} Victory! {winner.display_name} Triumphs!", description=detail, color=0x57f287)
    e.add_field(name="🏆 Scoreboard", value=f"{'🟩'*s1}{'⬛'*(need-s1)}  **{p1.display_name}**  `{s1}`\n{'🟩'*s2}{'⬛'*(need-s2)}  **{p2.display_name}**  `{s2}`", inline=False)
    return e

def embed_match_winner(m: dict, winner: discord.Member, loser: discord.Member) -> discord.Embed:
    rn, rc = get_rank(get_stats(winner.id)["wins"])
    ws     = get_stats(winner.id)
    offer  = m["offer1"] if winner.id == m["p1"].id else m["offer2"]
    e = discord.Embed(title="🏆 Epic Victory! Match Concluded!", description=f"## {winner.mention} Emerges Victorious!\n💰 Prize Pool: `{offer}`", color=rc, timestamp=datetime.now(timezone.utc))
    e.add_field(name="🎮 Game Mode",  value=f"{GAME_EMOJIS.get(m['game'],'🎲')} {m['game'].upper()}", inline=True)
    e.add_field(name="🎯 Best of",    value=str(m["best_of"]), inline=True)
    e.add_field(name="⭐ Rank",       value=rn, inline=True)
    e.add_field(name="📊 Final Score",value=f"**{m['score'][m['p1'].id]}** – {m['score'][m['p2'].id]}", inline=True)
    e.add_field(name="🎯 Win Rate",   value=_winrate(winner.id), inline=True)
    e.add_field(name="🔥 Win Streak", value=f"{ws['streak']} (best: {ws['best_streak']})", inline=True)
    e.set_thumbnail(url=winner.display_avatar.url)
    return e

def embed_loser_result(m: dict, winner: discord.Member, loser: discord.Member) -> discord.Embed:
    ls = get_stats(loser.id); rn, _ = get_rank(ls["wins"])
    e = discord.Embed(title="💀 Defeat! Better Luck Next Time", description=f"**{winner.display_name}** claimed the victory.", color=0xed4245, timestamp=datetime.now(timezone.utc))
    e.add_field(name="⭐ Rank",        value=rn,                    inline=True)
    e.add_field(name="🎯 Win Rate",    value=_winrate(loser.id),    inline=True)
    e.add_field(name="🌟 Reputation",  value=str(get_rep(loser.id)),inline=True)
    e.set_thumbnail(url=loser.display_avatar.url)
    return e

def embed_public_result(m: dict, winner: discord.Member, loser: discord.Member) -> discord.Embed:
    _, rc = get_rank(get_stats(winner.id)["wins"])
    e = discord.Embed(title=f"{GAME_EMOJIS.get(m['game'],'🎲')} Epic Result — `{m['match_id']}`", color=rc, timestamp=datetime.now(timezone.utc))
    e.add_field(name="🎮 Game",    value=m["game"].upper(),    inline=True)
    e.add_field(name="🎯 Best of", value=str(m["best_of"]),   inline=True)
    e.add_field(name="📊 Score",   value=f"{m['score'][m['p1'].id]}–{m['score'][m['p2'].id]}", inline=True)
    e.add_field(name="🏆 Champion",value=f"{winner.mention}\n`{m['offer1'] if winner.id==m['p1'].id else m['offer2']}`", inline=True)
    e.add_field(name="💀 Fallen",  value=f"{loser.mention}\n`{m['offer1'] if loser.id==m['p1'].id else m['offer2']}`", inline=True)
    return e

def _winrate(uid: int) -> str:
    s = get_stats(uid)
    if s["games_played"] == 0: return "N/A"
    return f"{s['wins']/s['games_played']*100:.1f}%"

# ══════════════════════════════════════════════════════════════════
#  VIEWS — Match
# ══════════════════════════════════════════════════════════════════
class MatchAcceptView(ui.View):
    def __init__(self, challenger):
        super().__init__(timeout=MATCH_TIMEOUT)
        self.challenger = challenger; self.accepted = None
    @ui.button(label="✅  Accept", style=discord.ButtonStyle.success)
    async def accept(self, i, b):
        self.accepted = True; self.stop()
        await i.response.edit_message(embed=E("✅  Accepted","Heading to your match channel...",0x57f287),view=None)
    @ui.button(label="❌  Decline", style=discord.ButtonStyle.danger)
    async def decline(self, i, b):
        self.accepted = False; self.stop()
        await i.response.edit_message(embed=E("❌  Declined",color=0xed4245),view=None)
    async def on_timeout(self): self.accepted = False; self.stop()

class GamePickView(ui.View):
    def __init__(self, allowed):
        super().__init__(timeout=90)
        self.allowed = allowed; self.chosen = None
    async def interaction_check(self, i):
        if i.user.id not in self.allowed:
            await i.response.send_message("Not your match.", ephemeral=True); return False
        return True
    @ui.button(label="🎲  Roll",      style=discord.ButtonStyle.primary)
    async def r(self, i, b): self.chosen="roll";     self.stop(); await i.response.defer()
    @ui.button(label="🪙  Coin Flip", style=discord.ButtonStyle.primary)
    async def c(self, i, b): self.chosen="coinflip"; self.stop(); await i.response.defer()
    @ui.button(label="✊  RPS",       style=discord.ButtonStyle.primary)
    async def p(self, i, b): self.chosen="rps";      self.stop(); await i.response.defer()
    async def on_timeout(self): self.chosen=None; self.stop()

class RollView(ui.View):
    def __init__(self, allowed):
        super().__init__(timeout=60); self.allowed=allowed; self.rolls={}
    async def interaction_check(self, i):
        if i.user.id not in self.allowed: await i.response.send_message("Not your match.",ephemeral=True); return False
        if i.user.id in self.rolls: await i.response.send_message("Already rolled!",ephemeral=True); return False
        return True
    @ui.button(label="🎲  Roll!", style=discord.ButtonStyle.primary)
    async def roll(self, i, b):
        v=random.randint(1,100); self.rolls[i.user.id]=v
        await i.response.send_message(f"🎲 You rolled **{v}**!",ephemeral=True)
        if len(self.rolls)==2: self.stop()
    async def on_timeout(self): self.stop()

class CoinView(ui.View):
    def __init__(self, allowed):
        super().__init__(timeout=60); self.allowed=allowed; self.calls={}
    async def interaction_check(self, i):
        if i.user.id not in self.allowed: await i.response.send_message("Not your match.",ephemeral=True); return False
        if i.user.id in self.calls: await i.response.send_message("Already called!",ephemeral=True); return False
        return True
    @ui.button(label="🪙  Heads", style=discord.ButtonStyle.success)
    async def h(self, i, b):
        self.calls[i.user.id]="heads"; await i.response.send_message("🪙 Called **Heads**!",ephemeral=True)
        if len(self.calls)==2: self.stop()
    @ui.button(label="🪙  Tails", style=discord.ButtonStyle.danger)
    async def t(self, i, b):
        self.calls[i.user.id]="tails"; await i.response.send_message("🪙 Called **Tails**!",ephemeral=True)
        if len(self.calls)==2: self.stop()
    async def on_timeout(self): self.stop()

class RPSView(ui.View):
    def __init__(self, allowed):
        super().__init__(timeout=60); self.allowed=allowed; self.picks={}
    async def interaction_check(self, i):
        if i.user.id not in self.allowed: await i.response.send_message("Not your match.",ephemeral=True); return False
        if i.user.id in self.picks: await i.response.send_message("Already picked!",ephemeral=True); return False
        return True
    @ui.button(label="🪨 Rock",     style=discord.ButtonStyle.secondary)
    async def ro(self, i, b): self.picks[i.user.id]="rock";     await i.response.send_message("🪨 Locked!",ephemeral=True); self.stop() if len(self.picks)==2 else None
    @ui.button(label="📄 Paper",    style=discord.ButtonStyle.secondary)
    async def pa(self, i, b): self.picks[i.user.id]="paper";    await i.response.send_message("📄 Locked!",ephemeral=True); self.stop() if len(self.picks)==2 else None
    @ui.button(label="✂️ Scissors", style=discord.ButtonStyle.secondary)
    async def sc(self, i, b): self.picks[i.user.id]="scissors"; await i.response.send_message("✂️ Locked!",ephemeral=True); self.stop() if len(self.picks)==2 else None
    async def on_timeout(self): self.stop()

class ItemConfirmView(ui.View):
    def __init__(self, match):
        super().__init__(timeout=120); self.match=match; self.added=set()
    async def interaction_check(self, i):
        if i.user.id not in {self.match["p1"].id,self.match["p2"].id}:
            await i.response.send_message("Not your match.",ephemeral=True); return False
        return True
    @ui.button(label="📦  Add My Item / Wager", style=discord.ButtonStyle.success)
    async def add(self, i, b):
        if i.user.id in self.added: await i.response.send_message("Already confirmed.",ephemeral=True); return
        await i.response.send_modal(ItemModal(self.match,i.user.id,self))
    async def on_timeout(self): self.stop()

class ItemModal(ui.Modal, title="Confirm Your Wager"):
    item_name = ui.TextInput(label="Item name",placeholder="e.g. Dragon Fruit",max_length=100)
    item_note = ui.TextInput(label="Notes",required=False,max_length=200)
    def __init__(self, match, uid, parent):
        super().__init__(); self.match=match; self.uid=uid; self.parent=parent
    async def on_submit(self, i):
        p1,p2=self.match["p1"],self.match["p2"]
        key="items_p1" if i.user.id==p1.id else "items_p2"
        self.match.setdefault(key,[]).append({"name":self.item_name.value,"note":self.item_note.value or "—"})
        self.parent.added.add(self.uid)
        await i.response.send_message(embed=E("📦  Item Logged",f"**{self.item_name.value}**\n{self.item_note.value or '—'}",0x57f287),ephemeral=True)
        if len(self.parent.added)==2:
            p1l="\n".join(f"• `{x['name']}` — {x['note']}" for x in self.match.get("items_p1",[]))or"Nothing"
            p2l="\n".join(f"• `{x['name']}` — {x['note']}" for x in self.match.get("items_p2",[]))or"Nothing"
            e=discord.Embed(title="📦  Both Items Confirmed!",color=0x5865F2)
            e.add_field(name=f"🔵 {p1.display_name}",value=p1l,inline=True)
            e.add_field(name=f"🔴 {p2.display_name}",value=p2l,inline=True)
            await self.match["channel"].send(embed=e); self.parent.stop()

class RobuxDoubleView(ui.View):
    def __init__(self, loser):
        super().__init__(timeout=30); self.loser=loser; self.choice=None
    async def interaction_check(self, i):
        if i.user.id!=self.loser.id: await i.response.send_message("Not your decision.",ephemeral=True); return False
        return True
    @ui.button(label="💎  Double or Nothing!", style=discord.ButtonStyle.danger)
    async def dbl(self, i, b): self.choice="double"; self.stop(); await i.response.defer()
    @ui.button(label="🚪  Accept Loss", style=discord.ButtonStyle.secondary)
    async def acc(self, i, b): self.choice="accept"; self.stop(); await i.response.defer()
    async def on_timeout(self): self.choice="accept"; self.stop()

class ChannelDeleteView(ui.View):
    def __init__(self, match):
        super().__init__(timeout=300); self.match=match; self.agreed=set()
    async def interaction_check(self, i):
        if i.user.id not in {self.match["p1"].id,self.match["p2"].id}:
            await i.response.send_message("Not your match.",ephemeral=True); return False
        return True
    @ui.button(label="🗑️  Delete Channel", style=discord.ButtonStyle.danger)
    async def done(self, i, b):
        self.agreed.add(i.user.id)
        p1,p2=self.match["p1"],self.match["p2"]; rem={p1.id,p2.id}-self.agreed
        if rem:
            other=p1 if i.user.id==p2.id else p2
            await i.response.edit_message(embed=E("⏳  Waiting...",f"Waiting for **{other.display_name}** to confirm.",0xfee75c),view=self)
        else:
            await i.response.edit_message(embed=E("🗑️  Deleting in 5s...",color=0xed4245),view=None); self.stop()
    async def on_timeout(self): self.stop()

class PointsGambleAcceptView(ui.View):
    def __init__(self, challenger, wager):
        super().__init__(timeout=60); self.challenger=challenger; self.wager=wager; self.accepted=None
    @ui.button(label="✅  Accept Gamble", style=discord.ButtonStyle.success)
    async def acc(self, i, b):
        if get_points(i.user.id)<self.wager:
            await i.response.send_message(embed=E("❌  Not Enough Points",f"Need **{self.wager:,} pts**.",0xed4245),ephemeral=True); return
        self.accepted=i.user; self.stop()
        await i.response.edit_message(embed=E("✅  Accepted!",f"**{i.user.display_name}** accepted!",0x57f287),view=None)
    @ui.button(label="❌  Decline", style=discord.ButtonStyle.secondary)
    async def dec(self, i, b): self.accepted=False; self.stop(); await i.response.edit_message(embed=E("❌  Declined",color=0xed4245),view=None)
    async def on_timeout(self): self.accepted=False; self.stop()

# ══════════════════════════════════════════════════════════════════
#  CASINO VIEWS
# ══════════════════════════════════════════════════════════════════
class BombGridView(ui.View):
    def __init__(self, user_id, wager, channel_msg_ref, luck=1.0):
        super().__init__(timeout=120)
        self.user_id=user_id; self.wager=wager; self.msg_ref=channel_msg_ref
        self.luck=luck; self.revealed=set(); self.done=False; self.net_change=0
        positions=list(range(BOMB_GRID_SIZE)); random.shuffle(positions)
        self.bombs=set(positions[:BOMB_COUNT]); self.diamonds=set(positions[BOMB_COUNT:BOMB_COUNT+5])
        self._build_buttons()

    def _build_buttons(self):
        self.clear_items()
        labels=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","🔢","🔣"]
        for idx in range(BOMB_GRID_SIZE):
            if idx in self.revealed: continue
            btn=ui.Button(label=labels[idx],style=discord.ButtonStyle.secondary,custom_id=f"bomb_{idx}",row=idx//4)
            btn.callback=self._make_callback(idx); self.add_item(btn)
        cash=ui.Button(label=f"💰  Cash Out ({self.net_change:+,} pts)",style=discord.ButtonStyle.success,custom_id="cashout",row=3)
        cash.callback=self._cashout; self.add_item(cash)

    def _make_callback(self, idx):
        async def callback(interaction):
            if interaction.user.id!=self.user_id:
                await interaction.response.send_message("This isn't your game!",ephemeral=True); return
            if self.done:
                await interaction.response.send_message("Game already over.",ephemeral=True); return
            self.revealed.add(idx)
            if idx in self.bombs:
                loss=int(self.wager*BOMB_LOSS_PCT/self.luck); self.net_change-=loss
                result_text=f"💣 **BOMB!** You lost **{loss:,} pts**!"; color=0xed4245
                if self.net_change<=-self.wager: self.net_change=-self.wager; self.done=True
            elif idx in self.diamonds:
                gain=int(self.wager*DIAMOND_GAIN_PCT*self.luck); self.net_change+=gain
                result_text=f"💎 **DIAMOND!** You found **+{gain:,} pts**!"; color=0x57f287
            else:
                result_text="⬜ **Nothing here.** Safe!"; color=0x5865F2
            self._build_buttons()
            e=discord.Embed(
                title="💣  Bomb Field" if not self.done else "💥  BUST — All Lost!",
                description=(f"{result_text}\n\nRunning P/L: `{self.net_change:+,} pts`\n"
                             f"Cells revealed: {len(self.revealed)}/{BOMB_GRID_SIZE}\n\n"
                             f"{'☠️ You hit 3 bombs — game over!' if self.done else 'Keep going or **Cash Out** to lock in your gains.'}"),
                color=0xed4245 if self.done else color,
            )
            if self.done:
                final=self.wager+self.net_change
                if final>0: add_points(self.user_id,final)
                await interaction.response.edit_message(embed=e,view=None); self.stop()
            else:
                await interaction.response.edit_message(embed=e,view=self)
        return callback

    async def _cashout(self, interaction):
        if interaction.user.id!=self.user_id:
            await interaction.response.send_message("Not your game!",ephemeral=True); return
        self.done=True; payout=self.wager+self.net_change
        if payout>0: add_points(self.user_id,payout)
        e=discord.Embed(title="💰  Cashed Out!",description=(f"You cashed out with `{self.net_change:+,} pts`!\nNew balance: **{get_points(self.user_id):,} pts**"),color=0x57f287 if self.net_change>=0 else 0xfee75c)
        await interaction.response.edit_message(embed=e,view=None); self.stop()

    async def on_timeout(self):
        self.done=True; payout=max(0,self.wager+self.net_change)
        if payout>0: add_points(self.user_id,payout); self.stop()

class MinesGridView(ui.View):
    def __init__(self, user_id, wager, luck=1.0):
        super().__init__(timeout=90)
        self.user_id=user_id; self.wager=wager; self.luck=luck
        self.revealed=set(); self.done=False; self.gems_found=0; self.gain=0
        positions=list(range(MINES_GRID_SIZE)); random.shuffle(positions)
        self.mines=set(positions[:2]); self._build()

    def _build(self):
        self.clear_items()
        labels=["①","②","③","④","⑤","⑥","⑦","⑧","⑨"]
        for idx in range(MINES_GRID_SIZE):
            if idx in self.revealed: continue
            btn=ui.Button(label=labels[idx],style=discord.ButtonStyle.primary,custom_id=f"mine_{idx}",row=idx//3)
            btn.callback=self._make_cb(idx); self.add_item(btn)
        cash=ui.Button(label=f"💎  Collect ({self.gain:+,} pts)",style=discord.ButtonStyle.success,custom_id="collect",row=3)
        cash.callback=self._collect; self.add_item(cash)

    def _make_cb(self, idx):
        async def cb(interaction):
            if interaction.user.id!=self.user_id:
                await interaction.response.send_message("Not your game!",ephemeral=True); return
            self.revealed.add(idx)
            if idx in self.mines:
                self.done=True
                e=discord.Embed(title="💥  Mine Hit!",description=f"You hit a mine and lost **{self.wager:,} pts**!\nGems found: {self.gems_found}",color=0xed4245)
                await interaction.response.edit_message(embed=e,view=None); self.stop(); return
            gain=int(self.wager*MINES_GAIN_PCT*self.luck); self.gain+=gain; self.gems_found+=1
            self._build()
            e=discord.Embed(title="💎  Mine Field",description=f"💎 **Gem found! +{gain:,} pts**\nGems: {self.gems_found} · Running gain: `{self.gain:+,} pts`",color=0x57f287)
            if len(self.revealed)==MINES_GRID_SIZE-2:
                payout=self.wager+self.gain; add_points(self.user_id,payout)
                await interaction.response.edit_message(embed=discord.Embed(title="🏆  Cleared the Field!",description=f"Won **{self.gain:,} pts**!\nNew balance: **{get_points(self.user_id):,} pts**",color=0xffd700),view=None); self.stop(); return
            await interaction.response.edit_message(embed=e,view=self)
        return cb

    async def _collect(self, interaction):
        if interaction.user.id!=self.user_id:
            await interaction.response.send_message("Not your game!",ephemeral=True); return
        if self.gems_found==0:
            await interaction.response.send_message("Find at least one gem first!",ephemeral=True); return
        self.done=True; payout=self.wager+self.gain; add_points(self.user_id,payout)
        await interaction.response.edit_message(embed=discord.Embed(title="💎  Collected!",description=f"Cashed out with **+{self.gain:,} pts**!\nNew balance: **{get_points(self.user_id):,} pts**",color=0x57f287),view=None); self.stop()

    async def on_timeout(self):
        if not self.done and self.gems_found>0:
            add_points(self.user_id,self.wager+self.gain); self.stop()

class BlackjackView(ui.View):
    DECK=[2,3,4,5,6,7,8,9,10,10,10,10,11]*4
    def __init__(self, user_id, wager, luck=1.0):
        super().__init__(timeout=90)
        self.user_id=user_id; self.wager=wager; self.luck=luck; self.done=False
        deck=self.DECK.copy(); random.shuffle(deck)
        self.player=[deck.pop(),deck.pop()]; self.dealer=[deck.pop(),deck.pop()]; self.deck=deck

    def hand_value(self, hand):
        total=sum(hand); aces=hand.count(11)
        while total>21 and aces: total-=10; aces-=1
        return total

    def cards_str(self, hand, hide_second=False):
        if hide_second: return f"`{hand[0]}` `?`"
        return " ".join(f"`{c}`" for c in hand)

    def status_embed(self, result_title="", result_desc="", result_color=0x5865F2):
        pv=self.hand_value(self.player); dv=self.hand_value(self.dealer)
        e=discord.Embed(title=result_title or "🃏  Blackjack",color=result_color or 0x5865F2)
        e.add_field(name=f"Your Hand ({pv})",value=self.cards_str(self.player),inline=True)
        e.add_field(name=f"Dealer Hand ({'?' if not self.done else dv})",value=self.cards_str(self.dealer,not self.done),inline=True)
        e.add_field(name="Wager",value=f"{self.wager:,} pts",inline=True)
        if result_desc: e.description=result_desc
        return e

    @ui.button(label="👊  Hit",style=discord.ButtonStyle.primary)
    async def hit(self, i, b):
        if i.user.id!=self.user_id: await i.response.send_message("Not your game!",ephemeral=True); return
        self.player.append(self.deck.pop()); pv=self.hand_value(self.player)
        if pv>21:
            self.done=True
            e=self.status_embed("💥  Bust!",f"You busted with **{pv}**. Lost **{self.wager:,} pts**.",0xed4245)
            await i.response.edit_message(embed=e,view=None); self.stop()
        else:
            await i.response.edit_message(embed=self.status_embed(),view=self)

    @ui.button(label="✋  Stand",style=discord.ButtonStyle.secondary)
    async def stand(self, i, b):
        if i.user.id!=self.user_id: await i.response.send_message("Not your game!",ephemeral=True); return
        self.done=True
        while self.hand_value(self.dealer)<17: self.dealer.append(self.deck.pop())
        pv,dv=self.hand_value(self.player),self.hand_value(self.dealer)
        if dv>21 or pv>dv:
            payout=int(self.wager*BJ_PAYOUT*self.luck); add_points(self.user_id,payout)
            e=self.status_embed("🏆  You Win!",f"You won **{payout:,} pts**!\nNew balance: **{get_points(self.user_id):,} pts**",0x57f287)
        elif pv==dv:
            add_points(self.user_id,self.wager)
            e=self.status_embed("🤝  Push!",f"Tie game — wager refunded.\nBalance: **{get_points(self.user_id):,} pts**",0xfee75c)
        else:
            e=self.status_embed("💀  Dealer Wins",f"Dealer had **{dv}**, you had **{pv}**. Lost **{self.wager:,} pts**.",0xed4245)
        await i.response.edit_message(embed=e,view=None); self.stop()

    async def on_timeout(self): self.done=True; self.stop()

class CoinFlipSoloView(ui.View):
    def __init__(self, user_id, wager, luck=1.0):
        super().__init__(timeout=30); self.user_id=user_id; self.wager=wager; self.luck=luck
    @ui.button(label="🪙  Heads",style=discord.ButtonStyle.success)
    async def h(self, i, b): await self._resolve(i,"heads")
    @ui.button(label="🪙  Tails",style=discord.ButtonStyle.danger)
    async def t(self, i, b): await self._resolve(i,"tails")
    async def _resolve(self, i, call):
        if i.user.id!=self.user_id: await i.response.send_message("Not your game!",ephemeral=True); return
        win_chance=0.5+min((self.luck-1.0)*0.1,0.3)
        result="heads" if random.random()<win_chance else "tails"; won=call==result
        if won: add_points(self.user_id,int(self.wager*2))
        e=discord.Embed(
            title=f"🪙  {'You Win!' if won else 'You Lose!'}",
            description=f"You called **{call}** — landed **{result}**\n{'Won' if won else 'Lost'}: **{self.wager:,} pts**\nNew balance: **{get_points(self.user_id):,} pts**",
            color=0x57f287 if won else 0xed4245,
        )
        await i.response.edit_message(embed=e,view=None); self.stop()
    async def on_timeout(self): self.stop()

# ══════════════════════════════════════════════════════════════════
#  SHOP VIEWS
# ══════════════════════════════════════════════════════════════════
class AddShopItemModal(ui.Modal, title="Add Shop Item"):
    name_f  = ui.TextInput(label="Item name",max_length=80)
    desc_f  = ui.TextInput(label="Description",style=discord.TextStyle.paragraph,max_length=300)
    price_f = ui.TextInput(label="Price (points)",placeholder="500")
    stock_f = ui.TextInput(label="Stock (-1 = unlimited)",placeholder="-1")
    img_f   = ui.TextInput(label="Image URL (optional)",required=False)
    game_f  = ui.TextInput(label="Game (e.g. Blox Fruits, MM2, Robux)",required=False,max_length=40)

    async def on_submit(self, i):
        global shop_id_counter
        try: price=int(self.price_f.value.strip()); stock=int(self.stock_f.value.strip())
        except ValueError:
            await i.response.send_message(embed=E("❌  Price/Stock must be integers.",color=0xed4245),ephemeral=True); return
        item={
            "id":          shop_id_counter,
            "name":        self.name_f.value.strip(),
            "description": self.desc_f.value.strip(),
            "price":       price,
            "stock":       stock,
            "image_url":   self.img_f.value.strip() or None,
            "game":        self.game_f.value.strip() or None,
            "added_by":    i.user.id,
        }
        shop_items.append(item); shop_id_counter+=1
        save_json("shop",{"items":shop_items,"counter":shop_id_counter})
        await i.response.send_message(embed=_embed_item(item))

class EditShopItemModal(ui.Modal, title="Edit Shop Item"):
    name_f  = ui.TextInput(label="New name (blank = keep)",required=False,max_length=80)
    desc_f  = ui.TextInput(label="New description (blank = keep)",required=False,style=discord.TextStyle.paragraph,max_length=300)
    price_f = ui.TextInput(label="New price (blank = keep)",required=False)
    stock_f = ui.TextInput(label="New stock (blank = keep)",required=False)
    game_f  = ui.TextInput(label="New game tag (blank = keep)",required=False,max_length=40)
    def __init__(self, item):
        super().__init__(); self.item=item
    async def on_submit(self, i):
        if self.name_f.value.strip():  self.item["name"]        = self.name_f.value.strip()
        if self.desc_f.value.strip():  self.item["description"] = self.desc_f.value.strip()
        if self.price_f.value.strip():
            try: self.item["price"]=int(self.price_f.value.strip())
            except ValueError: pass
        if self.stock_f.value.strip():
            try: self.item["stock"]=int(self.stock_f.value.strip())
            except ValueError: pass
        if self.game_f.value.strip(): self.item["game"]=self.game_f.value.strip()
        save_json("shop",{"items":shop_items,"counter":shop_id_counter})
        await i.response.send_message(embed=E("✅  Item Updated",color=0x57f287),ephemeral=True)

class TicketCloseView(ui.View):
    def __init__(self, ticket_id):
        super().__init__(timeout=None)
        self.ticket_id=ticket_id
        btn=ui.Button(label="🔒  Close Ticket",style=discord.ButtonStyle.danger,custom_id=f"close_ticket_{ticket_id}")
        btn.callback=self._close_cb; self.add_item(btn)

    async def _close_cb(self, interaction):
        if not is_supplier(interaction.user):
            await interaction.response.send_message("Only suppliers can close tickets.",ephemeral=True); return
        t=next((x for x in tickets if x["ticket_id"]==self.ticket_id),None)
        if t: t["status"]="closed"; save_json("tickets",tickets)
        await interaction.response.send_message(embed=E("🔒  Ticket Closed","Marked as fulfilled. Deleting in 10s.",0x57f287))
        await asyncio.sleep(10)
        try: await interaction.channel.delete(reason="Ticket closed")
        except Exception: pass

def _embed_item(item):
    e=discord.Embed(title=f"🛍️  {item['name']}",description=item["description"],color=0x5865F2)
    e.add_field(name="Price",value=f"💰 {item['price']:,} pts",inline=True)
    e.add_field(name="Stock",value=str(item["stock"]) if item["stock"]>=0 else "∞",inline=True)
    e.add_field(name="Item #",value=f"`#{item['id']}`",inline=True)
    if item.get("game"): e.add_field(name="Game",value=item["game"],inline=True)
    if item.get("image_url"): e.set_image(url=item["image_url"])
    e.set_footer(text=f"Use /buy {item['id']} to purchase")
    return e

def _embed_shop():
    e=discord.Embed(title="🛒 GambleMatch Marketplace",description="Acquire legendary items with your hard-earned gems!\nUse `/buy <number>` to claim your prize.",color=0x5865F2,timestamp=datetime.now(timezone.utc))
    if not shop_items:
        e.description="The marketplace is currently empty. New treasures arrive soon!"; return e
    for item in shop_items:
        stock=f"📦 Stock: **{item['stock']}**" if item["stock"]>=0 else "📦 Stock: ∞ (Unlimited)"
        game_tag=f" | 🎮 {item['game']}" if item.get("game") else ""
        e.add_field(name=f"`#{item['id']}`  {item['name']}  — {EMOJI_GEM} {item['price']:,}{game_tag}",value=f"{item['description']}\n{stock}",inline=False)
    return e

# ══════════════════════════════════════════════════════════════════
#  ROUND LOGIC
# ══════════════════════════════════════════════════════════════════
def _get_privileged_player(p1, p2, channel_id):
    p1_owns=any(r["owner_id"]==p1.id for r in rooms.values())
    p2_owns=any(r["owner_id"]==p2.id for r in rooms.values())
    room_owner_id=get_room_owner_id(channel_id)
    if room_owner_id:
        if room_owner_id==p1.id: return p1
        if room_owner_id==p2.id: return p2
    if p1_owns and not p2_owns: return p1
    if p2_owns and not p1_owns: return p2
    return None

async def play_one_round(channel, p1, p2, ctx=None):
    ctx=ctx or {}; allowed={p1.id,p2.id}
    score_bar=build_score_bar(ctx) if "score" in ctx else ""
    pick_e=discord.Embed(title="🎮  Pick a Game Mode",description=f"{score_bar}\n\n{p1.mention} {p2.mention} — choose below.",color=0x5865F2)
    gv=GamePickView(allowed); msg=await channel.send(embed=pick_e,view=gv); await gv.wait(); await msg.edit(view=None)
    if not gv.chosen:
        await channel.send(embed=E("⌛  No game chosen — round skipped.",color=0xed4245)); return None
    mode=gv.chosen; await asyncio.sleep(1)
    privileged=_get_privileged_player(p1,p2,channel.id)

    if mode=="roll":
        rv=RollView(allowed)
        await channel.send(embed=E("🎲  Both Roll — Highest Wins!",f"{p1.mention} {p2.mention} — click below.",0x5865F2),view=rv); await rv.wait()
        rolls=rv.rolls
        if len(rolls)<2:
            if not rolls: return None
            uid=list(rolls.keys())[0]; w=p1 if uid==p1.id else p2; l=p2 if w==p1 else p1
            return w,l,mode,f"Opponent no-show — {w.display_name} wins"
        r1,r2=rolls[p1.id],rolls[p2.id]
        if privileged:
            other=p2 if privileged==p1 else p1
            priv_roll=rolls.get(privileged.id,50); other_roll=rolls.get(other.id,50)
            if priv_roll<=other_roll:
                priv_roll=min(other_roll+random.randint(1,15),100)
                if privileged==p1: r1=priv_roll
                else: r2=priv_roll
        detail=f"🎲 **{p1.display_name}** `{r1}` vs **{p2.display_name}** `{r2}`"
        if r1==r2:
            await channel.send(embed=E("🎲  Tie! Same roll — replaying.",detail,0xfee75c)); await asyncio.sleep(1)
            return await play_one_round(channel,p1,p2,ctx)
        w=p1 if r1>r2 else p2; l=p2 if w==p1 else p1; return w,l,mode,detail

    elif mode=="coinflip":
        cv=CoinView(allowed)
        await channel.send(embed=E("🪙  Pick Heads or Tails",f"{p1.mention} {p2.mention}",0xfee75c),view=cv); await cv.wait()
        calls=cv.calls
        if len(calls)<2: return None
        flip=await channel.send(embed=E("🪙  Flipping...",color=0xfee75c)); await asyncio.sleep(2)
        if privileged and privileged.id in calls: result=calls[privileged.id]
        else: result=random.choice(["heads","tails"])
        await flip.edit(embed=E(f"🪙  It's **{result.upper()}**!",f"**{p1.display_name}** called `{calls.get(p1.id,'?')}`\n**{p2.display_name}** called `{calls.get(p2.id,'?')}`",0xfee75c))
        await asyncio.sleep(1)
        winners=[m for m in [p1,p2] if calls.get(m.id)==result]
        if len(winners)!=1:
            await channel.send(embed=E("🪙  Tie! Same call — replaying.",color=0xfee75c)); return await play_one_round(channel,p1,p2,ctx)
        w=winners[0]; l=p2 if w==p1 else p1
        return w,l,mode,f"**{p1.display_name}** `{calls.get(p1.id,'?')}` · **{p2.display_name}** `{calls.get(p2.id,'?')}` · Landed `{result}`"

    elif mode=="rps":
        rv2=RPSView(allowed)
        await channel.send(embed=E("✊  Pick Your Move",f"{p1.mention} {p2.mention} — reveal is simultaneous!",0x5865F2),view=rv2); await rv2.wait()
        picks=rv2.picks
        if len(picks)<2: return None
        await asyncio.sleep(1); c1,c2=picks[p1.id],picks[p2.id]
        emj={"rock":"🪨","paper":"📄","scissors":"✂️"}; beats={"rock":"scissors","scissors":"paper","paper":"rock"}
        await channel.send(embed=E("✊  Reveal!",f"**{p1.display_name}** threw {emj[c1]} **{c1}**\n**{p2.display_name}** threw {emj[c2]} **{c2}**",0x5865F2))
        await asyncio.sleep(1)
        if c1==c2:
            await channel.send(embed=E("✊  Tie! Replaying.",f"Both threw `{c1}`.",0xfee75c)); return await play_one_round(channel,p1,p2,ctx)
        w=p1 if beats[c1]==c2 else p2; l=p2 if w==p1 else p1
        return w,l,mode,f"{emj[c1]} `{c1}` vs {emj[c2]} `{c2}`"
    return None

# ══════════════════════════════════════════════════════════════════
#  MATCH LOOP
# ══════════════════════════════════════════════════════════════════
async def run_match(match, guild):
    channel=match["channel"]; p1,p2=match["p1"],match["p2"]
    bo=match["best_of"]; need=rounds_needed(bo)
    if match["game"]!="robux":
        iv=ItemConfirmView(match)
        await channel.send(embed=E("📦  Confirm Your Items","Click **Add My Item** to log your wager before we start.",0x5865F2),view=iv)
        try: await asyncio.wait_for(iv.wait(),timeout=90)
        except asyncio.TimeoutError: pass
        await asyncio.sleep(1)
    fw=fl=None
    while True:
        s1,s2=match["score"][p1.id],match["score"][p2.id]
        if s1>=need: fw,fl=p1,p2; break
        if s2>=need: fw,fl=p2,p1; break
        result=await play_one_round(channel,p1,p2,match)
        if result is None:
            await channel.send(embed=E("⌛  Match Abandoned",color=0xed4245)); active_matches.pop(match["match_id"],None); return
        rw,rl,mode,detail=result
        match["score"][rw.id]+=1; match["round"]+=1
        await asyncio.sleep(1); await channel.send(embed=embed_round_result(match,rw,mode,detail)); await asyncio.sleep(2)
    ws=get_stats(fw.id); ls=get_stats(fl.id)
    ws["wins"]+=1; ws["games_played"]+=1; ws["rounds_won"]+=match["score"][fw.id]; ws["rounds_lost"]+=match["score"][fl.id]
    ws["streak"]+=1; ws["best_streak"]=max(ws["best_streak"],ws["streak"])
    ls["losses"]+=1; ls["games_played"]+=1; ls["rounds_won"]+=match["score"][fl.id]; ls["rounds_lost"]+=match["score"][fw.id]; ls["streak"]=0
    add_rep(fw.id,1); save_all()
    await asyncio.sleep(1)
    await channel.send(content=f"{fw.mention} {fl.mention}",embed=embed_match_winner(match,fw,fl))
    await asyncio.sleep(1); await channel.send(embed=embed_loser_result(match,fw,fl)); await asyncio.sleep(1)
    if match["game"]=="robux":
        dv=RobuxDoubleView(fl)
        await channel.send(embed=discord.Embed(title="💎  Double or Nothing?",description=f"{fl.mention} — one last chance. Win → everything back + theirs. Lose → sealed.\n⏳ 30 seconds.",color=0xfee75c),view=dv)
        await dv.wait()
        if dv.choice=="double":
            await channel.send(embed=E("💎  Double or Nothing — ONE Round!",color=0xf0c040))
            match["score"]={p1.id:0,p2.id:0}; match["round"]=1
            res=await play_one_round(channel,p1,p2,match)
            if res: fw,fl,_,detail=res; save_all()
        else:
            await channel.send(embed=E("🚪  Loss accepted.",color=0x5865F2))
    match_history.append({"match_id":match["match_id"],"winner_id":fw.id,"loser_id":fl.id,"game":match["game"],"best_of":bo,"rounds":match["round"]-1,"timestamp":datetime.now(timezone.utc).isoformat()})
    active_matches.pop(match["match_id"],None); save_all()
    await _post_public_result(guild,match,fw,fl)
    dv2=ChannelDeleteView(match)
    await channel.send(embed=E("🗑️  Done? Delete Channel","Both click below.",0x2b2d31),view=dv2)
    await dv2.wait(); await asyncio.sleep(5)
    try: await channel.delete(reason="Match concluded")
    except Exception: pass

async def _post_public_result(guild, match, winner, loser):
    chan=discord.utils.get(guild.text_channels,name=MATCHES_CHANNEL)
    if not chan:
        try: chan=await guild.create_text_channel(MATCHES_CHANNEL)
        except: return
    msg=await chan.send(embed=embed_public_result(match,winner,loser))
    await msg.add_reaction("✅"); await msg.add_reaction("❌")

async def _create_match_channel(guild, match):
    p1,p2=match["p1"],match["p2"]
    ow={guild.default_role:discord.PermissionOverwrite(read_messages=False),
        p1:discord.PermissionOverwrite(read_messages=True,send_messages=True),
        p2:discord.PermissionOverwrite(read_messages=True,send_messages=True),
        guild.me:discord.PermissionOverwrite(read_messages=True,send_messages=True)}
    cat=discord.utils.get(guild.categories,name="matches")
    return await guild.create_text_channel(name=f"match-{match['match_id'].lower()}",overwrites=ow,category=cat)

async def _open_match(match, guild):
    ch=await _create_match_channel(guild,match); match["channel"]=ch
    active_matches[match["match_id"]]=match
    await ch.send(content=f"{match['p1'].mention} {match['p2'].mention}",embed=embed_match_intro(match))
    await asyncio.sleep(2); asyncio.create_task(run_match(match,guild))

# ══════════════════════════════════════════════════════════════════
#  SLASH — Matchmaking
# ══════════════════════════════════════════════════════════════════
@tree.command(name="findg",description="Find a gambling match")
@app_commands.describe(offer="What you're wagering",game="Game category",cross_trade="Allow cross-game matching?")
@app_commands.choices(game=[app_commands.Choice(name=g,value=g) for g in GAMES])
@findg_only()
async def findg(i, offer: str, game: app_commands.Choice[str], cross_trade: bool=False):
    user=i.user; guild=i.guild; now=datetime.now(timezone.utc)
    if user.id in cooldowns and (now-cooldowns[user.id]).total_seconds()<COOLDOWN_SECONDS:
        wait=int(COOLDOWN_SECONDS-(now-cooldowns[user.id]).total_seconds())
        await i.response.send_message(embed=E("⏳  Cooldown",f"Wait **{wait}s**.",0xfee75c),ephemeral=True); return
    if any(e["user"].id==user.id for e in queue):
        await i.response.send_message(embed=E("⚠️  Already Queued","Use `/leaveq` first.",0xed4245),ephemeral=True); return
    cooldowns[user.id]=now
    opp=find_opponent(user,game.value,cross_trade)
    if opp:
        queue.remove(opp); bo=rand_best_of()
        match={"match_id":gen_id(),"p1":user,"p2":opp["user"],"offer1":offer,"offer2":opp["offer"],"game":game.value,"cross_trade":cross_trade or opp["cross_trade"],"game_mode":None,"channel":None,"score":{user.id:0,opp["user"].id:0},"round":1,"best_of":bo}
        await i.response.send_message(embed=E("🎯  Opponent Found!",f"Matched with **{opp['user'].display_name}** — 🎲 **Best of {bo}** drawn!",0x57f287),ephemeral=True)
        await _open_match(match,guild)
    else:
        queue.append({"user":user,"offer":offer,"game":game.value,"cross_trade":cross_trade})
        e=discord.Embed(title="📋  Added to Queue",description="Scanning for an opponent...",color=0x5865F2)
        e.add_field(name="Offer",value=f"`{offer}`",inline=True); e.add_field(name="Game",value=f"{GAME_EMOJIS.get(game.value,'🎲')} {game.value.upper()}",inline=True)
        e.set_footer(text="/leaveq to cancel")
        await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="leaveq",description="Leave the matchmaking queue")
async def leaveq(i):
    entry=next((e for e in queue if e["user"].id==i.user.id),None)
    if entry: queue.remove(entry); await i.response.send_message(embed=E("✅  Left Queue",color=0x57f287),ephemeral=True)
    else: await i.response.send_message(embed=E("❓  Not in Queue",color=0xfee75c),ephemeral=True)

@tree.command(name="queue",description="View the matchmaking queue")
async def view_queue(i):
    if not queue: await i.response.send_message(embed=E("📭  Queue Empty","Use `/findg`!",0x5865F2),ephemeral=True); return
    e=discord.Embed(title=f"📋  Queue — {len(queue)} waiting",color=0x5865F2)
    for idx,entry in enumerate(queue,1):
        rn,_=get_rank(get_stats(entry["user"].id)["wins"])
        e.add_field(name=f"{idx}. {entry['user'].display_name}  {rn}",value=f"`{entry['offer']}`  ·  {GAME_EMOJIS.get(entry['game'],'🎲')} {entry['game'].upper()}",inline=False)
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="challenge",description="Directly challenge a player")
@app_commands.describe(member="Target",offer="Your wager",game="Game category")
@app_commands.choices(game=[app_commands.Choice(name=g,value=g) for g in GAMES])
async def challenge(i, member: discord.Member, offer: str, game: app_commands.Choice[str]):
    if member.id==i.user.id or member.bot: await i.response.send_message(embed=E("❌  Invalid target",color=0xed4245),ephemeral=True); return
    challenger=i.user; bo=rand_best_of()
    ce=discord.Embed(title=f"⚔️  Challenge from {challenger.display_name}!",description=f"**Best of {bo}** randomly drawn!\n{GAME_EMOJIS.get(game.value,'🎲')} {game.value.upper()}\nOffer: `{offer}`\n⏳ {MATCH_TIMEOUT}s to respond.",color=0xf0c040)
    ce.set_thumbnail(url=challenger.display_avatar.url)
    av=MatchAcceptView(challenger)
    try: dm=await member.create_dm(); await dm.send(embed=ce,view=av)
    except discord.Forbidden: await i.response.send_message(embed=E("⚠️  Can't DM",f"{member.mention} has DMs closed.",0xed4245),ephemeral=True); return
    await i.response.send_message(embed=E("⚔️  Challenge Sent",f"Waiting for **{member.display_name}**...",0x5865F2),ephemeral=True)
    await av.wait()
    if not av.accepted: await i.followup.send(embed=E("❌  Declined",color=0xed4245),ephemeral=True); return
    match={"match_id":gen_id(),"p1":challenger,"p2":member,"offer1":offer,"offer2":"TBD","game":game.value,"cross_trade":False,"game_mode":None,"channel":None,"score":{challenger.id:0,member.id:0},"round":1,"best_of":bo}
    await _open_match(match,i.guild)

# ══════════════════════════════════════════════════════════════════
#  SLASH — Economy
# ══════════════════════════════════════════════════════════════════
@tree.command(name="balance",description="Check your points balance")
async def balance(i):
    uid=i.user.id; wallet=get_points(uid)
    e=discord.Embed(title=f"{EMOJI_WALLET} Your Fortune Vault",color=0xffd700)
    e.set_author(name=i.user.display_name,icon_url=i.user.display_avatar.url)
    e.add_field(name=f"{EMOJI_WALLET} Active Wallet",value=fmt_bal(wallet),inline=True)
    e.add_field(name="🏦 Secure Bank",value=fmt_bal(get_bank(uid)),inline=True)
    e.add_field(name="💎 Total Wealth",value=fmt_bal(wallet+get_bank(uid)),inline=True)
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="daily",description="Claim your daily points reward")
async def daily(i):
    uid=i.user.id; today=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    import datetime as dt
    yesterday=(dt.datetime.fromisoformat(today)-dt.timedelta(days=1)).strftime("%Y-%m-%d")
    streak_data=daily_streak.get(uid,{"last":"","streak":0})
    last_claim=streak_data["last"]; streak=streak_data["streak"]
    if last_claim==today:
        await i.response.send_message(embed=discord.Embed(title=f"⏳  Already Claimed Today",description=f"Come back tomorrow!\n\n{EMOJI_GEM} Wallet: {fmt_bal(get_points(uid))}",color=0xfee75c),ephemeral=True); return
    if last_claim==yesterday: streak+=1
    else: streak=1
    reward=min(DAILY_BASE+(streak-1)*DAILY_STREAK_BONUS,DAILY_MAX)
    bonus=0; bonus_note=""
    if streak==7: bonus=5_000; bonus_note="\n🎉 **7-day streak bonus! +5,000**"
    elif streak==14: bonus=15_000; bonus_note="\n🎉 **14-day streak bonus! +15,000**"
    elif streak==30: bonus=50_000; bonus_note="\n👑 **30-day streak bonus! +50,000!**"
    elif streak%30==0 and streak>30: bonus=75_000; bonus_note=f"\n👑 **{streak}-day streak bonus! +75,000!**"
    total=reward+bonus; add_points(uid,total)
    daily_claimed[uid]=today; daily_streak[uid]={"last":today,"streak":streak}
    save_json("daily",{str(k):v for k,v in daily_claimed.items()})
    save_json("daily_streak",{str(k):v for k,v in daily_streak.items()})
    streak_bar="🔥"*min(streak,10)+("..." if streak>10 else "")
    e=discord.Embed(title=f"🎁 Daily Fortune Claimed — Streak Day {streak}!",description=(f"You've unlocked {fmt_bal(reward)} for today!{bonus_note}\n\n**Total Claimed:** {fmt_bal(total)}\n{EMOJI_WALLET} Updated Wallet: {fmt_bal(get_points(uid))}\n\n🔥 Streak: **{streak} day{'s' if streak!=1 else ''}** {streak_bar}"),color=0xf0c040,timestamp=datetime.now(timezone.utc))
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="gamble",description="Gamble points vs another player")
@app_commands.describe(member="Who to challenge",wager="How many points")
@casino_only()
async def gamble(i, member: discord.Member, wager: int):
    challenger=i.user
    if member.id==challenger.id or member.bot: await i.response.send_message(embed=E("❌  Invalid target",color=0xed4245),ephemeral=True); return
    if wager<=0: await i.response.send_message(embed=E("❌  Wager must be > 0",color=0xed4245),ephemeral=True); return
    if get_points(challenger.id)<wager: await i.response.send_message(embed=E("❌  Not Enough Points",f"You have **{get_points(challenger.id):,} pts**.",0xed4245),ephemeral=True); return
    ce=discord.Embed(title="💰  Points Gamble!",description=f"{challenger.mention} challenges {member.mention} for **{wager:,} gems**!\nWinner gets **{int(wager*POINTS_WIN_MULT):,} gems**.",color=0xf0c040)
    av=PointsGambleAcceptView(challenger,wager)
    await i.response.send_message(embed=ce,view=av); await av.wait()
    if not av.accepted or isinstance(av.accepted,bool): await i.followup.send(embed=E("❌  Declined or timed out.",color=0xed4245)); return
    opponent=av.accepted
    if opponent.id!=member.id: await i.followup.send(embed=E("❌  Wrong player accepted.",color=0xed4245)); return
    spend_points(challenger.id,wager); spend_points(opponent.id,wager)
    result=await play_one_round(i.channel,challenger,opponent,{})
    if result is None:
        add_points(challenger.id,wager); add_points(opponent.id,wager)
        await i.channel.send(embed=E("⌛  Timed out — wagers refunded.",color=0xfee75c)); return
    winner,loser,mode,detail=result
    prize=int(wager*POINTS_WIN_MULT); add_points(winner.id,prize)
    e=discord.Embed(title=f"{'🏆' if winner.id==challenger.id else '💀'}  Gamble Result",description=detail,color=0x57f287 if winner.id==challenger.id else 0xed4245)
    e.add_field(name="Winner",value=winner.mention,inline=True); e.add_field(name="Pot",value=f"**{prize:,} gems**",inline=True)
    await i.channel.send(embed=e)

@tree.command(name="give",description="Give points to another player")
@app_commands.describe(member="Recipient",amount="Amount to give")
async def give(i, member: discord.Member, amount: int):
    if amount<=0 or member.id==i.user.id: await i.response.send_message(embed=E("❌  Invalid",color=0xed4245),ephemeral=True); return
    if not spend_points(i.user.id,amount): await i.response.send_message(embed=E("❌  Not Enough Points",color=0xed4245),ephemeral=True); return
    add_points(member.id,amount)
    await i.response.send_message(embed=E("💸  Points Sent",f"Sent **{amount:,} gems** to {member.mention}.\nYour balance: **{get_points(i.user.id):,} gems**",0x57f287))

@tree.command(name="deposit",description="Deposit points into your bank")
@app_commands.describe(amount="How many points to deposit")
async def deposit_cmd(i, amount: int):
    uid=i.user.id
    if amount<=0: await i.response.send_message(embed=E("❌  Amount must be > 0",color=0xed4245),ephemeral=True); return
    if not deposit_bank(uid,amount): await i.response.send_message(embed=E("❌  Not Enough Points",color=0xed4245),ephemeral=True); return
    e=discord.Embed(title=f"🏦  Deposit Successful",color=0x57f287)
    e.add_field(name="Deposited",value=fmt_bal(amount),inline=True)
    e.add_field(name="🏦 Bank",value=fmt_bal(get_bank(uid)),inline=True)
    e.add_field(name=f"{EMOJI_WALLET} Wallet",value=fmt_bal(get_points(uid)),inline=True)
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="withdraw",description="Withdraw points from your bank")
@app_commands.describe(amount="How many points to withdraw")
async def withdraw_cmd(i, amount: int):
    uid=i.user.id
    if amount<=0: await i.response.send_message(embed=E("❌  Amount must be > 0",color=0xed4245),ephemeral=True); return
    if not withdraw_bank(uid,amount): await i.response.send_message(embed=E("❌  Not Enough in Bank",color=0xed4245),ephemeral=True); return
    e=discord.Embed(title=f"🏦  Withdrawal Successful",color=0x57f287)
    e.add_field(name="Withdrawn",value=fmt_bal(amount),inline=True)
    e.add_field(name="🏦 Bank",value=fmt_bal(get_bank(uid)),inline=True)
    e.add_field(name=f"{EMOJI_WALLET} Wallet",value=fmt_bal(get_points(uid)),inline=True)
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="bankbalance",description="Check your bank and wallet balance")
async def bankbalance_cmd(i):
    uid=i.user.id; wallet=get_points(uid); banked=get_bank(uid)
    e=discord.Embed(title=f"{EMOJI_WALLET}  Account Overview",color=0xffd700)
    e.set_author(name=i.user.display_name,icon_url=i.user.display_avatar.url)
    e.add_field(name=f"{EMOJI_WALLET} Wallet",value=fmt_bal(wallet),inline=True)
    e.add_field(name="🏦 Bank",value=fmt_bal(banked),inline=True)
    e.add_field(name=f"{EMOJI_GEM} Total",value=fmt_bal(wallet+banked),inline=True)
    await i.response.send_message(embed=e,ephemeral=True)

# ══════════════════════════════════════════════════════════════════
#  SLASH — Casino
# ══════════════════════════════════════════════════════════════════
@tree.command(name="bomb",description="Bomb Field — find diamonds, avoid bombs!")
@app_commands.describe(wager="How many points to wager")
@casino_only()
async def bomb_cmd(i, wager: int):
    uid=i.user.id
    if wager<=0: await i.response.send_message(embed=E("❌  Wager must be > 0",color=0xed4245),ephemeral=True); return
    current_points=get_points(uid); max_bet=int(current_points*0.0025)
    if wager>max_bet: await i.response.send_message(embed=E("❌  Max Bet Exceeded",f"Max bet is **{max_bet:,} pts**.",0xed4245),ephemeral=True); return
    cd=check_game_cooldown(uid,8)
    if cd: await i.response.send_message(embed=E("⏳  Cooldown",f"Wait **{cd}s**.",0xfee75c),ephemeral=True); return
    if not spend_points(uid,wager): await i.response.send_message(embed=E("❌  Not Enough Points",color=0xed4245),ephemeral=True); return
    luck=get_total_luck(uid); msg_ref=[]
    view=BombGridView(uid,wager,msg_ref,luck)
    e=discord.Embed(title="💣  Bomb Field",description=f"**{BOMB_COUNT} bombs** hidden in **{BOMB_GRID_SIZE} cells**.\nCash out at any time!",color=0xf0c040)
    e.add_field(name="Wager",value=f"**{wager:,} gems**",inline=True); e.add_field(name="Luck",value=f"**{luck:.2f}x**",inline=True)
    await i.response.send_message(embed=e,view=view)

@tree.command(name="mines",description="Mine Field — collect gems, avoid mines!")
@app_commands.describe(wager="How many points to wager")
@casino_only()
async def mines_cmd(i, wager: int):
    uid=i.user.id
    if wager<=0: await i.response.send_message(embed=E("❌  Wager must be > 0",color=0xed4245),ephemeral=True); return
    cd=check_game_cooldown(uid,8)
    if cd: await i.response.send_message(embed=E("⏳  Cooldown",f"Wait **{cd}s**.",0xfee75c),ephemeral=True); return
    if not spend_points(uid,wager): await i.response.send_message(embed=E("❌  Not Enough Points",color=0xed4245),ephemeral=True); return
    luck=get_total_luck(uid)
    view=MinesGridView(uid,wager,luck)
    e=discord.Embed(title="💎  Mine Field",description=f"**2 mines** hidden in **{MINES_GRID_SIZE} cells**.\nCollect at any time to bank your gems.",color=0x1e88e5)
    e.add_field(name="Wager",value=f"**{wager:,} gems**",inline=True); e.add_field(name="Luck",value=f"**{luck:.2f}x**",inline=True)
    await i.response.send_message(embed=e,view=view)

@tree.command(name="slots",description="Spin the slot machine!")
@app_commands.describe(wager="How many points to wager")
@casino_only()
async def slots_cmd(i, wager: int):
    uid=i.user.id
    if wager<=0: await i.response.send_message(embed=E("❌  Wager must be > 0",color=0xed4245),ephemeral=True); return
    if not spend_points(uid,wager): await i.response.send_message(embed=E("❌  Not Enough Points",color=0xed4245),ephemeral=True); return
    cd=check_game_cooldown(uid,5)
    if cd: await i.response.send_message(embed=E("⏳  Cooldown",f"Wait **{cd}s**.",0xfee75c),ephemeral=True); return
    luck=get_total_luck(uid)
    spin_e=discord.Embed(title="🎰  Spinning...",description="🎰 `[ ? | ? | ? ]`",color=0xf0c040)
    await i.response.send_message(embed=spin_e); await asyncio.sleep(1.5)
    reel=[random.choices(SLOTS_SYMBOLS,weights=SLOTS_WEIGHTS,k=1)[0] for _ in range(3)]
    combo=" | ".join(reel); key="".join(reel)
    mult=SLOTS_PAYOUTS.get(key,0)
    if mult==0 and (reel[0]==reel[1] or reel[1]==reel[2] or reel[0]==reel[2]): mult=SLOTS_TWO_PAYOUT
    mult*=luck; payout=int(wager*mult)
    if payout>0: add_points(uid,payout)
    won=payout>wager
    result_e=discord.Embed(
        title=f"🎰  {'JACKPOT! 🎉' if mult>=4 else 'You Win!' if won else 'No Luck!'}",
        description=f"## [ {combo} ]\n\n{'Won' if won else 'Lost'}: **{abs(payout-wager):,} gems**",
        color=0xffd700 if mult>=4 else 0x57f287 if won else 0xed4245,
    )
    result_e.add_field(name="Wager",value=f"{wager:,} gems",inline=True)
    result_e.add_field(name="Payout",value=f"{payout:,} gems",inline=True)
    result_e.add_field(name="Balance",value=f"{get_points(uid):,} gems",inline=True)
    await i.edit_original_response(embed=result_e)

@tree.command(name="flip",description="Solo coin flip vs the house")
@app_commands.describe(wager="How many points to wager")
@casino_only()
async def flip_cmd(i, wager: int):
    uid=i.user.id
    if wager<=0: await i.response.send_message(embed=E("❌  Wager must be > 0",color=0xed4245),ephemeral=True); return
    if not spend_points(uid,wager): await i.response.send_message(embed=E("❌  Not Enough Points",color=0xed4245),ephemeral=True); return
    cd=check_game_cooldown(uid,5)
    if cd: await i.response.send_message(embed=E("⏳  Cooldown",f"Wait **{cd}s**.",0xfee75c),ephemeral=True); return
    luck=get_total_luck(uid)
    view=CoinFlipSoloView(uid,wager,luck)
    e=discord.Embed(title="🪙  Coin Flip — Pick a Side!",description=f"Wager: **{wager:,} pts** · Win doubles it!",color=0xfee75c)
    e.add_field(name="Luck",value=f"**{luck:.2f}x**",inline=True)
    await i.response.send_message(embed=e,view=view)

@tree.command(name="blackjack",description="Play Blackjack vs the dealer")
@app_commands.describe(wager="How many points to wager")
@casino_only()
async def blackjack_cmd(i, wager: int):
    uid=i.user.id
    if wager<=0: await i.response.send_message(embed=E("❌  Wager must be > 0",color=0xed4245),ephemeral=True); return
    if not spend_points(uid,wager): await i.response.send_message(embed=E("❌  Not Enough Points",color=0xed4245),ephemeral=True); return
    cd=check_game_cooldown(uid,8)
    if cd: await i.response.send_message(embed=E("⏳  Cooldown",f"Wait **{cd}s**.",0xfee75c),ephemeral=True); return
    luck=get_total_luck(uid)
    view=BlackjackView(uid,wager,luck); pv=view.hand_value(view.player)
    e=view.status_embed(); e.title="🃏  Blackjack"; e.description=f"Get closer to **21** than the dealer.\nWager: **{wager:,} gems**"
    if pv==21:
        payout=int(wager*BJ_PAYOUT*luck); add_points(uid,payout)
        await i.response.send_message(embed=E("🃏  Blackjack! Instant win!",f"You were dealt **21**!\nWon: **{payout:,} pts**!",0xffd700)); return
    await i.response.send_message(embed=e,view=view)

# ══════════════════════════════════════════════════════════════════
#  SLASH — Shop
# ══════════════════════════════════════════════════════════════════
@tree.command(name="shop",description="Browse the points shop")
async def shop(i):
    await i.response.send_message(embed=_embed_shop())

@tree.command(name="buy",description="Buy an item from the shop")
@app_commands.describe(item_id="Item number from /shop")
async def buy(i, item_id: int):
    item=get_shop_item(item_id)
    if not item: await i.response.send_message(embed=E("❌  Item Not Found",color=0xed4245),ephemeral=True); return
    if item["stock"]==0: await i.response.send_message(embed=E("❌  Out of Stock",color=0xed4245),ephemeral=True); return
    if get_points(i.user.id)<item["price"]:
        await i.response.send_message(embed=E("❌  Not Enough Points",f"Need **{item['price']:,} gems**, you have **{get_points(i.user.id):,} gems**.",0xed4245),ephemeral=True); return
    spend_points(i.user.id,item["price"])
    if item["stock"]>0: item["stock"]-=1
    save_json("shop",{"items":shop_items,"counter":shop_id_counter})
    ticket_id=gen_id(8)
    purchase_log.append({"ticket_id":ticket_id,"buyer_id":i.user.id,"item_id":item["id"],"item_name":item["name"],"price":item["price"],"timestamp":datetime.now(timezone.utc).isoformat()})
    save_json("purchases",purchase_log)
    conf_e=discord.Embed(title="✅  Purchase Successful!",description=f"**{item['name']}** purchased for **{item['price']:,} gems**.\nA private ticket channel has been created.",color=0x57f287,timestamp=datetime.now(timezone.utc))
    conf_e.set_footer(text=f"Ticket ID: {ticket_id}")
    await i.response.send_message(embed=conf_e,ephemeral=True)
    guild=i.guild
    if guild:
        supplier_role=guild.get_role(SUPPLIER_ROLE_ID)
        ow={guild.default_role:discord.PermissionOverwrite(read_messages=False),
            i.user:discord.PermissionOverwrite(read_messages=True,send_messages=True),
            guild.me:discord.PermissionOverwrite(read_messages=True,send_messages=True)}
        if supplier_role: ow[supplier_role]=discord.PermissionOverwrite(read_messages=True,send_messages=True)
        cat=discord.utils.get(guild.categories,name="tickets")
        try:
            ticket_ch=await guild.create_text_channel(name=f"ticket-{ticket_id.lower()}",overwrites=ow,category=cat)
            tickets.append({"ticket_id":ticket_id,"buyer_id":i.user.id,"item_id":item["id"],"channel_id":ticket_ch.id,"status":"open","timestamp":datetime.now(timezone.utc).isoformat()})
            save_json("tickets",tickets)
            tick_e=discord.Embed(title=f"🎫  Purchase Ticket — #{ticket_id}",color=0x5865F2,timestamp=datetime.now(timezone.utc))
            tick_e.add_field(name="Item",value=f"**{item['name']}** `#{item['id']}`",inline=True)
            tick_e.add_field(name="Paid",value=f"{item['price']:,} pts",inline=True)
            tick_e.add_field(name="Buyer",value=i.user.mention,inline=True)
            close_v=TicketCloseView(ticket_id)
            await ticket_ch.send(content=f"{i.user.mention} {supplier_role.mention if supplier_role else ''}",embed=tick_e,view=close_v)
        except Exception as ex:
            log.warning(f"Failed to create ticket channel: {ex}")

@tree.command(name="additem",description="[Supplier] Add an item to the shop")
async def additem(i):
    if not is_supplier(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    await i.response.send_modal(AddShopItemModal())

@tree.command(name="edititem",description="[Supplier] Edit a shop item")
@app_commands.describe(item_id="Item number")
async def edititem(i, item_id: int):
    if not is_supplier(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    item=get_shop_item(item_id)
    if not item: await i.response.send_message(embed=E("❌  Item Not Found",color=0xed4245),ephemeral=True); return
    await i.response.send_modal(EditShopItemModal(item))

@tree.command(name="removeitem",description="[Supplier] Remove an item from the shop")
@app_commands.describe(item_id="Item number")
async def removeitem(i, item_id: int):
    if not is_supplier(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    item=get_shop_item(item_id)
    if not item: await i.response.send_message(embed=E("❌  Item Not Found",color=0xed4245),ephemeral=True); return
    shop_items.remove(item); save_json("shop",{"items":shop_items,"counter":shop_id_counter})
    await i.response.send_message(embed=E("🗑️  Removed",f"**{item['name']}** removed.",0xed4245))

@tree.command(name="setstock",description="[Supplier] Update item stock")
@app_commands.describe(item_id="Item number",stock="New stock (-1 = unlimited)")
async def setstock(i, item_id: int, stock: int):
    if not is_supplier(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    item=get_shop_item(item_id)
    if not item: await i.response.send_message(embed=E("❌  Item Not Found",color=0xed4245),ephemeral=True); return
    item["stock"]=stock; save_json("shop",{"items":shop_items,"counter":shop_id_counter})
    await i.response.send_message(embed=E("✅  Stock Updated",f"**{item['name']}** stock → `{stock}`.",0x57f287))

@tree.command(name="addpoints",description="[Supplier] Add points to a user")
@app_commands.describe(member="Recipient",amount="Points to add")
async def addpoints(i, member: discord.Member, amount: int):
    if not is_supplier(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    add_points(member.id,amount)
    await i.response.send_message(embed=E("💰  Points Added",f"Added **{amount:,} pts** to {member.mention}.",0x57f287))

@tree.command(name="value",description="Submit a value for an in-game item")
@app_commands.describe(game="Game name",rarity="Rarity",value="Proposed value",item_name="Item name")
async def value_cmd(i, game: str, rarity: str, value: str, item_name: str):
    ticket_id=gen_id(8)
    value_submissions.append({"ticket_id":ticket_id,"user_id":i.user.id,"game":game,"rarity":rarity,"value":value,"item_name":item_name,"status":"open","timestamp":datetime.now(timezone.utc).isoformat()})
    save_json("value_submissions",value_submissions)
    conf_e=discord.Embed(title="✅  Value Submission Received!",description=f"Game: **{game}**\nRarity: **{rarity}**\nValue: **{value}**\nItem: **{item_name}**",color=0x57f287,timestamp=datetime.now(timezone.utc))
    await i.response.send_message(embed=conf_e,ephemeral=True)
    guild=i.guild
    if guild:
        supplier_role=guild.get_role(SUPPLIER_ROLE_ID)
        ow={guild.default_role:discord.PermissionOverwrite(read_messages=False),
            i.user:discord.PermissionOverwrite(read_messages=True,send_messages=True),
            guild.me:discord.PermissionOverwrite(read_messages=True,send_messages=True)}
        if supplier_role: ow[supplier_role]=discord.PermissionOverwrite(read_messages=True,send_messages=True)
        cat=discord.utils.get(guild.categories,name="tickets")
        try:
            ticket_ch=await guild.create_text_channel(name=f"value-{ticket_id.lower()}",overwrites=ow,category=cat)
            tick_e=discord.Embed(title=f"🎫  Value Submission — #{ticket_id}",color=0x5865F2,timestamp=datetime.now(timezone.utc))
            tick_e.add_field(name="Game",value=game,inline=True); tick_e.add_field(name="Rarity",value=rarity,inline=True)
            tick_e.add_field(name="Value",value=value,inline=True); tick_e.add_field(name="Item",value=item_name,inline=True)
            tick_e.add_field(name="Submitter",value=i.user.mention,inline=True)
            close_v=TicketCloseView(ticket_id)
            await ticket_ch.send(content=f"{i.user.mention} {supplier_role.mention if supplier_role else ''}",embed=tick_e,view=close_v)
        except Exception as ex:
            log.warning(f"Failed to create value ticket: {ex}")

# ══════════════════════════════════════════════════════════════════
#  SLASH — Stats
# ══════════════════════════════════════════════════════════════════
@tree.command(name="stats",description="View gambling stats")
@app_commands.describe(member="Leave blank for your own")
async def player_stats(i, member: Optional[discord.Member]=None):
    t=member or i.user; s=get_stats(t.id); rn,rc=get_rank(s["wins"])
    e=discord.Embed(title=f"📊  {t.display_name}'s Stats",color=rc)
    e.set_thumbnail(url=t.display_avatar.url)
    e.add_field(name="Rank",value=rn,inline=True); e.add_field(name="Win Rate",value=_winrate(t.id),inline=True)
    e.add_field(name="⭐ Rep",value=str(get_rep(t.id)),inline=True)
    e.add_field(name="Wins",value=str(s["wins"]),inline=True); e.add_field(name="Losses",value=str(s["losses"]),inline=True)
    e.add_field(name="Games Played",value=str(s["games_played"]),inline=True)
    e.add_field(name="💰 Points",value=f"{get_points(t.id):,} pts",inline=True)
    await i.response.send_message(embed=e)

@tree.command(name="leaderboard",description="Top players by wins")
async def leaderboard(i):
    if not stats: await i.response.send_message(embed=E("🏆  No Data Yet",color=0xffd700),ephemeral=True); return
    sp=sorted(stats.items(),key=lambda x:x[1]["wins"],reverse=True)[:LEADERBOARD_SIZE]
    medals=["🥇","🥈","🥉"]
    e=discord.Embed(title="🏆  GambleMatch Leaderboard",color=0xffd700)
    for rank,(uid,s) in enumerate(sp,1):
        m=i.guild.get_member(uid); name=m.display_name if m else f"#{uid}"
        badge=medals[rank-1] if rank<=3 else f"`#{rank}`"; rn,_=get_rank(s["wins"])
        e.add_field(name=f"{badge}  {name}",value=f"{rn}  ·  **{s['wins']}W** {s['losses']}L  ·  {_winrate(uid)} WR",inline=False)
    await i.response.send_message(embed=e)

@tree.command(name="richlist",description="Top points holders")
async def richlist(i):
    if not points: await i.response.send_message(embed=E("💰  No Points Data",color=0xffd700),ephemeral=True); return
    sp=sorted(points.items(),key=lambda x:x[1],reverse=True)[:LEADERBOARD_SIZE]
    medals=["🥇","🥈","🥉"]
    e=discord.Embed(title="💰  Points Rich List",color=0xffd700)
    for rank,(uid,bal) in enumerate(sp,1):
        m=i.guild.get_member(uid); name=m.display_name if m else f"#{uid}"
        badge=medals[rank-1] if rank<=3 else f"`#{rank}`"
        e.add_field(name=f"{badge}  {name}",value=f"**{bal:,} pts**",inline=False)
    await i.response.send_message(embed=e)

@tree.command(name="history",description="Last 10 match results")
async def history(i):
    if not match_history: await i.response.send_message(embed=E("📜  No History",color=0x5865F2),ephemeral=True); return
    recent=match_history[-10:][::-1]
    e=discord.Embed(title="📜  Recent Matches",color=0x5865F2)
    for m in recent:
        win=i.guild.get_member(m["winner_id"]); los=i.guild.get_member(m["loser_id"])
        wn=win.display_name if win else f"#{m['winner_id']}"; ln=los.display_name if los else f"#{m['loser_id']}"
        e.add_field(name=f"`{m['match_id']}` · {GAME_EMOJIS.get(m['game'],'🎲')} {m['game'].upper()} · Bo{m['best_of']}",value=f"🏆 **{wn}** defeated {ln}",inline=False)
    await i.response.send_message(embed=e)

@tree.command(name="rep",description="Give +1 rep to a player")
@app_commands.describe(member="Who to vouch")
async def give_rep(i, member: discord.Member):
    if member.id==i.user.id: await i.response.send_message(embed=E("❌  No self-rep",color=0xed4245),ephemeral=True); return
    add_rep(member.id,1)
    await i.response.send_message(embed=E("⭐  Rep Given",f"+1 to {member.mention}  ·  Now at **{get_rep(member.id)} ⭐**",0xffd700))

@tree.command(name="help",description="GambleMatch command reference")
async def help_cmd(i):
    e=discord.Embed(title="🎰 GambleMatch — Ultimate Guide",description=f"v{BOT_VERSION}",color=0x5865F2)
    e.add_field(name=f"🔍 Duel Arena",value="`/findg`  `/leaveq`  `/queue`  `/challenge @user`",inline=False)
    e.add_field(name=f"🎰 Casino",value="`/gamble`  `/bomb`  `/mines`  `/slots`  `/flip`  `/blackjack`",inline=False)
    e.add_field(name=f"💎 Wealth",value="`/balance`  `/daily`  `/give`  `/deposit`  `/withdraw`  `/bankbalance`",inline=False)
    e.add_field(name="🛒 Shop",value="`/shop`  `/buy <number>`",inline=False)
    e.add_field(name="🏪 Supplier",value="`/additem`  `/edititem`  `/removeitem`  `/setstock`  `/addpoints`",inline=False)
    e.add_field(name="📊 Stats",value="`/stats`  `/leaderboard`  `/richlist`  `/history`  `/rep`",inline=False)
    e.add_field(name="🌐 Website",value=f"`/login` — Get your website login code\n{WEBSITE_URL}",inline=False)
    await i.response.send_message(embed=e)

# ══════════════════════════════════════════════════════════════════
#  ROOM TIER DEFINITIONS
# ══════════════════════════════════════════════════════════════════
ROOM_TIERS = [
    {"key":"bronze",  "label":"🥉 Bronze Room",   "color":0xcd7f32,"min":0,        "max":50_000,          "luck_mult":0.5, "max_members":1,"perks":["🍀 Luck: 0.5×","👤 1 guest"],"role_name":"🥉 Bronze Room"},
    {"key":"silver",  "label":"🥈 Silver Room",   "color":0xc0c0c0,"min":51_000,   "max":150_000,         "luck_mult":1.5, "max_members":2,"perks":["🍀 Luck: 1.5×","👥 2 guests"],"role_name":"🥈 Silver Room"},
    {"key":"gold",    "label":"🥇 Gold Room",     "color":0xffd700,"min":151_000,  "max":250_000,         "luck_mult":2.5, "max_members":2,"perks":["🍀 Luck: 2.5×","👥 2 guests"],"role_name":"🥇 Gold Room"},
    {"key":"platinum","label":"💠 Platinum Room", "color":0x00bcd4,"min":251_000,  "max":500_000,         "luck_mult":5.0, "max_members":2,"perks":["🍀 Luck: 5×","👥 2 guests"],"role_name":"💠 Platinum Room"},
    {"key":"ruby",    "label":"💎 Ruby Room",     "color":0xe53935,"min":501_000,  "max":1_000_000,       "luck_mult":7.5, "max_members":4,"perks":["🍀 Luck: 7.5×","👥 4 guests"],"role_name":"💎 Ruby Room"},
    {"key":"emerald", "label":"💚 Emerald Room",  "color":0x2e7d32,"min":1_000_001,"max":7_500_000,       "luck_mult":10.0,"max_members":5,"perks":["🍀 Luck: 10×","👥 5 guests"],"role_name":"💚 Emerald Room"},
    {"key":"lithium", "label":"⚡ Lithium Room",  "color":0x7e57c2,"min":10_000_000,"max":999_999_999_999,"luck_mult":15.0,"max_members":10,"perks":["🍀 Luck: 15×","👥 10 guests"],"role_name":"⚡ Lithium Room"},
]

def get_room_tier(balance):
    best=None
    for tier in ROOM_TIERS:
        if tier["min"]<=balance<=tier["max"]: best=tier
    if balance>=10_000_000: best=ROOM_TIERS[-1]
    return best

def get_invite_luck_bonus(uid):
    count=invite_counts.get(uid,0); bonus=0.0
    for mn,mx,b in INVITE_LUCK_TABLE:
        if mn<=count<=mx: bonus=b; break
        if count>mx: bonus=b
    return min(bonus,MAX_INVITE_LUCK_BONUS)

def get_total_luck(uid):
    vip_bonus=0.0
    if uid in vip_rooms:
        tier=vip_rooms[uid]; vip_bonus=VIP_TIERS.get(tier,{}).get("luck_bonus",0.0)-1.0
    room=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
    room_bonus=room["tier_luck"] if room else 0.0
    base=1.0+room_bonus+vip_bonus
    return round(base+get_invite_luck_bonus(uid),2)

# ══════════════════════════════════════════════════════════════════
#  ROOM VIEWS
# ══════════════════════════════════════════════════════════════════
class RegisterRoomView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        btn=ui.Button(label="🏠  Register My Room",style=discord.ButtonStyle.success,custom_id="register_room_btn")
        btn.callback=self._register_cb; self.add_item(btn)

    async def _register_cb(self, interaction):
        uid=interaction.user.id; guild=interaction.guild; bal=get_points(uid)
        existing=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
        if existing:
            ch=guild.get_channel(int(existing["channel_id"]))
            await interaction.response.send_message(embed=discord.Embed(title="🏠  You Already Have a Room",description=f"Your room is at {ch.mention if ch else 'unknown'}.",color=0xfee75c),ephemeral=True); return
        tier=get_room_tier(bal)
        if tier is None:
            await interaction.response.send_message(embed=discord.Embed(title="❌  Not Enough Points",description=f"Balance: **{bal:,} pts**",color=0xed4245),ephemeral=True); return
        await interaction.response.defer(ephemeral=True)
        await _create_room(interaction.user,tier,guild,bal)
        room_data=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
        chan=guild.get_channel(int(room_data["channel_id"])) if room_data else None
        await interaction.followup.send(embed=discord.Embed(title=f"{tier['label']} Created!",description=f"Your room is ready: {chan.mention if chan else 'check rooms category'}",color=tier["color"]),ephemeral=True)

class RoomInviteView(ui.View):
    def __init__(self, room_channel_id):
        super().__init__(timeout=None)
        cid=str(room_channel_id)
        invite_btn=ui.Button(label="➕  Invite Guest",style=discord.ButtonStyle.primary,custom_id=f"room_invite_{cid}")
        kick_btn=ui.Button(label="➖  Kick Guest",style=discord.ButtonStyle.danger,custom_id=f"room_kick_{cid}")
        delete_btn=ui.Button(label="🗑️  Delete Room",style=discord.ButtonStyle.secondary,custom_id=f"room_delete_{cid}")
        invite_btn.callback=self._invite_cb; kick_btn.callback=self._kick_cb; delete_btn.callback=self._delete_cb
        self.add_item(invite_btn); self.add_item(kick_btn); self.add_item(delete_btn)
        self.room_channel_id=room_channel_id

    async def _invite_cb(self, interaction):
        room=rooms.get(str(self.room_channel_id))
        if not room or room["owner_id"]!=interaction.user.id:
            await interaction.response.send_message("Only the room owner can invite guests.",ephemeral=True); return
        tier_data=next((t for t in ROOM_TIERS if t["key"]==room["tier_key"]),None)
        current_guests=len(room.get("guests",[]))
        max_g=tier_data["max_members"] if tier_data else 1
        if current_guests>=max_g:
            await interaction.response.send_message(embed=discord.Embed(title="❌  Guest Limit Reached",color=0xed4245),ephemeral=True); return
        await interaction.response.send_modal(InviteGuestModal(self.room_channel_id))

    async def _kick_cb(self, interaction):
        room=rooms.get(str(self.room_channel_id))
        if not room or room["owner_id"]!=interaction.user.id:
            await interaction.response.send_message("Only the room owner can kick guests.",ephemeral=True); return
        if not room.get("guests"):
            await interaction.response.send_message("No guests to kick.",ephemeral=True); return
        await interaction.response.send_modal(KickGuestModal(self.room_channel_id))

    async def _delete_cb(self, interaction):
        room=rooms.get(str(self.room_channel_id))
        if not room or room["owner_id"]!=interaction.user.id:
            await interaction.response.send_message("Only the room owner can delete the room.",ephemeral=True); return
        await interaction.response.send_message(embed=E("🗑️  Deleting room in 5 seconds...",color=0xed4245),ephemeral=True)
        await asyncio.sleep(5)
        ch=interaction.guild.get_channel(self.room_channel_id)
        rooms.pop(str(self.room_channel_id),None); save_all()
        if ch:
            try: await ch.delete(reason="Owner deleted room")
            except Exception: pass

class InviteGuestModal(ui.Modal, title="Invite a Guest"):
    username=ui.TextInput(label="Guest username or user ID",placeholder="e.g. coolplayer or 123456789",max_length=50)
    def __init__(self, channel_id):
        super().__init__(); self.channel_id=channel_id
    async def on_submit(self, interaction):
        guild=interaction.guild; raw=self.username.value.strip(); member=None
        try: member=guild.get_member(int(raw))
        except ValueError: pass
        if not member: member=discord.utils.find(lambda m:m.name.lower()==raw.lower() or m.display_name.lower()==raw.lower(),guild.members)
        if not member:
            await interaction.response.send_message(embed=discord.Embed(title="❌  Member Not Found",color=0xed4245),ephemeral=True); return
        room=rooms.get(str(self.channel_id))
        if not room: await interaction.response.send_message("Room not found.",ephemeral=True); return
        if member.id in room.get("guests",[]):
            await interaction.response.send_message(f"{member.mention} is already a guest.",ephemeral=True); return
        ch=guild.get_channel(self.channel_id)
        if ch: await ch.set_permissions(member,read_messages=True,send_messages=True,use_application_commands=True)
        room.setdefault("guests",[]).append(member.id); save_all()
        await interaction.response.send_message(embed=discord.Embed(title="✅  Guest Invited",description=f"{member.mention} has been added!",color=0x57f287),ephemeral=True)
        if ch: await ch.send(embed=discord.Embed(title="👋  New Guest!",description=f"Welcome {member.mention} to the room! 🎉",color=0x57f287))

class KickGuestModal(ui.Modal, title="Kick a Guest"):
    username=ui.TextInput(label="Guest username or user ID to kick",max_length=50)
    def __init__(self, channel_id):
        super().__init__(); self.channel_id=channel_id
    async def on_submit(self, interaction):
        guild=interaction.guild; raw=self.username.value.strip()
        room=rooms.get(str(self.channel_id))
        if not room: await interaction.response.send_message("Room not found.",ephemeral=True); return
        member=None
        try: member=guild.get_member(int(raw))
        except ValueError: pass
        if not member: member=discord.utils.find(lambda m:m.name.lower()==raw.lower() or m.display_name.lower()==raw.lower(),guild.members)
        if not member or member.id not in room.get("guests",[]):
            await interaction.response.send_message("Guest not found in this room.",ephemeral=True); return
        ch=guild.get_channel(self.channel_id)
        if ch: await ch.set_permissions(member,overwrite=None)
        room["guests"].remove(member.id); save_all()
        await interaction.response.send_message(embed=discord.Embed(title="✅  Guest Removed",color=0xfee75c),ephemeral=True)

async def _create_room(owner, tier, guild, balance):
    global register_msg_id
    invite_bonus=get_invite_luck_bonus(owner.id); total_luck=round(tier["luck_mult"]+invite_bonus,2)
    cat=discord.utils.get(guild.categories,name=ROOMS_CATEGORY_NAME)
    if not cat: cat=await guild.create_category(ROOMS_CATEGORY_NAME)
    overwrites={
        guild.default_role:discord.PermissionOverwrite(read_messages=True,send_messages=False,use_application_commands=False),
        owner:discord.PermissionOverwrite(read_messages=True,send_messages=True,manage_messages=True,use_application_commands=True),
        guild.me:discord.PermissionOverwrite(read_messages=True,send_messages=True,manage_channels=True,use_application_commands=True),
    }
    safe_name=owner.display_name.lower().replace(" ","-")[:20]
    ch=await guild.create_text_channel(
        name=f"{tier['key']}-{safe_name}",overwrites=overwrites,category=cat,
        topic=f"{tier['label']} · Owner: {owner.display_name} · Luck: {total_luck}×",
    )
    perk_list="\n".join(f"• {p}" for p in tier["perks"])
    e=discord.Embed(title=f"{tier['label']} — {owner.display_name}'s Room",description=f"Welcome to your room!\n\n**Your Total Luck: {total_luck}×**",color=tier["color"],timestamp=datetime.now(timezone.utc))
    e.add_field(name="💰 Balance",value=f"{balance:,} pts",inline=True)
    e.add_field(name="🍀 Luck",value=f"{total_luck}×",inline=True)
    e.add_field(name="👥 Guest Slots",value=f"{tier['max_members']} max",inline=True)
    e.add_field(name="✨ Perks",value=perk_list,inline=False)
    e.set_thumbnail(url=owner.display_avatar.url)
    view=RoomInviteView(ch.id)
    await ch.send(content=owner.mention,embed=e,view=view)
    rooms[str(ch.id)]={"owner_id":owner.id,"channel_id":ch.id,"tier_key":tier["key"],"tier_luck":tier["luck_mult"],"total_luck":total_luck,"balance_at_creation":balance,"guests":[],"created_at":datetime.now(timezone.utc).isoformat()}
    save_all()
    await _assign_room_role(owner,tier,guild)

async def _assign_room_role(member, tier, guild):
    for t in ROOM_TIERS:
        role=discord.utils.get(guild.roles,name=t["role_name"])
        if role and role in member.roles:
            try: await member.remove_roles(role,reason="Room tier update")
            except Exception: pass
    role=discord.utils.get(guild.roles,name=tier["role_name"])
    if not role: role=await guild.create_role(name=tier["role_name"],color=discord.Color(tier["color"]),reason="GambleMatch room tier role")
    try: await member.add_roles(role,reason=f"Room tier: {tier['label']}")
    except Exception as ex: log.warning(f"Could not assign room role: {ex}")

async def _setup_invite_roles(guild):
    for n in range(1,51):
        name=f"🔗 {n} Invite{'s' if n>1 else ''}"
        if not discord.utils.get(guild.roles,name=name):
            try: await guild.create_role(name=name,color=discord.Color(0x5865F2),reason="GambleMatch invite tracking role"); await asyncio.sleep(0.3)
            except Exception as ex: log.warning(f"Could not create invite role {name}: {ex}")

async def _assign_invite_role(member, guild):
    count=invite_counts.get(member.id,0)
    if count<1 or count>50: return
    target_name=f"🔗 {count} Invite{'s' if count>1 else ''}"
    for n in range(1,51):
        rname=f"🔗 {n} Invite{'s' if n>1 else ''}"
        role=discord.utils.get(guild.roles,name=rname)
        if role and role in member.roles:
            try: await member.remove_roles(role,reason="Invite count update")
            except Exception: pass
    target_role=discord.utils.get(guild.roles,name=target_name)
    if not target_role:
        try: target_role=await guild.create_role(name=target_name,color=discord.Color(0x5865F2))
        except Exception: return
    try: await member.add_roles(target_role,reason="Invite tracking")
    except Exception as ex: log.warning(f"Invite role assign failed: {ex}")

# ══════════════════════════════════════════════════════════════════
#  SLASH — Room commands
# ══════════════════════════════════════════════════════════════════
@tree.command(name="myroom",description="View your room info and luck stats")
async def myroom(i):
    uid=i.user.id; room=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
    if not room:
        await i.response.send_message(embed=discord.Embed(title="🏠  No Room",description=f"Head to <#{ROOM_REGISTER_CHANNEL_ID}> and click **Register My Room**!",color=0xfee75c),ephemeral=True); return
    tier=next((t for t in ROOM_TIERS if t["key"]==room["tier_key"]),None)
    ch=i.guild.get_channel(int(room["channel_id"])); inv_bonus=get_invite_luck_bonus(uid); total=get_total_luck(uid)
    e=discord.Embed(title="🏠  Your Room",color=tier["color"] if tier else 0x5865F2)
    e.add_field(name="Tier",value=tier["label"] if tier else room["tier_key"],inline=True)
    e.add_field(name="Channel",value=ch.mention if ch else "unknown",inline=True)
    e.add_field(name="Base Luck",value=f"{room['tier_luck']}×",inline=True)
    e.add_field(name="Invite Bonus",value=f"+{inv_bonus}× ({invite_counts.get(uid,0)} invites)",inline=True)
    e.add_field(name="⚡ Total Luck",value=f"**{total}×**",inline=True)
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="deleteroom",description="Delete your room")
async def deleteroom(i):
    uid=i.user.id; room=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
    if not room: await i.response.send_message(embed=discord.Embed(title="❌  No Room to Delete",color=0xed4245),ephemeral=True); return
    ch=i.guild.get_channel(int(room["channel_id"]))
    rooms.pop(str(room["channel_id"]),None); save_all()
    if ch:
        try: await ch.delete(reason="Owner deleted room via /deleteroom")
        except Exception: pass
    await i.response.send_message(embed=discord.Embed(title="🗑️  Room Deleted",color=0xed4245),ephemeral=True)

@tree.command(name="rooms",description="List all active rooms")
async def list_rooms(i):
    if not rooms:
        await i.response.send_message(embed=discord.Embed(title="🏠  No Active Rooms",color=0x5865F2)); return
    e=discord.Embed(title=f"🏠  Active Rooms ({len(rooms)})",color=0x5865F2,timestamp=datetime.now(timezone.utc))
    for cid,room in list(rooms.items())[:15]:
        ch=i.guild.get_channel(int(cid)); owner=i.guild.get_member(room["owner_id"])
        tier=next((t for t in ROOM_TIERS if t["key"]==room["tier_key"]),None)
        e.add_field(
            name=f"{tier['label'] if tier else room['tier_key']} — {owner.display_name if owner else 'unknown'}",
            value=f"{ch.mention if ch else 'unknown'}  ·  Luck: **{room['total_luck']}×**",inline=False,
        )
    await i.response.send_message(embed=e)

@tree.command(name="upgraderoom",description="Upgrade your room based on your current balance")
async def upgraderoom(i):
    uid=i.user.id; bal=get_points(uid); tier=get_room_tier(bal)
    if not tier: await i.response.send_message(embed=discord.Embed(title="❌  Balance too low.",color=0xed4245),ephemeral=True); return
    existing=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
    if not existing: await i.response.send_message(embed=discord.Embed(title="❌  No room yet. Use the register button.",color=0xed4245),ephemeral=True); return
    if existing["tier_key"]==tier["key"]: await i.response.send_message(embed=discord.Embed(title="ℹ️  Already at this tier.",color=0xfee75c),ephemeral=True); return
    ch=i.guild.get_channel(int(existing["channel_id"]))
    rooms.pop(str(existing["channel_id"]),None)
    if ch:
        try: await ch.delete(reason="Room upgrade")
        except Exception: pass
    await i.response.defer(ephemeral=True)
    await _create_room(i.user,tier,i.guild,bal)
    await i.followup.send(embed=discord.Embed(title=f"⬆️  Upgraded to {tier['label']}!",color=tier["color"]),ephemeral=True)

@tree.command(name="myluck",description="Show your total luck multiplier")
async def myluck(i):
    uid=i.user.id; room=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
    base=room["tier_luck"] if room else 1.0; inv_bonus=get_invite_luck_bonus(uid); total=get_total_luck(uid)
    e=discord.Embed(title="🍀  Your Luck Stats",color=0x57f287)
    e.add_field(name="Room Luck",value=f"{base}×",inline=True)
    e.add_field(name="Invite Bonus",value=f"+{inv_bonus}×",inline=True)
    e.add_field(name="⚡ Total Luck",value=f"**{total}×**",inline=True)
    e.add_field(name="Invites",value=str(invite_counts.get(uid,0)),inline=True)
    await i.response.send_message(embed=e,ephemeral=True)

# ══════════════════════════════════════════════════════════════════
#  SLASH — VIP / Redeem Codes
# ══════════════════════════════════════════════════════════════════
@tree.command(name="register",description="[CODE_MAKER] Register a user for a VIP room tier")
@app_commands.describe(user="User to register",tier="VIP tier")
@app_commands.choices(tier=[app_commands.Choice(name="VIP 💎",value="vip"),app_commands.Choice(name="VVIP 👑",value="vvip"),app_commands.Choice(name="VVVIP 🌟",value="vvvip")])
async def register_cmd(i, user: discord.Member, tier: str):
    if not any(role.id==CODE_MAKER_ROLE_ID for role in i.user.roles):
        await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    if tier not in VIP_TIERS: await i.response.send_message(embed=E("❌  Invalid Tier",color=0xed4245),ephemeral=True); return
    tier_info=VIP_TIERS[tier]; vip_rooms[user.id]=tier
    save_json("vip_rooms",{str(k):v for k,v in vip_rooms.items()})
    e=discord.Embed(title=f"🎉  VIP Registration Confirmed!",description=f"{user.mention} registered for **{tier_info['name']}**!\n{tier_info['emoji']} Luck Bonus: **+{tier_info['luck_bonus']}x**",color=0xffd700,timestamp=datetime.now(timezone.utc))
    await i.response.send_message(embed=e)

CODE_TYPES=["currency","room_rank","role"]

@tree.command(name="addcode",description="[Code Maker] Create a redeem code")
@app_commands.describe(code_type="What the code gives",value="Amount / tier / role",code="The code string",max_uses="Max uses (0=unlimited)")
@app_commands.choices(code_type=[app_commands.Choice(name="💰 Currency",value="currency"),app_commands.Choice(name="🏠 Room rank",value="room_rank"),app_commands.Choice(name="🏅 Role",value="role")])
async def addcode(i, code_type: app_commands.Choice[str], value: str, code: str, max_uses: int=1):
    if not is_code_maker(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    code_upper=code.upper().strip()
    if code_upper in redeem_codes: await i.response.send_message(embed=E("❌  Code Already Exists",color=0xed4245),ephemeral=True); return
    redeem_codes[code_upper]={"type":code_type.value,"value":value.strip(),"uses_left":max_uses if max_uses>0 else -1,"uses_total":max_uses if max_uses>0 else -1,"created_by":i.user.id,"created_at":datetime.now(timezone.utc).isoformat(),"used_by":[]}
    save_json("redeem_codes",redeem_codes)
    e=discord.Embed(title="✅  Code Created",color=0x57f287)
    e.add_field(name="Code",value=f"`{code_upper}`",inline=True); e.add_field(name="Gives",value=value,inline=True); e.add_field(name="Max Uses",value="Unlimited" if max_uses<=0 else str(max_uses),inline=True)
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="redeem",description="Redeem a code for a reward")
@app_commands.describe(code="The code to redeem")
async def redeem(i, code: str):
    uid=i.user.id; code_upper=code.upper().strip(); entry=redeem_codes.get(code_upper)
    if not entry: await i.response.send_message(embed=E("❌  Invalid Code",color=0xed4245),ephemeral=True); return
    if uid in entry["used_by"]: await i.response.send_message(embed=E("❌  Already Used",color=0xed4245),ephemeral=True); return
    if entry["uses_left"]==0: await i.response.send_message(embed=E("❌  Code Expired",color=0xed4245),ephemeral=True); return
    guild=i.guild; result_desc=""
    if entry["type"]=="currency":
        amount=int(entry["value"]); add_points(uid,amount)
        result_desc=f"{EMOJI_GEM} You received {fmt_bal(amount)}!\nNew balance: {fmt_bal(get_points(uid))}"
    elif entry["type"]=="room_rank":
        tier_key=entry["value"].lower(); tier=next((t for t in ROOM_TIERS if t["key"]==tier_key),None)
        if not tier: await i.response.send_message(embed=E("❌  Invalid tier in code.",color=0xed4245),ephemeral=True); return
        existing=next((r for r in rooms.values() if r.get("owner_id")==uid),None)
        if existing:
            ch=guild.get_channel(int(existing["channel_id"])); rooms.pop(str(existing["channel_id"]),None)
            if ch:
                try: await ch.delete(reason="Room rank code redeemed")
                except Exception: pass
        await _create_room(i.user,tier,guild,get_points(uid))
        result_desc=f"🏠 Room set to **{tier['label']}**! Luck: **{tier['luck_mult']}×**"
    elif entry["type"]=="role":
        role=None
        try: role=guild.get_role(int(entry["value"]))
        except ValueError: role=discord.utils.get(guild.roles,name=entry["value"])
        if not role: await i.response.send_message(embed=E("❌  Role Not Found",color=0xed4245),ephemeral=True); return
        try: await i.user.add_roles(role,reason=f"Redeem code: {code_upper}")
        except discord.Forbidden: await i.response.send_message(embed=E("❌  Can't Assign Role",color=0xed4245),ephemeral=True); return
        result_desc=f"🏅 You received the **{role.name}** role!"
    entry["used_by"].append(uid)
    if entry["uses_left"]>0: entry["uses_left"]-=1
    save_json("redeem_codes",redeem_codes)
    e=discord.Embed(title="🎉  Code Redeemed!",description=result_desc,color=0x57f287,timestamp=datetime.now(timezone.utc))
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="deletecode",description="[Code Maker] Delete a redeem code")
@app_commands.describe(code="Code to delete")
async def deletecode(i, code: str):
    if not is_code_maker(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    code_upper=code.upper().strip()
    if code_upper not in redeem_codes: await i.response.send_message(embed=E("❌  Code Not Found",color=0xed4245),ephemeral=True); return
    del redeem_codes[code_upper]; save_json("redeem_codes",redeem_codes)
    await i.response.send_message(embed=E("🗑️  Code Deleted",f"`{code_upper}` removed.",0xed4245),ephemeral=True)

@tree.command(name="listcodes",description="[Code Maker] List all active redeem codes")
async def listcodes(i):
    if not is_code_maker(i.user): await i.response.send_message(embed=E("❌  No Permission",color=0xed4245),ephemeral=True); return
    if not redeem_codes: await i.response.send_message(embed=E("📋  No Active Codes",color=0x5865F2),ephemeral=True); return
    e=discord.Embed(title="📋  Active Redeem Codes",color=0x5865F2,timestamp=datetime.now(timezone.utc))
    for code_str,data in list(redeem_codes.items())[:20]:
        uses="∞" if data["uses_left"]==-1 else f"{data['uses_left']}/{data['uses_total'] if data['uses_total']!=-1 else '∞'}"
        e.add_field(name=f"`{code_str}` — {data['type']}",value=f"Value: `{data['value']}` · Uses left: **{uses}** · Redeemed: {len(data['used_by'])}",inline=False)
    await i.response.send_message(embed=e,ephemeral=True)

@tree.command(name="grantroom",description="[Room Owner] Grant VIP room access to a user")
@app_commands.describe(user="User to grant access to",tier="Room tier")
@app_commands.choices(tier=[app_commands.Choice(name="VIP 💎",value="vip"),app_commands.Choice(name="VVIP 👑",value="vvip"),app_commands.Choice(name="VVVIP 🌟",value="vvvip")])
async def grantroom(i, user: discord.Member, tier: str):
    if tier not in VIP_TIERS: await i.response.send_message(embed=E("❌  Invalid Tier",color=0xed4245),ephemeral=True); return
    caller_room=next((r for r in rooms.values() if r.get("owner_id")==i.user.id),None)
    if not caller_room: await i.response.send_message(embed=E("❌  No Room",color=0xed4245),ephemeral=True); return
    tier_info=VIP_TIERS[tier]; vip_rooms[user.id]=tier
    save_json("vip_rooms",{str(k):v for k,v in vip_rooms.items()})
    e=discord.Embed(title=f"✅  {tier_info['name']} Granted!",description=f"{user.mention} granted **{tier_info['name']}** tier!\nLuck Bonus: **+{tier_info['luck_bonus']}x**",color=0xffd700,timestamp=datetime.now(timezone.utc))
    await i.response.send_message(embed=e)

# ══════════════════════════════════════════════════════════════════
#  EVENTS & BACKGROUND TASKS
# ══════════════════════════════════════════════════════════════════
@bot.event
async def on_message(message):
    if message.author.bot or not message.guild: return
    uid=message.author.id
    msg_counts[uid]=msg_counts.get(uid,0)+1; count=msg_counts[uid]
    if count%MSG_REWARD_EVERY==0:
        add_points(uid,MSG_REWARD_AMOUNT); save_json("msg_counts",{str(k):v for k,v in msg_counts.items()})
        try:
            await message.channel.send(embed=discord.Embed(title=f"💬  Message Milestone!",description=(f"🎉 {message.author.mention} just hit **{count:,} messages**!\nReward: {fmt_bal(MSG_REWARD_AMOUNT)} added!\nNew balance: {fmt_bal(get_points(uid))}"),color=0x57f287),delete_after=15)
        except Exception: pass
    await bot.process_commands(message)

@bot.event
async def on_invite_create(invite):
    if invite.inviter: invite_cache[invite.code]=(invite.inviter.id,invite.uses or 0)

@bot.event
async def on_invite_delete(invite):
    invite_cache.pop(invite.code,None)

@bot.event
async def on_member_join(member):
    guild=member.guild
    try: current_invites=await guild.invites()
    except discord.Forbidden: return
    inviter_id=None
    for inv in current_invites:
        cached=invite_cache.get(inv.code)
        if cached:
            cached_inviter,cached_uses=cached; current_uses=inv.uses or 0
            if current_uses>cached_uses and inv.inviter and inv.inviter.id==cached_inviter:
                inviter_id=cached_inviter; invite_cache[inv.code]=(cached_inviter,current_uses); break
    if inviter_id:
        invite_counts[inviter_id]=invite_counts.get(inviter_id,0)+1
        save_json("invite_counts",{str(k):v for k,v in invite_counts.items()})
        inviter=guild.get_member(inviter_id)
        if inviter:
            await _assign_invite_role(inviter,guild)
            current_inv=invite_counts[inviter_id]; scaled_reward=INVITE_REWARD_PTS+(current_inv-1)*500
            add_points(inviter_id,scaled_reward)
            try:
                await inviter.send(embed=discord.Embed(title="🔗 Invite Success!",description=(f"**{member.display_name}** joined through your invite!\nYou claimed {fmt_bal(scaled_reward)}!\nTotal invites: **{current_inv}**"),color=0x57f287))
            except discord.Forbidden: pass
            try:
                wc=guild.get_channel(WELCOME_CHANNEL_ID)
                if wc: await wc.send(embed=discord.Embed(title="🎉 Welcome to GambleMatch!",description=(f"**{member.mention}** joined via {inviter.mention}'s invite!\nStart with `/daily` and `/balance`!"),color=0x57f287))
            except discord.Forbidden: pass

# ── Background tasks ───────────────────────────────────────────────
@tasks.loop(seconds=60)
async def sync_website():
    """Push real shop + richlist to the website every 60 seconds."""
    if not bot.guilds: return
    guild=bot.guilds[0]
    await push_to_website(guild)

@sync_website.before_loop
async def before_sync():
    await bot.wait_until_ready()
    await asyncio.sleep(10)  # short delay after startup

@tasks.loop(hours=1)
async def room_hourly_reward():
    if not bot.guilds: return
    guild=bot.guilds[0]
    for cid,room in rooms.items():
        owner_id=room["owner_id"]; tier_key=room.get("tier_key","")
        reward=ROOM_HOURLY_REWARD.get(tier_key,0)
        if owner_id in vip_rooms:
            vip_tier=vip_rooms[owner_id]; vip_info=VIP_TIERS.get(vip_tier,{}); reward+=vip_info.get("hourly_reward",0)
        if reward>0: add_points(owner_id,reward)
    save_json("points",{str(k):v for k,v in points.items()})

@room_hourly_reward.before_loop
async def before_room_reward():
    await bot.wait_until_ready(); await asyncio.sleep(120)

@tasks.loop(minutes=15)
async def auto_update_rooms():
    if not bot.guilds: return
    guild=bot.guilds[0]
    for cid,room in list(rooms.items()):
        owner=guild.get_member(room["owner_id"])
        if not owner: continue
        bal=get_points(room["owner_id"]); cur_tier=next((t for t in ROOM_TIERS if t["key"]==room["tier_key"]),None)
        new_tier=get_room_tier(bal)
        if not new_tier or (cur_tier and new_tier["key"]==cur_tier["key"]): continue
        old_label=cur_tier["label"] if cur_tier else room["tier_key"]
        ch=guild.get_channel(int(cid)); rooms.pop(cid,None)
        if ch:
            try: await ch.delete(reason="Auto room tier update")
            except Exception: pass
        await _create_room(owner,new_tier,guild,bal)
        try:
            await owner.send(embed=discord.Embed(title="🏠  Room Tier Updated",description=f"Your room was updated from **{old_label}** → **{new_tier['label']}**!",color=0x5865F2))
        except discord.Forbidden: pass
    save_all()

@auto_update_rooms.before_loop
async def before_auto_rooms():
    await bot.wait_until_ready(); await asyncio.sleep(60)

@tasks.loop(minutes=20)
async def send_tips():
    if not bot.guilds: return
    guild=bot.guilds[0]; tip=random.choice(TIPS)
    target_id=random.choice([POINTS_CHANNEL_ID,FINDG_CHANNEL_ID])
    chan=guild.get_channel(target_id)
    if chan:
        try: await chan.send(embed=discord.Embed(description=tip,color=0xfee75c),delete_after=300)
        except Exception: pass

@send_tips.before_loop
async def before_tips():
    await bot.wait_until_ready(); await asyncio.sleep(random.randint(60,300))

@tasks.loop(minutes=30)
async def autosave():
    save_all()

@autosave.before_loop
async def before_autosave():
    await bot.wait_until_ready()

@tasks.loop(hours=1)
async def send_promos():
    if not bot.guilds: return
    guild=bot.guilds[0]; channels=[c for c in guild.text_channels if c.permissions_for(guild.me).send_messages]
    if not channels: return
    chan=random.choice(channels); promo=random.choice(PROMO_MESSAGES)
    e=discord.Embed(description=f"💎 **{promo}**",color=0xffd700); e.set_footer(text="GambleMatch Promotion")
    try: await chan.send(embed=e)
    except Exception: pass

@send_promos.before_loop
async def before_promos():
    await bot.wait_until_ready(); await asyncio.sleep(60)

@tasks.loop(minutes=5)
async def update_presence():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"{len(queue)} in queue | {len(active_matches)} active"))

@update_presence.before_loop
async def before_presence():
    await bot.wait_until_ready()

# ══════════════════════════════════════════════════════════════════
#  ON READY
# ══════════════════════════════════════════════════════════════════
async def _restore_persistent_views():
    bot.add_view(RegisterRoomView())
    for cid_str in rooms:
        try: bot.add_view(RoomInviteView(int(cid_str)))
        except Exception as ex: log.warning(f"Could not restore RoomInviteView for {cid_str}: {ex}")
    for ticket in tickets:
        if ticket.get("status")!="closed":
            try: bot.add_view(TicketCloseView(ticket["ticket_id"]))
            except Exception as ex: log.warning(f"Could not restore TicketCloseView: {ex}")

async def _ensure_register_message(guild):
    global register_msg_id
    chan=guild.get_channel(ROOM_REGISTER_CHANNEL_ID)
    if not chan: return
    if register_msg_id:
        try:
            existing=await chan.fetch_message(register_msg_id)
            await existing.edit(view=RegisterRoomView()); return
        except (discord.NotFound,discord.HTTPException): pass
    tier_lines="\n".join(f"• **{t['label']}** — {t['min']:,}–{t['max']:,} pts · Luck **{t['luck_mult']}×** · {t['max_members']} guest(s)" for t in ROOM_TIERS)
    e=discord.Embed(title="🏠  Register Your Room",description=(f"Click below to register a private room based on your points balance.\n\n**Room Tiers:**\n{tier_lines}\n\n📌 Use `/upgraderoom` when your balance grows.\n🍀 Invite friends for extra luck bonuses!\n\n🌐 Check our website: **{WEBSITE_URL}**"),color=0x5865F2,timestamp=datetime.now(timezone.utc))
    e.set_footer(text="GambleMatch Room System")
    view=RegisterRoomView(); msg=await chan.send(embed=e,view=view)
    register_msg_id=msg.id; save_all()

@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user} ({bot.user.id})")
    await _restore_persistent_views()
    if GUILD_ID:
        g=discord.Object(id=GUILD_ID)
        tree.copy_global_to(guild=g); await tree.sync(guild=g)
        log.info(f"Synced to guild {GUILD_ID}")
    else:
        await tree.sync(); log.info("Synced globally")

    update_presence.start()
    autosave.start()
    send_tips.start()
    send_promos.start()
    auto_update_rooms.start()
    room_hourly_reward.start()
    sync_website.start()   # ← NEW: push data to website every 60s

    for guild in bot.guilds:
        try:
            invites=await guild.invites()
            for inv in invites:
                if inv.inviter: invite_cache[inv.code]=(inv.inviter.id,inv.uses or 0)
        except Exception: pass
        asyncio.create_task(_setup_invite_roles(guild))
        asyncio.create_task(_ensure_register_message(guild))

    meta=load_json("meta",{})
    if meta.get("last_changelog_ver")!=BOT_VERSION:
        await send_changelog(
            f"GambleMatch v{BOT_VERSION} — Website Sync",
            f"**New in v{BOT_VERSION}:**\n• 🌐 Real-time website sync — shop and richlist now live on the website!\n• Website: **{WEBSITE_URL}**\n• All previous features preserved.",
            color=0x57f287,
        )
        save_json("meta",{"last_changelog_ver":BOT_VERSION})

if __name__=="__main__":
    bot.run(BOT_TOKEN)
