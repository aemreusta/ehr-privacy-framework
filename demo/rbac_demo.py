#!/usr/bin/env python3
"""
Healthcare RBAC System Demo

This script demonstrates the comprehensive Healthcare Role-Based Access Control
system with real-world scenarios and direct method calls as mentioned in the
README.md usage examples.

Usage:
    python demo/rbac_demo.py
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from access_control.rbac import create_healthcare_rbac_system


def main():
    """Demonstrate the enhanced RBAC system with direct method calls."""
    print("=" * 60)
    print("🏥 Healthcare RBAC System - Enhanced Implementation Demo")
    print("=" * 60)
    print()

    # Create the RBAC system
    print("🔧 Initializing Healthcare RBAC System...")
    rbac = create_healthcare_rbac_system()
    print(
        f"✅ System initialized with {rbac.get_total_permissions()} permissions across {len(rbac.roles_permissions)} roles"
    )
    print()

    # Add some realistic users
    print("👥 Adding healthcare users to the system...")
    users_to_add = [
        ("dr_alice_smith", "attending_physician"),
        ("dr_bob_jones", "resident_physician"),
        ("nurse_carol_williams", "nurse"),
        ("nurse_david_brown", "nurse"),
        ("pharmacist_eve_davis", "pharmacist"),
        ("researcher_frank_chen", "researcher"),
        ("analyst_grace_garcia", "data_analyst"),
        ("admin_henry_taylor", "system_admin"),
    ]

    for username, role in users_to_add:
        success = rbac.add_user(username, role)
        if success:
            print(f"  ✅ Added {username} as {role}")
        else:
            print(f"  ❌ Failed to add {username}")
    print()

    # Display role-permission matrix
    print("📋 Role-Permission Matrix:")
    print("-" * 40)
    for role, permissions in rbac.roles_permissions.items():
        print(f"🔹 {role.replace('_', ' ').title()}: {len(permissions)} permissions")
        for perm in sorted(permissions)[:3]:  # Show first 3 permissions
            print(f"   • {perm}")
        if len(permissions) > 3:
            print(f"   ... and {len(permissions) - 3} more")
        print()

    # Demonstrate direct permission checking
    print("🔍 Direct Permission Testing (as mentioned in README):")
    print("-" * 50)

    test_cases = [
        ("dr_alice_smith", "prescribe_medication", "Emergency prescription"),
        (
            "nurse_carol_williams",
            "prescribe_medication",
            "Nurse attempting prescription",
        ),
        ("researcher_frank_chen", "read_anonymized_data", "Research data access"),
        (
            "researcher_frank_chen",
            "read_all_patient_data",
            "Research attempting patient data",
        ),
        ("pharmacist_eve_davis", "verify_prescriptions", "Drug safety check"),
        ("admin_henry_taylor", "manage_users", "User management"),
        (
            "admin_henry_taylor",
            "read_all_patient_data",
            "Admin attempting patient access",
        ),
        ("dr_bob_jones", "modify_diagnosis", "Resident diagnosis attempt"),
        ("dr_alice_smith", "access_sensitive_data", "Attending sensitive data access"),
    ]

    for username, action, context in test_cases:
        # This is the direct method call approach mentioned in the README
        has_permission = rbac.check_permission(username, action)
        user_role = rbac.users_roles.get(username, "unknown")

        status = "✅ ALLOWED" if has_permission else "❌ DENIED"
        print(f"{status} | {username} ({user_role}) → {action}")
        print(f"         Context: {context}")
        print()

    # Show user-specific permissions
    print("👤 User Permission Details:")
    print("-" * 30)
    sample_users = ["dr_alice_smith", "nurse_carol_williams", "researcher_frank_chen"]

    for username in sample_users:
        permissions = rbac.get_user_permissions(username)
        role = rbac.users_roles.get(username, "unknown")
        print(f"🔹 {username} ({role}): {len(permissions)} permissions")
        for perm in sorted(permissions)[:4]:  # Show first 4
            print(f"   • {perm}")
        if len(permissions) > 4:
            print(f"   ... and {len(permissions) - 4} more")
        print()

    # Run comprehensive compliance test
    print("🧪 Running Comprehensive Compliance Test...")
    print("-" * 40)
    compliance_results = rbac.run_compliance_test()

    print("📊 Test Results:")
    print(f"   • Total Tests: {compliance_results['total_tests']}")
    print(f"   • Passed: {compliance_results['successful_tests']}")
    print(f"   • Failed: {compliance_results['failed_tests']}")
    print(f"   • Compliance Rate: {compliance_results['compliance_rate']:.1%}")
    print(f"   • RBAC Effectiveness: {compliance_results['rbac_effectiveness']}")
    print(f"   • Security Violations: {compliance_results['security_violations']}")
    print()

    # Generate reports
    print("📄 Generating Reports...")
    print("-" * 25)

    access_log_path = rbac.generate_access_log_report()
    compliance_report_path = rbac.generate_compliance_report()

    print(f"✅ Access log saved to: {access_log_path}")
    print(f"✅ Compliance report saved to: {compliance_report_path}")
    print()

    # System status
    status = rbac.get_system_status()
    print("📈 System Status:")
    print("-" * 20)
    print(f"   • System Initialized: {status['system_initialized']}")
    print(f"   • Active Users: {status['active_users']}")
    print(f"   • Total Roles: {status['total_roles']}")
    print(f"   • Total Permissions: {status['total_permissions']}")
    print(f"   • Access Log Entries: {status['access_log_entries']}")
    print(f"   • Available Roles: {', '.join(status['roles'])}")
    print()

    # Demonstrate README usage pattern
    print("📖 README Usage Pattern Demo:")
    print("-" * 35)
    print("# Example from README - Direct method calls:")
    print()
    print("from src.access_control.rbac import HealthcareRBAC")
    print()
    print("# Create system")
    print("rbac = HealthcareRBAC()")
    print()
    print("# Add users")
    print("rbac.add_user('dr_smith', 'attending_physician')")
    print("rbac.add_user('nurse_jones', 'nurse')")
    print()
    print("# Check permissions directly")
    print("can_prescribe = rbac.check_permission('dr_smith', 'prescribe_medication')")
    print(
        "can_nurse_prescribe = rbac.check_permission('nurse_jones', 'prescribe_medication')"
    )
    print()
    print("# Run compliance testing")
    print("results = rbac.run_compliance_test()")
    print("print(f'Compliance: {results[\"compliance_rate\"]:.1%}')")
    print()

    print("=" * 60)
    print("✅ Healthcare RBAC Demo Complete!")
    print("This demonstrates the enhanced RBAC implementation that replaces")
    print("the placeholder simulate_rbac() function with comprehensive")
    print("healthcare-specific access control capabilities.")
    print("=" * 60)


if __name__ == "__main__":
    main()
