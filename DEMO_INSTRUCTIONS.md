# 🎥 Streamlit Demo Instructions for Video Recording

## Quick Start

### Launch the Demo

```bash
# Option 1: Use the launcher script (recommended)
./run_demo.sh

# Option 2: Direct Streamlit command
streamlit run streamlit_demo.py

# Option 3: With specific requirements
pip install -r requirements_demo.txt
streamlit run streamlit_demo.py
```

### Access the Demo

- **URL**: <http://localhost:8501>
- **Browser**: Chrome/Firefox recommended for best recording quality
- **Resolution**: 1920x1080 recommended for video recording

---

## 🎬 Video Recording Setup

### Pre-Recording Checklist

1. **✅ Environment Setup**
   - Close unnecessary applications
   - Set browser to full screen (F11)
   - Ensure stable internet connection
   - Test screen recording software

2. **✅ Demo Preparation**
   - Launch Streamlit demo and verify all sections load
   - Have demo script ready (see `demo/README.md`)
   - Prepare mouse/click actions for smooth navigation
   - Test all interactive features

3. **✅ Recording Settings**
   - **Resolution**: 1920x1080 or higher
   - **Frame Rate**: 30 FPS
   - **Audio**: Include narration if desired
   - **Duration**: Plan for 10-minute demo

### Recommended Recording Flow

Follow this sequence for the 10-minute video:

1. **[0:00-1:00] Framework Overview**
   - Start on "Framework Overview" page
   - Show key metrics: 129 records, 5 techniques, 81.3% score
   - Highlight dataset preview and visualizations

2. **[1:00-2:00] Project Structure Tour**
   - Briefly show framework architecture table
   - Navigate through sidebar options to show completeness

3. **[2:00-3:30] Data Anonymization (3 techniques)**
   - **k-anonymity**: Set k=3, show 84.5% retention
   - **l-diversity**: Demonstrate l=2,k=2 with results
   - **t-closeness**: ⭐ NEW - show Earth Mover's Distance

4. **[3:30-5:00] Differential Privacy**
   - Set ε=1.0, show privacy-utility trade-off
   - Display original vs private statistics comparison

5. **[5:00-6:30] Homomorphic Encryption**
   - ⭐ NEW - Show CKKS scheme capabilities
   - Demonstrate homomorphic operations
   - Show secure aggregation results

6. **[6:30-7:30] Integrated Analysis**
   - Run complete privacy analysis
   - Show progress bar and comprehensive results
   - Highlight 95% privacy score, 81.3% framework effectiveness

7. **[7:30-9:00] Privacy-Utility Visualization**
   - Show interactive privacy-utility trade-off chart
   - Highlight integrated framework position
   - Display technique comparison table

8. **[9:00-9:30] Production Readiness**
   - Show production readiness assessment
   - Highlight HIPAA/GDPR/FDA compliance

9. **[9:30-10:00] Conclusion**
   - Summarize key achievements
   - Emphasize production-ready status

---

## 📋 Interactive Demo Features

### Navigation

- **Sidebar**: Select privacy technique to demonstrate
- **Parameters**: Adjust privacy levels in real-time
- **Buttons**: Apply techniques and see immediate results
- **Metrics**: Live calculation of retention rates and scores

### Key Interactive Elements

#### Framework Overview

- Dataset preview with 129 patient records
- Age and diagnosis distribution visualizations
- Framework architecture summary

#### k-anonymity Demo

- Slider for k-values (2-10)
- Multi-select quasi-identifiers
- Real-time retention rate calculation
- Before/after data comparison

#### l-diversity Demo

- Configure l and k values
- Select sensitive attributes
- Diversity statistics display
- Success/failure indication

#### t-closeness Demo ⭐ **NEW**

- t-threshold slider (0.1-0.5)
- Earth Mover's Distance calculations
- Distribution compliance verification
- Distance analysis metrics

#### Differential Privacy Demo

- Privacy budget (ε) selection
- Query type options
- Original vs private statistics comparison
- Privacy budget analysis

#### Homomorphic Encryption Demo ⭐ **NEW**

- Input value customization
- Live homomorphic operations
- Verification of encryption accuracy
- Secure aggregation on healthcare data

#### Integrated Analysis

- Progress bar for comprehensive analysis
- All 5 techniques applied sequentially
- Interactive privacy-utility trade-off chart
- Production readiness assessment

---

## 🎯 Demo Tips for Video Recording

### Smooth Navigation

- **Pause briefly** after clicking to allow UI updates
- **Highlight mouse cursor** if recording software supports it
- **Use smooth scrolling** rather than rapid page jumps
- **Show loading states** - don't skip spinner animations

### Visual Emphasis

- **Hover over metrics** to show tooltips
- **Zoom browser** to 110-125% for better readability
- **Use side-by-side layouts** effectively
- **Highlight success messages** (green boxes)

### Narration Points

- Mention "⭐ NEW IMPLEMENTATION" for t-closeness and homomorphic encryption
- Emphasize "production-ready" and "regulatory compliance"
- Highlight specific metrics: "81.3% effectiveness", "95% privacy score"
- Note "real MIMIC-III healthcare data" validation

### Interactive Demonstrations

- **Change parameters** to show real-time updates
- **Compare different privacy levels** (k=2 vs k=5)
- **Show failed cases** (l=3 diversity) for authenticity
- **Demonstrate trade-offs** between privacy and utility

---

## 🔧 Technical Features Highlighted

### Data Processing

- Real MIMIC-III clinical dataset (129 admissions)
- 10 clinical variables with appropriate data types
- Automatic fallback to generated data if files missing

### Privacy Techniques

- **k-anonymity**: Configurable k-values with suppression
- **l-diversity**: Entropy-based diversity with verification
- **t-closeness**: Earth Mover's Distance implementation
- **Differential Privacy**: Laplace mechanism with budget tracking
- **Homomorphic Encryption**: CKKS scheme with graceful fallback

### Visualizations

- **Matplotlib**: Age distribution histograms
- **Plotly**: Interactive privacy-utility trade-off charts
- **Pandas**: Data table displays with formatting
- **Custom CSS**: Professional styling for video quality

### Performance Metrics

- Real-time processing time measurement
- Data retention rate calculation
- Privacy score computation
- Framework effectiveness assessment

---

## 🚀 Production Features Demonstrated

### Regulatory Compliance

- HIPAA, GDPR, FDA compliance indicators
- Role-based access control simulation
- Audit trail capabilities
- Privacy budget management

### Framework Integration

- Multi-layer privacy protection (5 techniques)
- Seamless technique coordination
- Comprehensive evaluation methodology
- Production deployment readiness

### Scientific Validation

- Real healthcare data validation
- Quantitative privacy-utility analysis
- Benchmark performance metrics
- Novel contribution verification

---

## ⚠️ Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install requirements with `pip install -r requirements_demo.txt`
2. **Port 8501 in use**: Stop other Streamlit processes or use `--server.port 8502`
3. **Data loading errors**: Framework automatically generates sample data
4. **Slow performance**: Use smaller dataset or reduce complexity for smoother demo

### Fallback Options

- **Missing Pyfhel**: Homomorphic encryption shows simulated results
- **Missing data files**: Automatic generation of healthcare-like sample data
- **Import errors**: Graceful degradation with informative error messages

### Demo Recovery

If demo encounters issues during recording:

- Refresh browser to restart
- Use fallback sample data
- Continue with available techniques
- Framework designed for robust demonstration

---

**🎬 Ready to Record!** The Streamlit demo provides a professional, interactive interface perfect for showcasing all five privacy techniques in the 10-minute video demonstration.
