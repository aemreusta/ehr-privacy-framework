#!/usr/bin/env python3
"""
Demo Log Analysis Script

Analyzes Streamlit demo logs to provide insights into:
- User interaction patterns
- Performance metrics
- Error tracking
- Demo session analytics
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd


def parse_log_files():
    """Parse all demo log files and extract metrics"""
    log_dir = Path("logs")

    if not log_dir.exists():
        print("❌ No logs directory found")
        return

    analytics = {
        "session_info": {},
        "user_interactions": [],
        "performance_metrics": {},
        "errors": [],
        "technique_usage": Counter(),
        "processing_times": defaultdict(list),
    }

    # Parse user interactions log
    interactions_file = log_dir / "user_interactions.log"
    if interactions_file.exists():
        print("📊 Analyzing user interactions...")
        with open(interactions_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    analytics["user_interactions"].append(data)

                    # Extract technique usage
                    if "technique" in data.get("message", ""):
                        technique = extract_technique_from_message(data["message"])
                        if technique:
                            analytics["technique_usage"][technique] += 1

                except json.JSONDecodeError:
                    continue

    # Parse detailed log for performance metrics
    detailed_log = log_dir / "streamlit_demo_detailed.log"
    if detailed_log.exists():
        print("⚡ Analyzing performance metrics...")
        with open(detailed_log, "r") as f:
            for line in f:
                # Extract processing times
                time_match = re.search(r"completed in ([\d.]+)s", line)
                if time_match:
                    processing_time = float(time_match.group(1))
                    technique = extract_technique_from_line(line)
                    if technique:
                        analytics["processing_times"][technique].append(processing_time)

                # Extract session information
                if "Demo session started" in line:
                    timestamp = extract_timestamp(line)
                    analytics["session_info"]["start_time"] = timestamp

    # Parse errors log
    errors_file = log_dir / "errors.log"
    if errors_file.exists():
        print("🔍 Analyzing errors...")
        with open(errors_file, "r") as f:
            current_error = None
            for line in f:
                if " - ERROR - " in line:
                    if current_error:
                        analytics["errors"].append(current_error)
                    current_error = {
                        "timestamp": extract_timestamp(line),
                        "message": line.strip(),
                        "traceback": [],
                    }
                elif current_error and line.startswith(" "):
                    current_error["traceback"].append(line.strip())

            if current_error:
                analytics["errors"].append(current_error)

    return analytics


def extract_technique_from_message(message):
    """Extract technique name from log message"""
    techniques = [
        "k-anonymity",
        "l-diversity",
        "t-closeness",
        "differential_privacy",
        "homomorphic_encryption",
        "integrated_analysis",
    ]

    for technique in techniques:
        if technique in message.lower():
            return technique
    return None


def extract_technique_from_line(line):
    """Extract technique name from log line"""
    if "k-anonymity" in line.lower():
        return "k-anonymity"
    elif "differential privacy" in line.lower():
        return "differential_privacy"
    elif "l-diversity" in line.lower():
        return "l-diversity"
    elif "t-closeness" in line.lower():
        return "t-closeness"
    elif "homomorphic" in line.lower():
        return "homomorphic_encryption"
    elif "integrated" in line.lower():
        return "integrated_analysis"
    return None


def extract_timestamp(line):
    """Extract timestamp from log line"""
    match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
    return None


def generate_report(analytics):
    """Generate comprehensive analytics report"""
    print("\n" + "=" * 60)
    print("📊 STREAMLIT DEMO ANALYTICS REPORT")
    print("=" * 60)

    # Session overview
    print("\n📅 SESSION OVERVIEW")
    print("-" * 20)
    if analytics["session_info"].get("start_time"):
        print(f"Start Time: {analytics['session_info']['start_time']}")
    print(f"Total User Interactions: {len(analytics['user_interactions'])}")
    print(f"Total Errors: {len(analytics['errors'])}")

    # Technique usage
    print("\n🔐 PRIVACY TECHNIQUE USAGE")
    print("-" * 30)
    if analytics["technique_usage"]:
        for technique, count in analytics["technique_usage"].most_common():
            print(f"{technique:20} : {count:3d} interactions")
    else:
        print("No technique interactions recorded")

    # Performance metrics
    print("\n⚡ PERFORMANCE METRICS")
    print("-" * 25)
    if analytics["processing_times"]:
        for technique, times in analytics["processing_times"].items():
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                print(
                    f"{technique:20} : avg={avg_time:.3f}s, min={min_time:.3f}s, max={max_time:.3f}s"
                )
    else:
        print("No processing times recorded")

    # Error summary
    print("\n🚨 ERROR SUMMARY")
    print("-" * 17)
    if analytics["errors"]:
        error_types = Counter()
        for error in analytics["errors"]:
            error_type = extract_error_type(error["message"])
            error_types[error_type] += 1

        for error_type, count in error_types.items():
            print(f"{error_type:30} : {count}")
    else:
        print("✅ No errors recorded!")

    # Demo health assessment
    print("\n🏥 DEMO HEALTH ASSESSMENT")
    print("-" * 27)

    total_interactions = len(analytics["user_interactions"])
    error_count = len(analytics["errors"])

    if total_interactions > 0:
        error_rate = error_count / total_interactions
        if error_rate == 0:
            health = "🟢 EXCELLENT"
        elif error_rate < 0.1:
            health = "🟡 GOOD"
        else:
            health = "🔴 NEEDS ATTENTION"
    else:
        health = "⚪ NO DATA"

    print(f"Overall Health: {health}")
    print(
        f"Error Rate: {error_count}/{total_interactions} ({error_rate:.1%})"
        if total_interactions > 0
        else "Error Rate: N/A"
    )

    # Recent activity
    print("\n📈 RECENT ACTIVITY (Last 10 interactions)")
    print("-" * 45)
    recent_interactions = analytics["user_interactions"][-10:]
    for interaction in recent_interactions:
        try:
            data = (
                json.loads(interaction["message"])
                if isinstance(interaction.get("message"), str)
                else {}
            )
            timestamp = interaction.get("timestamp", "N/A")
            action = data.get("action", "unknown")
            technique = data.get("technique", "unknown")
            print(f"{timestamp[:19]} | {technique:15} | {action}")
        except (json.JSONDecodeError, KeyError):
            continue


def extract_error_type(error_message):
    """Extract error type from error message"""
    if "ImportError" in error_message:
        return "ImportError"
    elif "AttributeError" in error_message:
        return "AttributeError"
    elif "KeyError" in error_message:
        return "KeyError"
    elif "ValueError" in error_message:
        return "ValueError"
    elif "FileNotFoundError" in error_message:
        return "FileNotFoundError"
    else:
        return "Other"


def export_analytics_csv(analytics):
    """Export analytics to CSV files for further analysis"""
    output_dir = Path("logs/analytics")
    output_dir.mkdir(exist_ok=True)

    # Export user interactions
    if analytics["user_interactions"]:
        interactions_data = []
        for interaction in analytics["user_interactions"]:
            try:
                data = (
                    json.loads(interaction["message"])
                    if isinstance(interaction.get("message"), str)
                    else {}
                )
                interactions_data.append(
                    {
                        "timestamp": interaction.get("timestamp", ""),
                        "technique": data.get("technique", ""),
                        "action": data.get("action", ""),
                        "details": str(data.get("details", {})),
                    }
                )
            except (json.JSONDecodeError, KeyError):
                continue

        if interactions_data:
            df = pd.DataFrame(interactions_data)
            df.to_csv(output_dir / "user_interactions.csv", index=False)
            print(
                f"📁 Exported user interactions to {output_dir}/user_interactions.csv"
            )

    # Export performance metrics
    if analytics["processing_times"]:
        perf_data = []
        for technique, times in analytics["processing_times"].items():
            for time_val in times:
                perf_data.append({"technique": technique, "processing_time": time_val})

        if perf_data:
            df = pd.DataFrame(perf_data)
            df.to_csv(output_dir / "performance_metrics.csv", index=False)
            print(
                f"📁 Exported performance metrics to {output_dir}/performance_metrics.csv"
            )


def main():
    """Main analysis function"""
    print("🔍 Analyzing Streamlit demo logs...")

    analytics = parse_log_files()

    if not analytics:
        print("❌ No analytics data found")
        return

    generate_report(analytics)

    # Export CSV files
    try:
        export_analytics_csv(analytics)
    except Exception as e:
        print(f"⚠️ Could not export CSV files: {e}")

    print("\n📋 Analysis complete!")
    print("💡 Use this data to improve demo performance and user experience")


if __name__ == "__main__":
    main()
