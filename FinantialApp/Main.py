from ThirdParties.TelegramLauncher import Telegram

import os
from dotenv import load_dotenv

  

if __name__ == '__main__':
    load_dotenv()

    telegram_application= Telegram(os.getenv('TOKEN'))

    telegram_application.run_application()
    
