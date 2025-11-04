# SAM Demo - Quantitative Analyst Scenarios

Complete demo scenarios for Quantitative Analyst role with step-by-step conversations, expected responses, and data flows.

---

## Quantitative Analyst

### Quant Analyst - Factor Analysis & Performance Attribution

#### Business Context Setup

**Persona**: Dr. James Chen, Quantitative Analyst at Snowcrest Asset Management  
**Business Challenge**: Quantitative analysts need advanced factor analysis, performance attribution, and systematic strategy development tools to identify patterns, screen securities, and develop data-driven investment approaches. Traditional quant tools are siloed and don't integrate fundamental research insights with quantitative analysis.  
**Value Proposition**: AI-powered quantitative analysis that instantly accesses comprehensive factor exposures and combines sophisticated factor modeling with fundamental research integration, enabling systematic strategy development with both quantitative rigor and qualitative context in seconds rather than minutes.

**Agent**: `quant_analyst`  
**Data Available**: Enhanced factor exposures (7 factors × 5 years × monthly), fundamentals data, 1,200 broker reports, 800 earnings transcripts

#### Demo Flow

**Scene Setting**: Dr. Chen is developing a new systematic strategy focused on quality and momentum factors. He needs to screen securities, analyze factor exposures, backtest strategies, and validate findings with fundamental research to present a comprehensive investment case.

##### Step 1: Factor Screening
**User Input**: 
```
"Screen for stocks with improving momentum and quality factors over the last 6 months."
```

**Alternative Query (if needed)**: 
```
"Show me stocks with the highest momentum and quality factor exposures from the latest data."
```

**Tools Used**:
- `quantitative_analyzer` (Cortex Analyst) - Query SAM_QUANT_VIEW for securities with high momentum and quality factor scores

**Expected Response**:
- Table of securities with highest momentum and quality factor scores from recent period
- Specific momentum and quality factor exposures (numerical values showing factor loadings)
- Securities ranked by combined momentum and quality factor characteristics
- Available factors confirmed: Market, Size, Value, Growth, Momentum, Quality, Volatility
- Portfolio context showing which screened securities are already held

**Talking Points**:
- **Instant Factor Recognition**: Agent immediately understands available factors (Momentum, Quality, Value, Growth, etc.) without data exploration
- **Direct Factor Screening**: Systematic screening using pre-built factor metrics with statistical rigor
- **Portfolio Integration**: Immediate identification of factor exposures with portfolio context

**Key Features Highlighted**: 
- **Enhanced Factor Metrics**: Pre-built factor-specific metrics (MOMENTUM_SCORE, QUALITY_SCORE, VALUE_SCORE, GROWTH_SCORE)
- **Time-Series Factor Analysis**: Monthly factor exposures over 5 years enabling trend identification
- **Comprehensive Factor Coverage**: Complete factor universe (Market, Size, Value, Growth, Momentum, Quality, Volatility)

##### Step 2: Factor Comparison Analysis
**User Input**: 
```
"For the stocks with improving momentum and quality factors, compare their factor loadings against our current Value strategy and Growth strategy portfolios."
```

**Tools Used**:
- `quantitative_analyzer` (Cortex Analyst) - Query SAM_QUANT_VIEW to compare factor exposures between screened securities and portfolio holdings

**Expected Response**:
- Side-by-side factor loading comparison between screened securities and current portfolio holdings
- Statistical significance of differences between high momentum/quality stocks and portfolio averages
- Factor tilt analysis showing how these securities would impact portfolio factor exposure
- Risk-adjusted performance implications of adding screened securities to existing portfolios
- Style drift assessment: would adding these securities maintain or shift portfolio style characteristics

**Talking Points**:
- **Targeted Factor Analysis**: Factor comparison focused on high momentum/quality securities vs existing holdings
- **Portfolio Impact Assessment**: Understanding how these securities would change factor exposures
- **Style Consistency Evaluation**: Maintaining investment style while improving factor characteristics

