#!/usr/bin/env python3
"""
Runtime Sustainability Report Generator
Generates dynamic reports on-demand instead of static files
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
import time

class RuntimeSustainabilityReporter:
    """Generate sustainability reports in real-time"""
    
    def __init__(self, project_path="."):
        self.project_path = Path(project_path).absolute()
        self.analyzer_path = self.project_path / "sustainability-analyzer" / "analyzer" / "sustainability_analyzer.py"
        
    def generate_runtime_report(self, format_type="summary", output_format="console"):
        """Generate a fresh sustainability report at runtime"""
        print("🔄 Generating runtime sustainability analysis...")
        start_time = time.time()
        
        try:
            # Run the sustainability analyzer
            result = subprocess.run([
                sys.executable, 
                str(self.analyzer_path),
                '--path', str(self.project_path),
                '--output', '/tmp/runtime_analysis.json',
                '--format', 'json'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return {"error": f"Analysis failed: {result.stderr}"}
            
            # Load the fresh results
            with open('/tmp/runtime_analysis.json', 'r') as f:
                analysis_data = json.load(f)
            
            # Clean up temporary file
            os.remove('/tmp/runtime_analysis.json')
            
            execution_time = time.time() - start_time
            analysis_data['runtime_info'] = {
                'generated_at': datetime.now().isoformat(),
                'generation_time': execution_time,
                'format_type': format_type,
                'project_path': str(self.project_path)
            }
            
            return self._format_report(analysis_data, output_format)
            
        except subprocess.TimeoutExpired:
            return {"error": "Analysis timeout - project too large"}
        except Exception as e:
            return {"error": f"Runtime analysis failed: {str(e)}"}
    
    def _format_report(self, data, output_format):
        """Format the analysis data based on requested output format"""
        if output_format == "json":
            return data
        elif output_format == "console":
            return self._format_console_report(data)
        elif output_format == "html":
            return self._format_html_report(data)
        elif output_format == "markdown":
            return self._format_markdown_report(data)
        else:
            return data
    
    def _format_console_report(self, data):
        """Format for console output"""
        metrics = data['sustainability_metrics']
        summary = data['analysis_summary']
        runtime_info = data['runtime_info']
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║               🌱 RUNTIME SUSTAINABILITY REPORT              ║
╚══════════════════════════════════════════════════════════════╝

📊 OVERALL SCORE: {metrics['overall_score']:.1f}/100

┌─────────────────────────────┬────────┬──────────────────┐
│ Metric                      │ Score  │ Status           │
├─────────────────────────────┼────────┼──────────────────┤
│ Energy Efficiency           │ {metrics['energy_efficiency']:6.1f} │ {self._get_status(metrics['energy_efficiency'])} │
│ Resource Utilization        │ {metrics['resource_utilization']:6.1f} │ {self._get_status(metrics['resource_utilization'])} │
│ Carbon Footprint           │ {metrics['carbon_footprint']:6.1f} │ {self._get_carbon_status(metrics['carbon_footprint'])} │
│ Performance Optimization   │ {metrics['performance_optimization']:6.1f} │ {self._get_status(metrics['performance_optimization'])} │
│ Sustainable Practices      │ {metrics['sustainable_practices']:6.1f} │ {self._get_status(metrics['sustainable_practices'])} │
└─────────────────────────────┴────────┴──────────────────┘

🎯 QUALITY GATE: {self._get_quality_gate(metrics['overall_score'])}

📁 PROJECT ANALYSIS:
   • Files Analyzed: {summary['file_count']}
   • Languages: {', '.join([f"{lang.title()}({count})" for lang, count in summary['language_breakdown'].items()])}
   • Analysis Time: {summary['execution_time']:.3f}s
   • Report Generated: {runtime_info['generated_at'][:19]}
   • Generation Time: {runtime_info['generation_time']:.3f}s

💡 TOP RECOMMENDATIONS:
"""
        
        for i, rec in enumerate(data.get('recommendations', [])[:3], 1):
            priority_icon = self._get_priority_icon(rec['priority'])
            report += f"   {i}. {priority_icon} {rec['title']} ({rec['priority'].upper()})\n"
            report += f"      └─ {rec['description']}\n"
        
        report += f"\n🔄 This report was generated at runtime on {runtime_info['generated_at'][:19]}\n"
        
        return report
    
    def _format_html_report(self, data):
        """Generate runtime HTML report"""
        metrics = data['sustainability_metrics']
        summary = data['analysis_summary']
        runtime_info = data['runtime_info']
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Runtime Sustainability Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                margin: 0; padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: rgba(255,255,255,0.95); 
                     border-radius: 20px; padding: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; background: linear-gradient(45deg, #2ecc71, #27ae60); 
                  color: white; padding: 30px; border-radius: 15px; margin: -30px -30px 40px -30px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                   gap: 20px; margin: 30px 0; }}
        .metric {{ background: white; border-radius: 15px; padding: 25px; text-align: center; 
                  box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .score {{ font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }}
        .excellent {{ color: #27ae60; }}
        .good {{ color: #f39c12; }}
        .poor {{ color: #e74c3c; }}
        .runtime-info {{ background: #f8f9fa; border-radius: 10px; padding: 20px; margin: 20px 0; 
                        border-left: 5px solid #3498db; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 Runtime Sustainability Report</h1>
            <p>Generated on {runtime_info['generated_at'][:19]}</p>
        </div>
        
        <div class="runtime-info">
            <h3>📊 Runtime Analysis Info</h3>
            <p><strong>Analysis Time:</strong> {summary['execution_time']:.3f}s</p>
            <p><strong>Report Generation:</strong> {runtime_info['generation_time']:.3f}s</p>
            <p><strong>Files Analyzed:</strong> {summary['file_count']}</p>
            <p><strong>Languages:</strong> {', '.join([f"{lang.title()}: {count}" for lang, count in summary['language_breakdown'].items()])}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="score {self._get_css_class(metrics['overall_score'])}">{metrics['overall_score']:.1f}/100</div>
                <div>Overall Score</div>
            </div>
            <div class="metric">
                <div class="score {self._get_css_class(metrics['energy_efficiency'])}">{metrics['energy_efficiency']:.1f}</div>
                <div>Energy Efficiency</div>
            </div>
            <div class="metric">
                <div class="score {self._get_css_class(metrics['resource_utilization'])}">{metrics['resource_utilization']:.1f}</div>
                <div>Resource Utilization</div>
            </div>
            <div class="metric">
                <div class="score {self._get_css_class(metrics['performance_optimization'])}">{metrics['performance_optimization']:.1f}</div>
                <div>Performance</div>
            </div>
        </div>
        
        <h3>💡 Recommendations</h3>
        <ul>
"""
        
        for rec in data.get('recommendations', []):
            priority_color = {'high': '#e74c3c', 'medium': '#f39c12', 'low': '#27ae60'}.get(rec['priority'], '#3498db')
            html += f'<li style="color: {priority_color}"><strong>{rec["title"]}</strong> - {rec["description"]}</li>'
        
        html += f"""
        </ul>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <small>🔄 This report was generated at runtime • Refresh page for updated analysis</small>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _format_markdown_report(self, data):
        """Generate runtime markdown report"""
        metrics = data['sustainability_metrics']
        summary = data['analysis_summary']
        runtime_info = data['runtime_info']
        
        md = f"""# 🔄 Runtime Sustainability Analysis

> **Generated**: {runtime_info['generated_at'][:19]}  
> **Analysis Time**: {summary['execution_time']:.3f}s  
> **Report Generation**: {runtime_info['generation_time']:.3f}s

## 📊 Overall Score: {metrics['overall_score']:.1f}/100

| Metric | Score | Status |
|--------|-------|--------|
| Energy Efficiency | {metrics['energy_efficiency']:.1f}/100 | {self._get_status(metrics['energy_efficiency'])} |
| Resource Utilization | {metrics['resource_utilization']:.1f}/100 | {self._get_status(metrics['resource_utilization'])} |
| Carbon Footprint | {metrics['carbon_footprint']:.1f}/100 | {self._get_carbon_status(metrics['carbon_footprint'])} |
| Performance | {metrics['performance_optimization']:.1f}/100 | {self._get_status(metrics['performance_optimization'])} |
| Sustainable Practices | {metrics['sustainable_practices']:.1f}/100 | {self._get_status(metrics['sustainable_practices'])} |

## 🎯 Quality Gate: {self._get_quality_gate(metrics['overall_score'])}

## 📁 Analysis Summary
- **Files Analyzed**: {summary['file_count']}
- **Languages**: {', '.join([f"{lang.title()}: {count}" for lang, count in summary['language_breakdown'].items()])}

## 💡 Recommendations
"""
        
        for i, rec in enumerate(data.get('recommendations', []), 1):
            priority_icon = self._get_priority_icon(rec['priority'])
            md += f"\n{i}. {priority_icon} **{rec['title']}** ({rec['priority'].upper()})\n"
            md += f"   - {rec['description']}\n"
            md += f"   - Impact: {rec['impact']} | Effort: {rec['effort']}\n"
        
        md += f"\n---\n*🔄 Runtime report generated on {runtime_info['generated_at'][:19]}*\n"
        
        return md
    
    def _get_status(self, score):
        """Get status emoji based on score"""
        if score >= 80:
            return "✅ Excellent"
        elif score >= 60:
            return "⚠️ Good"
        elif score >= 40:
            return "🟡 Fair"
        else:
            return "❌ Poor"
    
    def _get_carbon_status(self, score):
        """Get carbon footprint status (lower is better)"""
        if score <= 30:
            return "✅ Excellent"
        elif score <= 50:
            return "⚠️ Good"
        elif score <= 70:
            return "🟡 Fair"
        else:
            return "❌ Poor"
    
    def _get_quality_gate(self, score):
        """Get quality gate status"""
        return "✅ PASS" if score >= 60 else "❌ FAIL"
    
    def _get_priority_icon(self, priority):
        """Get priority icon"""
        return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "🔵")
    
    def _get_css_class(self, score):
        """Get CSS class for score"""
        if score >= 70:
            return "excellent"
        elif score >= 40:
            return "good"
        else:
            return "poor"

def main():
    """Main CLI interface for runtime report generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Runtime Sustainability Report Generator')
    parser.add_argument('--path', default='.', help='Project path to analyze')
    parser.add_argument('--format', choices=['console', 'json', 'html', 'markdown'], 
                        default='console', help='Output format')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--serve', action='store_true', help='Start web server for live reports')
    
    args = parser.parse_args()
    
    reporter = RuntimeSustainabilityReporter(args.path)
    
    if args.serve:
        print("🚀 Starting runtime report web server...")
        start_web_server(reporter)
    else:
        result = reporter.generate_runtime_report(output_format=args.format)
        
        if isinstance(result, dict) and 'error' in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        
        if args.output:
            with open(args.output, 'w') as f:
                if args.format == 'json':
                    json.dump(result, f, indent=2)
                else:
                    f.write(result)
            print(f"✅ Runtime report saved to: {args.output}")
        else:
            if args.format == 'json':
                print(json.dumps(result, indent=2))
            else:
                print(result)

def start_web_server(reporter):
    """Start a simple web server for live reports"""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import urllib.parse
        
        class ReportHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    report = reporter.generate_runtime_report(output_format='html')
                    self.wfile.write(report.encode())
                
                elif self.path.startswith('/api/report'):
                    query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                    format_type = query.get('format', ['json'])[0]
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json' if format_type == 'json' else 'text/plain')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    report = reporter.generate_runtime_report(output_format=format_type)
                    if format_type == 'json':
                        self.wfile.write(json.dumps(report, indent=2).encode())
                    else:
                        self.wfile.write(report.encode())
                
                else:
                    self.send_error(404)
        
        server = HTTPServer(('localhost', 8000), ReportHandler)
        print("🌐 Runtime report server running at: http://localhost:8000")
        print("📊 API endpoint: http://localhost:8000/api/report?format=json")
        print("Press Ctrl+C to stop...")
        server.serve_forever()
        
    except ImportError:
        print("❌ Web server requires Python's http.server module")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()