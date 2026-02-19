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

# Admin commands
@bot.slash_command(description="Einen neuen Buchungsslot hinzufügen (Admin)")
@commands.has_permissions(administrator=True)
async def add_slot(ctx, time: str, capacity: int):
    slot_id = manager.add_slot(time, capacity)
    await ctx.respond(f"Slot hinzugefügt! ID: {slot_id}, Zeit: {time}, Kapazität: {capacity}")

@bot.slash_command(description="Einen Buchungsslot löschen (Admin)")
@commands.has_permissions(administrator=True)
async def delete_slot(ctx, slot_id: int):
    success = manager.delete_slot(slot_id)
    if success:
        await ctx.respond(f"Slot {slot_id} wurde gelöscht.")
    else:
        await ctx.respond(f"Slot {slot_id} nicht gefunden.")

@bot.slash_command(description="Alle Slots und Buchungen anzeigen (Admin)")
@commands.has_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = manager.get_all_slots()
    if not slots:
        await ctx.respond("Keine Slots vorhanden.")
        return

    response = "**Alle Buchungsslots:**\n"
    for slot in slots:
        booked_count = len(slot['booked_by'])
        response += f"ID: {slot['id']} | Zeit: {slot['time']} | Belegt: {booked_count}/{slot['max_capacity']} | User-IDs: {', '.join(map(str, slot['booked_by']))}\n"

    await ctx.respond(response)

# Public commands
@bot.slash_command(description="Verfügbare Buchungsslots anzeigen")
async def view_slots(ctx):
    slots = manager.get_all_slots()
    if not slots:
        await ctx.respond("Momentan sind keine Buchungsslots verfügbar.")
        return

    embed = discord.Embed(title="Verfügbare Buchungsslots", color=discord.Color.blue())
    for slot in slots:
        booked_count = len(slot['booked_by'])
        free_slots = slot['max_capacity'] - booked_count
        status = "VOLL" if free_slots <= 0 else f"{free_slots} frei"
        embed.add_field(
            name=f"Slot {slot['id']}: {slot['time']}",
            value=f"Kapazität: {booked_count}/{slot['max_capacity']} ({status})",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen Slot buchen")
async def book(ctx, slot_id: int):
    user_id = ctx.author.id
    success, message = manager.book_slot(slot_id, user_id)
    await ctx.respond(message)

@bot.slash_command(description="Meine Buchungen anzeigen")
async def my_bookings(ctx):
    user_id = ctx.author.id
    bookings = manager.get_user_bookings(user_id)
    if not bookings:
        await ctx.respond("Du hast aktuell keine Buchungen.")
        return

    response = "**Deine Buchungen:**\n"
    for slot in bookings:
        response += f"- Slot {slot['id']}: {slot['time']}\n"
    await ctx.respond(response)

@bot.slash_command(description="Eine Buchung stornieren")
async def cancel(ctx, slot_id: int):
    user_id = ctx.author.id
    success, message = manager.cancel_booking(slot_id, user_id)
    await ctx.respond(message)

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("Du hast nicht die erforderlichen Berechtigungen (Administrator), um diesen Befehl auszuführen.", ephemeral=True)
    else:
        raise error

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: DISCORD_TOKEN nicht in .env gefunden.")
