# 🧃 PteroBackupuccino

**PteroBackupuccino** is a Python tool for managing [Pterodactyl](https://pterodactyl.io) client backups. It periodically checks your servers, and if a server exceeds a configurable backup limit, it automatically deletes the oldest backups (optionally including locked ones). It also supports Discord webhook notifications.

## 🚀 Features

- ✅ Periodic backup cleanup (default every 6 hours)
- ✅ Auto-delete oldest backups if exceeding limit
- ✅ Optional handling of locked backups
- ✅ Safe HTTP retries with timeout handling
- ✅ Discord notifications for deleted backups
- ✅ Fully async using `aiohttp`

## ⚙️ Configuration

You can configure **PteroBackupuccino** via CLI arguments or a `.env` file.

### CLI Example

```bash
python app.py \
  --PTERODACTYL_API_URL https://panel.example.com/api/client \
  --PTERODACTYL_API_KEY your_client_api_key \
  --DISCORD_WEBHOOK_URL https://discord.com/api/webhooks/... \
  --MAX_BACKUP_LIMIT 3 \
  --DELETE_LOCKED false \
  --APP_CHECK_INTERVAL 21600
```

## 📝 How It Works

- Runs an asynchronous loop every `APP_CHECK_INTERVAL` seconds (default: 21600 seconds = 6 hours)

- Fetches all servers from the Pterodactyl client API

- For each server that is **not suspended or installing**:

  - Fetches all backups

  - Filters backups based on the locked status and your settings:
  
    - If `DELETE_LOCKED` is false, locked backups are excluded from deletion.

  - Keeps the newest `MAX_BACKUP_LIMIT` backups

  - Deletes any older backups exceeding the limit

- Sends a Discord notification whenever backups are deleted

- Logs all operations both to console and to a log file

## 📄 License

MIT © Martin Coplák

## 🔗 Links

- [Pterodactyl Panel](https://pterodactyl.io)
- [aiohttp Documentation](https://docs.aiohttp.org/)