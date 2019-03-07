import io

import aiohttp
import discord
from PIL import Image
from discord.ext import commands

from ...lib.imageManipulation import perspective_change, blend, logical_and, logical_or, logical_xor, multiply, filter


class Cog:
    def __init__(self, bot):
        self.bot = bot

    async def get_recent_images(self, ctx):
        images = []
        count = 0
        image_count = 0
        async for message in ctx.channel.history():

            if count > 30:
                await ctx.channel.send("Could not find messages fitting requirements")
                return

            if image_count == 2:
                break

            if len(message.attachments) > 0 and message.attachments[0].url[-4:].lower() in ['.jpg', '.png']:
                print(message.attachments[0].url)
                image_count += 1

                async with aiohttp.ClientSession() as session:
                    async with session.get(message.attachments[0].url) as resp:
                        images.append(Image.open(io.BytesIO(await resp.read())))

            count += 1
        return images

    @commands.command(pass_context=True)
    async def img_pinch(self, ctx, side, percentage):
        percentage = int(percentage) / 100
        is_image = True if ctx.message.attachments[0].url[-4:].lower() in ['.jpg', '.png'] else False
        if not is_image:
            await ctx.channel.send("Attachment is not an image of supported type (.jpg, .png)")
        print(side)
        async with aiohttp.ClientSession() as session:
            async with session.get(ctx.message.attachments[0].url) as resp:
                image = io.BytesIO(await resp.read())
                image = Image.open(image)
                width, height = image.size
                output = io.BytesIO()
                if side.lower() == "top":
                    # perspective_change(image, [[-width * percentage, 0], [width * (1 + percentage), 0], [width, height],
                    #                          [0, height]]).save(output, format='PNG')
                    perspective_change.perspective_change(image,
                                                          [[0, 0], [width, 0], [width * (1 - percentage), height],
                                                           [width * percentage, height]]).save(output, format='PNG')

                output.seek(0)
                await ctx.message.channel.send(file=discord.File(fp=output, filename="morphed image.png"))

    @commands.command(pass_context=True)
    async def img_blend(self, ctx, transparency):
        session = aiohttp.ClientSession()
        transparency = int(transparency) / 100

        images = await self.get_recent_images(ctx)
        await ctx.message.channel.send(
            file=discord.File(fp=blend.blend(images[0], images[1], transparency), filename="blended image.png"))

    @commands.command(pass_context=True)
    async def logical_and(self, ctx):
        images = await self.get_recent_images(ctx)
        await ctx.message.channel.send(
            file=discord.File(fp=logical_and.logical_and(images[0], images[1]), filename="blended image.png"))

    @commands.command(pass_context=True)
    async def logical_or(self, ctx):
        images = await self.get_recent_images(ctx)
        await ctx.message.channel.send(
            file=discord.File(fp=logical_or.logical_or(images[0], images[1]), filename="blended image.png"))

    @commands.command(pass_context=True)
    async def logical_xor(self, ctx):
        images = await self.get_recent_images(ctx)
        await ctx.message.channel.send(
            file=discord.File(fp=logical_xor.logical_xor(images[0], images[1]), filename="blended image.png"))

    @commands.command(pass_context=True)
    async def multiply(self, ctx, brightness):
        images = await self.get_recent_images(ctx)
        await ctx.message.channel.send(
            file=discord.File(fp=multiply.multiply(images[0], images[1], brightness), filename="blended image.png"))

    @commands.command(pass_context=True)
    async def filter(self, ctx, type):
        images = await self.get_recent_images(ctx)
        await ctx.message.channel.send(
            file=discord.File(fp=filter.filter(images[0], type), filename="blended image.png"))


def setup(bot):
    bot.add_cog(Cog(bot))
