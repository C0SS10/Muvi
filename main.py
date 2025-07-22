import os
from colorama import init, Fore, Style
from app.config import create_app, BANNER


if __name__ == "__main__":
    application = create_app()
    host = os.getenv("HOST_IP", "127.0.0.1")
    port = int(os.getenv("HOST_PORT", 5000))

    init(autoreset=True)
    print(Fore.GREEN + Style.DIM + BANNER)
    print(Fore.YELLOW + Style.BRIGHT + f"Running on http://{host}:{port}")

    application.run(host=host, port=port, debug=True, use_reloader=False)