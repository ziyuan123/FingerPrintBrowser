import asyncio
import pproxy
from loguru import logger as log


def start_socks5_proxy(listen_port: int, socks5_info: str):
    server = pproxy.Server(f'socks5://127.0.0.1:{listen_port}')
    remote = pproxy.Connection(f'socks5://{socks5_info}')
    args = dict( rserver = [remote],
                 verbose = log.debug )

    loop = asyncio.get_event_loop()
    handler = loop.run_until_complete(server.start_server(args))
    try:
        log.info(f"socks5 proxy started, listen: {f'socks5://127.0.0.1:{listen_port}'}")
        loop.run_forever()
    except KeyboardInterrupt:
        print('exit!')

    handler.close()
    loop.run_until_complete(handler.wait_closed())
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


if __name__ == "__main__":
    start_socks5_proxy(8080, '103.76.117.74:6339#sklvzzfn:07iqkr6resbs')