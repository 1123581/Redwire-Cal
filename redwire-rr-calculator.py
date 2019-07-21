import logging
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          InlineQueryHandler, MessageHandler, Updater)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


Calculator = range(1)
Compound = range(1)

def start(bot, update):
    update.message.reply_text("Welcome to RedWire's calculator. If you encounter any issues please contact"
                              " @CredoMeliora "
                              "click here--> /commands to begin.")

def cancel(bot, update):
    msg = """commands.  .  .
/calculator
/CompoundInterest"""
    bot.send_message(text=msg,
                     chat_id=update.message.chat_id,
                     message_id=update.message.message_id)
    return ConversationHandler.END


# list of commands----------------------
def commands(bot, update):
    msg = """commands.  .  .
/calculator
/CompoundInterest"""
    bot.send_message(text=msg,
                     chat_id=update.message.chat_id,
                     message_id=update.message.message_id)
    return ConversationHandler.END


def calculator(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Please input your entry price, stop price, and target price in the following format:\n'
                     '<entry>,<stop>,<target>\n\n'
                     'Example: 6000,5900,6200')
    return Calculator


def cal(bot, update):
    inputs = update.message.text
    if ',' not in inputs:
        bot.send_message(chat_id=update.message.chat_id,
                         text='The values you entered have an invalid format.\nPlease try again or press  /cancel to abort:')
        return Calculator  # return to loop to allow the user to reenter the orderID
    else:
        try:
            data = {}
            data['Entry'] = inputs.split(',')[0]
            data['Stop'] = inputs.split(',')[1]
            data['Target'] = inputs.split(',')[2]
            risk = int(data['Entry']) - int(data['Stop'])
            reward = int(data['Target']) - int(data['Entry'])
            rr = round(reward / risk, 2)
            profit = round(reward / int(data['Entry']), 2)
            loss = round(risk / int(data['Entry']), 2)
            ppercent = round(profit * 100, 2)
            lpercent = round(loss * 100, 2)
            poutput = str(ppercent)
            loutput = str(lpercent)
            rroutput = str(rr)
            print(rr)
            print(ppercent)
            print(lpercent)
            bot.send_message(chat_id=update.message.chat_id,
                             text='Entry: ' + data['Entry'] + '\n' + 'Stop: ' + data['Stop'] + '\n' + 'Target: ' + data['Target'])
            bot.send_message(chat_id=update.message.chat_id,
                             text='Risk/Reward: ' + rroutput + '\n' + 'Profit: ' + poutput + '%\n' + 'Loss: ' + loutput + '%')
            return ConversationHandler.END
        except:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Something went wrong. . .\ntry again or press /cancel to abort')
            print('')


#  Balance×(1+(Risk percentage÷100÷(1÷ Profit percentage)÷100))^ Time
def comcal(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Please input your initial capital, percent to risk, estimated profit percent, and time in days in the following format:\n'
                     '<initial investment>,<risk percent>,<reward percent>,<time>\n\n'
                     'Example: 100,2,4,367')
    return Compound


def com(bot, update):
    inputs = update.message.text
    if ',' not in inputs:
        bot.send_message(chat_id=update.message.chat_id,
                         text='The values you entered have an invalid format.\nPlease try again or press  /cancel to abort:')
        return Compound  # return to loop to allow the user to reenter the orderID
    else:
        try:
            data = {}
            data['initial'] = inputs.split(',')[0]
            initial = int(data['initial'])
            data['risk percent'] = inputs.split(',')[1]
            risk_percent = int(data['risk percent'])
            data['reward percent'] = inputs.split(',')[2]
            reward_percent = int(data['reward percent'])
            data['time'] = inputs.split(',')[3]
            time = int(data['time'])
            formula = round(initial*(1+(risk_percent / 100 / (1 / reward_percent) / 100)) ** time, 2)
            total = str(formula)
            profit = round(formula - initial, 2)
            preturn = round((profit / initial) * 100)
            output = str(profit)
            prof = str(preturn)
            print(formula)
            bot.send_message(chat_id=update.message.chat_id,
                             text='Initial Capital: ' + data['initial'] + '\n' + 'Risk Percent: ' + data['risk percent'] + '\n' + 'Reward Percent: ' + data['reward percent'] + '\n' + 'Time: ' + data['time'])
            bot.send_message(chat_id=update.message.chat_id,
                             text='Total: ' + total + '\n' + 'Return: ' + output + '\n' + 'Percent Profit: ' + prof + '%')
            return ConversationHandler.END
        except:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Something went wrong. . .\n Try again or press /cancel to abort')
            print('opps')

def main():
    # telegram token--------------------
    updater = Updater('944894024:AAEUEBhp0AY7tef2Sw-ZpZkcpfI36rzFzsg')
    calculator_conversationhandler = ConversationHandler(
        entry_points=[CommandHandler('CompoundInterest', comcal)],
        states={
            Compound: [MessageHandler(Filters.text, com)],
        },
        fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True)
    compound_conversationhandler = ConversationHandler(
        entry_points=[CommandHandler('calculator', calculator)],
        states={
            Calculator: [MessageHandler(Filters.text, cal)],
        },
        fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True)
    dp = updater.dispatcher
    dp.add_handler(calculator_conversationhandler)
    dp.add_handler(compound_conversationhandler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('commands', commands))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
