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


```bash
nano /lib/systemd/system/bot_task_0.3.service
```
```text
[Unit]
Description=Message Bot v0.3
After=network.target

[Service]
EnvironmentFile=/etc/environment
ExecStart=python3 mess_bot.py
ExecReload=python3 mess_bot.py
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
systemctl enable mess_bot_0.3
systemctl start mess_bot_0.3
systemctl status mess_bot_0.3

systemctl enable mess_task_0.3
systemctl start mess_task_0.3
systemctl status mess_task_0.3
```
## Disable & remove service
```bash
systemctl stop mess_bot_0.3
systemctl disable mess_bot_0.3
rm /etc/systemd/system/mess_bot_0.3.service
rm /usr/lib/systemd/system/mess_bot_0.3.service
systemctl daemon-reload
systemctl reset-failed
```

## Update
```bash
systemctl enable mess_bot_0.3
systemctl restart mess_bot_0.3
systemctl enable mess_task_0.3
systemctl restart mess_task_0.3
```
