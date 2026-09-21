const QUALITY_VALUES = new Set(["confirmed", "estimated", "stale", "unknown"]);
const COLLECTIONS = ["income", "assets", "liabilities", "recurring_flows"];
const MONEY_FIELDS = {
  income: "monthly_net",
  assets: "value",
  liabilities: "balance",
  recurring_flows: "amount_monthly",
};
const CATEGORY_VALUES = {
  assets: new Set(["cash", "investment", "pension", "property", "vehicle", "material-asset"]),
  liabilities: new Set(["mortgage", "loan", "credit-card", "student-loan", "other"]),
};

function parseScalar(raw) {
  const value = raw.trim();
  if (value === "[]") return [];
  if (value === "null" || value === "~") return null;
  if (value === "true") return true;
  if (value === "false") return false;
  if (/^-?\d+(?:\.\d+)?$/.test(value)) return Number(value);
  if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }
  return value;
}

function parseFrontmatter(markdown) {
  const match = markdown.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) throw new Error("Finance document must start with one YAML frontmatter block");
  const result = {};
  let listKey = null;
  for (const rawLine of match[1].split(/\r?\n/)) {
    if (!rawLine.trim() || rawLine.trimStart().startsWith("#")) continue;
    const listMatch = rawLine.match(/^\s+-\s+(.+)$/);
    if (listMatch && listKey) {
      result[listKey].push(parseScalar(listMatch[1]));
      continue;
    }
    const propertyMatch = rawLine.match(/^([A-Za-z0-9_-]+):(?:\s*(.*))?$/);
    if (!propertyMatch) throw new Error(`Unsupported frontmatter line: ${rawLine}`);
    const [, key, rawValue = ""] = propertyMatch;
    if (rawValue === "") {
      result[key] = [];
      listKey = key;
    } else {
      result[key] = parseScalar(rawValue);
      listKey = null;
    }
  }
  return { frontmatter: result, frontmatterText: match[0] };
}

export function parseDocumentFrontmatter(markdown) {
  return parseFrontmatter(markdown).frontmatter;
}

export function parseFinanceDocument(markdown) {
  if (typeof markdown !== "string") throw new TypeError("Finance document must be Markdown text");
  const { frontmatter, frontmatterText } = parseFrontmatter(markdown);
  const matches = [...markdown.matchAll(/```finance-data\s*\r?\n([\s\S]*?)\r?\n```/g)];
  if (matches.length !== 1) {
    throw new Error(`Finance document must contain exactly one finance-data block; found ${matches.length}`);
  }
  let data;
  try {
    data = JSON.parse(matches[0][1]);
  } catch (error) {
    throw new Error(`Invalid JSON in finance-data block: ${error.message}`);
  }
  return { frontmatter, data, body: markdown.slice(frontmatterText.length) };
}

function isDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(parsed.valueOf()) && parsed.toISOString().slice(0, 10) === value;
}

function ageInDays(older, newer) {
  return Math.floor((Date.parse(`${newer}T00:00:00Z`) - Date.parse(`${older}T00:00:00Z`)) / 86_400_000);
}

function issue(code, message, record, severity = "blocking") {
  return { code, message, item_id: record?.id ?? null, severity };
}

function matchingFreshnessRule(freshness, collection, category) {
  if (!freshness?.rules) return null;
  return freshness.rules.find((rule) => rule.collection === collection && rule.category === category)
    ?? freshness.rules.find((rule) => rule.collection === collection && rule.category === "*")
    ?? null;
}

function addIssue(result, entry, blocking = true) {
  result[blocking ? "blocking" : "warnings"].push({
    ...entry,
    severity: blocking ? "blocking" : "warning",
  });
}

