module.exports = {
  apps: [
    {
      name: "djanggo-skeleton",
      script: "venv/bin/gunicorn",
      args: "config.wsgi:application -c gunicorn.conf.py",
      interpreter: "none",
      watch: false,
      autorestart: true,
      max_memory_restart: "500M"
    }
  ]
}
