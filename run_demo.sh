#!/bin/bash

# Privacy-Preserving EHR Framework - Streamlit Demo Launcher
# Enhanced with comprehensive logging support and conda environment management

set -e  # Exit on any error

echo "🏥 Privacy-Preserving EHR Framework Demo"
echo "========================================"

# Check for conda and activate privacyenv if available
echo "🔍 Checking for conda environment..."
if command -v conda &> /dev/null; then
    echo "✅ Conda found in system"
    
    # Check if privacyenv exists
    if conda env list | grep -q "privacyenv"; then
        echo "🔄 Activating conda environment: privacyenv"
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate privacyenv
        echo "✅ Activated privacyenv environment"
    else
        echo "⚠️  privacyenv not found, creating new environment..."
        conda create -n privacyenv python=3.10 -y
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate privacyenv
        echo "✅ Created and activated privacyenv environment"
    fi
else
    echo "⚠️  Conda not found, using system Python"
fi

# Create logs directory
echo "📁 Setting up logging..."
mkdir -p logs

# Clear old log files (optional - comment out to keep history)
# rm -f logs/*.log

# Check Python version
echo "🐍 Checking Python environment..."
python_version=$(python --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"
if command -v conda &> /dev/null && [[ "$CONDA_DEFAULT_ENV" == "privacyenv" ]]; then
    echo "Environment: conda privacyenv"
else
    echo "Environment: system Python"
fi

# Install/check requirements
echo "📦 Installing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo "✅ Main requirements installed"
else
    echo "⚠️  requirements.txt not found"
fi

# Install development requirements if available
if [ -f "requirements-dev.txt" ]; then
    pip install -q -r requirements-dev.txt
    echo "✅ Development requirements installed"
fi

# Try to install Pyfhel for homomorphic encryption
echo "🔐 Attempting to install Pyfhel for homomorphic encryption..."
if python -c "import Pyfhel" 2>/dev/null; then
    echo "✅ Pyfhel already installed and working"
else
    echo "🔄 Installing Pyfhel..."
    # Try to install Pyfhel - this might fail on some systems
    if pip install Pyfhel; then
        echo "✅ Pyfhel installed successfully"
    else
        echo "⚠️  Pyfhel installation failed (this is optional)"
        echo "   Homomorphic encryption demos will use simulation mode"
        echo "   For manual installation: pip install Pyfhel"
    fi
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
echo "   • University branding with course information"
echo "   • Complete privacy framework integration"
if command -v conda &> /dev/null && [[ "$CONDA_DEFAULT_ENV" == "privacyenv" ]]; then
    echo "   • Running in conda privacyenv environment"
fi
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
echo "   • streamlit_demo_YYYYMMDD_HHMMSS.log - Complete debug information"
echo "   • streamlit_console.log - Console output"
if command -v conda &> /dev/null && [[ "$CONDA_DEFAULT_ENV" == "privacyenv" ]]; then
    echo ""
    echo "🔄 To deactivate conda environment later: conda deactivate"
fi 