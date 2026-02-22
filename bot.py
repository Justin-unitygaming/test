import discord
from discord.ext import commands
from discord import option
import os
from dotenv import load_dotenv
from booking_manager import BookingManager

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialisiere den Bot und den BookingManager
bot = discord.Bot()
manager = BookingManager()

@bot.event
async def on_ready():
    print(f"{bot.user} ist online und bereit!")

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("Du hast nicht die erforderlichen Berechtigungen (Administrator), um diesen Befehl auszuführen.", ephemeral=True)
    else:
        print(f"Ein Fehler ist aufgetreten: {error}")
        await ctx.respond("Ein unerwarteter Fehler ist aufgetreten.", ephemeral=True)

# Admin-Befehle
@bot.slash_command(description="Einen neuen Buchungsslot hinzufügen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("datum", description="Datum und Uhrzeit des Slots (z.B. 2023-10-27 10:00)")
@option("beschreibung", description="Kurze Beschreibung des Termins")
@option("kapazität", description="Maximale Anzahl an möglichen Buchungen", default=1)
async def add_slot(ctx, datum: str, beschreibung: str, kapazität: int):
    slot_id = await manager.add_slot(datum, beschreibung, kapazität)
    await ctx.respond(f"✅ Slot #{slot_id} für den **{datum}** ({beschreibung}) wurde erfolgreich erstellt.")

@bot.slash_command(description="Einen Buchungsslot löschen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("slot_id", description="Die ID des zu löschenden Slots")
async def delete_slot(ctx, slot_id: int):
    success = await manager.delete_slot(slot_id)
    if success:
        await ctx.respond(f"✅ Slot #{slot_id} wurde erfolgreich gelöscht.")
    else:
        await ctx.respond(f"❌ Slot #{slot_id} konnte nicht gefunden werden.", ephemeral=True)

@bot.slash_command(description="Alle Buchungsslots anzeigen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = await manager.get_all_slots()
    if not slots:
        await ctx.respond("Es sind derzeit keine Buchungsslots vorhanden.")
        return

    msg = "**📋 Liste aller Buchungsslots:**\n"
    for s in slots:
        bookings_count = len(s['bookings'])
        msg += f"• **ID: {s['id']}** | {s['datetime']} | {s['description']} | Buchungen: {bookings_count}/{s['capacity']}\n"
    await ctx.respond(msg)

# Nutzer-Befehle
@bot.slash_command(description="Verfügbare Buchungsslots anzeigen")
async def view_slots(ctx):
    slots = await manager.get_available_slots()
    if not slots:
        await ctx.respond("Aktuell sind leider keine freien Buchungsslots verfügbar.")
        return

    msg = "**📅 Verfügbare Buchungsslots:**\n"
    for s in slots:
        free_space = s['capacity'] - len(s['bookings'])
        msg += f"• **ID: {s['id']}** | {s['datetime']} | {s['description']} (Frei: {free_space}/{s['capacity']})\n"
    await ctx.respond(msg)

@bot.slash_command(description="Einen freien Slot buchen")
@option("slot_id", description="Die ID des Slots, den du buchen möchtest")
async def book(ctx, slot_id: int):
    success, message = await manager.book_slot(slot_id, ctx.author.id)
    if success:
        await ctx.respond(f"✅ {message}")
    else:
        await ctx.respond(f"❌ {message}", ephemeral=True)

@bot.slash_command(description="Deine eigenen Buchungen anzeigen")
async def my_bookings(ctx):
    slots = await manager.get_user_bookings(ctx.author.id)
    if not slots:
        await ctx.respond("Du hast aktuell keine aktiven Buchungen.")
        return

    msg = "**Your Bookings / Deine Buchungen:**\n"
    for s in slots:
        msg += f"• **ID: {s['id']}** | {s['datetime']} | {s['description']}\n"
    await ctx.respond(msg)

@bot.slash_command(description="Eine deiner Buchungen stornieren")
@option("slot_id", description="Die ID des Slots, den du stornieren möchtest")
async def cancel(ctx, slot_id: int):
    success, message = await manager.cancel_booking(slot_id, ctx.author.id)
    if success:
        await ctx.respond(f"✅ {message}")
    else:
        await ctx.respond(f"❌ {message}", ephemeral=True)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: DISCORD_TOKEN nicht in der .env Datei gefunden.")
        print("Bitte erstelle eine .env Datei mit DISCORD_TOKEN=dein_token_hier")
