import os
import logging
import xmlrpc.client
import telebot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
port = str(os.environ.get("RPC_SERVER_PORT"))
host = str(os.environ.get("RPC_SERVER_HOST"))
bot_token = str(os.environ.get("TELEGRAM_BOT_TOKEN"))

bot = telebot.TeleBot(bot_token)
client = xmlrpc.client.ServerProxy(f"http://{host}:{port}")

faq = "ℹ️ *FAQ*: \n" \
"  - Available commands: \n" \
"    `/help` - get bot's faq \n" \
"    `/start` - initialize ur wallet & assigns it to ur telegram id \n" \
"    __By default u get 100 of currency. Please, do not overcome limit. There's also fee payment, that would be taken from ur accoune (2 currency) __ \n" \
"    **Pattern `/view`:** \n" \
"    `/view blocks` - to view all current blocks in BC \n" \
"    `/view block <block number>` - to view specific block by its number \n" \
"    `/view txs` - to view all current txs in BC \n" \
"    `/view tx <block number> <tx hash>` - to view specific tx in block by its hash \n" \
"    `/view balance` - to view ur own balance \n" \
"    `/view balance <acc hash>` - to view ur own balance \n" \
"    __To view acc's balance u must first create a tx from/to it & then tx should be added to created block. This incovinience is folowed during blockchain arch limitation__ \n" \
"    __To view someone's else balance u must first get his acc hash, provided when calling /start Its also used for sending txs__ \n" \
"    **Pattern `/create`:** \n" \
"    `/create tx <reciever's hash> <amount>` - creates a transaction with given creds & adds it to buffer \n" \
"    __Note that tx should only point to another adress (do not try to send tx to urself!) to prevent bot crashes. This incovinience is folowed during blockchain arch limitation__ \n" \
"    `/create block` - creates block with txs from buffer"


def parse_block(data):
    beautified_string = "🕋 **Block**: \n" \
                        "Hash: `{}` \n" \
                        "Volume: `{}` \n" \
                        "Fees: `{}` \n" \
                        "Root: `{}` \n" \
                        "Previous Hash: `{}` \n" \
                        "Number: `{}` \n" \
                        "Transactions: \n".format(data['hash'],
                                                  data['volume'],  
                                                  data['fees'], 
                                                  client.pretty_hash(data['root']), 
                                                  client.pretty_hash(data['prev_hash']), 
                                                  data['number'])
    
    for tx in data['txs']:
        beautified_string += "   - From: `{}` \n" \
                             "     To: `{}` \n" \
                             "     Value: `{}` \n" \
                             "     Fee: `{}` \n" \
                             "     Nonce: `{}` \n".format(client.pretty_hash(tx['fr']), 
                                                      client.pretty_hash(tx['to']), 
                                                      tx['value'], 
                                                      tx['fee'], 
                                                      tx['nonce'])
    
    return beautified_string


def parse_blocks(data):
    beautified_string = "🕋🕋 **Blocks:** \n \n"
    for block in data['blocks']:
        beautified_string += parse_block(block)

    return beautified_string


def parse_tx(data):
    beautified_string = " 💸 **Transaction** \n" \
                             "   - Hash: `{}` \n" \
                             "     From: `{}` \n" \
                             "     To: `{}` \n" \
                             "     Value: `{}` \n" \
                             "     Fee: `{}` \n" \
                             "     Nonce: `{}` \n".format( data['hash'],
                                                      client.pretty_hash(data['fr']), 
                                                      client.pretty_hash((data['to'])), 
                                                      data['value'], 
                                                      data['fee'], 
                                                      data['nonce'])
    
    return beautified_string

def parse_txs(data):
    beautified_string = "💸💸 *Transactions:* \n \n"
    for tx in data['transactions']:
        beautified_string += parse_tx(tx)

    return beautified_string


def parse_balance(data):
    return f"Balance is: 💰`{data['balance']}`"


def parse_add_block(data):
    if data: return "✅ block added succesfuly!"
    else: return "😖 somthing went wrong during block adding... It might be no transactions to add. Refer /help"


def parse_add_tx(data):
    if data: return "✅ transaction succesfully added to staging! Create a block to commit it into blockchain"
    else: return "😖 somthing went wrong during transaction adding... It might be not enough balance for tx or fee. Refer /help"


def try_to_call(method, user_id, parse_method, *args):
    if all(arg is not None for arg in args):
        try: bot.send_message(chat_id=user_id, text=parse_method(getattr(client, method)(*args)), parse_mode="Markdown")
        except Exception as e: logger.warning(e); bot.send_message(chat_id=user_id, text="Something went wrong. Recheck arguments provided. See more: /help"); return None
    else: bot.send_message(chat_id=user_id, text="Not all arguments fullfilled. See more: /help")


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    acc = client.add_acc(str(user_id))
    bot.send_message(chat_id=user_id, text=f"Hello, `{client.pretty_hash(acc['pub'])}`! Welcome to *Blockchain From Scratch* client bot! Your wallet hash is `{str(acc['pub'])}`", parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def start(message):
    user_id = message.chat.id
    bot.send_message(chat_id=user_id, text=faq, parse_mode="Markdown")


@bot.message_handler(commands=['view'])
def view(message):
    user_id = message.chat.id
    command, *args = message.text.split()
    if len(args) == 0:
        bot.send_message(chat_id=user_id, text="Please provide the necessary arguments.")
        return
    args.extend([None] * (3 - len(args)))
    match args[0]:
        case "blocks":
            try_to_call("blocks", user_id, parse_blocks)
        case "block":
            try_to_call("block", user_id, parse_block, args[1])
        case "txs":
            try_to_call("txs", user_id, parse_txs)
        case "tx":
            try_to_call("tx", user_id, parse_tx, args[1], args[2])
        case "balance":
            if args[1]: try_to_call("acc", user_id, parse_balance, args[1])
            else: try_to_call("acc_by_id", user_id, parse_balance, str(user_id))
        case _:
            bot.send_message(chat_id=user_id, text="Invalid command. Please use '/view blocks \ txs \ balance'. See more: /help")


@bot.message_handler(commands=['create'])
def view(message):
    user_id = message.chat.id
    command, *args = message.text.split()
    if len(args) == 0:
        bot.send_message(chat_id=user_id, text="Please provide the necessary arguments.")
        return
    args.extend([None] * (3 - len(args)))
    match args[0]:
        case "block":
            try_to_call("add_block", user_id, parse_add_block)
        case "tx":
            try_to_call("add_tx", user_id, parse_add_tx, str(user_id), args[1], args[2])
        case _:
            bot.send_message(chat_id=user_id, text="Invalid command. Please use '/create block \ tx '. See more: /help")


logger.info("Starting bot... ")
bot.polling()
