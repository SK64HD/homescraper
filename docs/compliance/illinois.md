# Illinois compliance research

Checked: 2026-10-27

This is a research record, not legal advice. It is intentionally limited to points verified from primary Illinois sources during this implementation. Any transaction, advertising, solicitation, or brokerage workflow must be re-checked before activation.

## Verified points

### Broker licensing

The Illinois Department of Financial and Professional Regulation (IDFPR) states that a real-estate broker applicant must be at least 18, have a high-school diploma/GED, complete 75 hours of pre-license education, pass the state and national examination, and have sponsorship by a sponsoring broker. IDFPR also identifies 45 hours of post-license education in the first renewal period.

Source: IDFPR Professional Requirements for Licensure.
https://idfpr.illinois.gov/content/dam/soi/en/web/idfpr/forms/dre/Professional%20Requirements%20for%20Licensure.pdf

The Illinois Real Estate License Act, 225 ILCS 454/5-27, likewise specifies 75 hours of approved instruction, including 15 hours of situational/case-study instruction, and passage of the Department-authorized written examination. It also states that a person may not engage in activities covered by the Act until valid sponsorship is registered with the Department.

Source: Illinois General Assembly, 225 ILCS 454/5-27.
https://www.ilga.gov/legislation/ILCS/details?ActID=1364&ActName=Real%20Estate%20License%20Act%20of%202000.&ChapAct=225%20ILCS%20454%2F&Chapter=&ChapterID=24&MajorTopic=&Print=True&SeqEnd=1950000&SeqStart=450000

### Pattern involving contracts / buying and selling

The Act's broker definition includes, among other activities, a pattern of business of buying, selling, offering to buy or sell, marketing for sale, exchanging, or otherwise dealing in contracts, including assignable contracts for real estate. The statutory definition describes a pattern as one or more such practices on two or more occasions in any 12-month period.

Source: Illinois General Assembly, 225 ILCS 454 definitions.
https://ilga.gov/legislation/ILCS/details?ActID=1364&ActName=Real%20Estate%20License%20Act%20of%202000.&ChapAct=225%20ILCS%20454%2F&Chapter=PROFESSIONS%2C%20OCCUPATIONS%2C%20AND%20BUSINESS%20OPERATIONS&ChapterID=24&MajorTopic=REGULATION&SeqEnd=450000&SeqStart=100000

## System safeguards

- No automated contract signing.
- No automated legally binding offers.
- No automated brokerage activity.
- No automated mass SMS or calling.
- No automatic purchase of paid data/services.
- No scraping implementation until the source's access method, terms, robots policy, and legal concerns are documented.
- All consequential actions use an approval state.
- Compliance claims are stored with the date checked and primary source.

## Still requiring research

- Wholesaling-specific current Illinois guidance and applicability to the exact intended business model.
- Assignment/equitable-interest marketing boundaries for the intended workflows.
- TCPA/DNC, email, SMS, privacy, fair-housing, and local advertising requirements before activation.
- County-specific data access terms.
- Current approved education-provider comparison.
- County selection for the MVP.

These are deliberately not filled with guesses.
