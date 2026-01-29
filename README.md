# AI-Powered Stock & ETF Signal Generation Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## Overview

An enterprise-grade, end-to-end Python-based trading intelligence system that leverages machine learning, deep learning, and financial analytics to generate accurate buy/sell signals, backtest trading strategies, and deliver real-time market alerts. The platform features interactive dashboards, comprehensive strategy analysis, and seamless integration with financial APIs for live and historical stock and ETF data.

**For detailed documentation and presentation slides, see:**
- [AI-Powered Stock & ETF Signal Generation Platform Documentation](AI-%20POWERED%20STOCK%20%26%20ETF%20SIGNAL%20GENERATION%20PLATFORM%20Documentation.pdf)
- [AI-Powered Stock and ETF Signal Generation Platform Presentation](AI-Powered%20Stock%20and%20ETF%20Signal%20Generation%20Platform%20Presentation.pdf)

## Key Features

- **LSTM-Based Signal Generation**: Deep learning model predicting BUY/SELL/HOLD signals with 60%+ confidence threshold
- **Interactive Dashboards**: Real-time visualization of market signals and performance metrics using Streamlit
- **VectorBT-Powered Backtesting**: High-performance backtesting engine comparing ML strategy vs market performance
- **Technical Indicators**: 40+ TA-Lib indicators (RSI, MACD, EMA, Bollinger Bands, etc.) for comprehensive analysis
- **Confidence Scoring**: ML metrics combined with market metrics for signal reliability assessment
- **Multi-Asset Support**: Support for stocks, ETFs, and Indian securities (NSE)
- **REST API**: FastAPI-based microservice architecture for programmatic access
- **Automatic API Start**: Streamlit app automatically launches FastAPI backend on startup
- **Database Integration**: Supabase integration for scalable data persistence
- **Real-Time Alerts**: APScheduler-based scheduled alerts with customizable preferences

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Windows/Linux/macOS

### Step 1: Clone the Repository

```bash
git clone https://github.com/soumodip-ghosh/Al-Powered-Stock-ETF-Signal-Generation-Platform.git
cd Al-Powered-Stock-ETF-Signal-Generation-Platform
```

### Step 2: Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# API Configuration
API_HOST=localhost
API_PORT=8000

