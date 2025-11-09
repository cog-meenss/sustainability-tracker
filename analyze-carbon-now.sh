#!/bin/bash
echo "🌱 Carbon Footprint Analysis"
echo "============================"
echo ""

# Create timestamped output directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="carbon-analysis-$TIMESTAMP"

echo "📊 Running analysis..."
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Run the carbon analyzer
python3 carbon-footprint-analyzer/cli.py . --output "$OUTPUT_DIR" --format json html --detailed

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Analysis completed successfully!"
    echo "📊 Reports saved to: $OUTPUT_DIR/"
    echo "🌐 View results: open $OUTPUT_DIR/complete_analysis.html"
    echo ""
    
    # Show quick summary
    if [ -f "$OUTPUT_DIR/complete_analysis.json" ]; then
        echo "📋 Quick Summary:"
        cd carbon-footprint-analyzer
        python3 pipeline_helper.py --report "../$OUTPUT_DIR/complete_analysis.json" 2>/dev/null || echo "   Check the HTML report for detailed results"
        cd ..
    fi
else
    echo "❌ Analysis failed. Please check the error messages above."
fi
