import sys
import argparse
from system_diagnostic import SystemDiagnostic


def main():
    """Main entry point with command-line argument support"""
    parser = argparse.ArgumentParser(
        description='System Diagnostic Utility - Check system health and diagnose problems',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run all diagnostics
  python main.py --disk             # Check disk health only
  python main.py --memory           # Check memory only
  python main.py --cpu              # Check CPU only
  python main.py --save report.json # Save report to specific file
  python main.py --quiet            # Minimal output
        """
    )
    
    parser.add_argument(
        '--disk',
        action='store_true',
        help='Check disk health only'
    )
    parser.add_argument(
        '--memory',
        action='store_true',
        help='Check memory health only'
    )
    parser.add_argument(
        '--cpu',
        action='store_true',
        help='Check CPU health only'
    )
    parser.add_argument(
        '--network',
        action='store_true',
        help='Check network health only'
    )
    parser.add_argument(
        '--processes',
        action='store_true',
        help='Check process health only'
    )
    parser.add_argument(
        '--save',
        type=str,
        metavar='FILENAME',
        help='Save report to specified file'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output (only summary)'
    )
    
    args = parser.parse_args()
    
    diagnostic = SystemDiagnostic()
    
    # Run specific checks or all diagnostics
    if args.disk:
        diagnostic.check_disk_health()
    elif args.memory:
        diagnostic.check_memory_health()
    elif args.cpu:
        diagnostic.check_cpu_health()
    elif args.network:
        diagnostic.check_network_health()
    elif args.processes:
        diagnostic.check_process_health()
    else:
        # Run all diagnostics
        if not args.quiet:
            results = diagnostic.run_all_diagnostics()
        else:
            # Quiet mode - run checks but minimal output
            # Redirect stdout temporarily
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            
            results = diagnostic.run_all_diagnostics()
            
            sys.stdout.close()
            sys.stdout = old_stdout
    
    # Print summary
    if not args.quiet:
        diagnostic.print_summary()
    else:
        # Quiet mode - just print summary
        issues_count = len(diagnostic.results['issues'])
        if issues_count == 0:
            print("✓ System healthy - no issues detected")
        else:
            print(f"⚠ {issues_count} issue(s) detected")
            for issue in diagnostic.results['issues']:
                print(f"  - {issue}")
    
    # Save report if requested
    if args.save:
        diagnostic.save_report(args.save)
    elif not args.quiet:
        try:
            save = input("\nSave diagnostic report to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Enter filename (or press Enter for default): ").strip()
                diagnostic.save_report(filename if filename else None)
        except (EOFError, KeyboardInterrupt):
            print("\nReport not saved.")
    
    # Exit with error code if issues found
    if len(diagnostic.results['issues']) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