function validateRecord(record, collection, snapshot, freshness, result, ids) {
  const label = record?.id || record?.label || `${collection} item`;
  if (!record || typeof record !== "object" || Array.isArray(record)) {
    addIssue(result, issue("invalid_record", `${collection} contains a non-object record`, null));
    return;
  }
  if (typeof record.id !== "string" || !/^[a-z0-9][a-z0-9-]*$/.test(record.id)) {
    addIssue(result, issue("invalid_id", `${label} has an invalid id`, record));
  } else if (ids.has(record.id)) {
    addIssue(result, issue("duplicate_id", `${record.id} is used more than once`, record));
  } else {
    ids.add(record.id);
  }
  if (typeof record.label !== "string" || !record.label.trim()) {
    addIssue(result, issue("label_missing", `${label} must have a label`, record));
  }
  if (!QUALITY_VALUES.has(record.quality)) {
    addIssue(result, issue("invalid_quality", `${label} quality must be confirmed, estimated, stale, or unknown`, record));
    return;
  }
  if (CATEGORY_VALUES[collection] && !CATEGORY_VALUES[collection].has(record.category)) {
    addIssue(result, issue("invalid_category", `${label} has an invalid ${collection} category`, record));
  }
  if (typeof record.source !== "string" || !record.source.trim()) {
    addIssue(result, issue("source_missing", `${label} must name its source`, record));
  }

  const required = record.required_for_sealing !== false;
  const moneyField = MONEY_FIELDS[collection];
  const value = record[moneyField];
  if (record.quality === "unknown") {
    if (value !== null) addIssue(result, issue("unknown_has_value", `${label} is unknown and must not contain a substituted value`, record));
    addIssue(result, issue("unknown_value", `${label} is unknown and prevents sealing`, record), required);
    return;
  }
  if (typeof value !== "number" || !Number.isFinite(value) || value < 0) {
    addIssue(result, issue("invalid_value", `${label}.${moneyField} must be a non-negative finite number`, record));
  }
  if (!isDate(record.value_date)) {
    addIssue(result, issue("value_date_missing", `${label} must have a valid value_date`, record));
  } else if (record.value_date > snapshot.as_of) {
    addIssue(result, issue("future_value_date", `${label} value_date is after the checkpoint date`, record));
  }

  const rule = matchingFreshnessRule(freshness, collection, record.category ?? "*");
  if (record.quality === "stale") {
    addIssue(result, issue("stale_value", `${label} is explicitly stale and prevents sealing`, record), required && (rule?.blocking ?? true));
  } else if (rule && isDate(record.value_date) && isDate(snapshot.as_of)) {
    const age = ageInDays(record.value_date, snapshot.as_of);
    if (age > rule.max_age_days) {
      addIssue(
        result,
        issue("freshness_exceeded", `${label} is ${age} days old; maximum is ${rule.max_age_days}`, record, rule.blocking ? "blocking" : "warning"),
        Boolean(rule.blocking),
      );
    }
  }

  if (record.quality === "estimated") {
    if (typeof record.method !== "string" || !record.method.trim()) {
      addIssue(result, issue("estimate_method_missing", `${label} must describe its estimation method`, record));
    }
    if (collection === "assets") {
      if (!isDate(record.valuation_date)) {
        addIssue(result, issue("valuation_date_missing", `${label} must have a valuation_date`, record));
      }
      if (typeof record.valuation_method !== "string" || !record.valuation_method.trim()) {
        addIssue(result, issue("valuation_method_missing", `${label} must have a valuation_method`, record));
      }
      if (record.uncertainty_material) {
        const rangeValid = Number.isFinite(record.range_low)
          && Number.isFinite(record.range_high)
          && record.range_low <= value
          && value <= record.range_high;
        if (!rangeValid) addIssue(result, issue("estimate_range_invalid", `${label} must have a range enclosing its estimate`, record));
      }
    }
  }

  if (collection === "liabilities") {
    for (const field of ["interest_rate_percent", "monthly_payment"]) {
      if (typeof record[field] !== "number" || !Number.isFinite(record[field]) || record[field] < 0) {
        addIssue(result, issue("invalid_liability_terms", `${label}.${field} must be a non-negative finite number`, record));
      }
    }
  }
  if (collection === "recurring_flows") {
    if (!new Set(["income", "expense"]).has(record.direction)) {
      addIssue(result, issue("invalid_flow_direction", `${label} direction must be income or expense`, record));
    }
    if (!new Set(["fixed", "variable"]).has(record.category)) {
      addIssue(result, issue("invalid_flow_category", `${label} category must be fixed or variable`, record));
    }
  }
}

