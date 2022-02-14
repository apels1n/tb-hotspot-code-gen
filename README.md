# HotSpot Telegram bot control
## Used libs:
- [`RouterOS api`](https://github.com/socialwifi/RouterOS-api)

Перед запуском в дирректории нужно создать четыре файла:
- `auth.txt`
- `bot_token.txt`
- `schedule.csv` с заголовком ```create,remove```
- `users.csv` с заголовком ```id,first_name,last_name,tg_nickname,admin```

В файл `bot_token.txt` вставить токен от телеграм бота.<br>
В файле `auth.txt` написать данные для авторизации на роутерею
### `auth.txt` file mask:
```
login
password
ip(192.168.88.1)
port(8728)
```
### `users.csv` file mask:
```
id,first_name,last_name,tg_nickname,admin
000000000,First,User,@first_user,True
111111111,Second,User,@second_user,False
```
### `schedule.csv` file mask:
```
create,remove
08:00,08:40
08:45,09:25
09:40,10:20
10:25,11:05
11:20,12:00
12:05,12:45
12:55,13:35
13:40,14:20
```