**Key Features Highlighted**: 
- **Conversation-Aware Analysis**: Factor analysis that builds directly on previous screening conversation
- **Portfolio Integration Analysis**: Assessment of how screened securities fit with existing factor exposures
- **Style Impact Evaluation**: Understanding factor changes from incorporating screened securities

##### Step 3: Factor Evolution Analysis
**User Input**: 
```
"Analyze the factor exposure trends of our momentum and quality securities over the last 3 years and show how their factor characteristics have evolved."
```

**Tools Used**:
- `quantitative_analyzer` (Cortex Analyst) - Query SAM_QUANT_VIEW with time dimensions for factor trend analysis over 3 years

**Expected Response**:
- Time-series analysis of momentum and quality factor exposures for screened securities
- Factor stability analysis showing consistency of factor characteristics over time
- Comparison of factor evolution between screened securities and benchmark constituents
- Statistical significance of factor improvements over the 3-year period
- Portfolio impact assessment: how factor evolution affects current holdings

**Talking Points**:
- **Time-Series Factor Analysis**: Sophisticated analysis of factor evolution using 5 years of monthly data
- **Factor Stability Assessment**: Understanding consistency and persistence of factor characteristics
- **Trend Validation**: Statistical validation of factor improvement trends over time

**Key Features Highlighted**: 
- **Time-Series Analysis**: 5 years of monthly factor exposure data enabling sophisticated trend analysis
- **Factor Persistence Studies**: Understanding factor stability and consistency over time periods
- **Statistical Validation**: Rigorous analysis of factor improvement trends with significance testing

##### Step 4: Fundamental Context Integration
**User Input**: 
```
"For the securities with the strongest factor evolution trends, what fundamental themes and research support their improving factor characteristics?"
```

**Tools Used**:
- `quantitative_analyzer` (Cortex Analyst) - Get fundamental metrics from SAM_QUANT_VIEW (revenue growth, margins)
- `search_broker_research` (Cortex Search) - Get qualitative context for factor improvements

**Expected Response**:
- Analysis of fundamental characteristics of top-performing momentum and quality securities
- Earnings trends and analyst sentiment for securities that drove the strategy performance
- Thematic and sector drivers that explain the success of momentum and quality factor selection
- Research validation showing fundamental support for the quantitative factor improvements
- Integration of the complete workflow: factor screening → factor analysis → performance validation → fundamental context

**Talking Points**:
- **Complete Investment Validation**: Fundamental research validates the entire momentum/quality quantitative process
- **Factor-Fundamental Integration**: Understanding why the factor approach worked from both quantitative and qualitative perspectives  
- **Investment Thesis Completion**: Full investment case combining systematic factor analysis with fundamental validation

**Key Features Highlighted**: 
- **End-to-End Integration**: Complete quantitative-to-qualitative workflow validation from screening to fundamental context
- **Conversational Synthesis**: Fundamental analysis that validates and explains the quantitative findings developed in conversation
- **Comprehensive Investment Process**: Complete systematic investment approach combining factor analysis, backtesting, and fundamental research

#### Scenario Wrap-up

**Business Impact Summary**:
- **Speed & Efficiency**: Instant factor screening and analysis eliminating traditional data exploration delays (seconds vs minutes)
- **Strategy Development**: Enhanced systematic strategy development with pre-built factor metrics and time-series analysis
- **Investment Edge**: Earlier identification of factor-based opportunities with comprehensive 7-factor model coverage
- **Research Integration**: Seamless combination of quantitative factor models with fundamental research validation

**Technical Differentiators**:
- **Pre-Built Factor Metrics**: Instant access to factor-specific metrics (MOMENTUM_SCORE, QUALITY_SCORE) eliminating data exploration delays
- **Time-Series Factor Analysis**: 5 years of monthly factor exposures enabling sophisticated trend analysis and screening
- **Complete Factor Universe**: 7-factor model (Market, Size, Value, Growth, Momentum, Quality, Volatility) with sector-specific characteristics
- **Research Integration**: Unique combination of quantitative factor analysis with fundamental research validation

