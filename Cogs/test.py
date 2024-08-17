import discord
from discord import app_commands
import math
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command( )
    async def ping(self, ctx):
        ping_embed = discord.Embed(title="Ping", color=discord.Color.blue())
        ping_embed.add_field(name=f"{self.bot.user.name}'s Latency (ms): ", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        ping_embed.set_footer(text=f"requested by {ctx.author.name}.", icon_url=ctx.author.avatar)
        await ctx.send(embed=ping_embed)

    @app_commands.command(name="fl_run_calculator", description="Will tell you the total exp, runs required and estimated time to go from one level to the next")
    async def fl_run_calculator(self, interaction: discord.Interaction, start_level: int, end_level: int, exp_per_run: str, current_exp: str, run_time_mins: float = None):
        def calculate_exp(start_level, end_level):
            total_exp = 0
            for level in range(start_level, end_level):
                exp = 50 * (1.15 ** level)
                total_exp += exp
            return total_exp

        def convert_to_number(s):
            s = s.lower()
            if s.endswith('k'):
                return int(float(s[:-1]) * 10**3)
            elif s.endswith('m'):
                return int(float(s[:-1]) * 10**6)
            elif s.endswith('b'):
                return int(float(s[:-1]) * 10**9)
            elif s.endswith('t'):
                return int(float(s[:-1]) * 10**12)
            else:
                return int(s)

        def format_number(num):
            if num >= 1000000000000:
                return f"{num / 1000000000000:.2f}t"
            elif num >= 1000000000:
                return f"{num / 1000000000:.2f}b"
            elif num >= 1000000:
                return f"{num / 1000000:.2f}m"
            elif num >= 1000:
                return f"{num / 1000:.2f}k"
            else:
                return str(num)

        def calculate_runs(total_exp, exp_per_run):
            runs_needed = total_exp / exp_per_run
            return runs_needed

        def calculate_time(runs_needed, run_time_mins):
            total_time_mins = runs_needed * run_time_mins
            total_time_hours = total_time_mins / 60
            return total_time_hours

        total_exp = calculate_exp(start_level, end_level)
        current_exp = convert_to_number(current_exp)
        total_exp -= current_exp
        exp_per_run = convert_to_number(exp_per_run)
        runs_needed = calculate_runs(total_exp, exp_per_run)

        embed = discord.Embed(title="FL Run Calculator Results", color=0x280137)
        embed.set_thumbnail(url="https://i.imgur.com/4MkIkzt.png")
        embed.add_field(name="**Leveling Up!**", value=f"From Level {start_level} to Level {end_level}", inline=False)
        embed.add_field(name="**EXP per Run**", value=f"{format_number(exp_per_run)}", inline=False)
        embed.add_field(name="**Current EXP**", value=f"{format_number(current_exp)}", inline=False)
        embed.add_field(name="**Total EXP Required**", value=f"{format_number(total_exp)}", inline=False)
        embed.add_field(name="**Runs Required**", value=f"{math.ceil(runs_needed)}", inline=False)
        if run_time_mins is not None:
            embed.add_field(name="**Run Time (minutes)**", value=f"{run_time_mins:.2f}", inline=False)
            total_time_hours = calculate_time(runs_needed, run_time_mins)
            embed.add_field(name="**Estimated Time**", value=f"{total_time_hours:.2f} hours", inline=False)
        embed.set_footer(text="Good luck with your leveling!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Get help on how to use the FL Run Calculator command")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="FL Run Calculator Help", color=0x280137)
        embed.add_field(name="Command Syntax", value="/fl_run_calculator <start_level> <end_level> <exp_per_run> [run_time_mins]", inline=False)
        embed.add_field(name="Arguments:", value="*", inline=False)
        embed.add_field(name="  `<start_level>`", value="The current level you are at. (integer)", inline=False)
        embed.add_field(name="  `<end_level>`", value="The level you want to reach. (integer)", inline=False)
        embed.add_field(name="  `<exp_per_run>`", value="The amount of EXP you gain per run. You can use suffixes like 'k', 'm', 'b', or 't' to represent thousands, millions, billions, or trillions, respectively. (string)", inline=True)
        embed.add_field(name="  `[run_time_mins]`", value="The time it takes to complete one run in minutes. (float, optional) (for example 4.10 means 4 minutes .10 means 10 seconds)", inline=False)
        embed.add_field(name="Example:", value="/fl_run_calculator 10 20 5k 10.5", inline=False)
        embed.set_footer(text="If you have any questions or need further assistance, feel free to ask!")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Test(bot))