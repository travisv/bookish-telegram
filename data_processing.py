import pandas as pd

def clean_data(path):
    '''takes a file path to a .CSV containing financial data and does some
    initial cleaning'''

    df = pd.read_csv(path)
    # remove TTM values in order to handle the year variable created next
    df = df[df['period_end_date'] != 'TTM']
    df['year'] = pd.DatetimeIndex(df['period_end_date']).year
    # replace '-' values with zero so columns can be converted to numeric
    df = df.replace('-', 0)
    # convert columns to numeric if possible for future calculations
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    return df

def annualize_industries(df):
    grouped = df.groupby(['industry', 'year'])
    avg = grouped.mean()[AVERAGE_COLUMNS]
    tot = grouped.sum()[TOTAL_COLUMNS]
    dff = pd.concat([tot, avg], axis=1)
    return dff

# columns to use for mean after grouping
AVERAGE_COLUMNS = [
'price_to_earnings',
'price_to_book',
'price_to_sales',
'price_to_tangible_book',
'price_to_fcf',
'price_to_pretax_income',
'price_to_earnings_growth',
'enterprise_value_to_earnings',
'enterprise_value_to_book',
'enterprise_value_to_tangible_book',
'enterprise_value_to_sales',
'enterprise_value_to_fcf',
'enterprise_value_to_pretax_income',
'pe',
'pb',
'ps',
'p_pretax_inc',
'peg',
'ev_s',
'ev_ebitda',
'ev_ebit',
'ev_pretax_inc',
'ev_fcf',
'p_premiums',
'ev_premiums',
'price',
'volume',
'mkt_data_date',
'volume_avg_14d',
'volume_avg_50d',
'volume_avg_200d',
'beta',
'ebitda',
'capex',
'fcf',
'earning_assets',
'policy_revenue',
'underwriting_profit',
'dividends',
'payout_ratio',
'income_tax_rate',
'net_debt',
'gross_margin',
'ebitda_margin',
'operating_margin',
'pretax_margin',
'net_income_margin',
'fcf_margin',
'net_interest_margin',
'underwriting_margin',
'roe',
'roa',
'roic',
'roic_legacy',
'roce',
'rotce',
'roi',
'debt_to_equity',
'debt_to_assets',
'equity_to_assets',
'assets_to_equity',
'current_ratio',
'earning_assets_to_equity',
'loans_to_deposits',
'loan_loss_reserve_to_loans',
'revenue_per_share',
'ebitda_per_share',
'operating_income_per_share',
'pretax_income_per_share',
'fcf_per_share',
'book_value_per_share',
'tangible_book_per_share',
'premiums_per_share',
'revenue_growth',
'gross_profit_growth',
'ebitda_growth',
'operating_income_growth',
'pretax_income_growth',
'net_income_growth',
'eps_diluted_growth',
'shares_diluted_growth',
'shares_eop_growth',
'cash_and_equiv_growth',
'ppe_growth',
'total_assets_growth',
'total_equity_growth',
'cfo_growth',
'capex_growth',
'fcf_growth',
'revenue_cagr_10',
'eps_diluted_cagr_10',
'total_assets_cagr_10',
'total_equity_cagr_10',
'cf_cfo_cagr_10',
'fcf_cagr_10',
'premiums_growth',
'policy_revenue_growth',
'total_investments_growth',
'premiums_cagr_10',
'total_investments_cagr_10',
'net_interest_income_growth',
'loans_gross_growth',
'loans_net_growth',
'deposits_growth',
'earning_assets_growth',
'net_interest_income_cagr_10',
'loans_gross_cagr_10',
'earning_assets_cagr_10',
'deposits_cagr_10'
]


