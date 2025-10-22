# MikroTik Monitoring with Prometheus, Grafana, and SNMP

This project provides a complete monitoring solution for MikroTik devices using Prometheus, Grafana, and SNMP exporter running in Docker containers.

## Prerequisites

- Docker and Docker Compose installed
- MikroTik device with SNMP enabled
- Network access to the MikroTik device (10.72.100.1)

## MikroTik SNMP Configuration

Before starting the monitoring stack, ensure SNMP is enabled on your MikroTik device:

1. Connect to your MikroTik device via WinBox or SSH
2. Go to **IP → SNMP**
3. Enable SNMP with the following settings:
   - **Enabled**: Yes
   - **Contact**: Your contact information
   - **Location**: Device location
   - **Community**: `public` (or change in snmp.yml)
   - **Version**: 2c

## Quick Start

1. **Configure your MikroTik IP address** (if different from 10.72.100.1):
   ```bash
   # Edit prometheus/prometheus.yml file
   # Change targets: ['10.72.100.1'] to your MikroTik IP
   ```

2. **Start the monitoring stack**:
   ```bash
   docker-compose up -d
   ```

3. **Access the services**:
   - **Grafana**: http://10.72.100.28:3000 (admin/admin)
   - **Prometheus**: http://10.72.100.28:9090
   - **SNMP Exporter**: http://10.72.100.28:9116

## Services Overview

### Prometheus
- **Port**: 9090
- **Purpose**: Metrics collection and storage
- **Configuration**: `prometheus/prometheus.yml`
- **Data retention**: 200 hours

### Grafana
- **Port**: 3000
- **Purpose**: Visualization and dashboards
- **Default credentials**: admin/admin
- **Note**: No pre-configured dashboards included

### SNMP Exporter
- **Port**: 9116
- **Purpose**: SNMP to Prometheus metrics conversion
- **Configuration**: `snmp-exporter/snmp.yml`

## Monitored Metrics

The setup monitors the following MikroTik metrics:

- **System Information**:
  - System uptime (`snmp_sysUpTime`)
  - System name (`snmp_sysName`)
  - System location (`snmp_sysLocation`)

- **CPU and Memory**:
  - CPU usage (`snmp_hrProcessorLoad`)
  - Memory usage (`snmp_hrStorageUsed`, `snmp_hrStorageSize`)

- **Network Interfaces**:
  - Interface descriptions (`snmp_ifDescr`)
  - Interface types (`snmp_ifType`)
  - Interface speeds (`snmp_ifSpeed`)
  - Interface operational status (`snmp_ifOperStatus`)
  - Incoming/outgoing traffic (`snmp_ifInOctets`, `snmp_ifOutOctets`)
  - Interface errors (`snmp_ifInErrors`, `snmp_ifOutErrors`)

- **MikroTik Specific**:
  - CPU load (`snmp_mikrotik_cpu_load`)
  - Memory usage (`snmp_mikrotik_memory_usage`)
  - Temperature (`snmp_mikrotik_temperature`)
  - Voltage (`snmp_mikrotik_voltage`)
  - Fan speed (`snmp_mikrotik_fan_speed`)

## Configuration Files

- `docker-compose.yaml`: Main Docker Compose configuration
- `prometheus/prometheus.yml`: Prometheus scrape configuration
- `snmp-exporter/snmp.yml`: SNMP OID mappings for MikroTik

## Testing SNMP Connectivity

1. **Test SNMP connectivity**:
   ```bash
   snmpwalk -v2c -c public 10.72.100.1 1.3.6.1.2.1.1.1.0
   ```

2. **Test SNMP exporter**:
   ```bash
   curl "http://10.72.100.28:9116/snmp?target=10.72.100.1&module=mikrotik&auth=public_v2"
   ```

3. **Check Prometheus targets**:
   - Visit http://10.72.100.28:9090/targets
   - Ensure MikroTik target is UP

## Troubleshooting

### SNMP Connection Issues

1. **Check SNMP is enabled** on MikroTik:
   ```
   /ip snmp print
   ```

2. **Test SNMP connectivity**:
   ```bash
   snmpwalk -v2c -c public 10.72.100.1 1.3.6.1.2.1.1.1.0
   ```

3. **Check firewall rules** on MikroTik:
   ```
   /ip firewall filter print
   ```

### Container Issues

1. **Check container logs**:
   ```bash
   docker-compose logs prometheus
   docker-compose logs grafana
   docker-compose logs snmp-exporter
   ```

2. **Restart services**:
   ```bash
   docker-compose restart
   ```

3. **Check Prometheus targets**:
   - Visit http://10.72.100.28:9090/targets
   - Ensure MikroTik target is UP

## Customization

### Adding More Metrics

To monitor additional MikroTik OIDs:

1. Edit `snmp-exporter/snmp.yml`
2. Add new OIDs to the `walk` section
3. Restart the SNMP exporter:
   ```bash
   docker-compose restart snmp-exporter
   ```

### Creating Dashboards

1. Access Grafana at http://10.72.100.28:3000
2. Create new dashboards
3. Use SNMP metrics in your queries:
   - `snmp_sysUpTime`
   - `snmp_hrProcessorLoad`
   - `snmp_ifInOctets`
   - `snmp_ifOutOctets`

## Security Considerations

- Change default Grafana password
- Use SNMP community strings other than 'public' in production
- Consider SNMPv3 for enhanced security
- Restrict network access to monitoring ports

## Stopping the Services

```bash
docker-compose down
```

To remove all data volumes:
```bash
docker-compose down -v
```

## Support

For issues related to:
- **MikroTik SNMP**: Check MikroTik documentation
- **Prometheus**: Visit [Prometheus documentation](https://prometheus.io/docs/)
- **Grafana**: Visit [Grafana documentation](https://grafana.com/docs/)
- **SNMP Exporter**: Visit [SNMP Exporter documentation](https://github.com/prometheus/snmp_exporter)