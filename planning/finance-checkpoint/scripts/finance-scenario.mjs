#!/usr/bin/env node
import fs from "node:fs";
import { fail, loadJson, parseArgs, printJson, requireArg } from "./lib/cli.mjs";
import {
  calculateCompoundGrowth,
  calculateMortgageShock,
  calculateOverpayVsInvest,
  calculateRunwayShock,
} from "./lib/finance-scenario.mjs";

try {
  const valueOptions = [
    "type",
    "json",
    "input",
    "debt-balance",
    "debt-rate",
    "monthly",
    "years",
    "investment-return",
    "principal",
    "return",
    "inflation",
    "liquid-assets",
    "monthly-income",
    "income-reduction",
    "fixed-costs",
    "debt-service",
    "duration",
    "balance",
    "term-months",
    "current-rate",
    "new-rate",
    "current-payment",
  ];

  const args = parseArgs(process.argv.slice(2), valueOptions);

  let payload = {};
  if (args.input) {
    payload = loadJson(args.input);
  } else if (args.json) {
    payload = JSON.parse(args.json);
  }

  const scenarioType = payload.type ?? args.type;
  if (!scenarioType) {
    throw new Error("Missing scenario type. Specify --type, --json, or --input");
  }

  function num(argVal, payloadVal, defaultVal = undefined) {
    if (payloadVal !== undefined) return Number(payloadVal);
    if (argVal !== undefined) return Number(argVal);
    if (defaultVal !== undefined) return defaultVal;
    return undefined;
  }

  let result;
  switch (scenarioType) {
    case "mortgage-shock": {
      const balance = num(args.balance, payload.balance);
      const remainingTermMonths = num(args["term-months"], payload.term_months ?? payload.remaining_term_months);
      const currentRatePercent = num(args["current-rate"], payload.current_rate ?? payload.current_rate_percent);
      const newRatePercent = num(args["new-rate"], payload.new_rate ?? payload.new_rate_percent);
      const currentMonthlyPayment = num(args["current-payment"], payload.current_monthly_payment, null);

      if (balance === undefined || remainingTermMonths === undefined || currentRatePercent === undefined || newRatePercent === undefined) {
        throw new Error("mortgage-shock requires balance, term-months, current-rate, and new-rate");
      }

      result = calculateMortgageShock({
        balance,
        remainingTermMonths,
        currentRatePercent,
        newRatePercent,
        currentMonthlyPayment,
      });
      break;
    }

    case "compound-growth": {
      const initialPrincipal = num(args.principal, payload.principal ?? payload.initial_principal, 0);
      const monthlyContribution = num(args.monthly, payload.monthly ?? payload.monthly_contribution, 0);
      const years = num(args.years, payload.years);
      const annualReturnPercent = num(args.return, payload.return ?? payload.annual_return_percent);
      const inflationPercent = num(args.inflation, payload.inflation ?? payload.inflation_percent, 2.5);

      if (years === undefined || annualReturnPercent === undefined) {
        throw new Error("compound-growth requires years and return");
      }

      result = calculateCompoundGrowth({
        initialPrincipal,
        monthlyContribution,
        years,
        annualReturnPercent,
        inflationPercent,
      });
      break;
    }

    case "overpay-vs-invest": {
      const debtBalance = num(args["debt-balance"], payload.debt_balance);
      const debtRatePercent = num(args["debt-rate"], payload.debt_rate ?? payload.debt_rate_percent);
      const monthlyAmount = num(args.monthly, payload.monthly ?? payload.monthly_amount);
      const years = num(args.years, payload.years);
      const investmentReturnPercent = num(args["investment-return"], payload.investment_return ?? payload.investment_return_percent, 7.0);

      if (debtBalance === undefined || debtRatePercent === undefined || monthlyAmount === undefined || years === undefined) {
        throw new Error("overpay-vs-invest requires debt-balance, debt-rate, monthly, and years");
      }

      result = calculateOverpayVsInvest({
        debtBalance,
        debtRatePercent,
        monthlyAmount,
        years,
        investmentReturnPercent,
      });
      break;
    }

    case "runway-shock": {
      const liquidAssets = num(args["liquid-assets"], payload.liquid_assets);
      const monthlyIncome = num(args["monthly-income"], payload.monthly_income);
      const incomeReductionPercent = num(args["income-reduction"], payload.income_reduction ?? payload.income_reduction_percent);
      const monthlyFixedCosts = num(args["fixed-costs"], payload.fixed_costs ?? payload.monthly_fixed_costs);
      const monthlyDebtService = num(args["debt-service"], payload.debt_service ?? payload.monthly_debt_service);
      const shockDurationMonths = num(args.duration, payload.duration ?? payload.shock_duration_months, 6);

      if (liquidAssets === undefined || monthlyIncome === undefined || incomeReductionPercent === undefined || monthlyFixedCosts === undefined || monthlyDebtService === undefined) {
        throw new Error("runway-shock requires liquid-assets, monthly-income, income-reduction, fixed-costs, and debt-service");
      }

      result = calculateRunwayShock({
        liquidAssets,
        monthlyIncome,
        incomeReductionPercent,
        monthlyFixedCosts,
        monthlyDebtService,
        shockDurationMonths,
      });
      break;
    }

    default:
      throw new Error(`Unknown scenario type: ${scenarioType}. This helper provides calculation primitives for: mortgage-shock, compound-growth, overpay-vs-invest, runway-shock. For custom or multi-variable scenarios, work through the calculations directly in Financial Scenarios.md.`);
  }

  printJson(result);
} catch (error) {
  fail(error);
}
