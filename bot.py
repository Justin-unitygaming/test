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
    embed = discord.Embed(
        title="✅ Slot erstellt",
        description=f"Slot **#{slot_id}** wurde erfolgreich angelegt.",
        color=discord.Color.green()
    )
    embed.add_field(name="Datum", value=datum, inline=True)
    embed.add_field(name="Beschreibung", value=beschreibung, inline=True)
    embed.add_field(name="Kapazität", value=str(kapazität), inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen Buchungsslot löschen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("slot_id", description="Die ID des zu löschenden Slots")
async def delete_slot(ctx, slot_id: int):
    success = await manager.delete_slot(slot_id)
    if success:
        embed = discord.Embed(
            title="✅ Slot gelöscht",
            description=f"Slot **#{slot_id}** wurde erfolgreich entfernt.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Fehler",
            description=f"Slot **#{slot_id}** konnte nicht gefunden werden.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(description="Details einer Buchung anzeigen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("slot_id", description="Die ID des Slots")
async def show_bookings(ctx, slot_id: int):
    slot = await manager.get_slot_by_id(slot_id)
    if not slot:
        await ctx.respond(f"❌ Slot #{slot_id} wurde nicht gefunden.", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"📋 Buchungsdetails für Slot #{slot_id}",
        description=f"**Datum:** {slot['datetime']}\n**Beschreibung:** {slot['description']}",
        color=discord.Color.blue()
    )

    if not slot['bookings']:
        embed.add_field(name="Buchungen", value="Keine Buchungen vorhanden.", inline=False)
    else:
        mentions = [f"<@{uid}>" for uid in slot['bookings']]
        embed.add_field(name=f"Buchungen ({len(mentions)}/{slot['capacity']})", value="\n".join(mentions), inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Alle Buchungsslots anzeigen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = await manager.get_all_slots()
    if not slots:
        await ctx.respond("Es sind derzeit keine Buchungsslots vorhanden.", ephemeral=True)
        return

    embed = discord.Embed(
        title="📋 Liste aller Buchungsslots",
        color=discord.Color.blue()
    )
    for s in slots:
        bookings_count = len(s['bookings'])
        status = f"📅 {s['datetime']}\n📝 {s['description']}\n👥 Buchungen: {bookings_count}/{s['capacity']}"
        embed.add_field(name=f"Slot #{s['id']}", value=status, inline=False)

    await ctx.respond(embed=embed)

# Nutzer-Befehle
@bot.slash_command(description="Verfügbare Buchungsslots anzeigen")
async def view_slots(ctx):
    slots = await manager.get_available_slots()
    if not slots:
        await ctx.respond("Aktuell sind leider keine freien Buchungsslots verfügbar.", ephemeral=True)
        return

    embed = discord.Embed(
        title="📅 Verfügbare Buchungsslots",
        description="Nutze `/book <ID>`, um einen Termin zu reservieren.",
        color=discord.Color.gold()
    )
    for s in slots:
        free_space = s['capacity'] - len(s['bookings'])
        info = f"🕒 {s['datetime']}\n📝 {s['description']}\n🔓 Frei: {free_space}/{s['capacity']}"
        embed.add_field(name=f"Slot #{s['id']}", value=info, inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen freien Slot buchen")
@option("slot_id", description="Die ID des Slots, den du buchen möchtest")
async def book(ctx, slot_id: int):
    success, message = await manager.book_slot(slot_id, ctx.author.id)
    if success:
        embed = discord.Embed(
            title="✅ Buchung erfolgreich",
            description=message,
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Buchung fehlgeschlagen",
            description=message,
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(description="Deine eigenen Buchungen anzeigen")
async def my_bookings(ctx):
    slots = await manager.get_user_bookings(ctx.author.id)
    if not slots:
        await ctx.respond("Du hast aktuell keine aktiven Buchungen.", ephemeral=True)
        return

    embed = discord.Embed(
        title="👤 Deine Buchungen",
        color=discord.Color.purple()
    )
    for s in slots:
        info = f"📅 {s['datetime']}\n📝 {s['description']}"
        embed.add_field(name=f"Slot #{s['id']}", value=info, inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Hilfe-Menü anzeigen")
async def help(ctx):
    embed = discord.Embed(
        title="📖 Hilfe & Befehle",
        description="Hier findest du eine Übersicht aller verfügbaren Befehle des Buchungssystems.",
        color=discord.Color.light_grey()
    )

    user_cmds = (
        "`/view_slots` - Zeigt alle verfügbaren Termine an.\n"
        "`/book <id>` - Reserviert einen freien Slot.\n"
        "`/my_bookings` - Listet deine reservierten Termine auf.\n"
        "`/cancel <id>` - Storniert eine deiner Buchungen.\n"
        "`/help` - Zeigt dieses Menü."
    )
    embed.add_field(name="Für Nutzer", value=user_cmds, inline=False)

    admin_cmds = (
        "`/add_slot` - Erstellt einen neuen Buchungsslot.\n"
        "`/delete_slot <id>` - Entfernt einen Termin.\n"
        "`/list_all_slots` - Übersicht aller Slots inkl. Status.\n"
        "`/show_bookings <id>` - Zeigt an, wer einen Slot gebucht hat."
    )
    embed.add_field(name="Für Administratoren", value=admin_cmds, inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Eine deiner Buchungen stornieren")
@option("slot_id", description="Die ID des Slots, den du stornieren möchtest")
async def cancel(ctx, slot_id: int):
    success, message = await manager.cancel_booking(slot_id, ctx.author.id)
    if success:
        embed = discord.Embed(
            title="✅ Stornierung erfolgreich",
            description=message,
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Stornierung fehlgeschlagen",
            description=message,
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: DISCORD_TOKEN nicht in der .env Datei gefunden.")
        print("Bitte erstelle eine .env Datei mit DISCORD_TOKEN=dein_token_hier")
