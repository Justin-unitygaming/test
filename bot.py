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
        embed = discord.Embed(
            title="Fehler",
            description="Du hast nicht die erforderlichen Berechtigungen (Administrator), um diesen Befehl auszuführen.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        print(f"Ein Fehler ist aufgetreten: {error}")
        embed = discord.Embed(
            title="Fehler",
            description="Ein unerwarteter Fehler ist aufgetreten.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

# Admin-Befehle
@bot.slash_command(description="Einen neuen Buchungsslot hinzufügen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("datum", description="Datum und Uhrzeit des Slots (z.B. 2023-10-27 10:00)")
@option("beschreibung", description="Kurze Beschreibung des Termins")
@option("kapazitaet", description="Maximale Anzahl an möglichen Buchungen", default=1, min_value=1)
async def add_slot(ctx, datum: str, beschreibung: str, kapazitaet: int):
    slot_id, error = await manager.add_slot(datum, beschreibung, kapazitaet)
    if error:
        embed = discord.Embed(
            title="Fehler beim Erstellen des Slots",
            description=f"❌ {error}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(
        title="Slot erstellt",
        description=f"✅ Slot #{slot_id} wurde erfolgreich erstellt.",
        color=discord.Color.green()
    )
    embed.add_field(name="Datum", value=datum, inline=True)
    embed.add_field(name="Beschreibung", value=beschreibung, inline=True)
    embed.add_field(name="Kapazität", value=str(kapazitaet), inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen Buchungsslot löschen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("slot_id", description="Die ID des zu löschenden Slots")
async def delete_slot(ctx, slot_id: int):
    success = await manager.delete_slot(slot_id)
    if success:
        embed = discord.Embed(
            title="Slot gelöscht",
            description=f"✅ Slot #{slot_id} wurde erfolgreich gelöscht.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="Fehler",
            description=f"❌ Slot #{slot_id} konnte nicht gefunden werden.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(description="Alle Buchungsslots anzeigen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
async def list_all_slots(ctx):
    slots = await manager.get_all_slots()
    if not slots:
        embed = discord.Embed(
            title="Alle Slots",
            description="Es sind derzeit keine Buchungsslots vorhanden.",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(
        title="📋 Liste aller Buchungsslots",
        color=discord.Color.blue()
    )
    for s in slots:
        bookings_count = len(s['bookings'])
        embed.add_field(
            name=f"ID: {s['id']} | {s['datetime']}",
            value=f"**Beschreibung:** {s['description']}\n**Buchungen:** {bookings_count}/{s['capacity']}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Details einer Buchung anzeigen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("slot_id", description="Die ID des Slots")
async def show_bookings(ctx, slot_id: int):
    slot = await manager.get_slot_by_id(slot_id)
    if not slot:
        embed = discord.Embed(
            title="Fehler",
            description=f"❌ Slot #{slot_id} konnte nicht gefunden werden.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
        return

    bookings = slot.get("bookings", [])
    if not bookings:
        description = "Es liegen noch keine Buchungen für diesen Slot vor."
    else:
        description = "\n".join([f"• <@{user_id}> (ID: {user_id})" for user_id in bookings])

    embed = discord.Embed(
        title=f"Buchungen für Slot #{slot_id}",
        description=f"**Datum:** {slot['datetime']}\n**Beschreibung:** {slot['description']}\n\n**Gebucht von:**\n{description}",
        color=discord.Color.blue()
    )
    await ctx.respond(embed=embed)

# Nutzer-Befehle
@bot.slash_command(description="Hilfe zu den Befehlen anzeigen")
async def help(ctx):
    embed = discord.Embed(
        title="🤖 Hilfe zum Buchungssystem",
        description="Hier ist eine Übersicht aller verfügbaren Befehle:",
        color=discord.Color.gold()
    )

    admin_cmds = (
        "`/add_slot`: Neuen Termin erstellen\n"
        "`/delete_slot`: Termin löschen\n"
        "`/list_all_slots`: Alle Termine & Status anzeigen\n"
        "`/show_bookings`: Nutzerdetails eines Slots anzeigen"
    )

    user_cmds = (
        "`/view_slots`: Verfügbare Termine anzeigen\n"
        "`/book`: Einen Termin buchen\n"
        "`/my_bookings`: Eigene Buchungen anzeigen\n"
        "`/cancel`: Buchung stornieren\n"
        "`/help`: Diese Hilfe anzeigen"
    )

    embed.add_field(name="Für Nutzer", value=user_cmds, inline=False)
    embed.add_field(name="Für Administratoren", value=admin_cmds, inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Verfügbare Buchungsslots anzeigen")
async def view_slots(ctx):
    slots = await manager.get_available_slots()
    if not slots:
        embed = discord.Embed(
            title="Verfügbare Slots",
            description="Aktuell sind leider keine freien Buchungsslots verfügbar.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(
        title="📅 Verfügbare Buchungsslots",
        description="Nutze `/book <id>` um einen Termin zu buchen.",
        color=discord.Color.green()
    )
    for s in slots:
        free_space = s['capacity'] - len(s['bookings'])
        embed.add_field(
            name=f"ID: {s['id']} | {s['datetime']}",
            value=f"**Beschreibung:** {s['description']}\n**Frei:** {free_space}/{s['capacity']}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen freien Slot buchen")
@option("slot_id", description="Die ID des Slots, den du buchen möchtest")
async def book(ctx, slot_id: int):
    success, message = await manager.book_slot(slot_id, ctx.author.id)
    if success:
        embed = discord.Embed(
            title="Buchung erfolgreich",
            description=f"✅ {message}",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="Buchung fehlgeschlagen",
            description=f"❌ {message}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(description="Deine eigenen Buchungen anzeigen")
async def my_bookings(ctx):
    slots = await manager.get_user_bookings(ctx.author.id)
    if not slots:
        embed = discord.Embed(
            title="Deine Buchungen",
            description="Du hast aktuell keine aktiven Buchungen.",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(
        title="👤 Deine Buchungen",
        color=discord.Color.blue()
    )
    for s in slots:
        embed.add_field(
            name=f"ID: {s['id']} | {s['datetime']}",
            value=f"**Beschreibung:** {s['description']}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Eine deiner Buchungen stornieren")
@option("slot_id", description="Die ID des Slots, den du stornieren möchtest")
async def cancel(ctx, slot_id: int):
    success, message = await manager.cancel_booking(slot_id, ctx.author.id)
    if success:
        embed = discord.Embed(
            title="Stornierung erfolgreich",
            description=f"✅ {message}",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="Stornierung fehlgeschlagen",
            description=f"❌ {message}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: DISCORD_TOKEN nicht in der .env Datei gefunden.")
        print("Bitte erstelle eine .env Datei mit DISCORD_TOKEN=dein_token_hier")
