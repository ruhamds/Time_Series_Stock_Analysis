"""
Task 3: Forecast Future Market Trends Analysis
Analyzes LSTM forecast results and provides investment insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Your LSTM forecast results
FORECAST_RESULTS = {
    'current_price': 319.04,
    'forecast_6m_price': 205.52,
    'forecast_range_low': 205.52,
    'forecast_range_high': 301.93,
    'expected_return_6m': -0.356,  # -35.6%
    'forecast_period': '6 months'
}

def analyze_forecast_trends():
    """
    Analyze the LSTM forecast results and provide trend insights
    """
    print("=== TESLA (TSLA) FORECAST ANALYSIS ===")
    print(f"Analysis based on LSTM model predictions\n")
    
    # Current situation
    current_price = FORECAST_RESULTS['current_price']
    forecast_price = FORECAST_RESULTS['forecast_6m_price']
    expected_return = FORECAST_RESULTS['expected_return_6m']
    
    print("1. CURRENT MARKET POSITION")
    print("-" * 35)
    print(f"Current TSLA Price: ${current_price:.2f}")
    print(f"Market Cap Category: Large Cap Growth Stock")
    print(f"Sector: Consumer Discretionary (Electric Vehicles)")
    
    # Forecast analysis
    print(f"\n2. 6-MONTH FORECAST ANALYSIS")
    print("-" * 35)
    print(f"Predicted Price: ${forecast_price:.2f}")
    print(f"Expected Return: {expected_return*100:.1f}%")
    print(f"Price Change: ${forecast_price - current_price:.2f}")
    
    # Trend classification
    if expected_return < -0.20:
        trend_category = "Strong Bearish"
        trend_description = "Significant downward trend expected"
    elif expected_return < -0.10:
        trend_category = "Moderately Bearish"
        trend_description = "Moderate decline expected"
    elif expected_return < -0.05:
        trend_category = "Slightly Bearish" 
        trend_description = "Minor decline expected"
    elif expected_return < 0.05:
        trend_category = "Neutral"
        trend_description = "Sideways movement expected"
    elif expected_return < 0.15:
        trend_category = "Moderately Bullish"
        trend_description = "Moderate growth expected"
    else:
        trend_category = "Strong Bullish"
        trend_description = "Significant growth expected"
    
    print(f"\n3. TREND CLASSIFICATION")
    print("-" * 30)
    print(f"Trend Category: {trend_category}")
    print(f"Description: {trend_description}")

def analyze_volatility_and_risk():
    """
    Analyze volatility and risk based on forecast range
    """
    print(f"\n4. VOLATILITY AND RISK ANALYSIS")
    print("-" * 40)
    
    forecast_low = FORECAST_RESULTS['forecast_range_low']
    forecast_high = FORECAST_RESULTS['forecast_range_high']
    current_price = FORECAST_RESULTS['current_price']
    
    # Calculate forecast uncertainty
    forecast_range = forecast_high - forecast_low
    range_as_percent = (forecast_range / current_price) * 100
    
    print(f"Forecast Range: ${forecast_low:.2f} - ${forecast_high:.2f}")
    print(f"Range Width: ${forecast_range:.2f} ({range_as_percent:.1f}% of current price)")
    
    # Worst and best case scenarios
    worst_case_return = (forecast_low - current_price) / current_price
    best_case_return = (forecast_high - current_price) / current_price
    
    print(f"\nScenario Analysis:")
    print(f"• Best Case: {best_case_return*100:.1f}% return (${forecast_high:.2f})")
    print(f"• Expected Case: {FORECAST_RESULTS['expected_return_6m']*100:.1f}% return (${FORECAST_RESULTS['forecast_6m_price']:.2f})")
    print(f"• Worst Case: {worst_case_return*100:.1f}% return (${forecast_low:.2f})")
    
    # Risk assessment
    print(f"\nRisk Assessment:")
    if range_as_percent > 50:
        risk_level = "Very High"
    elif range_as_percent > 30:
        risk_level = "High"
    elif range_as_percent > 20:
        risk_level = "Moderate"
    else:
        risk_level = "Low"
    
    print(f"• Forecast Uncertainty: {risk_level}")
    print(f"• Confidence Interval Width: {range_as_percent:.1f}%")
    
    # Time horizon reliability
    print(f"\nForecast Reliability:")
    print("• LSTM models tend to be more accurate for shorter time horizons")
    print("• 6-month forecasts have moderate reliability for volatile stocks")
    print("• Confidence intervals widen significantly over longer periods")

def market_opportunities_and_risks():
    """
    Identify market opportunities and risks based on forecast
    """
    print(f"\n5. MARKET OPPORTUNITIES AND RISKS")
    print("-" * 45)
    
    expected_return = FORECAST_RESULTS['expected_return_6m']
    
    print("IDENTIFIED RISKS:")
    if expected_return < -0.20:
        print("🔴 HIGH RISK FACTORS:")
        print("• Model predicts significant price decline (-35.6%)")
        print("• Potential overvaluation correction")
        print("• Market sentiment shift against growth stocks")
        print("• Regulatory or competitive pressures possible")
        print("• Macroeconomic headwinds affecting EV sector")
    
    print(f"\n• Downside Risk: Up to {abs(expected_return)*100:.1f}% loss potential")
    print("• Volatility Risk: High price swings expected")
    print("• Model Risk: LSTM predictions can be uncertain")
    print("• Sector Risk: EV industry faces increasing competition")
    
    print(f"\nIDENTIFIED OPPORTUNITIES:")
    forecast_high = FORECAST_RESULTS['forecast_range_high']
    current_price = FORECAST_RESULTS['current_price']
    upside_potential = (forecast_high - current_price) / current_price
    
    if upside_potential > 0:
        print(f"• Upside Potential: Up to {upside_potential*100:.1f}% in best-case scenario")
    
    print("• Value Opportunity: If price declines as predicted, may create buying opportunity")
    print("• Contrarian Strategy: Market may be overly pessimistic")
    print("• Long-term Growth: EV market still has long-term potential")
    print("• Diversification: Can balance with defensive assets")

def investment_recommendations():
    """
    Provide investment recommendations based on forecast
    """
    print(f"\n6. INVESTMENT RECOMMENDATIONS")
    print("-" * 40)
    
    expected_return = FORECAST_RESULTS['expected_return_6m']
    
    print("PORTFOLIO STRATEGY IMPLICATIONS:")
    
    if expected_return < -0.30:
        print("🔴 DEFENSIVE STRATEGY RECOMMENDED:")
        print("• Reduce TSLA allocation significantly")
        print("• Increase allocation to defensive assets (BND)")
        print("• Consider hedging strategies")
        print("• Focus on capital preservation")
        
        recommended_allocation = "5-10%"
    elif expected_return < -0.15:
        print("🟡 CAUTIOUS STRATEGY RECOMMENDED:")
        print("• Moderate TSLA position")
        print("• Increase stable assets allocation")
        print("• Monitor for reversal signals")
        
        recommended_allocation = "10-15%"
    else:
        print("🟢 NEUTRAL TO OPTIMISTIC STRATEGY:")
        print("• Maintain balanced allocation")
        print("• Consider dollar-cost averaging")
        
        recommended_allocation = "15-25%"
    
    print(f"\nRECOMMENDED TSLA ALLOCATION: {recommended_allocation}")
    
    print(f"\nPORTFOLIO REBALANCING SUGGESTIONS:")
    print("• TSLA: Reduce allocation due to negative forecast")
    print("• SPY: Increase for stable market exposure")
    print("• BND: Increase for risk reduction and stability")
    
    print(f"\nRISK MANAGEMENT:")
    print("• Set stop-loss orders if holding TSLA")
    print("• Consider put options for downside protection")
    print("• Maintain diversification across asset classes")
    print("• Regular monitoring and rebalancing")

def confidence_interval_analysis():
    """
    Analyze the confidence intervals and their implications
    """
    print(f"\n7. CONFIDENCE INTERVAL ANALYSIS")
    print("-" * 40)
    
    current_price = FORECAST_RESULTS['current_price']
    forecast_low = FORECAST_RESULTS['forecast_range_low']
    forecast_high = FORECAST_RESULTS['forecast_range_high']
    
    print("FORECAST RELIABILITY ASSESSMENT:")
    
    # Calculate interval width over time
    interval_width = forecast_high - forecast_low
    relative_width = interval_width / current_price
    
    print(f"• Confidence Interval: ${forecast_low:.2f} - ${forecast_high:.2f}")
    print(f"• Interval Width: ${interval_width:.2f}")
    print(f"• Relative Width: {relative_width*100:.1f}% of current price")
    
    print(f"\nIMPLICATIONS:")
    if relative_width > 0.4:
        print("• Very Wide Interval: High forecast uncertainty")
        print("• Model confidence decreases over 6-month horizon")
        print("• Multiple scenarios equally plausible")
    elif relative_width > 0.2:
        print("• Moderate Interval: Reasonable forecast precision")
        print("• Model shows moderate confidence")
    else:
        print("• Narrow Interval: High forecast confidence")
        print("• Model predictions relatively precise")
    
    print(f"\nLONG-TERM FORECAST CHALLENGES:")
    print("• LSTM models work better for short-term predictions")
    print("• Stock price volatility makes long-term forecasting difficult")
    print("• External factors (news, events) not captured in historical patterns")
    print("• Market regime changes can invalidate historical relationships")

def generate_forecast_report():
    """
    Generate comprehensive forecast analysis report
    """
    print("\n" + "="*60)
    print("COMPREHENSIVE FORECAST ANALYSIS REPORT")
    print("="*60)
    
    analyze_forecast_trends()
    analyze_volatility_and_risk()
    market_opportunities_and_risks()
    investment_recommendations()
    confidence_interval_analysis()
    
    print(f"\n8. KEY TAKEAWAYS")
    print("-" * 25)
    print("• TSLA forecast shows significant downside risk (-35.6%)")
    print("• High volatility expected with wide confidence intervals")
    print("• Defensive portfolio positioning recommended")
    print("• Increased allocation to BND and SPY suggested")
    print("• Regular monitoring and risk management essential")
    print("• Consider forecast as one input among many factors")
    
    print(f"\n9. NEXT STEPS FOR PORTFOLIO OPTIMIZATION")
    print("-" * 50)
    print("• Use expected return of -35.6% for TSLA in optimization")
    print("• Calculate expected returns for BND and SPY from historical data")
    print("• Build covariance matrix from historical return correlations")
    print("• Run Mean Variance Optimization to find efficient frontier")
    print("• Identify optimal portfolio weights given risk tolerance")

if __name__ == "__main__":
    generate_forecast_report()