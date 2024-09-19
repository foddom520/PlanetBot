import discord
from discord import app_commands
import math
from discord.ext import commands
import datetime
import numpy as np

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        ping_embed = discord.Embed(title="Ping", color=discord.Color.blue())
        ping_embed.add_field(name=f"{self.bot.user.name}'s Latency (ms): ", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        ping_embed.set_footer(text=f"requested by {ctx.author.name}.", icon_url=ctx.author.avatar)
        await ctx.send(embed=ping_embed)

    @app_commands.command(name="fl_run_calculator", description="Will tell you the total exp, runs required and estimated time to go from one level to the next")
    async def fl_run_calculator(self, interaction: discord.Interaction, start_level: int, end_level: int, exp_per_run: str, current_exp: str, run_time_mins: float = None):
        if end_level <= start_level:
            return await interaction.response.send_message("Error: End level must be at least 1 higher than the start level.")
    
        def calculate_exp(start_level, end_level):
            return sum(50 * (1.15 ** level) for level in range(start_level, end_level))

        def convert_to_number(s):
            s = s.lower()
            suffixes = {'k': 10**3, 'm': 10**6, 'b': 10**9, 't': 10**12, 'q': 10**15, 'qi': 10**18, 'sx': 10**21, 'sp': 10**24, 'oc': 10**27, 'n': 10**30, 'dc': 10**33, 'ud': 10**36, 'dd': 10**39, 'td': 10**42, 'qd': 10**45, 'qid': 10**48, 'sd': 10**51, 'spd': 10**54, 'ocd': 10**57, 'nd': 10**60, 'vg': 10**63}
            for suffix, value in suffixes.items():
                if s.endswith(suffix):
                    return int(float(s[:-1]) * value)
            return int(s)

        def format_number(num):
            suffixes = ['Vg', 'Nd', 'Ocd', 'Spd', 'Sd', 'QiD', 'Qd', 'Td', 'Dd', 'Ud', 'Dc', 'N', 'Oc', 'Sp', 'Sx', 'Qi', 'Q', 'T', 'B', 'M', 'K']
            values = [10**63, 10**60, 10**57, 10**54, 10**51, 10**48, 10**45, 10**42, 10**39, 10**36, 10**33, 10**30, 10**27, 10**24, 10**21, 10**18, 10**15, 10**12, 10**9, 10**6, 10**3]
            for suffix, value in zip(suffixes, values):
                if num >= value:
                    return f"{num / value:.2f}{suffix}"
            return str(num)

        def calculate_runs(total_exp, exp_per_run):
            return total_exp / exp_per_run

        def calculate_time(runs_needed, run_time_mins):
            return runs_needed * run_time_mins / 60

        total_exp = calculate_exp(start_level, end_level)
        current_exp = convert_to_number(current_exp)
        total_exp -= current_exp
        exp_per_run = convert_to_number(exp_per_run)
        runs_needed = calculate_runs(total_exp, exp_per_run)

        embed = discord.Embed(title="FL Run Calculator Results", color=0x280137)
        embed.add_field(name="** **", value=f"Number of runs needed to go from **Level ** **{start_level}** to **Level** **{end_level}** with **{format_number(exp_per_run)}** experience per run.", inline=False)
        embed.add_field(name="**Total EXP Required**", value=f"{format_number(total_exp)}", inline=False)
        embed.add_field(name="**Runs Required**", value=f"{format_number(math.ceil(runs_needed))}", inline=False)
        if run_time_mins is not None:
            embed.add_field(name="**Run Time (minutes)**", value=f"{run_time_mins:.2f}", inline=False)
            total_time_hours = calculate_time(runs_needed, run_time_mins)
            embed.add_field(name="**Estimated Time**", value=f"{total_time_hours:.2f} hours", inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"{interaction.guild.name} |  Annarex", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pot_calculator", description="Calculate the pot value")
    async def pot_calculator(self, interaction: discord.Interaction, base_pot: int, num_upgrades: int, upgrades_done: int = 0):
        result = base_pot * (1.0050004482 ** (num_upgrades - upgrades_done))
        embed = discord.Embed(title="Potential Calculator", color=0x280137)
        embed.add_field(name="**Max Power**", value=f"{math.ceil(result)}", inline=False)
        embed.add_field(name="**Base Potential**", value=f"{base_pot:.2f}", inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"{interaction.guild.name} |  Annarex", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        await interaction.response.send_message(embed=embed)

    
    @app_commands.command(name="ring_calculator", description="Calculate the rings pot")
    async def ring_calculator(self, interaction: discord.Interaction, base_pot: int, num_runs: int, runs_done: int = 0):
        result = base_pot * (1.01 ** (num_runs - runs_done))
        embed = discord.Embed(title="Ring Pot Calculator Result", color=0x280137)
        embed.add_field(name="Base Pot", value=f"{base_pot:.2f}", inline=False)
        embed.add_field(name="Number of Runs", value=num_runs, inline=False)
        embed.add_field(name="Runs Done", value=runs_done, inline=False)
        embed.add_field(name="Calculated Pot Value", value=f"{math.ceil(result)}", inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"{interaction.guild.name} |  Annarex", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reroll_calculator", description="Calculate reroll probabilities")
    @app_commands.describe(maps="Choose a map.")
    @app_commands.choices(maps=[
        discord.app_commands.Choice(name="EF",  value="EF"),
        discord.app_commands.Choice(name="SC",  value="SC"),
    ])
    @app_commands.describe(item="Choose an item type.")
    @app_commands.choices(item=[
        discord.app_commands.Choice(name="weapon",  value="weapon"),
        discord.app_commands.Choice(name="armor",  value="armor"),
    ])
    @app_commands.describe(classes="Choose a class.")
    @app_commands.choices(classes=[
        discord.app_commands.Choice(name="War/mage",  value="war/mage"),
        discord.app_commands.Choice(name="Guardian",  value="guardian"),
    ])
    @app_commands.describe(rarity="Choose a rarity.")
    @app_commands.choices(rarity=[
        discord.app_commands.Choice(name="Secret",  value="secret"),
        discord.app_commands.Choice(name="Legendary",  value="legendary"),
        discord.app_commands.Choice(name="Epic",  value="epic"),
    ])
    async def reroll_calculator(self, interaction: discord.Interaction, item: str, current_value: float, maps: discord.app_commands.Choice[str], classes: discord.app_commands.Choice[str], rarity: discord.app_commands.Choice[str]):
        try:
            ranges = {
    "EF": {
        "war/mage": {
            "secret": {"weapon": (1527126, 1730499), "armor": (1324463, 1577538)},
            "legendary": {"weapon": (1324010, 1500035), "armor": (1141963, 1294038)},
            "epic": {"armor": (1016980, 1152418)},
        },
        "guardian": {
            "secret": {"armor": (31066616, 34005283)},
            "legendary": {"armor": (22066616, 25005283)},
        },
    },
    "SC": {
        "war/mage": {
            "secret": {"weapon": (509055, 576849)},
            "legendary": {"weapon": (441348, 500123)},
            "secret": {"armor": (475163, 525859)},
            "legendary": {"armor": (380663, 431359)},
            "epic": {"armor": (339002, 384153)},
        },
        "guardian": {
            "secret": {"armor": (10723329, 11751857)},
            "legendary": {"armor": (7723329, 8751857)},
        },
    },
    }

            if maps.value not in ranges:
                await interaction.response.send_message(f"Invalid map: {maps.value}")
                return

            if classes.value not in ranges[maps.value]:
                await interaction.response.send_message(f"Invalid class: {classes.value}")
                return

            if rarity.value not in ranges[maps.value][classes.value]:
                await interaction.response.send_message(f"Invalid rarity: {rarity.value} for class {classes.value}")
                return

            minimum_value, maximum_value = ranges[maps.value][classes.value][rarity.value].get(item, (None, None))

            if minimum_value is not None and maximum_value is not None:
                if current_value < minimum_value or current_value > maximum_value:
                    await interaction.response.send_message(f"Incorrect item pot: {item} on map {maps.value} for class {classes.value} with rarity {rarity.value}. Value must be between {minimum_value} and {maximum_value}.")
                    return
            
            if classes.value == "guardian" and item == "weapon":
                await interaction.response.send_message("You cannot match a weapon with the guardian class!")
                return
            
            if minimum_value is None or maximum_value is None:
                await interaction.response.send_message(f"Invalid item type: {item} on map {maps.value} for class {classes.value} with rarity {rarity.value}")
                return

            probability_up = (maximum_value - current_value) / (maximum_value - minimum_value)
            probability_down = (current_value - minimum_value) / (maximum_value - minimum_value)

            embed = discord.Embed(title="Probability Calculation", color=0x280137)
            embed.add_field(name="Item Information", value=f"Map: {maps.value}\nClass: {classes.value}\nRarity: {rarity.value}\nItem Type: {item}\nOriginal Pot: {int(current_value)}", inline=False)
            embed.add_field(name="Probability Up", value=f"{int(probability_up * 100)}%", inline=False)
            embed.add_field(name="Probability Down", value=f"{int(probability_down * 100)}%", inline=False)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"{interaction.guild.name} |  Annarex", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Test(bot))