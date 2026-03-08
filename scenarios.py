"""
Sample mortgage servicing scenarios.
Synthetic but realistic data, segmented by entity type.

Segments:
  SERVICER        — Valon, Mr. Cooper, LoanCare (day-to-day servicing)
  COLLECTIONS     — debt collectors, loss mitigation shops, special servicers
  ORIGINATOR      — lenders at point of sale or early servicing transfer
  INVESTOR/GSE    — Fannie Mae, Freddie Mac, Ginnie Mae, MBS investors
"""

# ═══════════════════════════════════════════════════════════════════
#  SERVICER SCENARIOS — core mortgage servicing operations
# ═══════════════════════════════════════════════════════════════════

SERVICER_SCENARIOS = {
    "Forbearance Request — Texas": {
        "segment": "Servicer",
        "borrower_name": "Maria Santos",
        "state": "TX",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (Conventional)",
        "original_amount": "$320,000",
        "current_balance": "$298,500",
        "interest_rate": "6.75%",
        "monthly_payment": "$2,076",
        "origination_date": "March 2022",
        "credit_score": "680",
        "dti_ratio": "42%",
        "payment_history": (
            "On-time payments for 24 months. "
            "Missed January and February 2026 payments. "
            "Borrower called requesting forbearance due to job loss."
        ),
        "situation": (
            "Borrower is requesting forbearance. Lost primary employment "
            "6 weeks ago. Spouse still employed part-time ($2,800/month). "
            "Has applied for unemployment benefits but not yet receiving them."
        ),
        "additional_context": (
            "Borrower has expressed anxiety about losing the home. "
            "Property estimated current value: $345,000. No other liens. "
            "Escrow balance is current."
        ),
    },
    "Refinance Inquiry — California": {
        "segment": "Servicer",
        "borrower_name": "James Chen",
        "state": "CA",
        "property_type": "Condo",
        "loan_type": "30-year Fixed (Conventional)",
        "original_amount": "$550,000",
        "current_balance": "$485,000",
        "interest_rate": "7.25%",
        "monthly_payment": "$3,753",
        "origination_date": "September 2023",
        "credit_score": "745",
        "dti_ratio": "35%",
        "payment_history": (
            "Perfect payment history — all 29 payments on time. "
            "Borrower also making additional principal payments of $200/month."
        ),
        "situation": (
            "Borrower inquiring about refinancing options. Believes rates "
            "have come down and wants to lower monthly payment. Also "
            "interested in potentially taking cash out for home improvements."
        ),
        "additional_context": (
            "Property estimated current value: $620,000. HOA dues: $450/month. "
            "Borrower recently received a promotion with 15% salary increase. "
            "No other debt besides auto loan ($18,000 remaining)."
        ),
    },
    "Escrow Shortage — Florida": {
        "segment": "Servicer",
        "borrower_name": "David & Lisa Thompson",
        "state": "FL",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (FHA)",
        "original_amount": "$280,000",
        "current_balance": "$265,000",
        "interest_rate": "5.50%",
        "monthly_payment": "$1,890 (PITI)",
        "origination_date": "June 2021",
        "credit_score": "710",
        "dti_ratio": "38%",
        "payment_history": (
            "Consistent on-time payments for 4+ years. No delinquencies ever."
        ),
        "situation": (
            "Annual escrow analysis revealed a $3,200 shortage due to property "
            "insurance premium increase (hurricane risk reassessment). New monthly "
            "payment would increase by $380/month. Borrowers are disputing the "
            "increase and requesting options."
        ),
        "additional_context": (
            "Property in coastal Florida (hurricane zone). Insurance premium "
            "increased from $2,400/yr to $6,200/yr after carrier reassessment. "
            "Borrowers are on fixed income (combined retirement + part-time "
            "work: $5,800/month). Property value: $310,000."
        ),
    },
    "Early Payoff Request — Arizona": {
        "segment": "Servicer",
        "borrower_name": "Thomas & Karen Mitchell",
        "state": "AZ",
        "property_type": "Single Family",
        "loan_type": "15-year Fixed (Conventional)",
        "original_amount": "$380,000",
        "current_balance": "$142,000",
        "interest_rate": "3.75%",
        "monthly_payment": "$2,764",
        "origination_date": "January 2017",
        "credit_score": "810",
        "dti_ratio": "15%",
        "payment_history": (
            "Perfect payment history for 9+ years. Never missed a payment. "
            "Consistently made extra principal payments of $500-1,000/month."
        ),
        "situation": (
            "Borrowers requesting a payoff quote. Planning to pay off remaining "
            "$142,000 balance in full using proceeds from a business sale. Want "
            "to understand exact payoff amount including per diem interest, any "
            "fees, and the payoff process timeline."
        ),
        "additional_context": (
            "Property value: $580,000. No other liens. Borrowers are semi-retired, "
            "ages 62 and 59. Want to be mortgage-free before full retirement. "
            "Escrow balance of $4,200 to be refunded. Also asking about lien "
            "release timeline and whether there's a prepayment penalty."
        ),
    },
}

