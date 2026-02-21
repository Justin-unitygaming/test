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
    print(f"{bot.user} ist online!")

@bot.slash_command(name="view_slots", description="Zeigt alle verfügbaren Termine an")
async def view_slots(ctx):
    slots = await manager.get_available_slots()
    if not slots:
        await ctx.respond("Momentan sind keine Termine verfügbar.", ephemeral=True)
        return

    response = "**Verfügbare Termine:**\n"
    for s in slots:
        response += f"ID: {s['id']} | Datum: {s['date']} | Uhrzeit: {s['time']}\n"

    await ctx.respond(response)

@bot.slash_command(name="book", description="Buche einen Termin mit der Slot-ID")
async def book(ctx, slot_id: int):
    success, message = await manager.book_slot(slot_id, ctx.author.id, str(ctx.author))
    await ctx.respond(message, ephemeral=True)

@bot.slash_command(name="add_slot", description="Fügt einen neuen Termin hinzu (Admin)")
@discord.default_permissions(administrator=True)
async def add_slot(ctx, datum: str, uhrzeit: str):
    slot_id = await manager.add_slot(datum, uhrzeit)
    await ctx.respond(f"Termin hinzugefügt mit ID: {slot_id}", ephemeral=True)

@bot.slash_command(name="delete_slot", description="Löscht einen Termin (Admin)")
@discord.default_permissions(administrator=True)
async def delete_slot(ctx, slot_id: int):
    await manager.delete_slot(slot_id)
    await ctx.respond(f"Termin {slot_id} gelöscht.", ephemeral=True)

@bot.slash_command(name="list_all_slots", description="Listet alle Termine auf (Admin)")
@discord.default_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = await manager.get_all_slots()
    if not slots:
        await ctx.respond("Keine Termine vorhanden.", ephemeral=True)
        return

    response = "**Alle Termine:**\n"
    for s in slots:
        status = "Verfügbar" if s['available'] else "Gebucht"
        response += f"ID: {s['id']} | Datum: {s['date']} | Uhrzeit: {s['time']} | Status: {status}\n"

    await ctx.respond(response, ephemeral=True)

@bot.slash_command(name="my_bookings", description="Zeigt deine Buchungen an")
async def my_bookings(ctx):
    bookings = await manager.get_user_bookings(ctx.author.id)
    if not bookings:
        await ctx.respond("Du hast keine aktiven Buchungen.", ephemeral=True)
        return

    response = "**Deine Buchungen:**\n"
    for b in bookings:
        response += f"Slot-ID: {b['slot_id']} | Datum: {b['date']} | Uhrzeit: {b['time']}\n"

    await ctx.respond(response, ephemeral=True)

@bot.slash_command(name="cancel", description="Storniert eine Buchung")
async def cancel(ctx, slot_id: int):
    success, message = await manager.cancel_booking(slot_id, ctx.author.id)
    await ctx.respond(message, ephemeral=True)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Warnung: DISCORD_TOKEN nicht in .env gefunden.")
