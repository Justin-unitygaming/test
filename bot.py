import discord
from discord import option
import os
from booking_manager import BookingManager

# Initialize the bot
bot = discord.Bot()
manager = BookingManager()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.slash_command(description="Add a booking slot (Admin only)")
@option("date_time", description="Date and time (e.g. 2023-12-01 14:00)")
@option("description", description="Description of the event")
async def add_slot(ctx, date_time: str, description: str):
    # Check for administrator permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Only administrators can add slots.", ephemeral=True)
        return
    slot_id = manager.add_slot(date_time, description)
    await ctx.respond(f"Slot added with ID: **{slot_id}** for **{date_time}**.")

@bot.slash_command(description="View available slots")
async def view_slots(ctx):
    slots = manager.get_available_slots()
    if not slots:
        await ctx.respond("No available slots.")
        return

    embed = discord.Embed(title="Available Booking Slots", color=discord.Color.blue())
    for slot in slots:
        embed.add_field(
            name=f"Slot ID: {slot['id']}",
            value=f"Time: {slot['datetime']}\nDescription: {slot['description']}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Book a slot")
@option("slot_id", description="The ID of the slot you want to book", type=int)
async def book(ctx, slot_id: int):
    success, message = manager.book_slot(slot_id, ctx.author.id, str(ctx.author))
    if success:
        await ctx.respond(f"Successfully booked slot **{slot_id}**!")
    else:
        await ctx.respond(f"Failed to book slot: {message}", ephemeral=True)

@bot.slash_command(description="View your bookings")
async def my_bookings(ctx):
    slots = manager.get_user_bookings(ctx.author.id)
    if not slots:
        await ctx.respond("You have no bookings.")
        return

    embed = discord.Embed(title="Your Bookings", color=discord.Color.green())
    for slot in slots:
        embed.add_field(
            name=f"Slot ID: {slot['id']}",
            value=f"Time: {slot['datetime']}\nDescription: {slot['description']}",
            inline=False
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Cancel a booking")
@option("slot_id", description="The ID of the slot to cancel", type=int)
async def cancel(ctx, slot_id: int):
    success, message = manager.cancel_booking(slot_id, ctx.author.id)
    if success:
        await ctx.respond(f"Successfully cancelled booking for slot **{slot_id}**.")
    else:
        await ctx.respond(f"Failed to cancel booking: {message}", ephemeral=True)

@bot.slash_command(description="Delete a booking slot (Admin only)")
@option("slot_id", description="The ID of the slot to delete", type=int)
async def delete_slot(ctx, slot_id: int):
    # Check for administrator permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Only administrators can delete slots.", ephemeral=True)
        return
    success, message = manager.delete_slot(slot_id)
    if success:
        await ctx.respond(f"Successfully deleted slot **{slot_id}**.")
    else:
        await ctx.respond(f"Failed to delete slot: {message}", ephemeral=True)

@bot.slash_command(description="List all slots (Admin only)")
async def list_all_slots(ctx):
    # Check for administrator permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Only administrators can view all slots.", ephemeral=True)
        return

    slots = manager.data["slots"]
    if not slots:
        await ctx.respond("No slots available.")
        return

    embed = discord.Embed(title="All Booking Slots", color=discord.Color.gold())
    for slot in slots:
        status = "Available" if slot["booked_by"] is None else f"Booked by {slot['booked_by_name']} ({slot['booked_by']})"
        embed.add_field(
            name=f"Slot ID: {slot['id']}",
            value=f"Time: {slot['datetime']}\nDescription: {slot['description']}\nStatus: {status}",
            inline=False
        )
    await ctx.respond(embed=embed)

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Error: DISCORD_TOKEN environment variable not set.")