# Feature Flags
ENABLE_ALERTS=true
ENABLE_BACKTESTING=true
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run 0_Overview.py
```

The Streamlit dashboard will launch and automatically start the FastAPI backend server.

### 3. Access the Dashboard

```
http://localhost:8501
```

### 4. Navigate Features

- **AI Signals**: View real-time buy/sell signals for tracked assets
- **Strategy Analysis**: Backtest and evaluate trading strategies
- **Alerts & Preferences**: Configure real-time market alerts

## Project Structure

```
AI-Powered-Stock-ETF-Signal-Generation-Platform/
│
├── app/                          # Core application modules
│   ├── engine.py                 # Signal generation engine
│   ├── data_loader.py            # Data loading utilities
│   ├── schemas.py                # Pydantic data schemas
│   └── __init__.py
│
├── backtesting/                  # Backtesting engine
│   ├── engine.py                 # Standard backtesting engine
│   ├── engine_vectorbt.py        # VectorBT-optimized engine
│   ├── main.py                   # Backtesting entry point
│   └── schemas.py                # Backtesting schemas
│
├── api/                          # REST API implementation
│   └── backtesting_api.py        # FastAPI application
│
├── signals/                      # Signal generation pipeline
│   ├── data_pipeline.py          # Data processing pipeline
│   ├── predictor.py              # Prediction logic
│   ├── train_lstm.py             # LSTM model training
│   ├── train_and_save.py         # Model persistence
│   └── data/                     # Signal data files
│
├── ml/                           # Machine learning models
│   ├── pradict_lstm.py           # LSTM predictions
│   ├── predictor.py              # Generic predictor interface
│   ├── genai_ensem.py            # Ensemble models
│   └── models/                   # Trained model artifacts
│       ├── lstm_stock_model.h5   # LSTM weights
│       └── xgb_model.json        # XGBoost model
│
├── data/                         # Data management
│   ├── fetcher.py                # Financial data fetching
│   ├── api_client.py             # API client utilities
│   ├── pipeline_adapter.py       # Pipeline adapters
│   └── historical/               # Historical stock data (CSV)
│
├── alerts/                       # Alert system
│   ├── main.py                   # Alert scheduler
│   └── requirements.txt          # Alert-specific dependencies
│
├── ui/                           # User interface components
│   ├── components/               # Streamlit UI components
│   │   ├── charts.py             # Chart rendering
│   │   ├── controls.py           # UI controls
│   │   ├── indicators.py         # Technical indicators display
│   │   └── metrics.py            # Performance metrics
│   └── utils/                    # UI utilities
│       ├── constants.py          # UI constants
│       └── design.py             # UI design system
│
├── pages/                        # Streamlit multi-page app
│   ├── 1_📊_AI_Signals.py        # Signal viewing page
│   ├── 2_📈_Strategy_Analysis.py # Backtesting page
│   └── 3_⚙️_Alerts_&_Preferences.py # Settings page
│
├── contracts/                    # Data contracts
│   └── schema.py                 # Shared schemas
│
├── scripts/                      # Utility scripts
│   ├── run_api.py                # API startup script
│   ├── test_backtest.py          # Backtesting tests
│   ├── send_test_alert.py        # Alert testing
│   └── send_instant_report.py    # Report generation
│
├── tests/                        # Test files
│   ├── system_check.py           # System validation
│   └── check_log.txt             # Log files
│
├── docs/                         # Documentation
│   ├── README.md                 # Additional documentation
│   ├── SUPABASE_SETUP.md         # Database setup guide
│   └── SUPABASE_TABLE_SCHEMA.md  # Database schema
│
├── utils/                        # Utility modules
│   └── api_starter.py            # API management utilities
│
├── 0_Overview.py                 # Main Streamlit app
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .env.example                  # Environment template
└── LICENSE                       # MIT License
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SUPABASE_URL` | Supabase project URL | Required |
| `SUPABASE_KEY` | Supabase API key | Required |
| `API_HOST` | API server hostname | localhost |
| `API_PORT` | API server port | 8000 |
| `ENABLE_ALERTS` | Enable alert system | true |
| `ENABLE_BACKTESTING` | Enable backtesting | true |
| `LOG_LEVEL` | Logging level | INFO |

## Usage

### Running the Application

Simply install dependencies and run Streamlit:

```bash
pip install -r requirements.txt
streamlit run 0_Overview.py
```

The application automatically starts:
- **Streamlit Dashboard** on http://localhost:8501
- **FastAPI Backend** on http://localhost:8000

Both services run automatically in the background when you launch the Streamlit app.

### Application Features

**Overview Page**
- Key metrics and platform status
- API server status indicator
- Quick access to main features

**AI Signals Page (📊)**
- Real-time buy/sell/hold signals for tracked assets
- Signal confidence scores
- Technical indicator display
- Historical signal performance

**Strategy Analysis Page (📈)**
- Backtest any ticker symbol
- Compare ML strategy vs market performance
- View equity curves and profit/loss graphs
- Analyze winning and losing trades
- Win rate and profit factor metrics

**Alerts & Preferences Page (⚙️)**
- Configure alert thresholds
- Set notification preferences
- Schedule alert checks
- Manage tracked assets

## Technical Architecture

### Core Components

**Frontend (Streamlit)**
- Multi-page dashboard with responsive UI
- Real-time signal visualization
- Interactive backtesting interface
- Alert configuration and management

**Backend (FastAPI)**
- RESTful API for backtesting (`POST /api/v1/backtest/run`)
- Health check endpoints
- VectorBT integration for performance calculations
- Automatic startup via Streamlit

**ML Pipeline**
- LSTM neural network (20-day sequence, 40+ indicators)
- 3-class classification: BUY (2), HOLD (1), SELL (0)
- Confidence threshold: 60% minimum
- Feature: 40+ TA-Lib technical indicators
- Multi-asset support (US stocks, ETFs, NSE securities)

**Database (Supabase)**
- Persistent storage for signals and results
- User alert preferences and configurations
- Historical backtesting data

### Technologies Used

| Component | Technology |
|-----------|-----------|
| Web Framework | Streamlit |
| API Framework | FastAPI |
| ML/Deep Learning | TensorFlow/Keras |
| Backtesting | VectorBT (High-performance) |
| Data Processing | Pandas, NumPy |
| Technical Analysis | TA-Lib (40+ indicators) |
| Market Data | yfinance |
| Task Scheduling | APScheduler |
| Database | Supabase (PostgreSQL) |
| Visualization | Plotly, Matplotlib |
| Model Management | Joblib, pickle |

## API Documentation

### Backtesting Endpoint

```
POST /api/v1/backtest/run
Content-Type: application/json

