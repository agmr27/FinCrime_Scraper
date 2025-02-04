

import re

# Compile the regex pattern with case-insensitivity
keywords = re.compile(r"(?i)\b(fraud|account(?:ing fraud|ing gimmick)?|inflated|market manipulation|insider trading|price manipulation|restated financials|revised financial statement|restate (?:company(?:’s)?|companies) (?:financials|financial statements|statements)|restatement of previously issued financial statements|sham|long(?: |-)?island(?: |-)?based|brooklyn|pump|missed projection|redemption rights|conducting an internal investigation|launch of an internal investigation|formed a special committee to investigate|potential misconduct|violations of internal (?:controls|accounting controls)|misappropriate|mismarked)\b")

sec_keywords =re.compile(r"(?i)\b(internal (?:investigation|review|accounting controls|controls)|external auditors|actions of (?:certain senior|executive) management|special (?:committee to investigate|investigation)|alleged misconduct|potential misconduct|reported misconduct|allegations of misconduct|violations of company (?:policy|policies)|ongoing investigation|potential breaches|violations of internal controls|possible termination|restating financial statements|revisions to previously reported financial results|sensitive nature|correction of accounting errors|materially misstated|errors related to revenue recognition|accounting errors|accounting treatment of financial instruments|improper (?:classification of expenses|capitalizing of expenses|reporting of financial instruments)|misapplications of GAAP|revised financial reports|audit committee review|independent audit|review of internal (?:controls|accounting controls)|overstatement|overstated|understatement of liabilities|disclose material facts|certain off-balance-sheet|misapplication of generally accepted accounting principles|more accurate reporting|correct errors|errors in the valuation|of these errors)\b")

##Original test keywords
# keywords = [
#     "account",
#     "accounting fraud",
#     "inflated revenues",
#     "market manipulation",
#     "insider trading",
#     "price manipulation",
#     "restated financials",
#     "accounting gimmick",
#     "sham",
#     "long island based",
#     "long-island-based",
#     "brooklyn",
#     "pump",
#     "missed projection",
#     "revised financial statement",
#     "restate companies financials",
#     "restate companies financial statements",
#     "restate companies statements",
#     "restatement of previously issued financial statements",
#     "redemption rights"
# ]