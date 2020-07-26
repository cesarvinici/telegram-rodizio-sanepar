from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from conf.settings import TELEGRAM_TOKEN
from model.DAO import busca_rodizio, get_cidades
from datetime import datetime
import logging
import math
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(CURRENT_DIR, "log")
MSG_LENGHT = 4095

today = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO,
                     filename=os.path.join(LOG_DIR,"rodizio.log" ))

def start(bot, update): 
    """ A mensagem que usuário irá receber quando acessar o chat pela primeira vez
        ou usar o comando /help
     """
    response_message = """
    Verifique a data e horario do rodizio de aguá na sua cidade e bairro.\n
    Utilize os comandos /rodizio cidade, ex /rodizio Curitiba para receber informação de dia e hora e bairros afetados.\n
    Você pode também utilizar /rodizio cidade-bairro, ex /rodizio Curitiba-centro para ter informação do rodizio no bairro informado.\n
   
    Para saber as cidades cadastradas envie /cidades

    Para ver esta mensagem novamente envie /help
    """

    bot.send_message(
        chat_id = update.message.chat_id,
        text = response_message,
        parse_mode = "HTML"
    )

def ver_rodizio(bot, update, args):
    """
        Retorna a informação do rodizio para o usuário
    """

    args = " ".join(args)

    logging.info(f"chat_id: {update.message.chat_id}, args: {args}")

    if args == '':
        return unknown(bot, update)

    if("-" in args):
        cidade = args.split("-")[0].strip()
        bairro = args.split("-")[1].strip()
        rodizio = busca_rodizio(cidade, bairro)
    else:
        rodizio = busca_rodizio(args)

    string_size = len(rodizio)
    qtd_messages = math.ceil(string_size / MSG_LENGHT)
    total_per_page = int(string_size / qtd_messages)
    for i in range(1, (qtd_messages+1)):
        if(i == 1):
            inicio = 0
            final = total_per_page * i
        else:
            inicio = total_per_page * (i-1)
            final = total_per_page * i

        bot.send_message(
            chat_id=update.message.chat_id,
            text=rodizio[inicio:final],
            parse_mode='Markdown'
        )

def ver_cidades(bot, update, args):
    logging.info(f"chat_id: {update.message.chat_id}, args: {args}")
    cidades = ["\n\t\t" + cidade for cidade in get_cidades()['cidade']]
    message = "Cidades:" + "".join(cidades).title()
    bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )





def unknown(bot, update):
    response_message = "Mensagem incorreta, envie /help para mais informações."
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )

def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler("start", start)
    )

    dispatcher.add_handler(
        CommandHandler("help", start)
    )

    dispatcher.add_handler(
        CommandHandler('rodizio', ver_rodizio, pass_args=True)
    )

    dispatcher.add_handler(
        CommandHandler('cidades', ver_cidades, pass_args=True)
    )

    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()