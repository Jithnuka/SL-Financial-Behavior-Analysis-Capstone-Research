from src.load_data import load_data
from src.processing import preprocess
from src.credit_sources import credit_sources
from src.demographics import demographic_analysis
from src.borrowing_purpose import borrowing_purpose
from src.plots import bar_plot
from src.advanced_plots import income_quintile_plot

# Load
# Use the provided data file if available
df = load_data("data/Findex_Microdata_2025_Sri Lanka_Clean.csv")
df = preprocess(df)

# Q1: Credit Sources
credit = credit_sources(df)
bar_plot(credit, "Primary Sources of Credit in Sri Lanka", "credit_sources.png")

# Q2: Demographics
gender = demographic_analysis(df, "gender", "borrow_any")
bar_plot(gender, "Borrowing by Gender", "borrow_gender.png")

# Map income quintile numeric codes to readable labels
income_map = {
	1: 'Poorest',
	2: 'Lower-middle',
	3: 'Middle',
	4: 'Upper-middle',
	5: 'Richest'
}
income = demographic_analysis(df, "income_quintile", "borrow_any")
if not income.empty:
	try:
		income.index = [income_map.get(int(x), str(x)) for x in income.index]
	except Exception:
		income.index = [income_map.get(x, str(x)) for x in income.index]
bar_plot(income, "Borrowing by Income Group", "borrow_income.png")

# Advanced income quintile plot (static + interactive)
try:
	income_quintile_plot(df, income_col='inc_q', borrow_col='borrow_any', map_names=income_map, replace_with_names=False, show_both=True, annotate_counts=True, ci_boot=True, n_boot=1000, split_by='gender', out_png='output/figures/borrow_income_advanced.png', out_html='output/figures/borrow_income_advanced.html')
except Exception as e:
	print('Could not create advanced income plot:', e)

age = demographic_analysis(df, "age_group", "borrow_any")
bar_plot(age, "Borrowing by Age Group", "borrow_age.png")

purpose = borrowing_purpose(df)
purpose_map = {
	'fin30': 'Business/Investment (fin30)',
	'fin24a': 'Consumption/Household (fin24a)',
	'fin24b': 'Health (fin24b)',
	'fin32': 'Education (fin32)',
	'fin24c': 'Emergency (fin24c)',
	'fin24': 'Other (fin24)'
}
if not purpose.empty:
	purpose.index = [purpose_map.get(str(i), str(i)) for i in purpose.index]
	bar_plot(purpose, "Main Purpose of Borrowing", "borrow_purpose.png")

print("=== ANALYSIS COMPLETE ===")
print("Plots saved in output/figures/")
