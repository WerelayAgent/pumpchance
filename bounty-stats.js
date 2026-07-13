/* ============================================================
   $pumpchance — live bounty stats (shared)
   Sourced from the coin's pump.fun bounties (via our Worker proxy,
   which is CORS-safe + cached). pump.fun is the source of truth:
     - poolUsd  = sum of ACTIVE bounty rewards  → "up for grabs"
     - paidUsd  = sum of PAID/RESOLVED bounties  → "paid out"
   (Bounty funds are escrowed in pump vaults, not the dev wallet, so
    the wallet balance is NOT a correct source for these numbers.)

   window.PumpchanceBounty.fetchStats() → { poolUsd, poolCount, paidUsd, paidCount }
   ============================================================ */
window.PumpchanceBounty = (function () {
  const CONFIG = {
    bountyEndpoint: "https://pumpchance-bounty.f4mqj9vdb7.workers.dev/bounties",
    pumpUrl: "https://pump.fun/coin/JCKwsT8UAbygnFkZ7u3amDUM7BXRtwUhCsHQv2khpump",
  };

  let _last = { poolUsd: 0, poolCount: 0, paidUsd: 0, paidCount: 0, submissions: 0, links: [] };

  async function fetchStats() {
    try {
      const r = await fetch(CONFIG.bountyEndpoint, { cache: "no-store" });
      const d = await r.json();
      if (!d || !d.ok) throw new Error("bounties unavailable");
      _last = {
        poolUsd: Number(d.totalUsd) || 0,
        poolCount: Number(d.activeCount) || 0,
        paidUsd: Number(d.paidUsd) || 0,
        paidCount: Number(d.paidCount) || 0,
        submissions: Number(d.submissions) || 0,
        links: Array.isArray(d.links) ? d.links : [],
      };
      return _last;
    } catch (_) {
      return _last; // keep last good values; never blank the UI
    }
  }

  function fmtUSD(n) { return "$" + (Math.max(0, n) || 0).toLocaleString("en-US", { maximumFractionDigits: 0 }); }
  function animateTo(el, target, fmt) {
    fmt = fmt || fmtUSD;
    const start = el._val || 0, t0 = performance.now(), dur = 900;
    (function step(t) {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(start + (target - start) * e);
      if (k < 1) requestAnimationFrame(step); else el._val = target;
    })(t0);
  }

  return { fetchStats, fmtUSD, animateTo, CONFIG };
})();
