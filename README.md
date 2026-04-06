# MikroTik Monitoring

Monitoring solution for MikroTik routers using mktxp, Prometheus, Grafana, and Alertmanager with Telegram notifications.

## Stack

| Service | Port | Purpose |
|---------|------|---------|
| **Prometheus** | 9090 | Metrics storage & alert evaluation |
| **Grafana** | 3000 | Dashboard visualization |
| **mktxp** | 49090 | MikroTik RouterOS API exporter |
| **Alertmanager** | 9093 | Alert routing & Telegram notifications |

## Metrics Collected

- **System**: CPU load, memory, uptime, temperature, fan speeds, HDD space, power consumption
- **Interfaces**: traffic (rx/tx bytes, packets), errors, drops, link status, SFP info
- **DHCP**: leases, active count per server
- **IP Pools**: address usage per pool
- **Queues**: simple queue rates, bytes, dropped, queued
- **Public IP**: cloud address lookup
- **Voltage/Power**: PSU voltage (CCR1072 only)

## Alerts

| Alert | Condition | Duration |
|-------|-----------|----------|
| MikroTikDeviceDown | Exporter unreachable | 2 min |
| MikroTikRouterUnreachable | Router stops reporting | 3 min |
| InterfaceDown | Active interface goes down | 1 min |
| InterfaceHighErrorRate | > 10 errors/sec | 5 min |
| NoTrafficOnInterface | WAN interface zero traffic | 5 min |
| HighCPULoad | CPU > 90% | 5 min |
| HighMemoryUsage | Memory > 90% | 5 min |
| HighTemperature | CPU temp > 85°C | 2 min |
| IPPoolAlmostFull | Pool > 240/254 used | 5 min |

Alert thresholds can be adjusted in `prometheus/rules/mikrotik_alerts.yml`.

## Prerequisites

- Docker and Docker Compose
- MikroTik routers with RouterOS API enabled (port 8728)
- API user with read-only access on each router
- Telegram bot token and chat ID (for alerts)

## MikroTik Router Setup

On each MikroTik, create a monitoring user:

```
/user group add name=monitoring policy=api,read,winbox
/user add name=prometheus password=YOUR_PASSWORD group=monitoring
```

Enable the API service:

```
/ip service enable api
```

## Quick Start

1. **Clone and configure mktxp**:

   Edit `mktxp/mktxp.conf` — set hostnames, usernames, and passwords for each router.

2. **Set up Telegram bot token**:

   ```bash
   echo "YOUR_BOT_TOKEN_HERE" > alertmanager/telegram_bot_token
   ```

   Edit `alertmanager/alertmanager.yml` and set your `chat_id`.

   > **The token file is gitignored and must be created manually on each deployment.**

3. **Start the stack**:

   ```bash
   docker compose up -d
   ```

4. **Access services**:

   - **Grafana**: http://YOUR_SERVER_IP:3000 (admin/admin)
   - **Prometheus**: http://YOUR_SERVER_IP:9090
   - **Alertmanager**: http://YOUR_SERVER_IP:9093

## Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.yaml` | Service orchestration |
| `prometheus/prometheus.yml` | Scrape targets & alerting config |
| `prometheus/rules/mikrotik_alerts.yml` | Alert rules & thresholds |
| `alertmanager/alertmanager.yml` | Alert routing & Telegram config |
| `alertmanager/telegram_bot_token` | Telegram bot token (**gitignored**) |
| `mktxp/mktxp.conf` | Router connections & metric collection settings |
| `grafana/datasources/datasource.yml` | Prometheus datasource config |
| `grafana/dashboards/dashboard.yml` | Dashboard provisioning config |
| `grafana/dashboards/mikrotik-mktxp.json` | Grafana dashboard definition |

## Security

### Secrets Management

The Telegram bot token is stored in a separate file `alertmanager/telegram_bot_token` which is **excluded from git** via `.gitignore`. The `alertmanager.yml` config references this file via `bot_token_file` so the token never appears in committed code.

To set up on a new server:

```bash
echo "YOUR_BOT_TOKEN" > alertmanager/telegram_bot_token
```

### Other Recommendations

- Change the default Grafana password (`GF_SECURITY_ADMIN_PASSWORD` in `docker-compose.yaml`)
- Restrict network access to monitoring ports (9090, 3000, 9093) via firewall
- Use strong passwords for the MikroTik API user
- Consider placing Grafana behind a reverse proxy with HTTPS

## Useful Commands

```bash
# Start all services
docker compose up -d

# Restart a single service
docker compose restart prometheus

# View logs
docker compose logs -f alertmanager

# Check Prometheus alert rules
# Visit http://YOUR_SERVER_IP:9090/alerts

# Send a test alert to Telegram
curl -XPOST http://localhost:9093/api/v2/alerts \
  -H "Content-Type: application/json" \
  -d '[{"labels":{"alertname":"TestAlert","severity":"warning","routerboard_name":"Test"},"annotations":{"description":"Test alert from InterMax Monitoring."}}]'

# Stop all services
docker compose down

# Stop and remove all data
docker compose down -v
```
