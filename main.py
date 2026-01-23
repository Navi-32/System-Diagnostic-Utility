"""
Simple command-line interface for System Diagnostic Utility
"""

import sys
from system_diagnostic import SystemDiagnostic


def main():
    """Main function - run all diagnostics"""
    print("Starting System Diagnostic...\n")
    
    # Create diagnostic object
    diagnostic = SystemDiagnostic()
    
    # Run all checks
    diagnostic.run_all_diagnostics()
    
    # Show summary
    diagnostic.print_summary()
    
    # Ask if user wants to save report
    try:
        save = input("\nSave diagnostic report to file? (y/n): ").strip().lower()
        if save == 'y':
            diagnostic.save_report()
            print("Report saved!")
    except:
        pass  # Non-interactive mode


if __name__ == "__main__":
    main()
