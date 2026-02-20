import discord
from discord.ext import commands
from discord import option, default_permissions
import os
from dotenv import load_dotenv
from booking_manager import BookingManager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Bot()
manager = BookingManager()

@bot.event
async def on_ready():
    print(f"{bot.user} ist online und bereit!")

@bot.slash_command(name="add_slot", description="Fügt einen neuen Buchungs-Slot hinzu (Admin only)")
@option("datum", description="Datum des Slots (z.B. 2025-10-01)")
@option("uhrzeit", description="Uhrzeit des Slots (z.B. 10:00)")
@option("max_teilnehmer", description="Maximale Anzahl an Teilnehmern", type=int)
@default_permissions(administrator=True)
async def add_slot(ctx, datum: str, uhrzeit: str, max_teilnehmer: int):
    slot_id, error = await manager.add_slot(datum, uhrzeit, max_teilnehmer)
    if error:
        await ctx.respond(error, ephemeral=True)
    else:
        await ctx.respond(f"Slot erfolgreich hinzugefügt! ID: {slot_id} am {datum} um {uhrzeit}.", ephemeral=True)

@bot.slash_command(name="view_slots", description="Zeigt alle verfügbaren Buchungs-Slots an")
async def view_slots(ctx):
    slots = await manager.get_slots()
    if not slots:
        await ctx.respond("Momentan sind keine Slots verfügbar.", ephemeral=True)
        return

    embed = discord.Embed(title="Verfügbare Buchungs-Slots", color=discord.Color.blue())
    for slot in slots:
        free_spaces = slot['max_participants'] - len(slot['participants'])
        if free_spaces > 0:
            embed.add_field(
                name=f"Slot ID: {slot['id']}",
                value=f"Datum: {slot['date']}\nUhrzeit: {slot['time']}\nFreie Plätze: {free_spaces}/{slot['max_participants']}",
                inline=False
            )

    if not embed.fields:
        await ctx.respond("Alle Slots sind bereits voll gebucht.", ephemeral=True)
    else:
        await ctx.respond(embed=embed)

@bot.slash_command(name="book", description="Buche einen freien Slot")
@option("slot_id", description="Die ID des Slots, den du buchen möchtest", type=int)
async def book(ctx, slot_id: int):
    success, message = await manager.book_slot(slot_id, str(ctx.author.id))
    await ctx.respond(message, ephemeral=True)

@bot.slash_command(name="my_bookings", description="Zeigt deine aktuellen Buchungen an")
async def my_bookings(ctx):
    bookings = await manager.get_user_bookings(str(ctx.author.id))
    if not bookings:
        await ctx.respond("Du hast aktuell keine aktiven Buchungen.", ephemeral=True)
        return

    embed = discord.Embed(title="Deine Buchungen", color=discord.Color.green())
    for slot in bookings:
        embed.add_field(
            name=f"Slot ID: {slot['id']}",
            value=f"Datum: {slot['date']}\nUhrzeit: {slot['time']}",
            inline=False
        )
    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="cancel", description="Storniere eine deiner Buchungen")
@option("slot_id", description="Die ID des Slots, den du stornieren möchtest", type=int)
async def cancel(ctx, slot_id: int):
    success, message = await manager.cancel_booking(slot_id, str(ctx.author.id))
    await ctx.respond(message, ephemeral=True)

@bot.slash_command(name="delete_slot", description="Löscht einen Slot (Admin only)")
@option("slot_id", description="Die ID des Slots, der gelöscht werden soll", type=int)
@default_permissions(administrator=True)
async def delete_slot(ctx, slot_id: int):
    if await manager.delete_slot(slot_id):
        await ctx.respond(f"Slot {slot_id} wurde erfolgreich gelöscht.", ephemeral=True)
    else:
        await ctx.respond(f"Slot {slot_id} konnte nicht gefunden werden.", ephemeral=True)

@bot.slash_command(name="list_all_slots", description="Listet alle Slots mit Teilnehmern auf (Admin only)")
@default_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = await manager.get_slots()
    if not slots:
        await ctx.respond("Es existieren keine Slots.", ephemeral=True)
        return

    embed = discord.Embed(title="Alle Buchungs-Slots (Admin Übersicht)", color=discord.Color.orange())
    for slot in slots:
        participants_count = len(slot['participants'])
        embed.add_field(
            name=f"Slot ID: {slot['id']} ({slot['date']} {slot['time']})",
            value=f"Teilnehmer: {participants_count}/{slot['max_participants']}",
            inline=False
        )
    await ctx.respond(embed=embed, ephemeral=True)

if __name__ == "__main__":
    if not TOKEN:
        print("Fehler: DISCORD_TOKEN nicht in .env gefunden.")
    else:
        bot.run(TOKEN)
