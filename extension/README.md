# ClearVote Browser Extension

The extension currently provides a placeholder popup and local webpage-text extraction. It does not send text to a backend or display analysis results yet.

## Prerequisites

- Google Chrome with access to Developer mode on the extensions page.
- A local clone of this repository (see the [root setup guide](../README.md#getting-started)).

No Node.js installation, build command, API keys, or environment variables are required.

## Load the Extension

1. Open `chrome://extensions` in Chrome.
2. Turn on **Developer mode**.
3. Click **Load unpacked**.
4. Select the repository's `extension/` directory, which contains `manifest.json`.
5. Open Chrome's Extensions menu and select **ClearVote**. You can pin it for easier access.

The popup should show **ClearVote** and **Extension shell is working.**

## Verify Page Text Extraction

1. Open or refresh a normal HTTP or HTTPS webpage with article or main content. Chrome's internal pages, such as `chrome://extensions`, do not run this content script.
2. Open that webpage's Developer Tools and select **Console**. Ensure informational logs are visible.
3. Look for `ClearVote content script loaded.` and `ClearVote extracted text length:` followed by a number between 0 and 5,000.

The extractor targets headings, paragraphs, and list items within `article` or `main`, plus blockquotes. It normalizes whitespace and filters certain hidden elements, forms, editable fields, navigation, and footers. A length of zero can mean the page has no matching content. Extraction runs once when the page becomes idle; dynamically added content may require a page reload.

The console reports the length rather than the extracted text. These filters are an initial implementation, not a guarantee that all private content is excluded; use a public page for verification.

## Reload After Changes

1. Save your extension changes.
2. Return to `chrome://extensions` and click **Reload** on the ClearVote card.
3. Refresh the webpage to load the updated content scripts, and reopen the popup to check popup changes.

If loading fails, confirm that you selected `extension/`, then check the extension card's **Errors** button if present. Popup logs appear in the popup's own Developer Tools (right-click the popup and choose **Inspect**); content-script logs appear in the webpage's console.
