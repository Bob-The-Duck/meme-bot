import discord
from discord.ext import commands
from discord import app_commands
import discord.ui
from discord.ui import Button, View
import config  # Upewnij się, że masz plik config.py z tokenem i ID kanału
 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)
memy = []
#-------------------------------------------



loadingEmoji = 1413972619132403752# do uzupełnienia przez id emoji
acceptedEmoji = 1413972637964570645
rejectedEmoji = 1413972646206509227
staffEmoji = 1413972608499585044
veryfiedEmoji = 1413972621846118670


#-------------------------------------------
class MemeModerationView(View):
    def __init__(self, author: discord.User, embed: discord.Embed):
        super().__init__(timeout=None)
        self.author = author
        self.embed = embed

    @discord.ui.button(label="✅ Akceptuj", style=discord.ButtonStyle.success, custom_id="accept_meme")
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"<:accepted:1413972637964570645> Mem zaakceptowany przez {interaction.user.mention} <:verfied:1413972621846118670>", ephemeral=True)
        try:
            await self.author.send(f"<:accepted:1413972637964570645> Twój mem został **zaakceptowany** przez {interaction.user.mention} <:verfied:1413972621846118670>!")
        except discord.Forbidden:
            pass

        self.accept_button.disabled = True
        self.reject_button.disabled = True
        await interaction.message.edit(view=self)
        meme_ch = bot.get_channel(config.meme_channel)
        if meme_ch:
            self.embed.remove_footer()
            self.embed.add_field(name="Zatwierdzone!", value=f"<:staff:1413972608499585044> Mem został zaakceptowany przez {interaction.user.mention} <:veryfied:1413972621846118670>", inline=False)
            await meme_ch.send(embed=self.embed)

    @discord.ui.button(label="❌ Odrzuć", style=discord.ButtonStyle.danger, custom_id="reject_meme")
    async def reject_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"❌ Mem odrzucony przez {interaction.user.mention}", ephemeral=True)
        try:
            await self.author.send(f"<:rejected:1413972646206509227> Twój mem został **odrzucony** przez {interaction.user.mention}<:verfied:1413972621846118670>.")
        except discord.Forbidden:
            pass
        self.accept_button.disabled = True
        self.reject_button.disabled = True
        await interaction.message.edit(view=self)
#-------------------------------------------

@bot.event
async def on_ready():
    print(f'[+] Zalogowano jako: [{bot.user.name}]')
    await bot.tree.sync()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='/meme | Discord Bot Makers Union'))


#-------------------------------------------

# Prosta komenda tekstowa
@bot.command()
async def hello(ctx):
    await ctx.send("hello")


@bot.tree.command(name="meme", description="Wyślij mema z opisem")
@app_commands.describe(
    obrazek="Obrazek, który chcesz wysłać",
    opis="Opis mema"
)
async def wyslij_obrazek(interaction: discord.Interaction, obrazek: discord.Attachment, opis: str):

    if not obrazek.content_type.startswith("image/"):
        await interaction.response.send_message("To nie jest obrazek!", ephemeral=True)
        return

    memeIndex = (len(memy)+1)

    embed = discord.Embed(
        title="Nowy meme od użytkownika",
        description=opis,
        color=discord.Color.blue()
    )
    embed.add_field(name="Autor", value=f"<@{interaction.user.id}>", inline=False)
    embed.add_field(name="Index", value=f"Index mema: {memeIndex}", inline=False)
    embed.set_image(url=obrazek.url)
    
    Autor = interaction.user
    memy.append(Autor)
    print(memy)
    print(memeIndex)

    await interaction.response.send_message(f"<a:loading:1413972619132403752> Twój mem został zgłoszony do administracji!", ephemeral=True)


    log_channel = bot.get_channel(config.meme_log_ch)
    if log_channel:
        view = MemeModerationView(author=interaction.user, embed=embed)
        await log_channel.send(embed=embed, view=view)


    else:
        print("❌ Nie znaleziono kanału logów (sprawdź ID w config.py)")

 
    try:
        embed.set_footer(text=f"<:staff:1413972608499585044> Twój mem został wysłan do administracji i czeka na rozpatrzenie!")
        await interaction.user.send(embed=embed)
        await interaction.user.send(f"<a:loading:1413972619132403752> Proszę czekać, aż administracja zaakceptuje Twojego mema.")
    except discord.Forbidden:
        print(f"❌ Nie można wysłać DM do {interaction.user} (zablokowane prywatne wiadomości)")

#-------------------------------------------
# Uruchomienie bota
bot.run(config.tokenBota)
