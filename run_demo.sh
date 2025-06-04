#!/bin/bash

# Privacy-Preserving EHR Framework - Streamlit Demo Launcher
# Enhanced with comprehensive logging support

set -e  # Exit on any error

echo "🏥 Privacy-Preserving EHR Framework Demo"
echo "========================================"

# Create logs directory
echo "📁 Setting up logging..."
mkdir -p logs

# Clear old log files (optional - comment out to keep history)
# rm -f logs/*.log

# Check Python version
echo "🐍 Checking Python environment..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"

# Install/check requirements
echo "📦 Checking requirements..."
if [ -f "requirements_demo.txt" ]; then
    pip install -q -r requirements_demo.txt
    echo "✅ Requirements installed"
else
    echo "⚠️  requirements_demo.txt not found, proceeding anyway"
fi

# Check if logging config exists
if [ -f "logging_config.yaml" ]; then
    echo "✅ Logging configuration found"
else
    echo "⚠️  logging_config.yaml not found, using default logging"
fi

# Set environment variables for better logging
export PYTHONUNBUFFERED=1
export STREAMLIT_LOGGER_LEVEL=INFO

# Launch Streamlit with optimal settings for demo recording
echo "🚀 Launching Streamlit demo..."
echo "📹 Optimized for video recording at http://localhost:8501"
echo ""
echo "🔧 Demo features:"
echo "   • Real-time parameter adjustment"
echo "   • Performance monitoring"
echo "   • Comprehensive error handling"
echo "   • Debug panel in sidebar"
echo "   • Detailed logging to logs/ directory"
echo ""

# Start the demo with logging
streamlit run streamlit_demo.py \
    --server.port 8501 \
    --server.address localhost \
    --server.headless false \
    --server.runOnSave false \
    --server.allowRunOnSave false \
    --browser.gatherUsageStats false \
    --global.developmentMode false \
    --theme.base "light" \
    --theme.primaryColor "#1f77b4" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f0f2f6" \
    --theme.textColor "#262730" \
    2>&1 | tee logs/streamlit_console.log

echo ""
echo "📊 Demo session completed"
echo "📁 Check logs/ directory for detailed logs:"
echo "   • streamlit_demo_detailed.log - Complete debug information"
echo "   • user_interactions.log - User interaction analytics"
echo "   • errors.log - Error tracking"
echo "   • streamlit_console.log - Console output" 