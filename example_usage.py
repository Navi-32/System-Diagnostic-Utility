"""
Example usage of the System Diagnostic Utility
Demonstrates various ways to use the diagnostic tool
"""

from system_diagnostic import SystemDiagnostic


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    diagnostic = SystemDiagnostic()
    results = diagnostic.run_all_diagnostics()
    diagnostic.print_summary()


def example_specific_checks():
    """Example of running specific checks"""
    print("\n" + "=" * 60)
    print("Example 2: Specific Checks")
    print("=" * 60)
    
    diagnostic = SystemDiagnostic()
    
    # Check only disk health
    print("\nChecking disk health...")
    diagnostic.check_disk_health()
    
    # Check only memory
    print("\nChecking memory...")
    diagnostic.check_memory_health()
    
    # Access results
    print(f"\nDisk Usage Summary:")
    for device, info in diagnostic.results['disk_health'].items():
        if isinstance(info, dict):
            print(f"  {device}: {info.get('percent_used', 0):.1f}% used")


def example_custom_report():
    """Example of generating custom reports"""
    print("\n" + "=" * 60)
    print("Example 3: Custom Report")
    print("=" * 60)
    
    diagnostic = SystemDiagnostic()
    diagnostic.check_disk_health()
    diagnostic.check_memory_health()
    diagnostic.check_cpu_health()
    
    # Save custom report
    filename = diagnostic.save_report("custom_report.json")
    print(f"\nCustom report saved to: {filename}")


def example_monitoring():
    """Example of continuous monitoring"""
    print("\n" + "=" * 60)
    print("Example 4: Continuous Monitoring")
    print("=" * 60)
    
    import time
    
    diagnostic = SystemDiagnostic()
    
    print("Monitoring system for 3 iterations (5 seconds apart)...")
    for i in range(3):
        print(f"\n--- Iteration {i+1} ---")
        diagnostic.check_cpu_health()
        diagnostic.check_memory_health()
        
        cpu_usage = diagnostic.results['cpu_health'].get('usage_percent', 0)
        mem_usage = diagnostic.results['memory_health'].get('percent_used', 0)
        
        print(f"CPU: {cpu_usage:.1f}% | Memory: {mem_usage:.1f}%")
        
        if i < 2:  # Don't sleep after last iteration
            time.sleep(5)


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_specific_checks()
    example_custom_report()
    example_monitoring()