# columns to use for sum after grouping
TOTAL_COLUMNS = [
'revenue',
'cogs',
'gross_profit',
'sga',
'rnd',
'special_charges',
'other_opex',
'total_opex',
'operating_income',
'interest_income',
'interest_expense',
'net_interest_income_normal',
'other_nonoperating_income',
'pretax_income',
'income_tax',
'net_income_continuing',
'net_income_discontinued',
'income_allocated_to_minority_interest',
'other_income_statement_items',
'net_income',
'preferred_dividends',
'net_income_available_to_shareholders',
'eps_basic',
'eps_diluted',
'cash_and_equiv',
'st_investments',
'receivables',
'inventories',
'other_current_assets',
'total_current_assets',
'equity_and_other_investments',
'ppe_gross',
'accumulated_depreciation',
'ppe_net',
'intangible_assets',
'goodwill',
'other_lt_assets',
'total_assets',
'accounts_payable',
'tax_payable',
'current_accrued_liabilities',
'st_debt',
'current_deferred_revenue',
'current_deferred_tax_liability',
'current_capital_leases',
'other_current_liabilities',
'total_current_liabilities',
'lt_debt',
'noncurrent_capital_leases',
'pension_liabilities',
'noncurrent_deferred_revenue',
'other_lt_liabilities',
'total_liabilities',
'common_stock',
'preferred_stock',
'retained_earnings',
'aoci',
'apic',
'treasury_stock',
'other_equity',
'minority_interest_liability',
'total_equity',
'total_liabilities_and_equity',
'total_investments',
'deferred_policy_acquisition_cost',
'unearned_premiums',
'future_policy_benefits',
'loans_gross',
'allowance_for_loan_losses',
'unearned_income',
'loans_net',
'deposits_liability',
'cfo_net_income',
'cfo_da',
'cfo_receivables',
'cfo_inventory',
'cfo_prepaid_expenses',
'cfo_other_working_capital',
'cfo_change_in_working_capital',
'cfo_deferred_tax',
'cfo_stock_comp',
'cfo_other_noncash_items',
'cf_cfo',
'cfi_ppe_purchases',
'cfi_ppe_sales',
'cfi_ppe_net',
'cfi_acquisitions',
'cfi_divestitures',
'cfi_acquisitions_net',
'cfi_investment_purchases',
'cfi_investment_sales',
'cfi_investment_net',
'cfi_intangibles_net',
'cfi_other',
'cf_cfi',
'cff_common_stock_issued',
'cff_common_stock_repurchased',
'cff_common_stock_net',
'cff_pfd_issued',
'cff_pfd_repurchased',
'cff_pfd_net',
'cff_debt_issued',
'cff_debt_repaid',
'cff_debt_net',
'cff_dividend_paid',
'cff_other',
'cf_cff',
'cf_forex',
'cf_net_change_in_cash',
'mkt_cap',
'market_cap',
'period_end_price',
'shares_float',
'ev',
'enterprise_value',
'book_value',
'tangible_book_value'
]

