from environs import Env
env = Env()
env.read_env()

from API import app, configs


def main():
    import uvicorn
    host = "0.0.0.0" # 默认监听所有地址
    port = 8000 # 默认监听8000端口

    host = env.str("HOST", host)
    port = env.int("PORT", port)

    host = configs.get_config("server.host", host).get_value(str)
    port = configs.get_config("server.port", port).get_value(int)

    uvicorn.run(
        app = app,
        host = host,
        port = port
    )

if __name__ == "__main__":
    main()