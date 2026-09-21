function toMinor(value) {
  return Math.round(value * 100);
}

function fromMinor(value) {
  return value / 100;
}

export function calculateMortgagePayment(principal, annualRatePercent, termMonths) {
  if (typeof principal !== "number" || principal < 0) {
    throw new TypeError("principal must be a non-negative number");
  }
  if (typeof annualRatePercent !== "number" || annualRatePercent < 0) {
    throw new TypeError("annualRatePercent must be a non-negative number");
  }
  if (typeof termMonths !== "number" || termMonths <= 0 || !Number.isInteger(termMonths)) {
    throw new TypeError("termMonths must be a positive integer");
  }
  if (principal === 0) return 0;
  const monthlyRate = annualRatePercent / 100 / 12;
  if (monthlyRate === 0) {
    return fromMinor(Math.round(toMinor(principal) / termMonths));
  }
  const factor = (1 + monthlyRate) ** termMonths;
  const payment = principal * (monthlyRate * factor) / (factor - 1);
  return fromMinor(Math.round(payment * 100));
}

export function calculateMortgageShock({
  balance,
  remainingTermMonths,
  currentRatePercent,
  newRatePercent,
  currentMonthlyPayment = null,
}) {
  if (typeof balance !== "number" || balance < 0) {
    throw new TypeError("balance must be a non-negative number");
  }
  if (typeof remainingTermMonths !== "number" || remainingTermMonths <= 0) {
    throw new TypeError("remainingTermMonths must be a positive number");
  }
  if (typeof currentRatePercent !== "number" || currentRatePercent < 0) {
    throw new TypeError("currentRatePercent must be a non-negative number");
  }
  if (typeof newRatePercent !== "number" || newRatePercent < 0) {
    throw new TypeError("newRatePercent must be a non-negative number");
  }

  const currentPayment = currentMonthlyPayment !== null
    ? currentMonthlyPayment
    : calculateMortgagePayment(balance, currentRatePercent, remainingTermMonths);
  const newPayment = calculateMortgagePayment(balance, newRatePercent, remainingTermMonths);
  const monthlyDifference = fromMinor(toMinor(newPayment) - toMinor(currentPayment));
  const annualDifference = fromMinor(toMinor(monthlyDifference) * 12);
  const percentChange = currentPayment > 0
    ? Math.round(((newPayment - currentPayment) / currentPayment) * 10_000) / 100
    : 0;

  return {
    scenario: "mortgage-shock",
    balance,
    remaining_term_months: remainingTermMonths,
    current_rate_percent: currentRatePercent,
    new_rate_percent: newRatePercent,
    current_monthly_payment: currentPayment,
    new_monthly_payment: newPayment,
    monthly_difference: monthlyDifference,
    annual_difference: annualDifference,
    percent_change: percentChange,
  };
}