# ═══════════════════════════════════════════════════════════════════
#  COLLECTIONS & SPECIAL SERVICING SCENARIOS
# ═══════════════════════════════════════════════════════════════════

COLLECTIONS_SCENARIOS = {
    "Pre-Foreclosure Notice — Ohio": {
        "segment": "Collections",
        "borrower_name": "Marcus Johnson",
        "state": "OH",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (Conventional)",
        "original_amount": "$185,000",
        "current_balance": "$172,000",
        "interest_rate": "5.875%",
        "monthly_payment": "$1,245",
        "origination_date": "April 2022",
        "credit_score": "540",
        "dti_ratio": "61%",
        "payment_history": (
            "On-time for 12 months. Then irregular — made 8 of the next 18 payments. "
            "Currently 150 days delinquent ($7,475 past due including late fees). "
            "Multiple collection calls unanswered. One payment plan attempted "
            "and broken after 2 months."
        ),
        "situation": (
            "Loan is being referred to foreclosure. Servicer must send pre-foreclosure "
            "notice (breach letter) per state and federal requirements. Borrower has "
            "not responded to prior loss mitigation outreach. Last contact was 45 days "
            "ago when borrower said 'I know I'm behind, I'll figure it out.'"
        ),
        "additional_context": (
            "Property value: $195,000. City of Columbus, OH. Ohio is a judicial "
            "foreclosure state (takes 12-18 months). No second lien. Borrower is "
            "single, works hourly construction ($3,400/month gross, seasonal). "
            "Property has minor deferred maintenance. Investor is Freddie Mac."
        ),
    },
    "Debt Validation Dispute — Georgia": {
        "segment": "Collections",
        "borrower_name": "Keisha & Darnell Washington",
        "state": "GA",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (FHA)",
        "original_amount": "$225,000",
        "current_balance": "$210,000",
        "interest_rate": "6.125%",
        "monthly_payment": "$1,620 (PITI)",
        "origination_date": "July 2022",
        "credit_score": "590",
        "dti_ratio": "48%",
        "payment_history": (
            "On-time for 20 months. Servicing transferred from LoanCare to new "
            "servicer 6 months ago. Since transfer, borrowers claim they sent "
            "3 payments that were not credited. Currently showing 90 days delinquent "
            "but borrowers dispute this and have bank statements showing payments."
        ),
        "situation": (
            "Borrowers sent a written debt validation letter under FDCPA disputing "
            "the delinquency. They claim the servicing transfer caused payment "
            "misapplication. Demanding full accounting of all payments since transfer, "
            "correction of credit reporting, and removal of late fees. Have retained "
            "a consumer attorney who sent a formal demand letter."
        ),
        "additional_context": (
            "Property value: $240,000. This is an FDCPA/RESPA qualified written "
            "request situation. 60-day acknowledgment deadline applies. Prior "
            "servicer (LoanCare) has history of servicing transfer complaints. "
            "Borrowers have filed a CFPB complaint. State AG office may be monitoring."
        ),
    },
    "Deficiency Judgment Collection — Nevada": {
        "segment": "Collections",
        "borrower_name": "Steven Park",
        "state": "NV",
        "property_type": "Condo",
        "loan_type": "30-year Fixed (Conventional)",
        "original_amount": "$350,000",
        "current_balance": "$0 (foreclosed)",
        "interest_rate": "N/A (loan closed)",
        "monthly_payment": "N/A",
        "origination_date": "June 2020",
        "credit_score": "480",
        "dti_ratio": "N/A",
        "payment_history": (
            "On-time for 24 months. Then complete default — no payments for 14 months. "
            "Foreclosure completed October 2025. Property sold at auction for $265,000. "
            "Outstanding balance at foreclosure was $328,000."
        ),
        "situation": (
            "Foreclosure sale resulted in $63,000 deficiency. Investor is considering "
            "pursuing a deficiency judgment. Loan has been assigned to a collection "
            "agency. Must determine if deficiency judgment is permissible in Nevada "
            "and what borrower protections apply."
        ),
        "additional_context": (
            "Nevada has anti-deficiency protections for certain loans. Original loan "
            "was purchase money mortgage. Borrower's current address is unknown — "
            "skip tracing needed. Borrower may have filed bankruptcy (Chapter 7). "
            "Statute of limitations for deficiency action in NV is 6 months from "
            "foreclosure sale. Collection agency must comply with FDCPA."
        ),
    },
    "Third-Party Collector Handoff — Pennsylvania": {
        "segment": "Collections",
        "borrower_name": "Anthony & Maria Russo",
        "state": "PA",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (Conventional)",
        "original_amount": "$275,000",
        "current_balance": "$258,000",
        "interest_rate": "6.50%",
        "monthly_payment": "$1,738",
        "origination_date": "December 2021",
        "credit_score": "560",
        "dti_ratio": "55%",
        "payment_history": (
            "On-time for 18 months. Then sporadic — 6 of the last 18 months paid. "
            "Currently 120 days delinquent ($8,690 past due including $1,520 in "
            "accumulated late fees). Two prior repayment plans failed."
        ),
        "situation": (
            "Servicer is transferring collection activity to a third-party debt "
            "collector (special servicer). Must ensure proper FDCPA initial "
            "communication, validation notice, and mini-Miranda warning. Borrowers "
            "have previously expressed hardship due to Anthony's disability "
            "(partial disability, receiving $1,800/month SSDI)."
        ),
        "additional_context": (
            "Property value: $290,000. PA is a judicial foreclosure state. "
            "Anthony receives SSDI ($1,800/month) which has garnishment protections. "
            "Maria works part-time ($2,100/month). Two prior loss mitigation "
            "reviews completed — modification offered but paperwork not returned. "
            "Investor is Fannie Mae. Third-party collector must be licensed in PA "
            "and comply with PA FCEUA."
        ),
    },
}

