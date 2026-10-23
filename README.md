<img src="assets/hero.svg" width="100%" alt="Jerry Inyang. Quant researcher. I test whether trading edges are real, and keep the record when they aren't.">

## Now

- Running **arb**, a Go daemon that watches Polymarket and Kalshi for the same event priced two ways.
- Measuring whether BTC and ETH options pay a volatility premium once costs are counted.
- Building **minerva** in Rust, to throw out backtests that a search on noise could have produced.

## The lab

Most of the current work lives in private repos. Public ones are linked.

<p>
<img src="assets/cards/edgehog.svg" width="49%" alt="edgehog: My research workspace. Every idea goes in with a hypothesis and comes out with a verdict, after an agent council audits the design. Status: Active.">
<img src="assets/cards/minerva.svg" width="49%" alt="minerva: Rust detector for backtest overfitting. 0 seals across 14,891 real-data candidates that a search on noise could also have found. Status: Active.">
</p>

<p>
<img src="assets/cards/arb.svg" width="49%" alt="arb: Go daemon hunting cross-venue arbitrage between Polymarket and Kalshi, with recorders and Telegram control. Status: Active.">
<img src="assets/cards/optionr.svg" width="49%" alt="optionr: Direction-agnostic BTC and ETH options research on Deribit: volatility premium, straddle P&amp;L, carry against funding. Status: Researching.">
</p>

<p>
<a href="https://github.com/jerryinyang/fundr"><img src="assets/cards/fundr.svg" width="49%" alt="fundr: Can hourly perp funding be traded between Hyperliquid and Lighter? ~33 bp of costs against 1–10 bp of carry said no. Status: Concluded: no edge."></a>
<a href="https://github.com/jerryinyang/rustybt"><img src="assets/cards/rustybt.svg" width="49%" alt="rustybt: Backtesting engine on Zipline-Reloaded with Decimal precision, Polars data and live trading. On PyPI. Status: Shipped."></a>
</p>

<p>
<img src="assets/cards/todd.svg" width="49%" alt="todd: Deterministic 2D animation renderer. The same code in gives the same frames out, every time. Status: Building.">
<a href="https://www.tradingview.com/u/Professeur_X/"><img src="assets/cards/pine-script.svg" width="49%" alt="Pine Script: Indicators and strategies published as Professeur_X on TradingView, plus an open Pine Script codebase. Status: Published."></a>
</p>

## How I work

- **Costs before models.** fundr ended before a single model was fitted: measured round-turn costs of ~33 bp swamped 1&ndash;10 bp of carry.
- **Beat the noise.** A backtest counts only if it beats what the same search finds on shuffled data.
- **Keep the record.** Dead ideas get written up with what was tested, so they stay dead.

## Instruments

<img src="assets/instruments.svg" width="100%" alt="Research: Python, Polars, pandas, NumPy, SciPy, NautilusTrader, Jupyter, uv. Systems: Rust, Go, TypeScript, C#, Postgres, Docker, Linux servers on Hetzner and AWS. Venues: Polymarket, Kalshi, Deribit, Hyperliquid, Lighter, MetaTrader, cTrader, TradingView. Methods: cost and slippage models, deflated Sharpe and search-luck tests, volatility forecasting, event-based bars, live market recorders. Agents: Claude Code skills, multi-agent design audits, rubric-graded review.">

<br>

<img src="assets/footer.svg" width="100%" alt="Off the clock: pickup basketball, chasing Kyrie's handle, and teaching code to animate.">

Find me on [TradingView](https://www.tradingview.com/u/Professeur_X/), [X](https://x.com/thejerryinyang), [LinkedIn](https://www.linkedin.com/in/jerry-inyang-047870180/) and [Instagram](https://instagram.com/thejerryinyang), or write to [notjerry@altmail.kr](mailto:notjerry@altmail.kr).
