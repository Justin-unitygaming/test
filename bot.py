import discord
import os
from booking_manager import BookingManager
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Bot()
manager = BookingManager()

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.slash_command(description="Zeigt alle verfügbaren Buchungsslots an")
async def view_slots(ctx):
    slots = manager.get_available_slots()
    if not slots:
        await ctx.respond("Momentan sind keine freien Slots verfügbar.")
        return

    embed = discord.Embed(title="Verfügbare Buchungsslots", color=discord.Color.blue())
    for slot in slots:
        embed.add_field(
            name=f"Slot ID: {slot['id']}",
            value=f"📅 Datum: {slot['date']}\n⏰ Zeit: {slot['time']}\n📝: {slot['description']}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Buche einen verfügbaren Slot")
async def book(ctx, slot_id: str):
    success, message = manager.book_slot(slot_id, ctx.author.id, ctx.author.name)
    await ctx.respond(message)

@bot.slash_command(description="Zeigt deine aktuellen Buchungen an")
async def my_bookings(ctx):
    bookings = manager.get_user_bookings(ctx.author.id)
    if not bookings:
        await ctx.respond("Du hast momentan keine aktiven Buchungen.")
        return

    embed = discord.Embed(title="Deine Buchungen", color=discord.Color.green())
    for slot in bookings:
        embed.add_field(
            name=f"Slot ID: {slot['id']}",
            value=f"📅 Datum: {slot['date']}\n⏰ Zeit: {slot['time']}\n📝: {slot['description']}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Storniere eine deiner Buchungen")
async def cancel(ctx, slot_id: str):
    success, message = manager.cancel_booking(slot_id, ctx.author.id)
    await ctx.respond(message)

# Admin-Befehle
@bot.slash_command(description="Fügt einen neuen Buchungsslot hinzu")
@discord.default_permissions(administrator=True)
async def add_slot(ctx, datum: str, zeit: str, beschreibung: str):
    slot_id = manager.add_slot(datum, zeit, beschreibung)
    await ctx.respond(f"Slot erfolgreich hinzugefügt! ID: {slot_id}")

@bot.slash_command(description="Entfernt einen Buchungsslot")
@discord.default_permissions(administrator=True)
async def delete_slot(ctx, slot_id: str):
    success = manager.delete_slot(slot_id)
    if success:
        await ctx.respond(f"Slot {slot_id} wurde gelöscht.")
    else:
        await ctx.respond(f"Fehler: Slot {slot_id} nicht gefunden.")

@bot.slash_command(description="Listet alle Slots (verfügbar und gebucht) auf")
@discord.default_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = manager.get_all_slots()
    if not slots:
        await ctx.respond("Keine Slots vorhanden.")
        return

    embed = discord.Embed(title="Alle Buchungsslots", color=discord.Color.dark_gray())
    for slot in slots:
        status = "Gebucht von: " + slot['booked_by_name'] if slot['booked_by'] else "Frei"
        embed.add_field(
            name=f"Slot ID: {slot['id']} ({status})",
            value=f"📅 Datum: {slot['date']}\n⏰ Zeit: {slot['time']}\n📝: {slot['description']}",
            inline=False
        )
    await ctx.respond(embed=embed)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: DISCORD_TOKEN nicht in den Umgebungsvariablen gefunden.")
