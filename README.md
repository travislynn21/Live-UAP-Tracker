# Coinbase Paper Trading Bot - Backend

This folder contains the Python backend for the trading bot. It connects to the Coinbase Advanced API sandbox, executes the trading strategy, and serves data to the frontend dashboard.

## ⚠️ Important: Before You Start - Get Your Sandbox API Keys

This bot trades with **fake money** in the **Coinbase Sandbox environment**. It is completely separate from your real Coinbase account. You need to generate a specific set of API keys from the sandbox.

**Follow these steps carefully:**

### Step 1: Access the Coinbase Developer Portal

1.  Go to the Coinbase Cloud homepage: [https://cloud.coinbase.com/](https://cloud.coinbase.com/)
2.  If you have a Coinbase account, you can sign in directly. If not, you'll need to create a free account.
3.  Once logged in, you will be on the Coinbase Cloud dashboard.

### Step 2: Navigate to the Advanced API Section

1.  In the left-hand navigation menu, click on **Advanced API**.
2.  You will be taken to the API Keys page.

### Step 3: Enable and Access the Sandbox Environment

1.  The live environment is shown by default. **Do not create a key here.**
2.  Look for a toggle or button at the top or side of the page that says **"Go to Sandbox"** or **"Sandbox Settings"**. Click it.
3.  The interface will now switch to the Sandbox mode. This is a simulation environment. You will likely be credited with test funds (e.g., fake BTC, ETH, and USD).

### Step 4: Create a New API Key

1.  In the Sandbox environment, click the **"New API Key"** button.
2.  A window will appear for configuring the API key permissions.
3.  **Permissions are critical.** The bot needs to be able to read market data and execute trades. Grant the following permissions:
    *   `wallet:user:read`
    *   `wallet:accounts:read`
    *   `trade:read`
    *   `trade:write`
    *   You can optionally grant `wallet:buys:create`, `wallet:sells:create` but `trade` permissions are the standard for the Advanced API. Select all trade-related permissions for maximum compatibility.

4.  Give the API key a name, like "PaperTradingBot".
5.  Click **"Create & Download"**.

### Step 5: Securely Copy Your API Key and Secret

1.  After creating the key, Coinbase will show you the **API Key** and the **API Secret**.
2.  **This is the only time the API Secret will ever be displayed.**
3.  Immediately copy both the **API Key** and the **API Secret**.
4.  You will use these in the `config.ini` file for this backend. Do not share them or commit them to git.

You now have the keys you need to run the trading bot.

---

## 🛸 Live Radar Tracker & Physics Engine
This repository also encompasses a state-of-the-art live radar tracking module (`live_flight_tracker.py`) and a zero-dependency mathematical physics engine (`uaps_found.py`) capable of verifying high-G maneuvers, scraping OpenSky API telemetry, and predicting interactive trajectory maps dynamically.

## License & Commercial Terms
This software is strictly provided under a custom license detailed in the `LICENSE` file.

### Commercial Royalties
If this software (or any substantial portion of the tracking engine) is used for **commercial gain**, the user unconditionally agrees to pay **10% of all royalties or gross revenue** generated from its use directly to the original author, **Travis Lynn**.

### Support & Donations
Donations are exceptionally appreciated and directly support further research, development, and server costs! You can send donations via email directly to:
**[travislynn21@protonmail.com](mailto:travislynn21@protonmail.com)**
