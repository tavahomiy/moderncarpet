import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# تعریف متغییرها و پیام های مورد نیاز
TOKEN = '6172879447:AAFLvRCm3Q0Ly3kPjKrBhPHtzDFTIxEOxYc'
admin_id = '1143940708'
welcome_message = 'به ربات ثبت نام دوره طراحی فرش خوش آمدید!'
register_message = 'لطفا نام و نام خانوادگی خود را وارد کنید:'
discount_code_message = 'لطفا کد تخفیف خود را وارد کنید:'
thank_you_message = 'ممنون از ثبت نام شما. لطفا منتظر تایید مدیریت باشید.'
admin_keyboard = [[InlineKeyboardButton('لیست کاربران ثبت نام شده', callback_data='user_list')],
                  [InlineKeyboardButton('ارسال کد تخفیف', callback_data='send_discount')]]
admin_menu = InlineKeyboardMarkup(admin_keyboard)

# تابع برای ارسال پیام های خوش آمدگویی به کاربر
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=register_message)

# تابع برای ثبت نام کابر و ارسال پیام واکنش به آن
def register_user(update, context):
    name = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=discount_code_message)
    context.user_data['name'] = name

# تابع برای ثبت کد تخفیف وارد شده توسط کاربر و ارسال پیام واکنش به آن
def register_discount_code(update, context):
    code = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=thank_you_message)
    context.user_data['discount_code'] = code

# تابع برای نمایش دکمه های مدیریت به ادمین
def admin_menu_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='لطفا یکی از گزینه های زیر را انتخاب کنید:', reply_markup=admin_menu)

# تابع برای نمایش لیست کاربران ثبت نام شده به ادمین
def user_list_handler(update, context):
    user_list = []
    for user in context.user_data:
        if 'name' in context.user_data[user]:
            user_list.append(context.user_data[user]['name'])
    user_list_text = '\n'.join(user_list)
    context.bot.send_message(chat_id=admin_id, text=user_list_text)

# تابع برای ارسال کد تخفیف به کاربران به ادمین
def send_discount_handler(update, context):
    for user in context.user_data:
        if 'discount_code' in context.user_data[user]:
            discount_code = context.user_data[user]['discount_code']
            user_id = user
            try:
                context.bot.send_message(chat_id=user_id, text='کد تخفیف شما:\n{}'.format(discount_code))
                context.bot.send_message(chat_id=admin_id, text='کد تخفیف با موفقیت به کاربر ارسال شد.')
            except:
                context.bot.send_message(chat_id=admin_id, text='مشکلی در ارسال کد تخفیف به کاربر رخ داد.')

# تابع اصلی برای ران کردن ربات
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # ثبت دستورات
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('register', register_user))
    dispatcher.add_handler(CommandHandler('discount', register_discount_code))
    dispatcher.add_handler(CallbackQueryHandler(admin_menu_handler, pattern='^(user_list)$'))
    dispatcher.add_handler(CallbackQueryHandler(send_discount_handler, pattern='^(send_discount)$'))

    updater.start_polling()
    updater.idle()