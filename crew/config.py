import os

topic = "oil and gas market latest news, oil and gas stock prices, oil and gas supply and demand, and oil and gas production rates"

entities = [
    "OPEC", "Oil Companies", "ADNOC", "Aramco", "SNPC", "Sonatrach",
    "GEPetrol", "Gabon Oil", "National Iranian Oil Company",
    "Iraq Petroleum", "Kuwait Oil Company", "PDVSA", "IEA", "APEC",
    "Sinopec", "PetroChina", "GazProm", "QatarEnergy", "CNOOC",
    "ExxonMobil", "Shell", "Marathon Petroleum", "Valero Energy",
    "ConocoPhillips", "Canadian Natural Resources",
    "TotalEnergies", "British Petroleum", "BP",  "Chevron",
    "Equinor", "Eni", "Petrobras"
]

relevant_keywords = [
    "OPEC", "Oil Companies", "ADNOC", "Aramco", "SNPC", "Sonatrach",
    "GEPetrol", "Gabon Oil", "National Iranian Oil Company",
    "Iraq Petroleum", "Kuwait Oil Company", "PDVSA", "IEA", "APEC",
    "Sinopec", "PetroChina", "GazProm", "QatarEnergy", "CNOOC",
    "ExxonMobil", "Shell", "Marathon Petroleum", "Valero Energy",
    "ConocoPhillips", "Canadian Natural Resources", "TotalEnergies",
    "British Petroleum", "BP", "Chevron", "Equinor", "Eni", "Petrobras",
    "oil prices", "gas prices", "oil stock market", "oil company",
    "oil supply", "oil demand", "oil production", "gas production",
    "energy market", "oil trading", "gas trading", "crude oil",
    "natural gas", "commodity prices", "oil futures", "gas futures",
    "oilfield services", "petroleum", "LNG", "oil reserves", "shale oil",
    "oil exports", "oil imports", "oil consumption", "oil inventory",
    "Light Distillate", "Naphtha", "LPG", "Biofuels", "Middle Distillate",
    "Jet Fuel", "Gas Oil", "Condensate", "Fuel Oil and Bunker", "Brent",
    "WTI", "RBOB", "RBOB Gas", "EBOB", "CBOB", "Singapore gasoline R92",
    "Europe Gasoil", "Gasoil", "Marine gasoil", "Far east index",
    "Mt Belvieu Propane", "Mont Belvieu Propane", "Mt Belvieu Butane",
    "Mont Belvieu Butane", "Normal Butane", "ULSD New York", "Far east index propane",
    "Far east index butane", "gasoil", "europe gasoil", "asia gasoil",
    "marine gasoil", "AFEI", "Natural Gasoline", "energy trading",
    "market integration", "supply chain optimization", "hedging strategies",
    "risk management", "derivatives trading", "financial instruments",
    "market analysis", "price volatility", "global supply chains",
    "trade compliance", "regulatory frameworks", "futures contracts",
    "spot markets", "forward contracts", "trade finance", "commodity exchanges",
    "strategic partnerships", "joint ventures", "market expansion",
    "value chain"
]

general_keywords = [
    "propane", "butane", "Diesel", "Gasoline", "downstream", "upstream",
    "midstream", "exploration", "refining", "pipelines", "drilling",
    "trade", "market", "trend", "forecast", "logistics", "storage",
    "distribution", "shipping", "transportation", "energy sector",
    "sustainability", "carbon footprint", "renewable energy",
    "technological innovation", "digital transformation", "market dynamics",
    "industry trends", "investment strategies", "economic impact"
]

