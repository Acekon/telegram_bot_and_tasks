# Messgage bot 0.3.0

```text
First start
```
Create table
```bash
CREATE TABLE "messages" (
	"ids"	INTEGER NOT NULL UNIQUE,
	"text_message"	TEXT,
	"last_send"	TEXT,
	PRIMARY KEY("ids" AUTOINCREMENT)
);
```
Create folder for image
```bash
mkdir img/
```

```text
[Unit]
Description=Message Bot v0.3
After=network.target

[Service]
EnvironmentFile=/etc/environment
ExecStart=python3 joke_bot.py
ExecReload=python3 joke_bot.py
WorkingDirectory=/opt/bot/0.3/
KillMode=process
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```text
About:
Description — описание службы.
EnvironmentFile — путь к файлу с переменными.
ExecStart и ExecReload — это команды для запуска и перезапуска бота.
WorkingDirectory — путь к папке в которой файл запуска main.py.
```
## Add service
```bash
systemctl enable joke_bot_0.3
systemctl start joke_bot_0.3
systemctl status joke_bot_0.3

systemctl enable bot_task_0.3
systemctl start bot_task_0.3
systemctl status bot_task_0.3
```
## Disable & remove service
```bash
systemctl stop joke_bot_0.3
systemctl disable joke_bot_0.3
rm /etc/systemd/system/joke_bot_0.3.service
rm /usr/lib/systemd/system/joke_bot_0.3.service
systemctl daemon-reload
systemctl reset-failed
```

## Update
```bash
systemctl enable joke_bot_0.3
systemctl restart joke_bot_0.3
systemctl enable bot_task_0.3
systemctl restart bot_task_0.3
```
## Change log
``` 

Joke bot 0.3 start 29.06.2023
Refactor codes start 29.06.2023
