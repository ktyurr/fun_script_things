from discord.ext import commands
import discord.file
import urllib.request
from PIL import Image
from googletrans import LANGUAGES
from googletrans import Translator

bot = commands.Bot(command_prefix='!')

# Tämä tehty lähinnä puhtaasti opettavaisuuden nimissä
# Olin vastikään käynyt kurssia algoritmeistä ja tietokannoista, joten
# tuli väsättyä komento botille joka järjestää kirjaimet aakkosjärjestykseen insertion sortilla 
@bot.command(name="sort")
async def sort_text(ctx, *args):
    args = args[0:]
    text = "".join(args)
    text_as_list = []
    for char in text:
        text_as_list.append(char)

    cycles = 0
    switches = 0
    continue_sort = True
    while continue_sort:

        # oletetaan kaikki järjestyksessä
        in_order = True

        # käydään merkit yksitellen läpi, vaihdetaan epäjärjestyksessä olvat parit päittäin
        for i in range(0, len(text_as_list) - 1):
            if text_as_list[i] > text_as_list[i+1]:
                tmp = text_as_list[i]
                text_as_list[i] = text_as_list[i+1]
                text_as_list[i+1] = tmp
                switches += 1

        # järjestyksen tarkistus
        for i in range(len(text_as_list)-1):
            if text_as_list[i] > text_as_list[i+1]:
                in_order = False

        # Ylimääräistä, koodin kirjoittamisesta jokin tovi,
        # niin muistaakseni tämä oli sen takia että
        # oli päheetä nähdä välivaiheet
        if in_order == True:
            continue_sort = False
        cycles += 1

        await ctx.send("".join(text_as_list))
    await ctx.send("{} {}".format("Switches:", switches))
    await ctx.send("{} {}".format("Whole thing inspections:", cycles))


# Testattiin miten saisi botin oppimaan tulkkaamista
@bot.command(name="trans")
async def translate_text(ctx, *args):
    try:
        language = args[0]
        args = args[1:]
        text_to_translate = " ".join(args)

        translator = Translator()
        translated = translator.translate(text_to_translate, dest=language)
        teksti = translated.text
        kieli = translated.src
        kielialkupera = "käännetty kielestä: " + LANGUAGES[kieli] + "\n"
        kielialkupera += teksti
        await ctx.send(kielialkupera)
    except ValueError:
        await ctx.send("ei oo tommost kielt iha oikeest")


# kielten lyhenteet pastebinissä
@bot.command(name="langs")
async def languages(ctx):
    await ctx.send("https://pastebin.com/raw/4XSpGRGi")


# hello world tier toimivuustesti botille
@bot.command(name="voiveljet")
async def veljet(ctx, *args):
    numero = int(args[0])
    for i in range(numero):
        await ctx.send("voi veljet")

# kuvan muuttaminen ei ASCII-artiksi, vaan emoji-artiksi
@bot.command(name="image")
async def print_image(ctx, *args):

    image_link = args[0]
    kuva = "kuva.png"
    urllib.request.urlretrieve(image_link, kuva)
    im = Image.open(kuva).convert('RGB')
    width, height = im.size
    aspect_ratio = width / height
    width = 50 # mielivaltaisesti määritelty, pitää näyttää hyvältä discordissa
    height = round(width / aspect_ratio)
    im = im.resize((width, height), Image.BILINEAR)
    im.save(kuva)

    pixels = im.getdata()
    art = "."
    iter = 0
    for r, g, b in pixels:
        r = int(r)
        g = int(g)
        b = int(b)
        mark = ""

        # näille if, elif, else sotkuille varmasti jokin parempi ratkaisu,
        # ajatuksenvirta johti tähän, koska oli helppo silmämääräisesti
        # määritellä raja-arvot värien välille.

        # asiaan palaamisen arvoinen onklema
        if r >= g or r >= b:
            if g >= 0.80 * r:
                mark = ":yellow_square:"
            elif b >= 0.80 * r:
                mark = ":purple_square:"
            else:
                mark = ":red_square:"

        elif g >= b or g >= r:
            if b >= 0.80 * g:
                mark = ":blue_circle:"
            elif r >= 0.80 * g:
                mark = ":yellow:"
            else:
                mark = ":green_square:"

        elif b >= r or b >= g:
            if r >= 0.80 * b:
                mark = ":purple_square:"
            elif g >= 0.80 * b:
                mark = ":blue_square:"
            else:
                mark = ":blue_square:"

        elif r >= 160 and g >= 160 and b >= 160:
            mark = ":white_medium_square:"
            if r >= 200 and g >= 200 and b >= 200:
                mark = ":white_medium_square"
                if r >= 230 and g >= 230 and b >= 230:
                    mark = ":white_medium_square"

        elif r < 50 and g < 50 and b < 50:
            mark = ":black_small_square:"
            if r < 34 and g < 34 and b < 34:
                mark = ":black_medium_square:"
                if r < 20 and g < 20 and b < 20:
                    mark = ":black_large_square:"

        if b < 55:
            if g > 50 and g < 150:
                if r > 120 and r < 220:
                    mark = ":brown_square:"

        art += mark
        iter += 1

        if iter % width == 0:
            art += "\n"
            iter = 0
            await ctx.send(art)
            art = "."
    await ctx.send(file=discord.File(kuva))


bot.run('get_your_own_api_key')