export function calculateCompoundGrowth({
  initialPrincipal = 0,
  monthlyContribution = 0,
  years,
  annualReturnPercent,
  inflationPercent = 2.5,
  returnSensitivities = [4, 6, 8],
}) {
  if (typeof initialPrincipal !== "number" || initialPrincipal < 0) {
    throw new TypeError("initialPrincipal must be a non-negative number");
  }
  if (typeof monthlyContribution !== "number" || monthlyContribution < 0) {
    throw new TypeError("monthlyContribution must be a non-negative number");
  }
  if (typeof years !== "number" || years <= 0) {
    throw new TypeError("years must be a positive number");
  }
  if (typeof annualReturnPercent !== "number") {
    throw new TypeError("annualReturnPercent must be a number");
  }

  const totalMonths = Math.round(years * 12);
  const totalContributed = fromMinor(toMinor(initialPrincipal) + toMinor(monthlyContribution * totalMonths));

  function computeFutureValue(returnRate) {
    const monthlyRate = returnRate / 100 / 12;
    if (monthlyRate === 0) {
      return totalContributed;
    }
    const factor = (1 + monthlyRate) ** totalMonths;
    const fvPrincipal = initialPrincipal * factor;
    const fvContributions = monthlyContribution * ((factor - 1) / monthlyRate);
    return fromMinor(Math.round((fvPrincipal + fvContributions) * 100));
  }

  const futureValueNominal = computeFutureValue(annualReturnPercent);
  const totalGrowth = fromMinor(toMinor(futureValueNominal) - toMinor(totalContributed));
  const discountFactor = (1 + inflationPercent / 100) ** years;
  const futureValueReal = fromMinor(Math.round((futureValueNominal / discountFactor) * 100));

  const sensitivities = returnSensitivities.map((rate) => {
    const fv = computeFutureValue(rate);
    const fvReal = fromMinor(Math.round((fv / discountFactor) * 100));
    return {
      annual_return_percent: rate,
      future_value_nominal: fv,
      growth_earned: fromMinor(toMinor(fv) - toMinor(totalContributed)),
      future_value_real: fvReal,
    };
  });

  return {
    scenario: "compound-growth",
    initial_principal: initialPrincipal,
    monthly_contribution: monthlyContribution,
    years,
    total_contributed: totalContributed,
    annual_return_percent: annualReturnPercent,
    future_value_nominal: futureValueNominal,
    growth_earned: totalGrowth,
    inflation_percent: inflationPercent,
    future_value_real: futureValueReal,
    sensitivities,
  };
}

export function calculateOverpayVsInvest({
  debtBalance,
  debtRatePercent,
  monthlyAmount,
  years,
  investmentReturnPercent = 7.0,
  returnSensitivities = [4, 6, 8],
}) {
  if (typeof debtBalance !== "number" || debtBalance < 0) {
    throw new TypeError("debtBalance must be a non-negative number");
  }
  if (typeof debtRatePercent !== "number" || debtRatePercent < 0) {
    throw new TypeError("debtRatePercent must be a non-negative number");
  }
  if (typeof monthlyAmount !== "number" || monthlyAmount < 0) {
    throw new TypeError("monthlyAmount must be a non-negative number");
  }
  if (typeof years !== "number" || years <= 0) {
    throw new TypeError("years must be a positive number");
  }

  const totalMonths = Math.round(years * 12);
  const totalAllocated = fromMinor(toMinor(monthlyAmount * totalMonths));

  const debtMonthlyRate = debtRatePercent / 100 / 12;
  let debtCompoundValue;
  if (debtMonthlyRate === 0) {
    debtCompoundValue = totalAllocated;
  } else {
    const factor = (1 + debtMonthlyRate) ** totalMonths;
    debtCompoundValue = fromMinor(Math.round((monthlyAmount * ((factor - 1) / debtMonthlyRate)) * 100));
  }
  const interestSaved = fromMinor(toMinor(debtCompoundValue) - toMinor(totalAllocated));

  function computeInvestFv(rate) {
    const monthlyRate = rate / 100 / 12;
    if (monthlyRate === 0) return totalAllocated;
    const factor = (1 + monthlyRate) ** totalMonths;
    return fromMinor(Math.round((monthlyAmount * ((factor - 1) / monthlyRate)) * 100));
  }

  const investmentFv = computeInvestFv(investmentReturnPercent);
  const investmentGrowth = fromMinor(toMinor(investmentFv) - toMinor(totalAllocated));
  const netAdvantageInvesting = fromMinor(toMinor(investmentFv) - toMinor(debtCompoundValue));

  const sensitivities = returnSensitivities.map((rate) => {
    const fv = computeInvestFv(rate);
    const advantage = fromMinor(toMinor(fv) - toMinor(debtCompoundValue));
    return {
      investment_return_percent: rate,
      future_value: fv,
      growth_earned: fromMinor(toMinor(fv) - toMinor(totalAllocated)),
      net_advantage_vs_debt: advantage,
    };
  });

  return {
    scenario: "overpay-vs-invest",
    debt_balance: debtBalance,
    debt_rate_percent: debtRatePercent,
    monthly_amount: monthlyAmount,
    years,
    total_allocated: totalAllocated,
    debt_interest_saved: interestSaved,
    debt_benefit_total: debtCompoundValue,
    investment_return_percent: investmentReturnPercent,
    investment_future_value: investmentFv,
    investment_growth: investmentGrowth,
    net_advantage_investing: netAdvantageInvesting,
    breakeven_annual_return_percent: debtRatePercent,
    sensitivities,
  };
}

