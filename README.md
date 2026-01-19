# EVision Berlin - Electric Vehicle Charging Station Analysis

## Project Overview

EVision Berlin analyzes the demand for electric vehicle (EV) charging stations in Berlin by visualizing:

1. **Population density** per postal code (PLZ)
2. **Existing charging station distribution** per postal code
3. **Power categories** for different charging speeds

The analysis helps identify areas with high population density but low charging station coverage, indicating potential demand for additional infrastructure. This project provides actionable insights for urban planners, policymakers, and EV infrastructure developers.

URL: **[evision-berlin.streamlit.app](https://evision-berlin.streamlit.app/)**

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.51+-red.svg)

</div>

<div align="center">

![Pylint](https://github.com/DAShaikh10/Fortgeschrittene-Softwaretechnik-Electric-Mobility-Berlin/actions/workflows/pylint.yml/badge.svg)
![Pytest](https://github.com/DAShaikh10/Fortgeschrittene-Softwaretechnik-Electric-Mobility-Berlin/actions/workflows/pytest.yml/badge.svg)
![Coverage](https://github.com/DAShaikh10/Fortgeschrittene-Softwaretechnik-Electric-Mobility-Berlin/actions/workflows/coverage.yml/badge.svg)

</div>

**Course:** Advanced Software Engineering  
**Professor:** Dr. Prof. Selcan Ipek Ugay

## Team Members

1. Amaan Aslam Shaikh
2. Danish Ali Abdul Kareem Shaikh
3. Hrusheekesh Sawarkar
4. Melisa Cihan

---

## Table of Contents

1. [Key Features](#key-features)
2. [Architecture Overview](#architecture-overview)
3. [Project Structure](#project-structure)
4. [Installation & Setup](#installation--setup)
5. [Task Commands](#task-commands)
6. [How to Run](#how-to-run)
7. [Application Usage](#application-usage)
8. [Data Sources](#data-sources)
9. [Data Quality Analysis](#data-quality-analysis)
10. [Results Interpretation](#results-interpretation)
11. [Demand Analysis](#demand-analysis)
12. [Testing Strategy](#testing-strategy)
13. [Limitations of Analysis](#limitations-of-analysis)
14. [Technologies Used](#technologies-used)

---

## Key Features

- 📊 **Data Quality Analysis & Outlier Detection:** Comprehensive statistical analysis with visualizations to identify anomalies, outliers, and data quality issues in the dataset
- 🗺️ **Interactive Map Visualization:** Dynamic Folium maps displaying Berlin charging stations with geographic precision
- 📊 **Population Density Heatmap:** Visual representation of resident distribution by postal code
- ⚡ **Power Category Filtering:** Analyze charging stations by power output:
  - Normal (< 50 kW) - AC charging, home wallboxes
  - Fast (50-150 kW) - DC fast charging
  - Ultra (≥ 150 kW) - Ultra-fast DC charging
- 🔍 **ZIP Code Search:** Instant lookup of specific postal code areas
- 📈 **Real-time Statistics Dashboard:** Key metrics and demand indicators
- 🔄 **Dual-layer Visualization:** Simultaneous comparison of population vs. charging infrastructure
- 📋 **Demand Priority Analysis:** Automated calculation of high-demand areas

---

## Architecture Overview

### Domain-Driven Design (DDD)

EVision Berlin is built using **Domain-Driven Design** principles with **Test-Driven Development** (TDD):

#### 🎯 Bounded Contexts

**1. Station Discovery Context**

- **Aggregate Root**: `PostalCodeAreaAggregate` - manages charging station collections by area
- **Entities**: `ChargingStation` - individual charging infrastructure
- **Value Objects**: `PostalCode`, `GeoLocation` - immutable domain concepts
- **Services**: `ChargingStationService`, `GeoLocationService` - use case orchestration
- **Repositories**: `CSVChargingStationRepository`, `CSVGeoDataRepository` - data persistence

**2. Demand Analysis Context**

- **Aggregate Root**: `DemandAnalysisAggregate` - encapsulates demand calculations and priority
- **Value Objects**: `DemandPriority` - priority level categorization
- **Services**: `DemandAnalysisService` - business logic for demand analysis
- **Domain Events**: `DemandAnalysisCalculatedEvent`, `HighDemandAreaIdentifiedEvent`
- **Repositories**: `InMemoryDemandAnalysisRepository` - demand data storage

**3. Shared Kernel**

- **Entities**: `ChargingStation` - charging infrastructure entity
- **Value Objects**: `PostalCode`, `GeoLocation`, `PowerCapacity` - shared across contexts
- **Domain Events**: `DomainEvent`, `StationSearchPerformedEvent` - event-driven architecture
- **Services**: `PostalCodeResidentService`, `PowerCapacityService`, `GeoLocationService` - shared services
- **Constants**: `InfrastructureThresholds`, `PopulationThresholds`, `PostalCodeThresholds`, `PowerThresholds` - business rules (no magic numbers)
- **Enums**: `ChargingCategory`, `CoverageLevel`, `PopulationDensityCategory`, `CapacityCategory` - type-safe categorizations

#### 🏗️ Architecture Layers

- **Domain Layer**: Business logic in aggregates and value objects, domain events for loose coupling
- **Application Layer**: Service orchestration, use case implementations, DTOs for presentation isolation
- **Infrastructure Layer**: CSV repositories, logging configuration, GeoDataFrame processing, event bus
- **UI Layer**: Streamlit presentation with DDD validation, interactive maps with Folium

#### ✅ Key DDD Features

- **Domain Validation**: PostalCode enforces Berlin-specific rules (10xxx-14xxx, 5 digits)
- **Event-Driven Architecture**: Domain events track searches and high-demand area identification
- **Type Safety**: Enums replace magic strings for better IDE support
- **Immutable Value Objects**: Validation enforced in `__post_init__`
- **Centralized Constants**: Business thresholds in dedicated constant classes

---

## Project Structure

```
EVision-Berlin/
├── main.py                          # Application entry point
├── config.py                        # Configuration management
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata & task configuration
├── README.md                        # This documentation
├── src/
│   ├── demand/                      # Demand Analysis bounded context
│   │   ├── domain/                  # Domain models, aggregates, events
│   │   │   ├── aggregates/          # DemandAnalysisAggregate
│   │   │   ├── value_objects/       # DemandPriority, StationCount, Population
│   │   │   ├── events/              # Domain events
│   │   │   └── enums.py             # Demand-specific enumerations
│   │   ├── application/             # Application services, DTOs
│   │   │   ├── services/            # DemandAnalysisService
│   │   │   ├── dtos/                # Data Transfer Objects
│   │   │   └── event_handlers/      # Event handlers
│   │   └── infrastructure/          # Repositories, event handlers
│   │       └── repositories/        # InMemoryDemandAnalysisRepository
│   ├── discovery/                   # Station Discovery bounded context
│   │   ├── domain/                  # Aggregates, entities, value objects
│   │   │   ├── aggregates/          # PostalCodeAreaAggregate
│   │   │   ├── entities/            # ChargingStation
│   │   │   └── value_objects/       # PostalCode, GeoLocation
│   │   ├── application/             # Services, use cases
│   │   │   └── services/            # ChargingStationService
│   │   └── infrastructure/          # Data access implementations
│   ├── shared/                      # Shared kernel
│   │   ├── domain/                  # Shared value objects, events
│   │   │   ├── aggregates/          # Shared aggregates
│   │   │   ├── entities/            # ChargingStation entity
│   │   │   ├── value_objects/       # PostalCode, GeoLocation, PowerCapacity
│   │   │   ├── events/              # DomainEvent, StationSearchPerformedEvent
│   │   │   ├── constants.py         # InfrastructureThresholds, PopulationThresholds, PostalCodeThresholds, PowerThresholds
│   │   │   ├── enums.py             # ChargingCategory, CoverageLevel, PopulationDensityCategory
│   │   │   ├── exceptions/          # Domain exceptions
│   │   │   └── services/            # Domain services
│   │   ├── application/             # Shared services
│   │   │   └── services/            # PostalCodeResidentService, PowerCapacityService, GeoLocationService
│   │   ├── views/                   # Shared UI components
│   │   │   ├── about_view.py        # About section view
│   │   │   └── components.py        # Reusable UI components
│   │   └── infrastructure/          # Event bus, logging, repositories
│   │       ├── event_bus.py         # InMemoryEventBus
│   │       ├── logging_config.py    # Centralized logging
│   │       ├── repositories/        # CSV repository implementations
│   │       └── datasets/            # Data files
│   │           ├── Ladesaeulenregister.csv  # Charging station data (BNetzA)
│   │           ├── plz_einwohner.csv        # Population data by postal code
│   │           └── geodata_berlin_plz.csv   # Postal code boundary geometries (WKT)
│   └── ui/                          # Presentation layer
│       └── application/             # Streamlit application
│           └── streamlit_app.py     # Main Streamlit app class
├── tests/                           # Test suite (TDD)
│   ├── conftest.py                  # Pytest configuration and shared fixtures
│   ├── demand/                      # Demand context tests
│   ├── discovery/                   # Discovery context tests
│   └── shared/                      # Shared kernel tests
├── docs/                            # Documentation
│   ├── about.py                     # About section for UI
│   └── DATA_QUALITY_ANALYSIS.md     # Data quality report
├── assets/                          # Static resources
│   ├── data_quality_charging_stations.png  # Generated visualizations
│   ├── data_quality_residents.png          # Generated visualizations
│   └── data_quality_combined.png           # Generated visualizations
└── htmlcov/                         # Test coverage reports (generated)
```

---

## Data Sources

### 1. Charging Station Infrastructure (`Ladesaeulenregister.csv`)

- **Source:** Bundesnetzagentur (Federal Network Agency of Germany)
- **URL:** [https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/start.html](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/start.html)
- **File Size:** ~35 MB (CSV format)
- **Total Records:** ~111,000 charging points across Germany
- **Berlin Records:** ~3,000+ charging points

**Key Columns Used:**

- `Postleitzahl`: Postal code (PLZ) - Primary geographic identifier
- `Bundesland`: Federal state (filtered to "Berlin")
- `Breitengrad`: Latitude coordinate (decimal format, comma-separated)
- `Längengrad`: Longitude coordinate (decimal format, comma-separated)
- `Nennleistung Ladeeinrichtung [kW]`: Nominal power output in kilowatts

**Data Quality Notes:**

- Coordinates use German decimal notation (comma as decimal separator)
- Application converts commas to periods for numeric processing
- PLZ range for Berlin: 10115 - 14199
- Some entries may have missing or invalid coordinates (filtered out)

### 2. Population Data (`plz_einwohner.csv`)

- **Source:** German open data portals for postal code statistics
- **Purpose:** Provides resident count per postal code
- **Records:** ~190 postal codes in Berlin

**Key Columns Used:**

- `plz`: Postal code (PLZ)
- `einwohner`: Number of residents
- `lat`: Latitude (optional, for reference)
- `lon`: Longitude (optional, for reference)

**Data Characteristics:**

- Population ranges from ~1,000 to ~40,000 residents per postal code
- Central districts typically have higher density
- Updated periodically from census data

### 3. Geographic Data (`geodata_berlin_plz.csv`)

- **Purpose:** Provides polygon geometries for postal code boundaries
- **Format:** CSV with WKT (Well-Known Text) geometry strings
- **Coordinate System:** WGS84 (EPSG:4326)

**Key Columns:**

- `PLZ`: Postal code identifier
- `geometry`: Polygon boundaries in WKT format

**Usage:**

- Enables choropleth maps (colored regions)
- Defines boundaries for each postal code area
- Allows spatial joins and geographic aggregations

---

## Installation & Setup

### Prerequisites

- **Python:** Version 3.10 or higher
- **pip:** Python package installer
- **Git:** For cloning the repository

### Step 1: Clone the Repository

```bash
git clone git@github.com:DAShaikh10/EVision-Berlin.git EVision-Berlin
cd EVision-Berlin
```

Or download the source code ZIP and extract to a folder named `EVision-Berlin`.

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies from your system Python installation.

**On macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

Your terminal prompt should now show `(.venv)` indicating the virtual environment is active.

### Step 3: Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

**Or using task command:**

```bash
task install
```

**Key Packages Installed:**

| Package            | Version | Purpose                        |
| ------------------ | ------- | ------------------------------ |
| `pandas`           | Latest  | Data manipulation and analysis |
| `geopandas`        | Latest  | Geospatial data processing     |
| `streamlit`        | 1.51+   | Web application framework      |
| `folium`           | Latest  | Interactive maps               |
| `streamlit-folium` | Latest  | Streamlit-Folium integration   |
| `matplotlib`       | Latest  | Statistical visualizations     |
| `seaborn`          | Latest  | Advanced statistical plots     |
| `scipy`            | Latest  | Statistical analysis           |
| `pytest`           | Latest  | Testing framework              |
| `pytest-cov`       | Latest  | Code coverage                  |
| `pylint`           | Latest  | Code quality linting           |
| `black`            | Latest  | Code formatter                 |
| `taskipy`          | Latest  | Task runner                    |

### Step 4: Verify Data Files

Ensure the following files are present in the `src/shared/infrastructure/datasets/` folder:

✅ `Ladesaeulenregister.csv` (charging stations)  
✅ `plz_einwohner.csv` (population data)  
✅ `geodata_berlin_plz.csv` (postal code boundaries)

**If Missing:**

- Download `Ladesaeulenregister.csv` from [Bundesnetzagentur](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/start.html)
- Rename to `Ladesaeulenregister.csv` if the filename includes a date
- Contact the repository maintainers for other data files

---

## Task Commands

The project uses **taskipy** for convenient task automation. All commands are defined in `pyproject.toml`.

### Development Commands

```bash
task install         # Install all project dependencies
task run            # Run the Streamlit application (streamlit run main.py)
task run-clean      # Clean __pycache__ and run application
task clean          # Remove all __pycache__ directories
```

### Testing Commands

```bash
task test           # Run all tests with verbose output
task test-cov       # Run tests with coverage report (HTML + terminal)
```

**Test Coverage Output:**

- HTML report generated in `htmlcov/` directory
- Terminal shows missing lines for quick identification
- Open `htmlcov/index.html` in browser for detailed visualization

### Code Quality Commands

```bash
task format         # Format code with black (auto-fix)
task format-check   # Check code formatting without modifying files
task lint           # Run pylint on main.py, config.py, src/, tests/
```

### Git Workflow Commands

```bash
task pull-main      # Stash changes, pull from main branch, restore changes
task pull-task      # Stash changes, pull from task branch, restore changes
```

**Note:** These commands automatically stash uncommitted changes, pull updates, and restore your work.

---

## How to Run

### Running Locally

1. **Activate Virtual Environment** (if not already active):

   ```bash
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

2. **Run the Streamlit Application:**

   ```bash
   streamlit run main.py
   ```

   **Or using task command:**

   ```bash
   task run
   ```

3. **Access the Application:**
   - The app will automatically open in your default browser
   - Default URL: `http://localhost:8501`
   - If the browser doesn't open, manually navigate to the URL shown in the terminal

4. **Stop the Application:**
   - Press `Ctrl+C` in the terminal
   - Or close the terminal window

### Deploying to Streamlit Cloud

For public deployment:

1. Push your code to a GitHub repository
2. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and branch
6. Set `main.py` as the main file path
7. Click "Deploy"

**Note:** Ensure all data files are included in your repository (check file size limits).

---

## Application Usage

### Main Interface Components

#### 1. Sidebar Controls

**Visualization Mode:**

- **Basic View**: Toggle between Residents layer and All Charging Stations layer
- **Power Capacity (KW) View**: Shows power capacity distribution with capacity range filters (All, Low, Medium, High)

**Postal Code Search:**

- Enter a specific Berlin postal code (10115-14199)
- Instantly zooms to and highlights the selected area
- Displays statistics for that postal code

#### 2. Statistics Dashboard

Located at the top of the main area:

- **Total Charging Stations:** Count of all stations in Berlin
- **Total Population:** Sum of residents across all postal codes
- **Average Stations per PLZ:** Mean distribution
- **Demand Ratio:** Residents per charging station (higher = more demand)

#### 3. Interactive Map

**Layers:**

- **Layer 1 - Population Density:** Colored by resident count
  - Toggle on/off via checkbox
  - Choropleth coloring (lighter to darker = fewer to more residents)
- **Layer 2 - Charging Stations:** Colored by station count
  - Toggle on/off via checkbox
  - Marker clusters for dense areas
  - Individual station markers

**Interactions:**

- **Zoom:** Mouse wheel or +/- buttons
- **Pan:** Click and drag
- **Click Postal Code:** View detailed statistics in popup
- **Click Marker:** View individual station information

#### 4. Demand Priority Table

Below the map:

- **High Demand Areas:** Postal codes with high population but few stations
- **Medium Demand Areas:** Balanced population-to-station ratios
- **Low Demand Areas:** Well-served areas or low population

---

## Results Interpretation

### Layer 1: Population Density per Postal Code

**Color Coding:**

- 🟡 **Yellow/Light:** Low population (< 5,000 residents)
- 🟠 **Orange:** Medium population (5,000 - 15,000 residents)
- 🔴 **Red/Dark:** High population (> 15,000 residents)

**Key Observations:**

1. **Central Districts (Mitte, Prenzlauer Berg, Friedrichshain)**
   - Darkest colors indicate highest density
   - Compact urban living with high apartment concentration
   - Young, urban demographic
   - **Expected Behavior:** High demand for public charging infrastructure

2. **Outer Districts (Pankow, Spandau, Köpenick, Marzahn-Hellersdorf)**
   - Lighter colors indicate lower density
   - More single-family homes with private parking
   - Higher likelihood of home charging installations
   - **Expected Behavior:** Lower demand for public charging

3. **Mixed-Use Areas (Kreuzberg, Neukölln, Charlottenburg)**
   - Medium-to-high population
   - Mix of residential and commercial
   - Diverse demographics
   - **Expected Behavior:** Moderate-to-high demand

**Population Distribution Insights:**

- Berlin's population centers around the inner ring (S-Bahn Ring)
- East-West divide less pronounced than historically
- Postal codes with universities/institutions may show anomalies

### Layer 2: Charging Stations per Postal Code

**Color Coding:**

- 🟡 **Yellow/Light:** Few or no stations (0-5 stations)
- 🟠 **Orange:** Moderate infrastructure (5-15 stations)
- 🔴 **Red/Dark:** Well-served areas (> 15 stations)

**Key Observations:**

1. **Business Districts & Tourist Areas**
   - Well-served despite lower resident populations
   - Examples: Potsdamer Platz, Kurfürstendamm, Alexanderplatz
   - Stations serve commuters, tourists, and commercial vehicles
   - **Insight:** Infrastructure follows economic activity, not just population

2. **Residential High-Density Areas**
   - Uneven distribution observed
   - Some high-population postal codes have minimal infrastructure
   - Historical building constraints limit installations
   - **Insight:** Old building stock creates barriers to charging station deployment

3. **Peripheral Areas**
   - Sparse coverage in outer districts
   - Long distances between stations (potential "charging deserts")
   - May rely on private home charging
   - **Insight:** Lower priority due to home charging availability

**Infrastructure Patterns:**

- Concentration along major roads and highways
- Clustering near shopping centers and parking facilities
- Gap in residential-only neighborhoods

---

## Data Quality Analysis

The project includes comprehensive data quality analysis and outlier detection to ensure the reliability of insights and identify anomalies in the dataset.

### Automated Analysis

When you run `python main.py`, the system automatically:

1. **Analyzes Missing Data** - Identifies incomplete records
2. **Detects Outliers** - Uses IQR (Interquartile Range) method
3. **Generates Visualizations** - Creates 3 PNG files with 16 plots total
4. **Produces Statistical Reports** - Prints detailed summaries to console

### Generated Visualizations

Three comprehensive visualization files are automatically created:

#### 1. `data_quality_charging_stations.png`

Contains 6 plots analyzing charging station data:

- **Power Capacity Distribution**: Histogram showing frequency of different power ratings
- **Outlier Detection**: Box plot identifying stations with unusual power capacities
- **Power Categories**: Bar chart showing distribution across Normal/Fast/Ultra categories
- **Stations per PLZ**: Distribution of infrastructure density
- **Missing Data**: Percentage of incomplete records
- **Top 10 PLZ**: Areas with highest station counts

#### 2. `data_quality_residents.png`

Contains 6 plots analyzing population data:

- **Population Distribution**: Histogram of residents per postal code
- **Population Outliers**: Box plot identifying unusual density areas
- **Population Categories**: Distribution across Very Low/Low/Medium/High/Very High
- **Top 10 PLZ**: Most populated postal codes
- **Missing Data**: Data completeness check
- **Q-Q Plot**: Statistical normality test for population distribution

#### 3. `data_quality_combined.png`

Contains 4 plots analyzing infrastructure-population relationships:

- **Correlation Scatter**: Population vs station count with correlation coefficient
- **Residents per Station**: Distribution of service burden
- **Correlation Heatmap**: Visual representation of variable relationships
- **Underserved Areas**: PLZ with high population but no stations

### Key Findings from Analysis

**Charging Stations:**

- Total: 3,664 stations in Berlin
- Power Range: 6-600 kW
- Outliers: 461 fast and ultra chargers (>77 kW)
- Missing Data: 22% of records lack power rating

**Population:**

- Total: 191 postal codes analyzed
- Range: 139 - 35,353 residents per PLZ
- Outliers: 2 areas (PLZ 12627: very high, PLZ 14053: very low)
- Missing Data: 0% (complete dataset)

**Infrastructure Coverage:**

- Correlation: 0.131 (weak) between population and stations
- Critical Gap: PLZ 10115 (20,313 residents, 0 stations)
- Average: 1,898 residents per station

### Statistical Methods

- **Outlier Detection**: IQR method (values beyond Q1-1.5×IQR or Q3+1.5×IQR)
- **Correlation Analysis**: Pearson correlation coefficient
- **Normality Testing**: Q-Q plots comparing to theoretical distribution

### Detailed Documentation

For complete analysis results, see [`DATA_QUALITY_ANALYSIS.md`](docs/DATA_QUALITY_ANALYSIS.md), which includes:

- Detailed explanations of each visualization
- Statistical summaries and thresholds
- Identified anomalies and their implications
- Recommendations for infrastructure planning

---

## Demand Analysis

### High-Demand Areas (Critical Priority)

**Identification Criteria:**

- **Population:** RED on residents map (> 15,000 residents)
- **Infrastructure:** YELLOW on charging stations map (< 5 stations)
- **Demand Ratio:** > 5,000 residents per charging station
- **Priority:** Immediate action required

**Characteristics of High-Demand Areas:**

- Dense residential neighborhoods
- Limited existing charging infrastructure
- High apartment-to-house ratio (limited private charging)
- Growing EV adoption in the area

**Recommended Actions:**

1. **Install Fast Chargers (50+ kW)**
   - Quick turnaround for multiple users
   - Suitable for residents without home charging

2. **Target Multi-Unit Residential Buildings**
   - Partner with building management
   - Install shared charging infrastructure in parking areas

3. **Deploy Street-Side Charging**
   - Lamppost chargers (on-street parking)
   - Sidewalk-accessible stations
   - Curbside installations

4. **Create Park-and-Charge Facilities**
   - Dedicated parking with charging
   - Overnight charging options
   - Subscription-based models

**Expected Impact:**

- Reduce range anxiety for residents
- Increase EV adoption rates
- Improve air quality in dense areas

### Medium-Demand Areas (High Priority)

**Identification Criteria:**

- **Population:** ORANGE on residents map (5,000-15,000 residents)
- **Infrastructure:** YELLOW-ORANGE on charging stations map (5-15 stations)
- **Demand Ratio:** 2,000-5,000 residents per station
- **Priority:** Near-term expansion

**Characteristics:**

- Moderate population density
- Some existing infrastructure but insufficient
- Mix of residential and commercial areas
- Growing EV market penetration

**Recommended Actions:**

1. **Add Standard Level 2 Chargers (11-22 kW)**
   - Overnight/long-duration charging
   - Cost-effective installation
   - Sufficient for daily charging needs

2. **Expand Existing Station Locations**
   - Add more charge points to existing sites
   - Leverage existing electrical infrastructure
   - Reduce installation costs

3. **Partner with Retail/Parking Facilities**
   - Shopping centers (destination charging)
   - Public parking garages
   - Workplace charging programs

**Expected Impact:**

- Prevent future congestion at charging stations
- Support continued EV adoption growth
- Improve convenience for existing EV owners

### Low-Demand Areas (Future Planning)

**Identification Criteria:**

- **Population:** YELLOW-ORANGE on residents map (< 10,000 residents)
- **Infrastructure:** ORANGE-RED on charging stations map (> 10 stations)
- **Demand Ratio:** < 2,000 residents per station
- **Priority:** Monitoring and long-term planning

**Characteristics:**

- Well-served by existing infrastructure
- Lower population density
- Higher home ownership (private charging available)
- Sufficient current capacity

**Recommended Actions:**

1. **Monitor Usage Patterns**
   - Track utilization rates of existing stations
   - Identify peak usage times
   - Adjust as needed based on data

2. **Track EV Adoption Rates**
   - Watch for increases in EV registrations
   - Survey residents about future EV purchase plans
   - Anticipate future demand

3. **Plan for Long-Term Expansion**
   - Identify potential future installation sites
   - Secure permits and agreements in advance
   - Budget for phased deployment

**Expected Impact:**

- Maintain sufficient capacity as EV adoption grows
- Avoid overbuilding in low-demand areas
- Optimize infrastructure investment

### Specific Demand Indicators

The application calculates and displays:

**Demand Score Calculation:**

```
Demand Score = (Population / Number of Stations) × Density Factor
```

**Categories:**

- **Critical (Red):** Demand score > 10,000
- **High (Orange):** Demand score 5,000-10,000
- **Medium (Yellow):** Demand score 2,000-5,000
- **Low (Green):** Demand score < 2,000

---

## Testing Strategy

### Test-Driven Development (TDD) Approach

EVision Berlin follows **Test-Driven Development** principles:

1. **Write Test First**: Define expected behavior before implementation
2. **Implement Code**: Write minimal code to pass the test
3. **Refactor**: Improve code while maintaining test coverage

### Test Structure

```
tests/
├── conftest.py                     # Pytest configuration and shared fixtures
├── demand/                         # Demand context tests
│   ├── test_aggregates.py          # DemandAnalysisAggregate tests
│   ├── test_services.py            # Service layer tests
│   └── test_value_objects.py       # Value object validation tests
├── discovery/                      # Discovery context tests
│   ├── test_aggregates.py          # PostalCodeAreaAggregate tests
│   ├── test_entities.py            # ChargingStation entity tests
│   └── test_value_objects.py       # PostalCode, GeoLocation tests
└── shared/                         # Shared kernel tests
    ├── test_events.py              # Domain event tests
    ├── test_services.py            # Shared service tests
    └── test_repositories.py        # Repository tests
```

### Running Tests

**Run all tests:**

```bash
task test
# Or: pytest tests/ -v
```

**Run with coverage:**

```bash
task test-cov
# Or: pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
```

**Run specific test file:**

```bash
pytest tests/unit/demand/test_aggregates.py -v
```

**Run specific test function:**

```bash
pytest tests/unit/demand/test_aggregates.py::test_demand_analysis_aggregate_creation -v
```

### Testing Tools

- **pytest**: Primary testing framework with fixtures and parametrization
- **pytest-cov**: Code coverage measurement and reporting
- **unittest.mock**: Mocking external dependencies and isolating units
- **GitHub Actions**: Automated CI/CD testing on every commit

### Coverage Goals

- **Domain Layer**: >90% coverage (critical business logic)
- **Application Layer**: >85% coverage (service orchestration)
- **Infrastructure Layer**: >75% coverage (external dependencies)
- **Overall Project**: >80% coverage

### Quality Assurance

**Automated Checks (GitHub Actions):**

- ✅ **pylint**: Code quality and style enforcement
- ✅ **pytest**: All tests must pass
- ✅ **coverage**: Minimum coverage thresholds

**Pre-commit Hooks:**

- Code formatting with `black`
- Linting with `pylint`
- Test execution before commit

### Test Categories

**1. Unit Tests:**

- Value object validation (PostalCode, GeoLocation)
- Aggregate business logic (DemandAnalysisAggregate)
- Service methods (isolated with mocks)
- Domain event creation and publishing

**2. Integration Tests:**

- Repository data access (CSV reading/writing)
- Event bus message passing
- Cross-context service interactions
- End-to-end use case flows

**3. Domain Validation Tests:**

- PostalCode format validation (Berlin-specific rules)
- GeoLocation coordinate validation
- Business rule enforcement (thresholds, priorities)
- Invariant protection in aggregates

### Example Test Patterns

**Value Object Validation:**

```python
def test_postal_code_invalid_format():
    with pytest.raises(InvalidPostalCodeError):
        PostalCode("12345")  # Not in Berlin range
```

**Aggregate Behavior:**

```python
def test_demand_analysis_calculates_priority():
    aggregate = DemandAnalysisAggregate(
        postal_code=PostalCode("10115"),
        population=Population(20000),
        station_count=StationCount(5)
    )
    assert aggregate.demand_priority == DemandPriority.HIGH
```

**Service Integration:**

```python
def test_demand_analysis_service_integration():
    service = DemandAnalysisService(repo, event_bus)
    result = service.analyze_demand(postal_code)
    assert result.priority == "HIGH"
    assert event_bus.published_events[0].event_type == "DemandAnalysisCalculated"
```

---

## Limitations of Analysis

### 1. Data Limitations

**Not Included in Analysis:**

❌ **Private Charging Stations**

- Home installations (wallboxes in private garages)
- Residential building charging (private access)
- **Impact:** Actual public demand may be overestimated in areas with high home ownership

❌ **Workplace Charging**

- Office building charging facilities
- Corporate fleet charging
- **Impact:** Commuters may charge at work, reducing public demand in residential areas

❌ **Semi-Public Charging**

- Shopping center charging (may be private)
- Hotel/restaurant charging (customer-only)
- **Impact:** These reduce demand but aren't always publicly accessible

❌ **Reserved/Fleet Charging**

- Taxi and ride-sharing fleet stations
- Car-sharing service stations
- Delivery vehicle charging
- **Impact:** Stations exist but aren't available for general public

**Consequence:** True public charging demand may be higher than calculated because we cannot account for private capacity.

### 2. Housing Type Not Considered

**Issue:**

- Single-family homeowners typically install private chargers
- Apartment dwellers rely heavily on public infrastructure
- Analysis treats all residents equally

**Missing Data:**

- Ratio of apartments to single-family homes per postal code
- Percentage of residents with private parking
- Building age (affects installation feasibility)

**Impact on Analysis:**

- Demand may be **underestimated** in apartment-heavy districts
- Demand may be **overestimated** in suburban areas with high home ownership

**Mitigation Strategy:**

- Visual inspection: high-rise areas likely have higher true demand
- Cross-reference with urban planning data
- Consider historical building patterns (inner city = apartments)

### 3. Temporal Factors Not Analyzed

**Missing Considerations:**

📅 **Growth Trends**

- Population increase/decrease over time
- New residential developments
- Urban migration patterns

⚡ **EV Adoption Rates**

- Current EV penetration varies by district
- Accelerating adoption curves
- Government incentive programs

🔄 **Seasonal Variations**

- Tourist influx in summer
- Temporary residents (students)
- Business travel patterns

**Consequence:** Analysis provides a snapshot, not a predictive model.

**Recommendation:**

- Update analysis **annually** or **semi-annually**
- Track charging station installations over time
- Monitor EV registration data by postal code

### 4. Utilization vs. Availability

**Critical Distinction:**

**Availability (This Analysis):**

- Number of charging stations present
- Geographic distribution
- Total capacity

**Utilization (Not Measured):**

- How often stations are used
- Wait times and congestion
- Peak vs. off-peak usage
- Average charging duration

**Reality:**

- **10 stations at 90% utilization** = severe shortage, long wait times
- **5 stations at 20% utilization** = excess capacity, no congestion

**Ideal Enhancement:**

- Integrate **real-time usage data** from charging networks
- Calculate **occupancy rates** and **wait times**
- Identify **congestion hotspots**
- Measure **charging session duration**

**Data Sources for Future Work:**

- Charging network APIs (e.g., Charge Point, Ionity)
- Berlin municipal data on public charging usage
- User surveys and complaint data

### 5. Power Output Distribution

**Current Analysis:**

- Counts stations regardless of power output
- Optional filtering by power category

**Missing Insights:**

- One ultra charger (150+ kW) serves more users per day than multiple normal chargers
- Charging speed affects turnover and capacity
- Mismatch between supply and user needs

**Future Improvement:**

- Weight stations by throughput capacity
- Calculate "effective" station count based on power output
- Recommend optimal mix of normal/fast/ultra chargers per area

### 6. Accessibility and Availability

**Not Addressed:**

- **24/7 Availability:** Some stations have restricted hours
- **Network Membership:** Some require specific RFID cards/apps
- **Pricing Tiers:** Cost variation affects usage patterns
- **Physical Accessibility:** Parking availability, wheelchair access

### 7. Competing Infrastructure

**Not Considered:**

- Proximity to neighboring postal codes with good infrastructure
- Residents may drive short distances to nearby areas
- Edge effects at postal code boundaries

**Impact:** Demand at borders may be shared between adjacent areas.

---

## Technologies Used

### Core Frameworks

| Technology       | Purpose                   | Key Features Used                         |
| ---------------- | ------------------------- | ----------------------------------------- |
| **Python 3.10+** | Programming language      | Type hints, dataclasses, f-strings        |
| **Streamlit**    | Web application framework | Interactive widgets, caching, layout      |
| **Folium**       | Interactive mapping       | Choropleth maps, markers, popups          |
| **Pandas**       | Data manipulation         | DataFrames, groupby, merge                |
| **GeoPandas**    | Geospatial data           | GeoDataFrames, spatial joins, WKT parsing |

### Supporting Libraries

| Library              | Purpose                                  |
| -------------------- | ---------------------------------------- |
| **Branca**           | Color mapping for visualizations         |
| **Streamlit-Folium** | Integration between Streamlit and Folium |
| **Pickle**           | Data serialization and caching           |

## Future Enhancements

### Planned Features

1. **Separate Layers for Each Power Category**
   - Individual map layers for Normal, Fast, and Ultra charging categories
   - Toggle each category independently
   - Analyze power availability distribution

2. **Data Quality Validation**
   - Automated checks for data integrity
   - Column format validation
   - Value range verification
   - Distribution analysis
   - Missing data reporting

3. **Predictive Modeling**
   - Forecast future demand based on trends
   - EV adoption rate projections
   - Population growth modeling

4. **Real-Time Data Integration**
   - Live charging station availability
   - Real-time occupancy rates
   - Wait time estimates

5. **User Feedback System**
   - Report missing stations
   - Suggest new locations
   - Rate existing infrastructure

---

## Acknowledgments

- **Bundesnetzagentur** for providing comprehensive charging station data
- **Berlin Open Data Portal** for geographic and demographic datasets
- **Streamlit Community** for excellent documentation and support
- **Course Instructors** for guidance and project requirements
