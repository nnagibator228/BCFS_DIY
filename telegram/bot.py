import os
import json
import xmlrpc.client
import telebot

host = str(os.environ.get("RPC_SERVER_HOST"))
bot_token = str(os.environ.get("BOT_TOKEN"))

bot = telebot.TeleBot(bot_token)
client = xmlrpc.client.ServerProxy(f"http://{host}:8000")

def parse_block(data):
    beautified_string = "🕋 *Block*: \n" \
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
    beautified_string = "🕋🕋 *Blocks:* \n \n"
    for block in data['blocks']:
        beautified_string += parse_block(block)

    return beautified_string


def parse_tx(data):
    beautified_string = " 💸 *Transaction* \n" \
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
        except Exception as e: print(e); bot.send_message(chat_id=user_id, text="Something went wrong. Recheck arguments provided. See more: /help"); return None
    else: bot.send_message(chat_id=user_id, text="Not all arguments fullfilled. See more: /help")


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    acc = client.add_acc(str(user_id))
    bot.send_message(chat_id=user_id, text=f"Hello, `{client.pretty_hash(acc['pub'])}`! Welcome to *Blockchain From Scratch* client bot! Your wallet hash is `{str(acc['pub'])}`", parse_mode="Markdown")


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


print("Starting bot... ")
bot.polling()
