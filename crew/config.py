topic = "oil and gas market latest news, oil and gas stock prices, oil and gas supply and demand, and oil and gas production rates"

relevant_keywords = [
    "oil prices", "gas prices", "oil stock market", "oil company",
    "oil supply", "oil demand", "oil production", "gas production",
    "energy market", "oil trading", "gas trading", "crude oil",
    "natural gas", "commodity prices", "oil futures", "gas futures",
    "exploration", "refining", "pipelines", "oilfield services",
    "petroleum", "downstream", "upstream", "midstream", "LNG",
    "oil reserves", "drilling", "shale oil",
    "oil exports", "oil imports", "OPEC",
    "oil consumption", "oil inventory",
    "Light Distillate", "Naphtha", "Gasoline", "LPG", "Biofuels",
    "Middle Distillate", "Jet Fuel", "Gas Oil", "Diesel", "Condensate",
    "Fuel Oil and Bunker"
]

categories = {
    "Market Trends": ["market", "trend", "forecast"],
    "Production Updates": ["production", "output", "supply", "production rates"],
    "Company News": ["company", "merger", "acquisition", "oil company"],
    "Stock Prices": ["stock prices", "oil stock market", "commodity prices", "oil futures", "gas futures"],
    "Supply and Demand": ["supply", "demand", "oil supply", "oil demand", "gas supply", "gas demand"],
    "Exploration": ["exploration", "drilling", "shale oil", "offshore drilling"],
    "Refining": ["refining", "oil refining capacity", "oil production cuts", "oil inventory"],
    "Commodities": ["Light Distillate", "Naphtha", "Gasoline", "LPG", " Biofuels", "Middle Distillate",
                    "Jet Fuel", "Gas Oil", " Diesel", "Condensate", "Fuel Oil and Bunker", "Brent", "WTI",
                    "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "Europe Gasoil", "Gasoil", "Marine gasoil",
                    "Far east index", "propane", "butane", "Mt Belv Propane", "Mt Belv Butane", "ULSD New york",
                    "UlSD"],
    "Trade and Export": ["trading", "export", "import", "oil exports", "oil imports",]
}

# ------------------------------------------------------------------------------
# Load API keys and initialize tools

# tavily_api_key = os.getenv("TAVILY_API_KEY")
# serper_api_key = os.getenv("SERPER_API_KEY")

# tavily_tool = TavilyAPI(api_key=tavily_api_key)
# serper_tool = SerperDevTool()