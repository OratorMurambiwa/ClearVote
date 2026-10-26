/**
 * ClearVote content script.
 * Extracts a limited amount of safe, visible webpage text.
 */

const visible_text =
    globalThis.VisibleTextExtractor.extract_visible_text();

console.log("ClearVote content script loaded.");
console.log(
    "ClearVote extracted text length:",
    visible_text.length
);