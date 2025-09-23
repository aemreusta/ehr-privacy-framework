#!/bin/bash

# Privacy-Preserving EHR Framework - Streamlit Demo Launcher
# Updated to prefer uv and conda env 'ehrEnv' with pip-tools (requirements.in)

set -e  # Exit on any error

echo "🏥 Privacy-Preserving EHR Framework Demo"
echo "========================================"

# Check for conda and activate privacyenv if available
EHR_CONDA_ENV=${EHR_CONDA_ENV:-ehrEnv}
echo "🔍 Checking for conda environment ($EHR_CONDA_ENV)..."
if command -v conda &> /dev/null; then
    echo "✅ Conda found in system"
    
    # Check if target env exists
    if conda env list | grep -q "${EHR_CONDA_ENV}"; then
        echo "🔄 Activating conda environment: ${EHR_CONDA_ENV}"
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate "${EHR_CONDA_ENV}"
        echo "✅ Activated ${EHR_CONDA_ENV} environment"
    else
        echo "⚠️  ${EHR_CONDA_ENV} not found, creating new environment..."
        conda create -n "${EHR_CONDA_ENV}" python=3.10 -y
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate "${EHR_CONDA_ENV}"
        echo "✅ Created and activated ${EHR_CONDA_ENV} environment"
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
if command -v conda &> /dev/null && [[ "$CONDA_DEFAULT_ENV" == "${EHR_CONDA_ENV}" ]]; then
    echo "Environment: conda ${EHR_CONDA_ENV}"
else
    echo "Environment: system Python"
fi

echo "📦 Resolving and installing dependencies (uv + pip-tools)..."

# Prefer uv if available
if command -v uv &> /dev/null; then
    # Compile requirements from *.in if needed
    if [ -f requirements.in ]; then
        if ! command -v pip-compile &> /dev/null; then
            echo "ℹ️  pip-compile not found in PATH; using uv to run it"
            uv run --with pip-tools pip-compile requirements.in -o requirements.txt --quiet || {
                echo "❌ Failed to compile requirements.txt with pip-compile"; exit 1;
            }
        else
            pip-compile requirements.in -o requirements.txt --quiet || {
                echo "❌ Failed to compile requirements.txt with pip-compile"; exit 1;
            }
        fi
    fi
    if [ -f requirements-dev.in ]; then
        if ! command -v pip-compile &> /dev/null; then
            uv run --with pip-tools pip-compile requirements-dev.in -o requirements-dev.txt --quiet || {
                echo "❌ Failed to compile requirements-dev.txt"; exit 1;
            }
        else
            pip-compile requirements-dev.in -o requirements-dev.txt --quiet || {
                echo "❌ Failed to compile requirements-dev.txt"; exit 1;
            }
        fi
    fi
    # Sync environment to compiled requirements
    if [ -f requirements.txt ] || [ -f requirements-dev.txt ]; then
        uv pip sync requirements.txt requirements-dev.txt || uv pip install -r requirements.txt
        echo "✅ Dependencies installed with uv"
    else
        echo "⚠️  No requirements files found to install"
    fi
else
    echo "⚠️  uv not found; falling back to pip/pip-tools where available"
    if command -v pip-compile &> /dev/null && [ -f requirements.in ]; then
        pip-compile requirements.in -o requirements.txt --quiet || true
    fi
    if command -v pip-compile &> /dev/null && [ -f requirements-dev.in ]; then
        pip-compile requirements-dev.in -o requirements-dev.txt --quiet || true
    fi
    if [ -f requirements.txt ]; then
        pip install -q -r requirements.txt
        echo "✅ Main requirements installed (pip)"
    fi
    if [ -f requirements-dev.txt ]; then
        pip install -q -r requirements-dev.txt
        echo "✅ Development requirements installed (pip)"
    fi
fi

# Try to install Pyfhel for homomorphic encryption
echo "🔐 Checking optional Pyfhel (homomorphic encryption)..."
if python -c "import Pyfhel" 2>/dev/null; then
    echo "✅ Pyfhel available"
else
    echo "ℹ️  Pyfhel not installed; demo will use simulation mode"
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
if command -v conda &> /dev/null && [[ "$CONDA_DEFAULT_ENV" == "${EHR_CONDA_ENV}" ]]; then
    echo "   • Running in conda ${EHR_CONDA_ENV} environment"
fi
echo ""

# Start the demo with logging (prefer uv run if available)
RUNNER="streamlit"
if command -v uv &> /dev/null; then
  RUNNER="uv run streamlit"
fi

$RUNNER run streamlit_demo.py \
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
if command -v conda &> /dev/null && [[ "$CONDA_DEFAULT_ENV" == "${EHR_CONDA_ENV}" ]]; then
    echo ""
    echo "🔄 To deactivate conda environment later: conda deactivate"
fi 