Request Body:
{
  "ticker": "AAPL"  // Stock ticker symbol
}

Response:
{
  "confidence_score": 0.75,
  "ml_metrics": {
    "win_rate": 0.65,
    "profit_factor": 1.8,
    "total_trades": 45,
    "avg_winning_trade": 150.25,
    "avg_losing_trade": -85.50,
    "largest_winning_trade": 520.75,
    "largest_losing_trade": -310.50
  },
  "market_metrics": {
    "total_return_pct": 28.5,
    "cagr_pct": 12.3,
    "volatility_pct": 18.5,
    "sharpe_ratio": 1.2,
    "max_drawdown_pct": 15.3
  },
  "trading_metrics": {
    "total_profit_loss": 5250.75,
    "total_fees": 180.50
  },
  "equity_curve": [1000000, 1005000, 1010200, ...],
  "pnl_graph": [...],
  "trade_visualization": [...]
}
```

### Health Check Endpoint

```
GET /
Response:
{
  "status": "active",
  "service": "Backtesting API (VectorBT)"
}
```

## Data Flow

1. **Data Fetching** - yfinance retrieves 6 months of historical price data
2. **Indicator Calculation** - TA-Lib computes 40+ technical indicators
3. **LSTM Prediction** - Neural network predicts BUY/SELL/HOLD signals
4. **Confidence Scoring** - Combines ML metrics with market analysis
5. **Backtesting** - VectorBT simulates strategy with market comparison
6. **Visualization** - Streamlit renders equity curves and metrics
7. **Alerts** - APScheduler triggers notifications based on signals

## Machine Learning Models

### LSTM Neural Network (Primary)
- **Architecture**: TensorFlow/Keras LSTM model with sequence length of 20 days
- **Input Features**: 40+ technical indicators computed via TA-Lib
- **Output**: 3-class classification (BUY, HOLD, SELL)
- **Confidence Threshold**: 60% minimum to generate signals
- **Training Data**: Historical 6-month price data with indicator features
- **Model File**: `ml/models/lstm_stock_model.h5`

### Ensemble Models
- Combines LSTM predictions with market-based metrics
- Calculates confidence scores from both ML and market performance data
- Produces more robust signals through multi-model voting

## Backtesting Engine

### VectorBT Integration
- High-performance vectorized backtesting
- Compares ML strategy performance vs buy-and-hold market strategy
- Generates comprehensive performance analytics

### Metrics Calculated

**Market Metrics (Buy & Hold)**:
- Total Return (%)
- CAGR (Compound Annual Growth Rate)
- Volatility
- Sharpe Ratio
- Maximum Drawdown

**ML Strategy Metrics**:
- Win Rate (% of profitable trades)
- Profit Factor (Gross Profit / Gross Loss)
- Trade Statistics (entry/exit points)
- PnL Analysis (winning vs losing trades)
- Equity Curve

**Confidence Score**: Combined ML metrics + market metrics assessment

## API Endpoints

### Backtesting Service

```
POST /api/v1/backtest/run
Content-Type: application/json

