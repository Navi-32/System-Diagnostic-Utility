
# System Diagnostic Utility

A comprehensive Python-based system diagnostic tool that checks various aspects of your system health, including disk space, memory usage, CPU performance, network connectivity, and more.

## Features

- **System Information**: OS version, architecture, processor details
- **Disk Health**: Disk space monitoring, partition analysis, low space warnings
- **Memory Health**: RAM usage, swap memory, memory leak detection
- **CPU Health**: CPU usage, per-core statistics, temperature monitoring (if available)
- **Network Health**: Network interface statistics, connectivity tests
- **Process Analysis**: Top CPU and memory consuming processes
- **Disk Error Detection**: Basic disk error checking and recommendations
- **Automated Recommendations**: Actionable suggestions based on diagnostic results
- **Report Generation**: Save detailed diagnostic reports to JSON files

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the diagnostic utility:
```bash
python system_diagnostic.py
```

The tool will:
1. Collect system information
2. Check disk health and space
3. Monitor memory usage
4. Analyze CPU performance
5. Test network connectivity
6. Analyze running processes
7. Check for disk errors
8. Generate recommendations

### Programmatic Usage

You can also use the diagnostic utility in your own Python scripts:

```python
from system_diagnostic import SystemDiagnostic

# Create diagnostic instance
diagnostic = SystemDiagnostic()

# Run all diagnostics
results = diagnostic.run_all_diagnostics()

# Print summary
diagnostic.print_summary()

# Save report to file
diagnostic.save_report("my_report.json")

# Access specific results
print(f"CPU Usage: {results['cpu_health']['usage_percent']}%")
print(f"Memory Usage: {results['memory_health']['percent_used']}%")
```

### Running Individual Checks

You can also run individual diagnostic checks:

```python
from system_diagnostic import SystemDiagnostic

diagnostic = SystemDiagnostic()

# Run specific checks
diagnostic.check_disk_health()
diagnostic.check_memory_health()
diagnostic.check_cpu_health()

# Access results
print(diagnostic.results)
```

## Output Format

The diagnostic utility provides:
- **Console Output**: Real-time diagnostic information printed to the console
- **JSON Reports**: Detailed reports saved as JSON files with all diagnostic data
- **Issue Detection**: Automatic detection and reporting of system issues
- **Recommendations**: Actionable recommendations based on detected issues

## Report Structure

The generated JSON report includes:
- `timestamp`: When the diagnostic was run
- `system_info`: Operating system and hardware information
- `disk_health`: Disk space and partition information
- `memory_health`: RAM and swap memory statistics
- `cpu_health`: CPU usage and performance metrics
- `network_health`: Network interface and connectivity data
- `process_health`: Top processes by CPU and memory usage
- `issues`: List of detected problems
- `recommendations`: Suggested actions to resolve issues

## Requirements

- Python 3.6 or higher
- psutil library (installed via requirements.txt)

## Platform Support

- **Windows**: Full support including disk checks, process monitoring
- **Linux**: Full support including temperature monitoring (if available)
- **macOS**: Full support with platform-specific optimizations

## Examples

### Check Disk Space Only
```python
from system_diagnostic import SystemDiagnostic

diagnostic = SystemDiagnostic()
diagnostic.check_disk_health()
diagnostic.print_summary()
```

### Monitor System Continuously
```python
import time
from system_diagnostic import SystemDiagnostic

diagnostic = SystemDiagnostic()

while True:
    diagnostic.check_cpu_health()
    diagnostic.check_memory_health()
    print("\n" + "="*60)
    time.sleep(5)  # Check every 5 seconds
```

## Troubleshooting

### Permission Errors
Some checks may require administrator/root privileges:
- Disk error checking
- Accessing certain system files
- Monitoring all processes

### Missing Temperature Data
CPU temperature monitoring depends on:
- Hardware sensors being available
- Platform-specific drivers
- May not be available on all systems

## License

This project is open source and available for use and modification.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

