from discord.ext import commands
import traceback
import asyncio
import discord
import logging
import datetime
import io

from modules import util, components

log = logging.getLogger('FortniteData.cogs.events')

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):

        lang = util.get_guild_lang(ctx)

        if isinstance(error, commands.CommandOnCooldown):

            end_seconds = int(str(error.retry_after)[0]) + 1

            embed = discord.Embed(
                description = util.get_str(lang, 'command_string_on_cooldown'),
                color = util.Colors.ORANGE
            )
            embed.set_footer(text=util.get_str(lang, 'command_string_on_cooldown_retry_after').format(seconds = end_seconds))
            
            await ctx.respond(
                embed=embed
            )
            return

        elif isinstance(error, commands.DisabledCommand):

            embed = discord.Embed(
                title = util.get_str(lang, 'command_string_disabled_command'),
                description = util.get_str(lang, 'command_string_disabled_command_description'),
                color = util.Colors.RED
            )
            embed.set_footer(text=util.get_str(lang, 'command_string_disabled_command_footer'))

            await ctx.respond(
                embed = embed
            )
            return

        else:

            traceback_str = ''.join(traceback.format_exception(None, error, error.__traceback__))

            util.error_cache[str(ctx.author.id)] = {} # save error to a temporary cache
            util.error_cache[str(ctx.author.id)][str(ctx.message.id)] = traceback_str

            description = util.get_str(lang, 'command_string_an_unknown_error_ocurred').format(traceback = traceback_str)

            if len(description) > 4096:
                description = util.get_str(lang, 'command_string_an_unknown_error_ocurred'.format(traceback = error))

            embed = discord.Embed(
                title = util.get_str(lang, 'command_string_an_error_ocurred'),
                description = util.get_str(lang, 'command_string_an_unknown_error_ocurred').format(traceback = traceback_str),
                color = util.Colors.RED
            )

            await ctx.respond(
                embed = embed,
                view = components.ReportToDeveloper(lang)
            )


    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        util.database_store_server(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        util.database_remove_server(guild)


def setup(bot):
    bot.add_cog(Events(bot))