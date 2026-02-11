import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import os

class CryptoScanner:
    def __init__(self):
        self.symbols = ['BTC/USDT']  # Add more symbols as needed
        self.timeframes = ['15m', '1h', '4h']
        self.state = {}
        self.output_dir = 'crypto_reports'
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self, symbol, timeframe):
        """Simulate data loading - replace with actual API call"""
        # Generate synthetic data for demonstration
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        dates = pd.date_range(start_date, end_date, freq=timeframe)
        prices = np.cumprod(1 + np.random.normal(0.001, 0.02, len(dates))) * 30000
        
        return pd.DataFrame({
            'timestamp': dates,
            'close': prices
        }).set_index('timestamp')

    def detect_expansion(self, df):
        """Detect expansion patterns"""
        last_5 = df['close'].iloc[-5:].values
        return (last_5.max() - last_5.min()) / last_5.min() > 0.15

    def detect_tc20(self, df):
        """Detect TC20 pattern (simplified version)"""
        close = df['close'].values
        return close[-1] > close[-5] * 1.05 and close[-1] > close[-10] * 1.1

    def analyze_symbol(self, symbol):
        """Analyze symbol across all timeframes"""
        results = []
        
        for tf in self.timeframes:
            df = self.load_data(symbol, tf)
            expansion = self.detect_expansion(df)
            tc20 = self.detect_tc20(df)
            
            results.append({
                'timeframe': tf,
                'expansion': expansion,
                'tc20': tc20,
                'last_price': df['close'].iloc[-1]
            })
        
        return results

    def generate_html_report(self, symbol, analysis):
        """Generate mobile-friendly HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{symbol} Market Analysis</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .timeframe {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .signal-true {{ color: green; font-weight: bold; }}
                .signal-false {{ color: gray; }}
                h2 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>{symbol} Market Analysis</h1>
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        for result in analysis:
            html += f"""
            <div class="timeframe">
                <h2>{result['timeframe']}</h2>
                <p>Last Price: ${result['last_price']:.2f}</p>
                <p>Expansion: <span class="signal-{result['expansion']}">{str(result['expansion'])}</span></p>
                <p>TC20: <span class="signal-{result['tc20']}">{str(result['tc20'])}</span></p>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        filename = f"{self.output_dir}/{symbol.replace('/', '_')}.html"
        with open(filename, 'w') as f:
            f.write(html)
        return filename

    def run(self):
        """Main scanning loop"""
        print(f"Starting crypto scanner at {datetime.now()}")
        print("="*50)
        
        for symbol in self.symbols:
            if symbol not in self.state:
                self.state[symbol] = {
                    'last_scan': None,
                    'signals': []
                }
            
            analysis = self.analyze_symbol(symbol)
            report_path = self.generate_html_report(symbol, analysis)
            
            # Check for new signals
            new_signals = []
            for tf_result in analysis:
                if tf_result['expansion'] or tf_result['tc20']:
                    new_signals.append({
                        'timeframe': tf_result['timeframe'],
                        'type': 'expansion' if tf_result['expansion'] else 'tc20',
                        'timestamp': datetime.now()
                    })
            
            if new_signals:
                self.state[symbol]['signals'].extend(new_signals)
                print(f"\nNEW SIGNALS FOR {symbol}:")
                for signal in new_signals:
                    print(f"- {signal['timeframe']}: {signal['type'].upper()} SIGNAL")
                print(f"Full report: file://{os.path.abspath(report_path)}")
            else:
                print(f"\nNo new signals for {symbol}")
            
            print("="*50)

if __name__ == "__main__":
    scanner = CryptoScanner()
    scanner.run()