#  to use for sum after grouping
ALL_COLUMNS = [
'symbol',
'qfs_symbol',
'exchange',
'name',
'company_type',
'currency',
'industry',
'period_type',
'period_end_date',
'revenue',
'cogs',
'gross_profit',
'sga',
'rnd',
'special_charges',
'other_opex',
'total_opex',
'operating_income',
'interest_income',
'interest_expense',
'net_interest_income_normal',
'other_nonoperating_income',
'pretax_income',
'income_tax',
'net_income_continuing',
'net_income_discontinued',
'income_allocated_to_minority_interest',
'other_income_statement_items',
'net_income',
'preferred_dividends',
'net_income_available_to_shareholders',
'eps_basic',
'eps_diluted',
'shares_basic',
'shares_diluted',
'shares_eop',
'shares_eop_change',
'premiums_earned',
'net_investment_income',
'fees_and_other_income',
'net_policyholder_claims_expense',
'policy_acquisition_expense',
'interest_expense_insurance',
'total_interest_income',
'total_interest_expense',
'net_interest_income',
'total_noninterest_revenue',
'credit_losses_provision',
'net_interest_income_after_credit_losses_provision',
'total_noninterest_expense',
'da_income_statement_supplemental',
'cash_and_equiv',
'st_investments',
'receivables',
'inventories',
'other_current_assets',
'total_current_assets',
'equity_and_other_investments',
'ppe_gross',
'accumulated_depreciation',
'ppe_net',
'intangible_assets',
'goodwill',
'other_lt_assets',
'total_assets',
'accounts_payable',
'tax_payable',
'current_accrued_liabilities',
'st_debt',
'current_deferred_revenue',
'current_deferred_tax_liability',
'current_capital_leases',
'other_current_liabilities',
'total_current_liabilities',
'lt_debt',
'noncurrent_capital_leases',
'pension_liabilities',
'noncurrent_deferred_revenue',
'other_lt_liabilities',
'total_liabilities',
'common_stock',
'preferred_stock',
'retained_earnings',
'aoci',
'apic',
'treasury_stock',
'other_equity',
'minority_interest_liability',
'total_equity',
'total_liabilities_and_equity',
'total_investments',
'deferred_policy_acquisition_cost',
'unearned_premiums',
'future_policy_benefits',
'loans_gross',
'allowance_for_loan_losses',
'unearned_income',
'loans_net',
'deposits_liability',
'cfo_net_income',
'cfo_da',
'cfo_receivables',
'cfo_inventory',
'cfo_prepaid_expenses',
'cfo_other_working_capital',
'cfo_change_in_working_capital',
'cfo_deferred_tax',
'cfo_stock_comp',
'cfo_other_noncash_items',
'cf_cfo',
'cfi_ppe_purchases',
'cfi_ppe_sales',
'cfi_ppe_net',
'cfi_acquisitions',
'cfi_divestitures',
'cfi_acquisitions_net',
'cfi_investment_purchases',
'cfi_investment_sales',
'cfi_investment_net',
'cfi_intangibles_net',
'cfi_other',
'cf_cfi',
'cff_common_stock_issued',
'cff_common_stock_repurchased',
'cff_common_stock_net',
'cff_pfd_issued',
'cff_pfd_repurchased',
'cff_pfd_net',
'cff_debt_issued',
'cff_debt_repaid',
'cff_debt_net',
'cff_dividend_paid',
'cff_other',
'cf_cff',
'cf_forex',
'cf_net_change_in_cash',
'mkt_cap',
'market_cap',
'period_end_price',
'shares_float',
'ev',
'enterprise_value',
'book_value',
'tangible_book_value',
'price_to_earnings',
'price_to_book',
'price_to_sales',
'price_to_tangible_book',
'price_to_fcf',
'price_to_pretax_income',
'price_to_earnings_growth',
'enterprise_value_to_earnings',
'enterprise_value_to_book',
'enterprise_value_to_tangible_book',
'enterprise_value_to_sales',
'enterprise_value_to_fcf',
'enterprise_value_to_pretax_income',
'pe',
'pb',
'ps',
'p_pretax_inc',
'peg',
'ev_s',
'ev_ebitda',
'ev_ebit',
'ev_pretax_inc',
'ev_fcf',
'p_premiums',
'ev_premiums',
'price',
'volume',
'mkt_data_date',
'volume_avg_14d',
'volume_avg_50d',
'volume_avg_200d',
'beta',
'ebitda',
'capex',
'fcf',
'earning_assets',
'policy_revenue',
'underwriting_profit',
'dividends',
'payout_ratio',
'income_tax_rate',
'net_debt',
'gross_margin',
'ebitda_margin',
'operating_margin',
'pretax_margin',
'net_income_margin',
'fcf_margin',
'net_interest_margin',
'underwriting_margin',
'roe',
'roa',
'roic',
'roic_legacy',
'roce',
'rotce',
'roi',
'debt_to_equity',
'debt_to_assets',
'equity_to_assets',
'assets_to_equity',
'current_ratio',
'earning_assets_to_equity',
'loans_to_deposits',
'loan_loss_reserve_to_loans',
'revenue_per_share',
'ebitda_per_share',
'operating_income_per_share',
'pretax_income_per_share',
'fcf_per_share',
'book_value_per_share',
'tangible_book_per_share',
'premiums_per_share',
'revenue_growth',
'gross_profit_growth',
'ebitda_growth',
'operating_income_growth',
'pretax_income_growth',
'net_income_growth',
'eps_diluted_growth',
'shares_diluted_growth',
'shares_eop_growth',
'cash_and_equiv_growth',
'ppe_growth',
'total_assets_growth',
'total_equity_growth',
'cfo_growth',
'capex_growth',
'fcf_growth',
'revenue_cagr_10',
'eps_diluted_cagr_10',
'total_assets_cagr_10',
'total_equity_cagr_10',
'cf_cfo_cagr_10',
'fcf_cagr_10',
'premiums_growth',
'policy_revenue_growth',
'total_investments_growth',
'premiums_cagr_10',
'total_investments_cagr_10',
'net_interest_income_growth',
'loans_gross_growth',
'loans_net_growth',
'deposits_growth',
'earning_assets_growth',
'net_interest_income_cagr_10',
'loans_gross_cagr_10',
'earning_assets_cagr_10',
'deposits_cagr_10',
'gross_margin_median',
'pretax_margin_median',
'operating_income_margin_median',
'fcf_margin_median',
'roa_median',
'roe_median',
'roic_median',
'assets_to_equity_median',
'debt_to_assets_median',
'debt_to_equity_median',
'roi_median',
'equity_to_assets_median',
'underwriting_margin_median',
'nim_median',
'earning_assets_to_equity_median',
'loans_to_deposits_median',
'loan_loss_reserve_to_loans_median',
'year'
]


