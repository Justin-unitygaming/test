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
        title="✅ Slot Erstellt",
        description=f"Ein neuer Buchungsslot wurde erfolgreich angelegt.",
        color=discord.Color.green()
    )
    embed.add_field(name="ID", value=f"#{slot_id}", inline=True)
    embed.add_field(name="Datum", value=datum, inline=True)
    embed.add_field(name="Kapazität", value=str(kapazität), inline=True)
    embed.add_field(name="Beschreibung", value=beschreibung, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(description="Einen Buchungsslot löschen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("slot_id", description="Die ID des zu löschenden Slots")
async def delete_slot(ctx, slot_id: int):
    success = await manager.delete_slot(slot_id)
    if success:
        embed = discord.Embed(
            title="🗑️ Slot Gelöscht",
            description=f"Der Slot **#{slot_id}** wurde erfolgreich entfernt.",
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
        field_value = f"Datum: {s['datetime']}\nBeschreibung: {s['description']}\nBuchungen: {bookings_count}/{s['capacity']}"
        embed.add_field(name=f"Slot #{s['id']}", value=field_value, inline=False)

    await ctx.respond(embed=embed)

# Nutzer-Befehle
@bot.slash_command(description="Verfügbare Buchungsslots anzeigen")
async def view_slots(ctx):
    slots = await manager.get_available_slots()
    if not slots:
        embed = discord.Embed(
            title="📅 Verfügbare Slots",
            description="Aktuell sind leider keine freien Buchungsslots verfügbar.",
            color=discord.Color.orange()
        )
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(
        title="📅 Verfügbare Buchungsslots",
        description="Hier sind die aktuell verfügbaren Termine:",
        color=discord.Color.gold()
    )
    for s in slots:
        free_space = s['capacity'] - len(s['bookings'])
        field_value = f"Datum: {s['datetime']}\nBeschreibung: {s['description']}\nFrei: {free_space}/{s['capacity']}"
        embed.add_field(name=f"Slot #{s['id']}", value=field_value, inline=False)

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
        embed = discord.Embed(
            title="👤 Meine Buchungen",
            description="Du hast aktuell keine aktiven Buchungen.",
            color=discord.Color.light_grey()
        )
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(
        title="👤 Deine Buchungen",
        color=discord.Color.purple()
    )
    for s in slots:
        field_value = f"Datum: {s['datetime']}\nBeschreibung: {s['description']}"
        embed.add_field(name=f"Slot #{s['id']}", value=field_value, inline=False)

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

@bot.slash_command(description="Buchungen eines spezifischen Slots anzeigen (Administrator erforderlich)")
@commands.has_permissions(administrator=True)
@option("slot_id", description="Die ID des Slots")
async def show_bookings(ctx, slot_id: int):
    slot = await manager.get_slot_by_id(slot_id)
    if not slot:
        embed = discord.Embed(
            title="❌ Fehler",
            description=f"Slot **#{slot_id}** konnte nicht gefunden werden.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
        return

    users_list = "\n".join([f"• <@{uid}> (`ID: {uid}`)" for uid in slot['bookings']])
    if not users_list:
        users_list = "Keine Buchungen vorhanden."

    embed = discord.Embed(
        title=f"👥 Buchungen für Slot #{slot_id}",
        description=f"**Datum:** {slot['datetime']}\n**Beschreibung:** {slot['description']}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Gebuchte Nutzer:", value=users_list, inline=False)
    embed.add_field(name="Auslastung:", value=f"{len(slot['bookings'])}/{slot['capacity']}", inline=True)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Hilfe zu allen Befehlen anzeigen")
async def help(ctx):
    embed = discord.Embed(
        title="🤖 Buchungssystem Hilfe",
        description="Hier ist eine Übersicht über alle verfügbaren Befehle:",
        color=discord.Color.blue()
    )

    embed.add_field(name="📅 Nutzer-Befehle", value=(
        "`/view_slots`: Zeigt alle verfügbaren Termine an.\n"
        "`/book`: Bucht einen freien Termin per ID.\n"
        "`/my_bookings`: Zeigt deine aktuellen Buchungen.\n"
        "`/cancel`: Storniert eine deiner Buchungen."
    ), inline=False)

    embed.add_field(name="🛠️ Admin-Befehle", value=(
        "`/add_slot`: Erstellt einen neuen Termin.\n"
        "`/delete_slot`: Löscht einen Termin.\n"
        "`/list_all_slots`: Zeigt alle Termine mit Buchungsstatus an.\n"
        "`/show_bookings`: Zeigt die Liste der Nutzer für einen Slot an."
    ), inline=False)

    await ctx.respond(embed=embed)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Fehler: DISCORD_TOKEN nicht in der .env Datei gefunden.")
        print("Bitte erstelle eine .env Datei mit DISCORD_TOKEN=dein_token_hier")
