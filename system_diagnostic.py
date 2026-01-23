"""
System Diagnostic Utility
A simple tool to check your computer's health
"""

import platform
import subprocess
import psutil
import json
from datetime import datetime


class SystemDiagnostic:
    """Main class that checks your computer's health"""
    
    def __init__(self):
        # Create a dictionary to store all results
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {},
            'disk_health': {},
            'memory_health': {},
            'cpu_health': {},
            'network_health': {},
            'process_health': {},
            'issues': [],
            'recommendations': []
        }
    
    def run_all_diagnostics(self):
        """Run all health checks"""
        print("=" * 60)
        print("SYSTEM DIAGNOSTIC UTILITY")
        print("=" * 60)
        print()
        
        print("Collecting system information...")
        self.check_system_info()
        
        print("Checking disk health...")
        self.check_disk_health()
        
        print("Checking memory usage...")
        self.check_memory_health()
        
        print("Checking CPU usage...")
        self.check_cpu_health()
        
        print("Checking network connectivity...")
        self.check_network_health()
        
        print("Analyzing running processes...")
        self.check_process_health()
        
        print("Checking disk errors...")
        self.check_disk_errors()
        
        print("\nGenerating recommendations...")
        self.generate_recommendations()
        
        return self.results
    
    def check_system_info(self):
        """Get basic information about your computer"""
        try:
            # Get system information using the platform library
            system_info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'os_release': platform.release(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'python_version': platform.python_version()
            }
            
            # Save the information
            self.results['system_info'] = system_info
            
            # Print the information
            print(f"  OS: {system_info['os']} {system_info['os_release']}")
            print(f"  Architecture: {system_info['architecture']}")
            print(f"  Processor: {system_info['processor']}")
            
        except Exception as e:
            # If something goes wrong, add it to issues
            self.results['issues'].append(f"Error collecting system info: {str(e)}")
            print(f"  Error: {str(e)}")
    
    def check_disk_health(self):
        """Check how much space is left on your hard drives"""
        try:
            disk_info = {}
            
            # Get all disk drives (C:, D:, etc.)
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    # Get disk usage information
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Convert bytes to gigabytes (GB)
                    total_gb = partition_usage.total / (1024**3)
                    used_gb = partition_usage.used / (1024**3)
                    free_gb = partition_usage.free / (1024**3)
                    percent_used = (partition_usage.used / partition_usage.total) * 100
                    
                    # Store the information
                    disk_info[partition.device] = {
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_gb': round(total_gb, 2),
                        'used_gb': round(used_gb, 2),
                        'free_gb': round(free_gb, 2),
                        'percent_used': round(percent_used, 2),
                        'status': 'healthy'
                    }
                    
                    # Check if disk is getting full
                    if percent_used > 90:
                        disk_info[partition.device]['status'] = 'critical'
                        self.results['issues'].append(
                            f"CRITICAL: {partition.device} ({partition.mountpoint}) is {percent_used:.1f}% full!"
                        )
                    elif percent_used > 80:
                        disk_info[partition.device]['status'] = 'warning'
                        self.results['issues'].append(
                            f"WARNING: {partition.device} ({partition.mountpoint}) is {percent_used:.1f}% full"
                        )
                    
                    # Print the information
                    print(f"  {partition.device} ({partition.mountpoint}):")
                    print(f"    Total: {total_gb:.2f} GB | Used: {used_gb:.2f} GB | Free: {free_gb:.2f} GB")
                    print(f"    Usage: {percent_used:.1f}% - Status: {disk_info[partition.device]['status']}")
                    
                except PermissionError:
                    # Can't access this drive (permission denied)
                    disk_info[partition.device] = {
                        'mountpoint': partition.mountpoint,
                        'status': 'access_denied'
                    }
                    print(f"  {partition.device}: Access denied")
                except Exception as e:
                    # Something else went wrong
                    disk_info[partition.device] = {
                        'mountpoint': partition.mountpoint,
                        'status': f'error: {str(e)}'
                    }
                    print(f"  {partition.device}: Error - {str(e)}")
            
            # Save all disk information
            self.results['disk_health'] = disk_info
            
        except Exception as e:
            self.results['issues'].append(f"Error checking disk health: {str(e)}")
            print(f"  Error: {str(e)}")
    
    def check_memory_health(self):
        """Check how much RAM (memory) is being used"""
        try:
            # Get memory information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Convert bytes to gigabytes
            memory_total_gb = memory.total / (1024**3)
            memory_used_gb = memory.used / (1024**3)
            memory_available_gb = memory.available / (1024**3)
            memory_percent = memory.percent
            
            swap_total_gb = swap.total / (1024**3)
            swap_used_gb = swap.used / (1024**3)
            swap_percent = swap.percent if swap.total > 0 else 0
            
            # Store the information
            memory_info = {
                'total_gb': round(memory_total_gb, 2),
                'used_gb': round(memory_used_gb, 2),
                'available_gb': round(memory_available_gb, 2),
                'percent_used': round(memory_percent, 2),
                'swap_total_gb': round(swap_total_gb, 2),
                'swap_used_gb': round(swap_used_gb, 2),
                'swap_percent': round(swap_percent, 2),
                'status': 'healthy'
            }
            
            # Check if memory usage is too high
            if memory_percent > 90:
                memory_info['status'] = 'critical'
                self.results['issues'].append(
                    f"CRITICAL: Memory usage is {memory_percent:.1f}%!"
                )
            elif memory_percent > 80:
                memory_info['status'] = 'warning'
                self.results['issues'].append(
                    f"WARNING: Memory usage is {memory_percent:.1f}%"
                )
            
            # Check swap usage (extra memory on disk)
            if swap_percent > 80 and swap_total_gb > 0:
                self.results['issues'].append(
                    f"WARNING: High swap usage ({swap_percent:.1f}%) - system may be low on RAM"
                )
            
            # Save the information
            self.results['memory_health'] = memory_info
            
            # Print the information
            print(f"  RAM: {memory_used_gb:.2f} GB / {memory_total_gb:.2f} GB ({memory_percent:.1f}%)")
            print(f"  Available: {memory_available_gb:.2f} GB")
            print(f"  Swap: {swap_used_gb:.2f} GB / {swap_total_gb:.2f} GB ({swap_percent:.1f}%)")
            print(f"  Status: {memory_info['status']}")
            
        except Exception as e:
            self.results['issues'].append(f"Error checking memory: {str(e)}")
            print(f"  Error: {str(e)}")
    
    def check_cpu_health(self):
        """Check how hard your processor (CPU) is working"""
        try:
            # Get CPU usage percentage (wait 1 second to get accurate reading)
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            # Store basic CPU information
            cpu_info = {
                'usage_percent': round(cpu_percent, 2),
                'cores': cpu_count,
                'status': 'healthy'
            }
            
            # Add frequency information if available
            if cpu_freq:
                cpu_info['current_freq_mhz'] = round(cpu_freq.current, 2)
                cpu_info['min_freq_mhz'] = round(cpu_freq.min, 2)
                cpu_info['max_freq_mhz'] = round(cpu_freq.max, 2)
            
            # Get usage for each CPU core
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            cpu_info['per_core_percent'] = [round(x, 2) for x in cpu_per_core]
            
            # Check if CPU usage is too high
            if cpu_percent > 90:
                cpu_info['status'] = 'critical'
                self.results['issues'].append(
                    f"CRITICAL: CPU usage is {cpu_percent:.1f}%!"
                )
            elif cpu_percent > 80:
                cpu_info['status'] = 'warning'
                self.results['issues'].append(
                    f"WARNING: CPU usage is {cpu_percent:.1f}%"
                )
            
            # Try to get CPU temperature (not available on all systems)
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    if temps:
                        cpu_info['temperatures'] = {}
                        for name, entries in temps.items():
                            for entry in entries:
                                if 'cpu' in name.lower() or 'core' in name.lower():
                                    cpu_info['temperatures'][entry.label or name] = {
                                        'current': round(entry.current, 2),
                                        'high': round(entry.high, 2) if entry.high else None,
                                        'critical': round(entry.critical, 2) if entry.critical else None
                                    }
                                    if entry.critical and entry.current > entry.critical:
                                        self.results['issues'].append(
                                            f"CRITICAL: CPU temperature ({entry.current}°C) exceeds critical threshold!"
                                        )
            except:
                pass  # Temperature not available on all systems
            
            # Save the information
            self.results['cpu_health'] = cpu_info
            
            # Print the information
            print(f"  CPU Usage: {cpu_percent:.1f}%")
            print(f"  Cores: {cpu_count}")
            if cpu_freq:
                print(f"  Frequency: {cpu_freq.current:.2f} MHz")
            print(f"  Status: {cpu_info['status']}")
            
        except Exception as e:
            self.results['issues'].append(f"Error checking CPU: {str(e)}")
            print(f"  Error: {str(e)}")
    
    def check_network_health(self):
        """Check network connection and statistics"""
        try:
            network_info = {}
            
            # Get network statistics
            net_io = psutil.net_io_counters()
            net_interfaces = psutil.net_if_addrs()
            net_stats = psutil.net_if_stats()
            
            # Store overall network statistics
            network_info['total_bytes_sent'] = net_io.bytes_sent
            network_info['total_bytes_recv'] = net_io.bytes_recv
            network_info['total_packets_sent'] = net_io.packets_sent
            network_info['total_packets_recv'] = net_io.packets_recv
            network_info['interfaces'] = {}
            
            # Get information about each network interface
            for interface_name, addrs in net_interfaces.items():
                interface_info = {
                    'addresses': [],
                    'is_up': False,
                    'speed_mbps': 0
                }
                
                # Get addresses for this interface
                for addr in addrs:
                    interface_info['addresses'].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask if hasattr(addr, 'netmask') else None
                    })
                
                # Get status and speed
                if interface_name in net_stats:
                    stats = net_stats[interface_name]
                    interface_info['is_up'] = stats.isup
                    interface_info['speed_mbps'] = stats.speed
                
                network_info['interfaces'][interface_name] = interface_info
            
            # Test if we can connect to localhost (basic connectivity test)
            try:
                if platform.system() == 'Windows':
                    result = subprocess.run(['ping', '-n', '1', '127.0.0.1'], 
                                          capture_output=True, timeout=5)
                else:
                    result = subprocess.run(['ping', '-c', '1', '127.0.0.1'], 
                                          capture_output=True, timeout=5)
                network_info['localhost_connectivity'] = result.returncode == 0
            except:
                network_info['localhost_connectivity'] = False
            
            # Save the information
            self.results['network_health'] = network_info
            
            # Print the information
            print(f"  Bytes Sent: {net_io.bytes_sent / (1024**2):.2f} MB")
            print(f"  Bytes Received: {net_io.bytes_recv / (1024**2):.2f} MB")
            print(f"  Interfaces: {len(net_interfaces)}")
            print(f"  Localhost Connectivity: {'OK' if network_info['localhost_connectivity'] else 'FAILED'}")
            
        except Exception as e:
            self.results['issues'].append(f"Error checking network: {str(e)}")
            print(f"  Error: {str(e)}")
    
    def check_process_health(self):
        """Check which programs are using the most resources"""
        try:
            processes = []
            high_cpu_processes = []
            high_memory_processes = []
            
            # Go through all running processes
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    processes.append(pinfo)
                    
                    # Find processes using lots of CPU (>50%)
                    if pinfo['cpu_percent'] and pinfo['cpu_percent'] > 50:
                        high_cpu_processes.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'cpu_percent': round(pinfo['cpu_percent'], 2)
                        })
                    
                    # Find processes using lots of memory (>10%)
                    if pinfo['memory_percent'] and pinfo['memory_percent'] > 10:
                        high_memory_processes.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'memory_percent': round(pinfo['memory_percent'], 2)
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass  # Skip processes we can't access
            
            # Sort by usage (highest first)
            high_cpu_processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            high_memory_processes.sort(key=lambda x: x['memory_percent'], reverse=True)
            
            # Store the information
            process_info = {
                'total_processes': len(processes),
                'top_cpu_processes': high_cpu_processes[:5],
                'top_memory_processes': high_memory_processes[:5]
            }
            
            self.results['process_health'] = process_info
            
            # Print the information
            print(f"  Total Processes: {len(processes)}")
            print(f"  Top CPU Processes:")
            for proc in high_cpu_processes[:3]:
                print(f"    {proc['name']} (PID: {proc['pid']}): {proc['cpu_percent']:.1f}%")
            print(f"  Top Memory Processes:")
            for proc in high_memory_processes[:3]:
                print(f"    {proc['name']} (PID: {proc['pid']}): {proc['memory_percent']:.1f}%")
            
        except Exception as e:
            self.results['issues'].append(f"Error checking processes: {str(e)}")
            print(f"  Error: {str(e)}")
    
    def check_disk_errors(self):
        """Check for disk errors"""
        try:
            # Give instructions based on operating system
            if platform.system() == 'Windows':
                print("  Note: Run 'chkdsk C: /f' as administrator to check for disk errors")
                print("  Note: Check Event Viewer for disk-related errors")
            else:
                print("  Note: Run 'fsck' or check system logs for disk errors")
                print("  Note: Check /var/log/syslog or dmesg for disk errors")
            
            # Try to get disk I/O statistics
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    print(f"  Disk Read Count: {disk_io.read_count}")
                    print(f"  Disk Write Count: {disk_io.write_count}")
                    if hasattr(disk_io, 'read_errs'):
                        print(f"  Disk Read Errors: {disk_io.read_errs}")
                    if hasattr(disk_io, 'write_errs'):
                        print(f"  Disk Write Errors: {disk_io.write_errs}")
            except:
                pass
                
        except Exception as e:
            self.results['issues'].append(f"Error checking disk errors: {str(e)}")
            print(f"  Error: {str(e)}")
    
    def generate_recommendations(self):
        """Suggest what to do about any problems found"""
        recommendations = []
        
        # Check disk space
        for device, info in self.results['disk_health'].items():
            if isinstance(info, dict) and info.get('percent_used', 0) > 80:
                recommendations.append(
                    f"Free up space on {device} ({info.get('mountpoint', 'unknown')}). "
                    f"Currently {info.get('percent_used', 0):.1f}% full."
                )
        
        # Check memory
        if self.results['memory_health'].get('percent_used', 0) > 80:
            recommendations.append(
                "High memory usage detected. Consider closing unnecessary applications "
                "or adding more RAM."
            )
        
        # Check CPU
        if self.results['cpu_health'].get('usage_percent', 0) > 80:
            recommendations.append(
                "High CPU usage detected. Check for resource-intensive processes "
                "or consider upgrading hardware."
            )
        
        # Check processes
        top_cpu = self.results['process_health'].get('top_cpu_processes', [])
        if top_cpu and top_cpu[0].get('cpu_percent', 0) > 80:
            recommendations.append(
                f"Process '{top_cpu[0].get('name', 'unknown')}' is using high CPU. "
                "Consider investigating or restarting it."
            )
        
        # If no problems, say so
        if not recommendations:
            recommendations.append("System appears to be running normally. No immediate action required.")
        
        # Save recommendations
        self.results['recommendations'] = recommendations
        
        # Print recommendations
        print("\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    def save_report(self, filename=None):
        """Save all results to a JSON file"""
        if filename is None:
            # Create a filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"diagnostic_report_{timestamp}.json"
        
        try:
            # Write the results to a file
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\nReport saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return None
    
    def print_summary(self):
        """Print a summary of any problems found"""
        print("\n" + "=" * 60)
        print("DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        issues_count = len(self.results['issues'])
        if issues_count == 0:
            print("✓ No critical issues detected")
        else:
            print(f"⚠ {issues_count} issue(s) detected:")
            for issue in self.results['issues']:
                print(f"  - {issue}")
        
        print("\n" + "=" * 60)


def main():
    """Simple main function - just run all checks"""
    diagnostic = SystemDiagnostic()
    results = diagnostic.run_all_diagnostics()
    diagnostic.print_summary()
    
    # Ask user if they want to save the report
    try:
        save = input("\nSave diagnostic report to file? (y/n): ").strip().lower()
        if save == 'y':
            diagnostic.save_report()
    except:
        pass  # Non-interactive mode


if __name__ == "__main__":
    main()
