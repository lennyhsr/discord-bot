import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

# ===== Webserver für Render =====
app = Flask('')

@app.route('/')
def home():
    return "Bot ist online!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# ===== Discord Bot =====
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")
    await bot.change_presence(activity=discord.Game(name="Überwacht deinen Server"))
    try:
        await bot.tree.sync()
        print("Slash Commands synchronisiert!")
    except Exception as e:
        print(e)

# Beispiel Slash Command Kick
@bot.tree.command(name="kick", description="Kickt ein Mitglied")
@app_commands.describe(member="Mitglied", reason="Grund")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member} gekickt!")
    else:
        await interaction.response.send_message("Keine Berechtigung!", ephemeral=True)

# Bot starten
bot.run(os.environ['MTQ0MDM3MjI5MjA5NzAxOTk5NA.GDtR2B.sRir5oMiFsuI1wveShlwrRE4saObB05po99nY4'])
