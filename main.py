import nextcord
from nextcord.ext import commands
from pretty_help import PrettyHelp
from unidecode import unidecode

import guess_the_player
import missing_11

import os
from dotenv import load_dotenv

load_dotenv()


intents = nextcord.Intents.default()
intents.message_content = True

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents, help_command=PrettyHelp())

@bot.event
async def on_ready():
    print("Bot's ready")


class SoccerGames(commands.Cog,  name='Soccer Games', description="Your best soccer games on Discord including Missing 11, Guess the player, etc."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='m11', brief="Guess the team's lineup from a history's match", usage="Type in the players' name in any order, try to finish all 11 players. Type `end` to end the game.",pass_context=True)
    async def m11(self, ctx):
        loading = await ctx.send("""```fix\nCreating Game... 🔃```""")
        bruh = missing_11.create_game()
        embed = missing_11.create_embed(bruh[0],bruh[1],bruh[2],bruh[3])
        await loading.delete()
        sent = await ctx.send(embed=embed)
        print(bruh[4])
        gk_done = []
        df_done = []
        mf_done = []
        fw_done = []
        def check(m):
            return m.content is not None and m.channel == ctx.channel
        submit_wait = True
        while submit_wait:
            msg = await bot.wait_for('message', check=check)
            if msg.content.lower() == "end":
                submit_wait = False
                await sent.delete()
                embed = missing_11.create_embed(bruh[0],bruh[1],bruh[2],bruh[3],gk_done+bruh[5],df_done+bruh[6],mf_done+bruh[7],fw_done+bruh[8])
                await ctx.send(embed=embed)
                await ctx.send(f"You got {11-len(bruh[4])}/11 correct players!")

            else:
                for player in bruh[5]:
                    if set(msg.content.lower().split()).issubset(set(unidecode(player.lower()).split())) and msg.content != "":
                        bruh[4].remove(player)
                        bruh[5].remove(player)
                        gk_done.append(player)
                        await msg.add_reaction("✅")
                for player in bruh[6]:
                    if set(msg.content.lower().split()).issubset(set(unidecode(player.lower()).split())) and msg.content != "":
                        bruh[4].remove(player)
                        bruh[6].remove(player)
                        df_done.append(player)
                        await msg.add_reaction("✅")
                for player in bruh[7]:
                    if set(msg.content.lower().split()).issubset(set(unidecode(player.lower()).split())) and msg.content != "":
                        bruh[4].remove(player)
                        bruh[7].remove(player)
                        mf_done.append(player)
                        await msg.add_reaction("✅")
                for player in bruh[8]:
                    if set(msg.content.lower().split()).issubset(set(unidecode(player.lower()).split())) and msg.content != "":
                        bruh[4].remove(player)
                        bruh[8].remove(player)
                        fw_done.append(player)
                        await msg.add_reaction("✅")
                await sent.delete()

                embed = missing_11.create_embed(bruh[0],bruh[1],bruh[2],bruh[3],gk_done,df_done,mf_done,fw_done)
                
                sent = await ctx.send(embed=embed)
                
                if bruh[4] == []:
                    submit_wait = False
                    await ctx.send("Done!")

    @commands.command(name="gtp", brief="Guess the player based on transfer history", usage="Type in the name of the player you think. Type `end` to end the game.", pass_context=True)
    async def gtp(self, ctx):
        def check(m):
            return m.content is not None and m.channel == ctx.channel
        loading = await ctx.send("""```fix\nCreating Game... 🔃```""")
        player_info = guess_the_player.rtp()
        print(player_info[0])
        embed = nextcord.Embed(title="Guess The Player", description="Guess the player based on transfer history")
        embed.add_field(name="Clubs", value=str("""```fix\n""")+player_info[1]+str("""```"""), inline=False)
        await loading.delete()
        await ctx.send(embed=embed)
        submit_wait = True
        while submit_wait:
            msg = await bot.wait_for('message', check=check)
            if msg.author != bot.user:
                if set(msg.content.lower().split()).issubset(set(unidecode(player_info[0].lower()).split())):
                    submit_wait = False
                    await msg.add_reaction("✅")
                    await ctx.send(f"Correct! You are good, {msg.author.display_name}")
                if msg.content.lower() == "end":
                    submit_wait = False
                    await ctx.send(f"End this question! The answer is {player_info[0]}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    msg = message.content
    if msg == "Hi Soccer Bot":
        await message.channel.send('Hi ' + message.author.display_name)
    await bot.process_commands(message)


bot.add_cog(SoccerGames(bot))
# Run the bot with your token
bot_token = os.getenv("BOT_TOKEN")
bot.run(bot_token)