Request:
{
  "ticker": "AAPL"
}

Response:
{
  "confidence_score": 0.75,
  "ml_metrics": {
    "win_rate": 0.65,
    "profit_factor": 1.8,
    "total_trades": 45
  },
  "market_metrics": {
    "total_return_pct": 28.5,
    "sharpe_ratio": 1.2,
    "max_drawdown_pct": 15.3
  },
  "trading_metrics": {...},
  "equity_curve": [...],
  "pnl_graph": [...],
  "trade_visualization": [...]
}
```

```
GET /
Health check endpoint returning service status
```

## Technologies Used

- **Frontend**: Streamlit for interactive dashboards
- **Backend**: FastAPI for REST API
- **ML/DL**: TensorFlow, Keras (LSTM models)
- **Data Processing**: Pandas, NumPy
- **Technical Analysis**: TA-Lib (40+ indicators)
- **Backtesting**: VectorBT (high-performance vectorized backtesting)
- **Market Data**: yfinance
- **Database**: Supabase (PostgreSQL)
- **Task Scheduling**: APScheduler
- **Visualization**: Plotly, Matplotlib

## Dependencies

See [requirements.txt](requirements.txt) for complete list. Key dependencies:

```
streamlit>=1.0.0
fastapi>=0.95.0
tensorflow>=2.13.0
pandas>=1.5.0
numpy>=1.24.0
yfinance>=0.2.30
scikit-learn>=1.3.0
xgboost>=1.7.0
vectorbt>=0.25.0
plotly>=5.14.0
supabase>=2.0.0
apscheduler>=3.10.4
ta>=0.10.2
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include type hints
- Write unit tests for new features
- Update documentation accordingly

## Known Limitations & Considerations

- LSTM model requires 20 days of historical data minimum for signal generation
- Confidence threshold (60%) may result in fewer signals during low-volatility periods
- Real-time data limited to market hours (9:30 AM - 4:00 PM ET)
- Supabase requires proper configuration and active internet connection
- Alert system requires continuous API running in background
- Model performance varies based on market conditions and data quality
- backtesting uses simulated execution (actual results may differ)

## Roadmap

- [ ] Machine learning model improvements
- [ ] Advanced portfolio optimization
- [ ] Risk management algorithms
- [ ] Real-time sentiment analysis
- [ ] Multi-strategy backtesting
- [ ] Performance optimization

## Troubleshooting

### API Server Won't Start

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database Connection Issues

- Verify `.env` configuration
- Check Supabase project status
- Ensure network connectivity

Contact support or check GitHub Issues for troubleshooting assistance.

## Performance Optimization

- Use VectorBT engine for large-scale backtesting
- Cache historical data locally
- Batch signal generation requests
- Monitor API memory usage

## Security Considerations

**Important**:
- Never commit `.env` files to version control
- Use environment variables for sensitive data
- Validate all API inputs
- Keep dependencies updated
- Use HTTPS in production

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Soumodip Ghosh**
- GitHub: [@soumodip-ghosh](https://github.com/soumodip-ghosh)

## Support

For issues, questions, or suggestions:

1. **GitHub Issues**: [Create an issue](https://github.com/soumodip-ghosh/Al-Powered-Stock-ETF-Signal-Generation-Platform/issues)
2. **Discussions**: Use GitHub Discussions

## Acknowledgments

- yfinance for financial data
- TensorFlow and Keras for deep learning
- VectorBT for backtesting framework
- Streamlit for frontend framework
- Supabase for database infrastructure

## Disclaimer

**This software is provided for educational and research purposes only.** It is not investment advice. Trading in financial markets involves significant risk. Past performance is not indicative of future results. Always consult with a qualified financial advisor before making investment decisions. The authors are not responsible for any financial losses or damages resulting from the use of this software.
