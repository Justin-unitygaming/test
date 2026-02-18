import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from booking_manager import BookingManager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Bot()
manager = BookingManager()

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.slash_command(description="Einen neuen Buchungsslot hinzufügen (Admin)")
@discord.default_permissions(administrator=True)
async def add_slot(ctx, time: str, description: str):
    slot_id = manager.add_slot(time, description)
    await ctx.respond(f"Slot hinzugefügt: ID {slot_id}, Zeit: {time}, Beschreibung: {description}")

@bot.slash_command(description="Alle verfügbaren Slots anzeigen")
async def view_slots(ctx):
    slots = manager.get_slots()
    available_slots = [s for s in slots if s['booked_by'] is None]

    if not available_slots:
        await ctx.respond("Momentan sind keine freien Slots verfügbar.")
        return

    embed = discord.Embed(title="Verfügbare Buchungsslots", color=discord.Color.green())
    for s in available_slots:
        embed.add_field(name=f"Slot ID: {s['id']}", value=f"Zeit: {s['time']}\nBeschreibung: {s['description']}", inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen Slot buchen")
async def book(ctx, slot_id: int):
    success, message = manager.book_slot(slot_id, ctx.author.id, str(ctx.author))
    await ctx.respond(message)

@bot.slash_command(description="Meine Buchungen anzeigen")
async def my_bookings(ctx):
    bookings = manager.get_user_bookings(ctx.author.id)
    if not bookings:
        await ctx.respond("Du hast keine aktiven Buchungen.")
        return

    embed = discord.Embed(title="Deine Buchungen", color=discord.Color.blue())
    for s in bookings:
        embed.add_field(name=f"Slot ID: {s['id']}", value=f"Zeit: {s['time']}\nBeschreibung: {s['description']}", inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Eine Buchung stornieren")
async def cancel(ctx, slot_id: int):
    success, message = manager.cancel_booking(slot_id, ctx.author.id)
    await ctx.respond(message)

@bot.slash_command(description="Einen Slot löschen (Admin)")
@discord.default_permissions(administrator=True)
async def delete_slot(ctx, slot_id: int):
    manager.delete_slot(slot_id)
    await ctx.respond(f"Slot {slot_id} wurde gelöscht.")

@bot.slash_command(description="Alle Slots anzeigen (Admin)")
@discord.default_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = manager.get_slots()
    if not slots:
        await ctx.respond("Es gibt keine Slots.")
        return

    embed = discord.Embed(title="Alle Buchungsslots", color=discord.Color.orange())
    for s in slots:
        status = f"Gebucht von {s['user_name']}" if s['booked_by'] else "Frei"
        embed.add_field(name=f"Slot ID: {s['id']} ({status})", value=f"Zeit: {s['time']}\nBeschreibung: {s['description']}", inline=False)

    await ctx.respond(embed=embed)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: DISCORD_TOKEN nicht in der .env Datei gefunden.")