export function validateSnapshot(snapshot, { freshness = null } = {}) {
  if (!snapshot || typeof snapshot !== "object" || Array.isArray(snapshot)) {
    throw new TypeError("Snapshot must be an object");
  }
  if (snapshot.schema_version !== 1) {
    throw new Error(`Unsupported schema_version ${snapshot.schema_version}`);
  }
  const result = { valid: false, blocking: [], warnings: [] };
  if (!isDate(snapshot.as_of)) addIssue(result, issue("invalid_as_of", "Snapshot as_of must be a real YYYY-MM-DD date"));
  if (typeof snapshot.currency !== "string" || !/^[A-Z]{3}$/.test(snapshot.currency)) {
    addIssue(result, issue("invalid_currency", "Snapshot currency must be a three-letter uppercase code"));
  }
  if (!Array.isArray(snapshot.household_members) || snapshot.household_members.length === 0
    || snapshot.household_members.some((name) => typeof name !== "string" || !name.trim())) {
    addIssue(result, issue("household_missing", "Snapshot must name at least one household member"));
  }

  const ids = new Set();
  for (const collection of COLLECTIONS) {
    if (!Array.isArray(snapshot[collection])) {
      addIssue(result, issue("collection_missing", `Snapshot ${collection} must be an array`));
      continue;
    }
    for (const record of snapshot[collection]) validateRecord(record, collection, snapshot, freshness, result, ids);
  }
  const assetIds = new Set(Array.isArray(snapshot.assets) ? snapshot.assets.map((asset) => asset?.id).filter(Boolean) : []);
  if (Array.isArray(snapshot.liabilities)) {
    for (const liability of snapshot.liabilities) {
      if (liability?.secured_asset_id && !assetIds.has(liability.secured_asset_id)) {
        addIssue(result, issue("secured_asset_missing", `${liability.id || liability.label} refers to missing asset ${liability.secured_asset_id}`, liability));
      }
    }
  }

  if (!Array.isArray(snapshot.overrides)) {
    addIssue(result, issue("overrides_missing", "Snapshot overrides must be an array"));
  } else {
    for (const override of snapshot.overrides) {
      const valid = override
        && typeof override.id === "string" && override.id.trim()
        && typeof override.item_id === "string" && ids.has(override.item_id)
        && typeof override.reason === "string" && override.reason.trim()
        && Array.isArray(override.approved_by) && override.approved_by.length > 0
        && typeof override.approved_at === "string" && !Number.isNaN(Date.parse(override.approved_at));
      if (!valid) {
        addIssue(result, issue("invalid_override", "Every override must reference an item and record reason, approver, and time", override));
      } else {
        addIssue(result, issue("override_recorded", `Override ${override.id} is recorded and does not suppress validation`, override, "warning"), false);
      }
    }
  }
  result.valid = result.blocking.length === 0;
  return result;
}

export function validateFinanceDocument(markdown, { mode = "draft", freshness = null } = {}) {
  const parsed = parseFinanceDocument(markdown);
  const result = validateSnapshot(parsed.data, { freshness });
  const expected = {
    type: "financial-snapshot",
    schema_version: parsed.data.schema_version,
    as_of: parsed.data.as_of,
    currency: parsed.data.currency,
  };
  for (const [key, value] of Object.entries(expected)) {
    if (parsed.frontmatter[key] !== value) {
      result.blocking.unshift(issue("metadata_mismatch", `Frontmatter ${key} must equal embedded data ${JSON.stringify(value)}`));
    }
  }
  if (mode === "seal") {
    if (parsed.frontmatter.status !== "approved") {
      result.blocking.push(issue("record_not_approved", "Snapshot status must be approved before sealing"));
    }
    if (!Array.isArray(parsed.frontmatter.approved_by) || parsed.frontmatter.approved_by.length === 0) {
      result.blocking.push(issue("approval_missing", "Snapshot must record at least one approver before sealing"));
    }
  }
  result.valid = result.blocking.length === 0;
  return { ...result, parsed };
}

