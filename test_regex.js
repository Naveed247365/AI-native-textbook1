// Test the regex pattern used in the frontend
const testInputs = [
    `Selected text:
"Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."

Ask a question about this text...`,

    `Selected text:
"Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."

Ask a question about this text...What is AI?`,

    `What is AI?`
];

console.log("Testing regex pattern: /Selected text:\\s*\"(.*?)\"\\s*\\n\\n/");
console.log();

testInputs.forEach((input, index) => {
    console.log(`Test ${index + 1}:`);
    console.log("Input:", JSON.stringify(input));

    const selectedTextMatch = input.match(/Selected text:\s*"(.*?)"\s*\n\n/);
    if (selectedTextMatch && selectedTextMatch[1]) {
        console.log("Extracted selected text:", JSON.stringify(selectedTextMatch[1]));
    } else {
        console.log("No match found");
    }

    // Test what the question text would be after removing the prefix
    const questionText = input.replace(/Selected text:\s*".*?"\s*\n\n/, '').trim();
    console.log("Question text:", JSON.stringify(questionText));
    console.log("---");
});