# ═══════════════════════════════════════════════════════════════════
#  ORIGINATOR SCENARIOS — point of sale / early servicing
# ═══════════════════════════════════════════════════════════════════

ORIGINATOR_SCENARIOS = {
    "Servicing Transfer Onboarding — New Jersey": {
        "segment": "Originator",
        "borrower_name": "Michelle & Brian O'Connor",
        "state": "NJ",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (Conventional)",
        "original_amount": "$425,000",
        "current_balance": "$418,000",
        "interest_rate": "6.875%",
        "monthly_payment": "$2,790",
        "origination_date": "November 2025",
        "credit_score": "720",
        "dti_ratio": "37%",
        "payment_history": (
            "Brand new loan — only 3 payments made, all on time. Servicing is "
            "being transferred from originator to new servicer effective April 1, 2026."
        ),
        "situation": (
            "Originator is transferring servicing rights to new servicer. Must "
            "send proper goodbye letter (15 days before transfer). New servicer "
            "must send welcome letter (within 15 days of transfer). Borrower "
            "called confused because they received a letter saying their loan "
            "was being 'sold' and is worried about losing their rate."
        ),
        "additional_context": (
            "Property value: $465,000. First-time homebuyers, unfamiliar with "
            "servicing transfers. Escrow account with $3,800 balance must be "
            "transferred accurately. Auto-pay needs to be re-established with "
            "new servicer. NJ has specific consumer notification requirements "
            "beyond federal RESPA."
        ),
    },
    "VA Loan Assumption — North Carolina": {
        "segment": "Originator",
        "borrower_name": "Sergeant Michael Torres",
        "state": "NC",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (VA)",
        "original_amount": "$310,000",
        "current_balance": "$285,000",
        "interest_rate": "3.25%",
        "monthly_payment": "$1,349",
        "origination_date": "February 2021",
        "credit_score": "730",
        "dti_ratio": "28%",
        "payment_history": (
            "Perfect payment history — all 60 payments on time."
        ),
        "situation": (
            "Borrower received PCS orders to Germany. Wants to sell but current "
            "rates are 6.5%+, making the 3.25% VA loan attractive for assumption. "
            "A potential buyer (non-veteran, credit score 710, income $6,500/month) "
            "has expressed interest in assuming the loan."
        ),
        "additional_context": (
            "Property value: $365,000. No other liens. Borrower wants to preserve "
            "VA entitlement if possible. Buyer is pre-approved for conventional "
            "at 6.75% but prefers assumption. Borrower deploying in 60 days. "
            "VA funding fee was financed into the original loan."
        ),
    },
}