export function calculateRunwayShock({
  liquidAssets,
  monthlyIncome,
  incomeReductionPercent,
  monthlyFixedCosts,
  monthlyDebtService,
  shockDurationMonths = 6,
}) {
  if (typeof liquidAssets !== "number" || liquidAssets < 0) {
    throw new TypeError("liquidAssets must be a non-negative number");
  }
  if (typeof monthlyIncome !== "number" || monthlyIncome < 0) {
    throw new TypeError("monthlyIncome must be a non-negative number");
  }
  if (typeof incomeReductionPercent !== "number" || incomeReductionPercent < 0 || incomeReductionPercent > 100) {
    throw new TypeError("incomeReductionPercent must be between 0 and 100");
  }
  if (typeof monthlyFixedCosts !== "number" || monthlyFixedCosts < 0) {
    throw new TypeError("monthlyFixedCosts must be a non-negative number");
  }
  if (typeof monthlyDebtService !== "number" || monthlyDebtService < 0) {
    throw new TypeError("monthlyDebtService must be a non-negative number");
  }

  const monthlyEssentialSpending = fromMinor(toMinor(monthlyFixedCosts) + toMinor(monthlyDebtService));
  const postShockMonthlyIncome = fromMinor(toMinor(monthlyIncome) * (1 - incomeReductionPercent / 100));
  const monthlyNetCashFlow = fromMinor(toMinor(postShockMonthlyIncome) - toMinor(monthlyEssentialSpending));

  let monthlyDeficit = 0;
  let totalDeficit = 0;
  let remainingLiquidity;
  let runwayMonths;

  if (monthlyNetCashFlow < 0) {
    monthlyDeficit = Math.abs(monthlyNetCashFlow);
    totalDeficit = fromMinor(toMinor(monthlyDeficit) * shockDurationMonths);
    remainingLiquidity = fromMinor(toMinor(liquidAssets) - toMinor(totalDeficit));
    runwayMonths = monthlyDeficit > 0 ? Math.round((liquidAssets / monthlyDeficit) * 10) / 10 : Infinity;
  } else {
    remainingLiquidity = fromMinor(toMinor(liquidAssets) + toMinor(monthlyNetCashFlow * shockDurationMonths));
    runwayMonths = Infinity;
  }

  const emergencyFund3Months = fromMinor(toMinor(monthlyEssentialSpending) * 3);
  const emergencyFund6Months = fromMinor(toMinor(monthlyEssentialSpending) * 6);
  const emergencyFund12Months = fromMinor(toMinor(monthlyEssentialSpending) * 12);
  const liquidCoverageMonths = monthlyEssentialSpending > 0
    ? Math.round((liquidAssets / monthlyEssentialSpending) * 10) / 10
    : 0;

  return {
    scenario: "runway-shock",
    liquid_assets: liquidAssets,
    monthly_income: monthlyIncome,
    income_reduction_percent: incomeReductionPercent,
    post_shock_monthly_income: postShockMonthlyIncome,
    monthly_fixed_costs: monthlyFixedCosts,
    monthly_debt_service: monthlyDebtService,
    monthly_essential_spending: monthlyEssentialSpending,
    monthly_net_cash_flow: monthlyNetCashFlow,
    monthly_deficit: monthlyDeficit,
    shock_duration_months: shockDurationMonths,
    total_deficit_during_shock: totalDeficit,
    remaining_liquidity_after_shock: remainingLiquidity,
    runway_months_under_shock: runwayMonths,
    is_solvent_after_shock: remainingLiquidity >= 0,
    benchmarks: {
      essential_monthly: monthlyEssentialSpending,
      coverage_months_zero_income: liquidCoverageMonths,
      target_3_months: emergencyFund3Months,
      target_6_months: emergencyFund6Months,
      target_12_months: emergencyFund12Months,
    },
  };
}
