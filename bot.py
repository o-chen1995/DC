import discord
from discord.ext import commands

# 設置機器人指令前綴
intents = discord.Intents.default()
intents.message_content = True  # 啟用訊息內容，允許讀取訊息的內容
bot = commands.Bot(command_prefix="!", intents=intents)

# 移除 Discord 默認的 help 命令
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="輸入 !margin 查看入場資金"))

@bot.command()
async def margin(ctx, entry_price: float, stop_price: float, leverage: int, max_loss: float):
    """
    計算所需的入場資金（保證金）
    指令格式：!margin [入場價格] [止損價格] [槓桿倍數] [最大虧損金額]
    """
    try:
        # 計算價格波動，根據是多單還是空單來決定
        if entry_price < stop_price:
            # 空單
            price_change = stop_price - entry_price
        elif entry_price > stop_price:
            # 多單
            price_change = entry_price - stop_price
        else:
            await ctx.send("入場價格與止損價格相等，請檢查您的輸入。")
            return
        
        # 計算總頭寸
        total_position = (max_loss * entry_price) / price_change

        # 計算保證金（入場資金）
        margin = total_position / leverage

        # 回覆用戶
        await ctx.send(
            f"入場價格：${entry_price:.2f}\n"
            f"止損價格：${stop_price:.2f}\n"
            f"槓桿倍數：{leverage}x\n"
            f"最大虧損：${max_loss:.2f} USDT\n"
            f"所需入場資金（保證金）：${margin:.2f} USDT"
        )
    except Exception as e:
        await ctx.send("發生錯誤，請確認輸入的參數格式正確！")
        print(e)

# 用你的機器人 Token 替換此處
bot.run("MTMyODQ2MTM4NTU5OTk0Njg1NA.G9cMzJ.tZOlIf7uND8BdYi1SpSEJSuQkyiSY-LePfQC2Y")