# ═══════════════════════════════════════════════════════════════════
#  INVESTOR / GSE SCENARIOS — Fannie, Freddie, Ginnie perspective
# ═══════════════════════════════════════════════════════════════════

INVESTOR_SCENARIOS = {
    "Loan Modification — Illinois": {
        "segment": "Investor/GSE",
        "borrower_name": "Robert & Angela Williams",
        "state": "IL",
        "property_type": "Single Family",
        "loan_type": "30-year Fixed (Conventional)",
        "original_amount": "$240,000",
        "current_balance": "$218,000",
        "interest_rate": "6.25%",
        "monthly_payment": "$1,478",
        "origination_date": "November 2021",
        "credit_score": "620",
        "dti_ratio": "52%",
        "payment_history": (
            "On-time for first 30 months. Then 60 days late twice in 2024. "
            "Caught up briefly, then missed last 3 payments (Dec 2025 - Feb 2026). "
            "Currently 90+ days delinquent."
        ),
        "situation": (
            "Borrowers requesting a loan modification. Robert had a medical emergency "
            "(heart surgery) in October 2025 resulting in $45,000 in medical bills and "
            "3 months unpaid leave. Angela's income ($3,200/month) cannot cover "
            "all expenses. Robert returning to work part-time next month."
        ),
        "additional_context": (
            "Property value: $260,000. Second lien: $15,000 HELOC (current). "
            "Medical debt in collections. 2 school-age children. Robert expects "
            "full-time return in 4 months. Previous combined income: $7,800/month. "
            "Investor is Fannie Mae — Flex Modification guidelines apply."
        ),
    },
    "Partial Claim — New York": {
        "segment": "Investor/GSE",
        "borrower_name": "Priya Sharma",
        "state": "NY",
        "property_type": "Condo",
        "loan_type": "30-year Fixed (FHA)",
        "original_amount": "$420,000",
        "current_balance": "$395,000",
        "interest_rate": "5.875%",
        "monthly_payment": "$2,860 (PITI)",
        "origination_date": "August 2022",
        "credit_score": "665",
        "dti_ratio": "46%",
        "payment_history": (
            "On-time for 18 months. Entered COVID-era forbearance (6 months). "
            "Resumed payments for 8 months. Then missed last 4 payments "
            "(Nov 2025 through Feb 2026)."
        ),
        "situation": (
            "Borrower recently ended forbearance and has $11,440 in arrears "
            "(4 months x $2,860). Cannot afford lump sum. Requesting FHA partial "
            "claim to defer arrears. Income has stabilized at $6,800/month gross."
        ),
        "additional_context": (
            "Property value: $440,000. HOA dues: $600/month. Previous forbearance "
            "resolved via deferral — this would be second loss mitigation event. "
            "FHA case number active. MIP is current. Single, no dependents. "
            "HUD guidelines on partial claim limits and eligibility apply."
        ),
    },
}

# ═══════════════════════════════════════════════════════════════════
#  Combined + grouped for the UI
# ═══════════════════════════════════════════════════════════════════

SCENARIOS = {}
SCENARIOS.update(SERVICER_SCENARIOS)
SCENARIOS.update(COLLECTIONS_SCENARIOS)
SCENARIOS.update(ORIGINATOR_SCENARIOS)
SCENARIOS.update(INVESTOR_SCENARIOS)

SCENARIO_GROUPS = {
    "🏦 Servicer": list(SERVICER_SCENARIOS.keys()),
    "📞 Collections & Special Servicing": list(COLLECTIONS_SCENARIOS.keys()),
    "🏠 Originator": list(ORIGINATOR_SCENARIOS.keys()),
    "📈 Investor / GSE": list(INVESTOR_SCENARIOS.keys()),
}
