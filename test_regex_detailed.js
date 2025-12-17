// Test the exact regex and replace patterns used in the frontend
const testInputs = [
    // Case 1: Default formatted input
    `Selected text:
"Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."

Ask a question about this text...`,

    // Case 2: User added a question
    `Selected text:
"Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."

Ask a question about this text...What is AI?`,

    // Case 3: User modified the question part
    `Selected text:
"Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."

Ask a question about this text...How does AI work?`,

    // Case 4: Different spacing (potential issue)
    `Selected text:\n"Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."\n\nAsk a question about this text...What is AI?`
];

console.log("Testing the exact patterns used in the frontend:");
console.log();

testInputs.forEach((input, index) => {
    console.log(`Test ${index + 1}:`);
    console.log("Full input:", JSON.stringify(input));

    // Extract selected text (same as line 67 in EnhancedChatbot.jsx)
    const selectedTextMatch = input.match(/Selected text:\s*"(.*?)"\s*\n\n/);
    if (selectedTextMatch && selectedTextMatch[1]) {
        console.log("✓ Extracted selected text:", JSON.stringify(selectedTextMatch[1]));
    } else {
        console.log("✗ No selected text match found");
    }

    // Extract question text (same as line 79 in EnhancedChatbot.jsx)
    const questionText = input.replace(/Selected text:\s*".*?"\s*\n\n/, '').trim();
    console.log("✓ Question text after removal:", JSON.stringify(questionText));

    // Test if the extracted parts make sense together
    if (selectedTextMatch && selectedTextMatch[1]) {
        console.log("✓ Selected text length:", selectedTextMatch[1].length);
    }
    console.log("✓ Question text length:", questionText.length);
    console.log("---");
});