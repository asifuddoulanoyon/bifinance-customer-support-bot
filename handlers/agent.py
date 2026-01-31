from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler
from database import get_case, assign_agent, add_message, close_case, cursor

async def agent_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👨‍💼 Agent Commands:\n"
        "/mycases - View your open cases\n"
        "/takecase <CASE_ID> - Take ownership\n"
        "/closecase <CASE_ID> - Close case\n"
        "/transfer <CASE_ID> - Transfer to another agent\n"
        "/search <CASE_ID> - Search case\n"
    )
    await update.message.reply_text(msg)

async def my_cases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agent_id = update.effective_user.id
    cursor.execute("SELECT * FROM cases WHERE assigned_agent=? AND status IN ('OPEN','IN_PROGRESS')", (agent_id,))
    cases = cursor.fetchall()
    if not cases:
        await update.message.reply_text("You have no open cases.")
        return
    buttons = [[InlineKeyboardButton(f"{c[0]}", callback_data=f"view_{c[0]}")] for c in cases]
    await update.message.reply_text("Your open cases:", reply_markup=InlineKeyboardMarkup(buttons))