specific_keywords = [
    "OPEC", "Oil Companies", "ADNOC", "Aramco", "SNPC", "Sonatrach",
    "GEPetrol", "Gabon Oil", "National Iranian Oil Company",
    "Iraq Petroleum", "Kuwait Oil Company", "PDVSA", "IEA", "APEC",
    "Sinopec", "PetroChina", "GazProm", "QatarEnergy", "CNOOC",
    "ExxonMobil", "Shell", "Marathon Petroleum", "Valero Energy",
    "ConocoPhillips", "Canadian Natural Resources", "TotalEnergies",
    "British Petroleum", "BP", "Chevron", "Equinor", "Eni", "Petrobras",
    "oil prices", "gas prices", "oil stock market", "oil company",
    "oil supply", "oil demand", "oil production", "gas production",
    "energy market", "oil trading", "gas trading", "crude oil",
    "natural gas", "commodity prices", "oil futures", "gas futures",
    "oilfield services", "petroleum", "LNG", "oil reserves", "shale oil",
    "oil exports", "oil imports", "oil consumption", "oil inventory",
    "Light Distillate", "Naphtha", "LPG", "Biofuels", "Middle Distillate",
    "Jet Fuel", "Gas Oil", "Condensate", "Fuel Oil and Bunker", "Brent",
    "WTI", "RBOB", "RBOB Gas", "EBOB", "CBOB", "Singapore gasoline R92",
    "Europe Gasoil", "Gasoil", "Marine gasoil", "Far east index",
    "Mt Belvieu Propane", "Mont Belvieu Propane", "Mt Belvieu Butane",
    "Mont Belvieu Butane", "Normal Butane", "ULSD New York", "Far east index propane",
    "Far east index butane", "gasoil", "europe gasoil", "asia gasoil",
    "marine gasoil", "AFEI", "Natural Gasoline", "energy trading",
    "market integration", "supply chain optimization", "hedging strategies",
    "risk management", "derivatives trading", "financial instruments",
    "market analysis", "price volatility", "global supply chains",
    "trade compliance", "regulatory frameworks", "futures contracts",
    "spot markets", "forward contracts", "trade finance", "commodity exchanges",
    "strategic partnerships", "joint ventures", "market expansion",
    "value chain""propane", "butane", "Diesel", "Gasoline", "downstream", "upstream",
    "midstream", "exploration", "refining", "pipelines", "drilling",
    "trade", "market", "trend", "forecast", "logistics", "storage",
    "distribution", "shipping", "transportation", "energy sector",
    "sustainability", "carbon footprint", "renewable energy",
    "technological innovation", "digital transformation", "market dynamics",
    "industry trends", "investment strategies", "economic impact"
]

categories = {
    "Market Trends": ["market", "trend", "forecast"],
    "Production Updates": ["production", "output", "supply", "production rates"],
    "Company News": ["company", "merger", "acquisition", "oil company", "OPEC", "Oil Companies",
                     "ADNOC", "Aramco", "SNPC", "Sonatrach", "GEPetrol", "Gabon Oil", "National Iranian Oil Company",
                     "Iraq Petroleum", "Kuwait Oil Company", "PDVSA", "IEA", "APEC", "Sinopec", "PetroChina", "GazProm",
                     "QatarEnergy", "CNOOC", "ExxonMobil", "Shell", "Marathon Petroleum", "Valero Energy",
                     "ConocoPhillips", "Canadian Natural Resources", "TotalEnergies", "British Petroleum (or BP)",
                     "Chevron", "Equinor", "Eni", "Petrobras"],
    "Stock Prices": ["stock prices", "oil stock market", "commodity prices", "oil futures", "gas futures"],
    "Supply and Demand": ["supply", "demand", "oil supply", "oil demand", "gas supply", "gas demand"],
    "Exploration": ["exploration", "drilling", "shale oil", "offshore drilling"],
    "Refining": ["refining", "oil refining capacity", "oil production cuts", "oil inventory"],
    "Commodities": ["Light Distillate", "Naphtha", "Gasoline", "LPG", " Biofuels", "Middle Distillate",
                    "Jet Fuel", "Gas Oil", " Diesel", "Condensate", "Fuel Oil and Bunker", "Brent", "WTI",
                    "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "gasoline R92" "Europe Gasoil", "Gasoil",
                    "Marine gasoil", "Far east index", "propane", "butane", "Mt Belv Propane", "Mt Belv Butane",
                    "ULSD New york", "UlSD", "Far east index propane", "Far east index butane", "gasoil",
                    "europe gasoil", "asia gasoil", "marine gasoil"],
    "Trade and Export": ["trading", "export", "import", "oil exports", "oil imports",]
}

commodity_list = ["Brent", "WTI", "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "Europe Gasoil",
                  "Marine gasoil 0.5% Singapore", "Far east index propane", "Far east index butane",
                  "Mt Belv Propane", "Mt Belv Butane", "ULSD New york", "asia gasoil", "marine gasoil",
                  "Gold", "Silver"]

# -----------------------------------------------------------------------------

def user_input_keywords():
    # Read the selected keywords from the file in user_data directory
    keywords_file = os.path.join(os.getcwd(), 'Frontend', 'data', 'user_input', 'selected_keywords.txt')
    
    if os.path.exists(keywords_file):
        with open(keywords_file, 'r') as f:
            selected_keywords = f.read().splitlines()
            print(f"Selected keywords: {selected_keywords}")
            return selected_keywords
    else:
        selected_keywords = ["no keywords found"]  # Default value if the file doesn't exist
        return 1


def user_input_commodities():
    # Read the selected words from the file
    commodities_file = os.path.join(os.getcwd(), 'Frontend', 'data', 'user_input', 'selected_commodities.txt')

    if os.path.exists(commodities_file):
        with open(commodities_file, 'r') as f:
            selected_commodities = f.read().splitlines()
            print(f"Selected words: {selected_commodities}")
            return selected_commodities
    else:
        selected_commodities = ["no commodities found"]  # Default value if the file doesn't exist
        return 1
