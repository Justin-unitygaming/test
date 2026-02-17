import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from booking_manager import BookingManager

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialisiere den Bot und den BookingManager
bot = discord.Bot()
manager = BookingManager()

@bot.event
async def on_ready():
    print(f"{bot.user} ist online und bereit!")

@bot.slash_command(description="Einen neuen Buchungsslot hinzufügen")
@discord.default_permissions(administrator=True)
async def add_slot(ctx, time: str, description: str, max_participants: int):
    slot_id = manager.add_slot(time, description, max_participants)
    await ctx.respond(f"Slot #{slot_id} hinzugefügt für {time}: {description} (Max. Teilnehmer: {max_participants})")

@bot.slash_command(description="Alle verfügbaren Buchungsslots anzeigen")
async def view_slots(ctx):
    slots = manager.list_all_slots()
    if not slots:
        await ctx.respond("Momentan sind keine Buchungsslots verfügbar.")
        return

    embed = discord.Embed(title="Verfügbare Buchungsslots", color=discord.Color.blue())
    for slot_id, slot in slots.items():
        participants_count = len(slot['participants'])
        max_p = slot['max_participants']
        embed.add_field(
            name=f"Slot #{slot_id}: {slot['time']}",
            value=f"Beschreibung: {slot['description']}\nTeilnehmer: {participants_count}/{max_p}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen bestimmten Slot buchen")
async def book(ctx, slot_id: int):
    success, message = manager.book(slot_id, ctx.author.id, ctx.author.name)
    await ctx.respond(message, ephemeral=True)

@bot.slash_command(description="Deine eigenen Buchungen anzeigen")
async def my_bookings(ctx):
    bookings = manager.get_my_bookings(ctx.author.id)
    if not bookings:
        await ctx.respond("Du hast aktuell keine Buchungen.", ephemeral=True)
        return

    embed = discord.Embed(title="Deine Buchungen", color=discord.Color.green())
    for slot_id, slot in bookings:
        embed.add_field(
            name=f"Slot #{slot_id}: {slot['time']}",
            value=f"Beschreibung: {slot['description']}",
            inline=False
        )
    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(description="Eine bestehende Buchung stornieren")
async def cancel(ctx, slot_id: int):
    success, message = manager.cancel_booking(slot_id, ctx.author.id)
    await ctx.respond(message, ephemeral=True)

@bot.slash_command(description="Einen Slot löschen (Nur für Administratoren)")
@discord.default_permissions(administrator=True)
async def delete_slot(ctx, slot_id: int):
    if manager.delete_slot(slot_id):
        await ctx.respond(f"Slot #{slot_id} wurde erfolgreich gelöscht.")
    else:
        await ctx.respond(f"Slot #{slot_id} konnte nicht gefunden werden.", ephemeral=True)

@bot.slash_command(description="Alle Buchungen und Teilnehmer auflisten (Nur für Administratoren)")
@discord.default_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = manager.list_all_slots()
    if not slots:
        await ctx.respond("Es sind keine Slots zum Auflisten vorhanden.", ephemeral=True)
        return

    response = "**Alle Buchungen im Überblick:**\n"
    for slot_id, slot in slots.items():
        participants = ", ".join(slot['participants'].values()) if slot['participants'] else "Keine Teilnehmer"
        response += f"**#{slot_id} {slot['time']}**: {slot['description']} - Teilnehmer: {participants}\n"

    if len(response) > 2000:
        await ctx.respond("Die Liste ist leider zu lang für eine Discord-Nachricht.", ephemeral=True)
    else:
        await ctx.respond(response, ephemeral=True)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: Kein DISCORD_TOKEN in der .env Datei gefunden!")
