/**
 * Safely extracts a limited amount of visible webpage text
 * for ClearVote analysis.
 */
class VisibleTextExtractor {
    static MAX_TEXT_LENGTH = 5000;

    /**
     * Check whether an element is visible to the user.
     */
    static is_visible(element) {
        const style = window.getComputedStyle(element);

        return (
            style.display !== "none" &&
            style.visibility !== "hidden" &&
            style.opacity !== "0" &&
            !element.hidden &&
            element.getAttribute("aria-hidden") !== "true"
        );
    }

    /**
     * Check whether an element is inside content
     * that ClearVote should avoid collecting.
     */
    static is_excluded(element) {
        const excluded_selectors = [
            "form",
            "input",
            "textarea",
            "select",
            "button",
            "script",
            "style",
            "noscript",
            "nav",
            "footer",
            "[contenteditable='true']"
        ];

        return Boolean(element.closest(excluded_selectors.join(",")));
    }

    /**
     * Extract visible article or main-page text.
     */
    static extract_visible_text() {
        const selectors = [
            "article h1",
            "article h2",
            "article h3",
            "article p",
            "article li",
            "main h1",
            "main h2",
            "main h3",
            "main p",
            "main li",
            "blockquote"
        ];

        const elements = document.querySelectorAll(
            selectors.join(",")
        );

        const text_parts = [];

        for (const element of elements) {
            if (!VisibleTextExtractor.is_visible(element)) {
                continue;
            }

            if (VisibleTextExtractor.is_excluded(element)) {
                continue;
            }

            const text = element.innerText
                .replace(/\s+/g, " ")
                .trim();

            if (text) {
                text_parts.push(text);
            }
        }

        const combined_text = text_parts.join(" ");

        return combined_text
            .replace(/\s+/g, " ")
            .trim()
            .slice(0, VisibleTextExtractor.MAX_TEXT_LENGTH);
    }
}

globalThis.VisibleTextExtractor = VisibleTextExtractor;