function toMinor(value) {
  return Math.round(value * 100);
}

function fromMinor(value) {
  return value / 100;
}

function sumMoney(records, field, predicate = () => true) {
  return fromMinor(records.filter(predicate).reduce((sum, record) => sum + toMinor(record[field]), 0));
}

export function calculateMetrics(snapshot, { freshness = null } = {}) {
  const validation = validateSnapshot(snapshot, { freshness });
  if (!validation.valid) {
    const codes = validation.blocking.map(({ code }) => code).join(", ");
    throw new Error(`Canonical calculations require a validated snapshot; blocking issues: ${codes}`);
  }
  const totalAssets = sumMoney(snapshot.assets, "value");
  const totalLiabilities = sumMoney(snapshot.liabilities, "balance");
  const pensionTotal = sumMoney(snapshot.assets, "value", (asset) => asset.category === "pension");
  const propertyTotal = sumMoney(snapshot.assets, "value", (asset) => asset.category === "property");
  const mortgageTotal = sumMoney(snapshot.liabilities, "balance", (liability) => liability.category === "mortgage");
  const vehicleTotal = sumMoney(snapshot.assets, "value", (asset) => asset.category === "vehicle");
  const vehicleIds = new Set(snapshot.assets.filter((asset) => asset.category === "vehicle").map((asset) => asset.id));
  const vehicleDebt = sumMoney(snapshot.liabilities, "balance", (liability) => vehicleIds.has(liability.secured_asset_id));
  const monthlyEmploymentIncome = sumMoney(snapshot.income, "monthly_net");
  const monthlyRecurringIncome = sumMoney(snapshot.recurring_flows, "amount_monthly", (flow) => flow.direction === "income");
  const monthlyExpenses = sumMoney(snapshot.recurring_flows, "amount_monthly", (flow) => flow.direction === "expense");
  const monthlyDebtService = sumMoney(snapshot.liabilities, "monthly_payment");
  const highInterestThreshold = freshness?.high_interest_debt_percent ?? 6;
  return {
    total_assets: totalAssets,
    total_liabilities: totalLiabilities,
    net_worth: fromMinor(toMinor(totalAssets) - toMinor(totalLiabilities)),
    net_worth_excluding_pensions: fromMinor(toMinor(totalAssets) - toMinor(pensionTotal) - toMinor(totalLiabilities)),
    liquid_assets: sumMoney(snapshot.assets, "value", (asset) => ["cash", "investment"].includes(asset.category)),
    home_equity: fromMinor(toMinor(propertyTotal) - toMinor(mortgageTotal)),
    vehicle_equity: fromMinor(toMinor(vehicleTotal) - toMinor(vehicleDebt)),
    monthly_debt_service: monthlyDebtService,
    monthly_fixed_costs: sumMoney(snapshot.recurring_flows, "amount_monthly", (flow) => flow.direction === "expense" && flow.category === "fixed"),
    monthly_surplus: fromMinor(toMinor(monthlyEmploymentIncome) + toMinor(monthlyRecurringIncome) - toMinor(monthlyExpenses) - toMinor(monthlyDebtService)),
    mortgage_ltv: propertyTotal > 0 ? Math.round((mortgageTotal / propertyTotal) * 10_000) / 100 : null,
    high_interest_debt: sumMoney(snapshot.liabilities, "balance", (liability) => liability.interest_rate_percent >= highInterestThreshold),
    pension_total: pensionTotal,
  };
}
