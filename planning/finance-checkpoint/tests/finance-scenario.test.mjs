import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import path from "node:path";
import {
  calculateCompoundGrowth,
  calculateMortgagePayment,
  calculateMortgageShock,
  calculateOverpayVsInvest,
  calculateRunwayShock,
} from "../scripts/lib/finance-scenario.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cliPath = path.join(root, "scripts/finance-scenario.mjs");

function runCli(args) {
  const result = spawnSync("node", [cliPath, ...args], {
    encoding: "utf8",
    env: { ...process.env, GIT_CONFIG_GLOBAL: "/dev/null" },
  });
  return {
    status: result.status,
    stdout: result.stdout.trim(),
    stderr: result.stderr.trim(),
    json: () => JSON.parse(result.stdout.trim()),
  };
}

test("calculateMortgagePayment produces exact standard amortization payment", () => {
  const payment = calculateMortgagePayment(300_000, 3.0, 300);
  assert.equal(payment, 1422.63);

  const zeroRate = calculateMortgagePayment(120_000, 0, 120);
  assert.equal(zeroRate, 1000);

  const zeroPrincipal = calculateMortgagePayment(0, 5.0, 300);
  assert.equal(zeroPrincipal, 0);
});

test("calculateMortgageShock computes monthly, annual, and percentage rate shock impacts", () => {
  const shock = calculateMortgageShock({
    balance: 250_000,
    remainingTermMonths: 300,
    currentRatePercent: 2.5,
    newRatePercent: 5.5,
  });

  assert.equal(shock.scenario, "mortgage-shock");
  assert.equal(shock.current_monthly_payment, 1121.54);
  assert.equal(shock.new_monthly_payment, 1535.22);
  assert.equal(shock.monthly_difference, 413.68);
  assert.equal(shock.annual_difference, 4964.16);
  assert.equal(shock.percent_change, 36.88);
});

test("calculateCompoundGrowth computes nominal accumulation, real purchasing power, and sensitivities", () => {
  const growth = calculateCompoundGrowth({
    initialPrincipal: 10_000,
    monthlyContribution: 500,
    years: 10,
    annualReturnPercent: 7.0,
    inflationPercent: 2.5,
  });

  assert.equal(growth.scenario, "compound-growth");
  assert.equal(growth.total_contributed, 70_000);
  assert.equal(growth.future_value_nominal, 106_639.02);
  assert.equal(growth.growth_earned, 36_639.02);
  assert.equal(growth.future_value_real, 83_306.23);
  assert.equal(growth.sensitivities.length, 3);
  assert.equal(growth.sensitivities[0].annual_return_percent, 4);
  assert.equal(growth.sensitivities[2].annual_return_percent, 8);
});

test("calculateOverpayVsInvest compares guaranteed debt interest saved with investment compounding", () => {
  const comparison = calculateOverpayVsInvest({
    debtBalance: 150_000,
    debtRatePercent: 5.0,
    monthlyAmount: 500,
    years: 5,
    investmentReturnPercent: 7.0,
  });

  assert.equal(comparison.scenario, "overpay-vs-invest");
  assert.equal(comparison.total_allocated, 30_000);
  assert.equal(comparison.debt_benefit_total, 34_003.04);
  assert.equal(comparison.debt_interest_saved, 4003.04);
  assert.equal(comparison.investment_future_value, 35_796.45);
  assert.equal(comparison.investment_growth, 5796.45);
  assert.equal(comparison.net_advantage_investing, 1793.41);
  assert.equal(comparison.breakeven_annual_return_percent, 5.0);
});

test("calculateRunwayShock calculates deficit, remaining liquidity, and emergency benchmarks", () => {
  const runway = calculateRunwayShock({
    liquidAssets: 30_000,
    monthlyIncome: 7750,
    incomeReductionPercent: 50,
    monthlyFixedCosts: 2000,
    monthlyDebtService: 2400,
    shockDurationMonths: 6,
  });

  assert.equal(runway.scenario, "runway-shock");
  assert.equal(runway.monthly_essential_spending, 4400);
  assert.equal(runway.post_shock_monthly_income, 3875);
  assert.equal(runway.monthly_deficit, 525);
  assert.equal(runway.total_deficit_during_shock, 3150);
  assert.equal(runway.remaining_liquidity_after_shock, 26_850);
  assert.equal(runway.runway_months_under_shock, 57.1);
  assert.equal(runway.is_solvent_after_shock, true);
  assert.equal(runway.benchmarks.target_3_months, 13_200);
  assert.equal(runway.benchmarks.target_6_months, 26_400);
  assert.equal(runway.benchmarks.coverage_months_zero_income, 6.8);
});

test("finance-scenario CLI runs and outputs structured JSON", () => {
  const cliMortgage = runCli([
    "--type", "mortgage-shock",
    "--balance", "250000",
    "--term-months", "300",
    "--current-rate", "2.5",
    "--new-rate", "5.5",
  ]);
  assert.equal(cliMortgage.status, 0);
  const data = cliMortgage.json();
  assert.equal(data.scenario, "mortgage-shock");
  assert.equal(data.monthly_difference, 413.68);

  const cliJsonMode = runCli([
    "--json",
    JSON.stringify({
      type: "compound-growth",
      principal: 5000,
      monthly: 250,
      years: 5,
      return: 6,
    }),
  ]);
  assert.equal(cliJsonMode.status, 0);
  const growth = cliJsonMode.json();
  assert.equal(growth.scenario, "compound-growth");
  assert.equal(growth.total_contributed, 20_000);

  const invalid = runCli(["--type", "unknown-scenario"]);
  assert.equal(invalid.status, 1);
  assert.match(invalid.stderr, /Unknown scenario type/);
});
