# ClearVote Privacy, Ethics, and Legal Research

## 1. Main Privacy Risk

ClearVote may read webpage text and browsing activity. Even if ClearVote does not collect names or emails, browser activity and website content can still be treated as user data.

The safest design is to collect and store as little user data as possible.

## 2. Chrome Web Store Rules

Chrome requires extensions that handle user data to clearly explain what they collect, why they collect it, and who receives it.

As of August 1, 2026, Chrome requires all extension data collection to be prominently disclosed.

Chrome also requires extensions to:

- collect data only when necessary for the extension's single stated purpose
- request only the minimum browser permissions needed
- obtain user consent before collecting data
- use secure transmission such as HTTPS
- publish an accurate privacy policy
- disclose third parties that receive user data

**ClearVote approach:** process as much as possible locally. Send only the minimum text needed for analysis.

## 3. Louisiana Law

Louisiana enacted the **Louisiana Data Privacy Act**, effective January 1, 2027.

It applies to businesses meeting certain thresholds, including more than $25 million in annual revenue, processing data of at least 75,000 consumers, households, or devices for commercial purposes, or earning at least 50% of revenue from selling personal data.

The law exempts institutions of higher education and nonprofit organizations.

ClearVote should not rely on an exemption unless the university confirms the project is legally operating under the institution.

Covered organizations must provide a clear privacy notice, limit data to what is necessary, protect it, and obtain consent before processing sensitive data.

Louisiana also has a separate **Database Security Breach Notification Law**. Organizations holding personal information must use reasonable security and may have notification duties after a breach.

## 4. Children

COPPA applies when an online service is directed to children under 13 or knowingly collects personal information from a child under 13.

**ClearVote approach:** do not target children under 13 and do not collect age information unless there is a clear need.

If child data is knowingly collected, get legal guidance before continuing.

## 5. Other U.S. States

A public extension may reach users in states with their own privacy laws.

For example, California's CCPA mainly applies to for-profit businesses that meet revenue, data-volume, or data-sale thresholds.

ClearVote is unlikely to meet those thresholds as a student MVP.

If ClearVote becomes a commercial or large national service, perform a new multi-state privacy review.

## 6. EU Users

If ClearVote intentionally offers the service to people in the EU or monitors their behavior, the GDPR may apply.

Political opinions are a protected special category of personal data under the GDPR.

**ClearVote approach:** do not build profiles of users' political beliefs or preferences.

For the first pilot, limit distribution to the U.S. unless the team is ready for GDPR compliance.

## 7. Data ClearVote Should Avoid Collecting

Do not collect unless absolutely necessary:

- full browsing history
- account names or personal email addresses
- passwords, cookies, authentication tokens, or form data
- precise location
- political profiles or inferred political affiliation
- health, financial, or other sensitive information
- content from private pages such as email, banking, or medical portals

## 8. Recommended Data Flow

1. Detect or select relevant text in the browser.
2. Prefer local processing for basic page or claim detection.
3. Send only the claim or short text needed for analysis.
4. Do not permanently store webpage text by default.
5. Do not store browsing history.
6. Keep API keys only on the backend, never inside the extension.
7. Use HTTPS for every backend or API request.
8. Keep only minimal technical logs and delete them on a written schedule.
9. Do not sell user data or use it for targeted advertising.
10. Tell users which outside APIs or AI providers receive submitted text.

## 9. Warning and Fairness Rules

ClearVote should not say a person is lying or intentionally spreading disinformation unless there is strong evidence of intent.

Prefer labels such as:

- **Potentially misleading — review the evidence**
- **Relevant fact check found**
- **Conflicting evidence**
- **Not enough evidence found**
- **No checkable claim identified**

Always show the original source, fact-check source, date, and important context.

Do not use political party, ideology, race, religion, gender, or similar traits to change the result.

Use the same evaluation process for claims from different political viewpoints.

Provide a way to report an incorrect result or outdated source.

## 10. Before Public Release

ClearVote should have:

- a public privacy policy
- a short in-extension privacy notice
- documented browser permissions and why each is needed
- a list of third-party APIs or providers receiving data
- a written data-retention and deletion rule
- a basic security and breach-response plan
- testing for false positives and political bias
- a correction or report-problem process
- review by the university or legal counsel before a broad public launch

## Sources

- FTC — Privacy and Security
- FTC — COPPA Rule
- Chrome Web Store — User Data Policies
- Chrome Web Store — 2026 Privacy Policy Updates
- Louisiana Data Privacy Act, Act 502 (2026)
- Louisiana Database Security Breach Notification Law
- California Attorney General — CCPA
- EU GDPR
