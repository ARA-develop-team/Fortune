""" PiGamma Discord Bot Module """

import discord
import logging
import asyncio

from queue import Queue

from . import config_parser
from .custom_types.statistics import Statistics


class PiGamma(discord.Client):
    CONFIG_FILE = "pigamma_config.json"

    def __init__(self, token, channel_id: int, stats_queue: Queue, exit_flag: asyncio.Event):
        super().__init__(intents=discord.Intents.default())
        self.logger = logging.getLogger(__class__.__name__)

        self._exit_flag = exit_flag
        self._channel_id = channel_id
        self._channel = None
        self.stats_queue = stats_queue

        self.logger.info("PiGamma configured successfully!")
        self.run(token)

    async def _await_exit_flag(self):
        await self._exit_flag.wait()
        await self._channel.send(":red_square: Fortune disconnected from Discord")
        await self.close()

    async def _send_stats(self, channel):
        if self.stats_queue.empty():
            await channel.send("Nothing new so far")
            return

        stats = None
        while not self.stats_queue.empty():
            stats = self.stats_queue.get()

        if not isinstance(stats, Statistics):
            self.logger.warning(f"Incorrect statistics were received, not of the `Statistics` type.\n{stats}")
            await channel.send("An unusual type of statistics was detected, necessitating further inspection")
            return

        message = f"Things are as follows:\n"
        for account in stats.accounts:
            message += f"Your current {account.currency} balance is {account.balance}\n"

        if stats.total is not None:
            self.logger.info(stats.total)
            message += f"Your total balance is {stats.total.balance:.2f} {stats.total.currency}\n"

        await channel.send(message)

    async def on_ready(self):
        asyncio.create_task(self._await_exit_flag())
        self._channel = self.get_channel(self._channel_id)
        self.logger.info("PiGamma ready!")
        await self._channel.send(":green_square: Fortune connected to Discord")

    async def on_message(self, message):
        if message.author == self.user or self.user not in message.mentions:
            return

        message_content = message.content.lower()
        if "ping" in message_content:
            await message.channel.send("Reply!")

        if "stats" in message_content or "statistics" in message_content:
            await self._send_stats(message.channel)


def configure_pigamma(file, stats_queue, exit_flag):
    data = config_parser.get_pigamma_data(file)
    PiGamma(data["TOKEN"], int(data["CHANNEL_ID"]), stats_queue, exit_flag)
