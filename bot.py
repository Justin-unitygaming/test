import discord
from discord.ext import commands
from discord import option
import os
from dotenv import load_dotenv
from booking_manager import BookingManager

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()
manager = BookingManager()

# Hilfsfunktion zur Überprüfung der Admin-Rechte
def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")

@bot.slash_command(description="Einen neuen Buchungsslot hinzufügen (Admin)")
@option("zeit", description="Datum und Uhrzeit (z.B. 2023-10-27 10:00)")
@option("beschreibung", description="Beschreibung des Events")
@option("plaetze", description="Maximale Teilnehmerzahl", default=1)
async def add_slot(ctx: discord.ApplicationContext, zeit: str, beschreibung: str, plaetze: int):
    if not is_admin(ctx):
        await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
        return

    slot = manager.add_slot(zeit, beschreibung, plaetze)
    await ctx.respond(f"Slot hinzugefügt: ID {slot['id']} - {zeit}: {beschreibung} ({plaetze} Plätze)")

@bot.slash_command(description="Alle verfügbaren Buchungsslots anzeigen")
async def view_slots(ctx: discord.ApplicationContext):
    slots = manager.get_slots()
    if not slots:
        await ctx.respond("Momentan sind keine Buchungsslots verfügbar.")
        return

    embed = discord.Embed(title="Verfügbare Buchungsslots", color=discord.Color.blue())
    for slot in slots:
        verfuegbar = slot["max_participants"] - len(slot["booked_by"])
        if verfuegbar > 0:
            embed.add_field(
                name=f"ID {slot['id']}: {slot['time']}",
                value=f"{slot['description']}\nVerfügbare Plätze: {verfuegbar}/{slot['max_participants']}",
                inline=False
            )

    if not embed.fields:
        await ctx.respond("Momentan sind alle Slots ausgebucht.")
    else:
        await ctx.respond(embed=embed)

@bot.slash_command(description="Einen Slot buchen")
@option("slot_id", description="Die ID des zu buchenden Slots", type=int)
async def book(ctx: discord.ApplicationContext, slot_id: int):
    success, message = manager.book_slot(slot_id, ctx.author.id, ctx.author.name)
    await ctx.respond(message, ephemeral=True)

@bot.slash_command(description="Meine aktuellen Buchungen anzeigen")
async def my_bookings(ctx: discord.ApplicationContext):
    bookings = manager.get_user_bookings(ctx.author.id)
    if not bookings:
        await ctx.respond("Du hast aktuell keine Buchungen.", ephemeral=True)
        return

    embed = discord.Embed(title="Deine Buchungen", color=discord.Color.green())
    for slot in bookings:
        embed.add_field(
            name=f"ID {slot['id']}: {slot['time']}",
            value=f"{slot['description']}",
            inline=False
        )
    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(description="Eine Buchung stornieren")
@option("slot_id", description="Die ID des zu stornierenden Slots", type=int)
async def cancel(ctx: discord.ApplicationContext, slot_id: int):
    success, message = manager.cancel_booking(slot_id, ctx.author.id)
    await ctx.respond(message, ephemeral=True)

@bot.slash_command(description="Einen Buchungsslot löschen (Admin)")
@option("slot_id", description="Die ID des zu löschenden Slots", type=int)
async def delete_slot(ctx: discord.ApplicationContext, slot_id: int):
    if not is_admin(ctx):
        await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
        return

    slot = manager.delete_slot(slot_id)
    if slot:
        await ctx.respond(f"Slot gelöscht: ID {slot['id']} - {slot['time']}: {slot['description']}")
    else:
        await ctx.respond("Slot mit dieser ID wurde nicht gefunden.", ephemeral=True)

@bot.slash_command(description="Alle Slots und Teilnehmer anzeigen (Admin)")
async def list_all_slots(ctx: discord.ApplicationContext):
    if not is_admin(ctx):
        await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
        return

    slots = manager.get_slots()
    if not slots:
        await ctx.respond("Keine Slots vorhanden.")
        return

    embed = discord.Embed(title="Alle Buchungsslots (Admin Übersicht)", color=discord.Color.gold())
    for slot in slots:
        teilnehmer = ", ".join([b["user_name"] for b in slot["booked_by"]]) if slot["booked_by"] else "Keine"
        embed.add_field(
            name=f"ID {slot['id']}: {slot['time']}",
            value=f"Beschreibung: {slot['description']}\nTeilnehmer: {teilnehmer} ({len(slot['booked_by'])}/{slot['max_participants']})",
            inline=False
        )
    await ctx.respond(embed=embed, ephemeral=True)

if __name__ == "__main__":
    if not TOKEN:
        print("Fehler: DISCORD_TOKEN nicht in der .env Datei gefunden.")
    else:
        bot.run(TOKEN)
