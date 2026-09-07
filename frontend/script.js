

const inputText = document.getElementById("inputText");

const translatedText =
    document.getElementById("translatedText");

const sourceLanguage =
    document.getElementById("sourceLanguage");

const targetLanguage =
    document.getElementById("targetLanguage");

const translateButton =
    document.getElementById("translateButton");

const copyButton =
    document.getElementById("copyButton");

const swapButton =
    document.getElementById("swapButton");

const clearButton =
    document.getElementById("clearButton");

const message =
    document.getElementById("message");
// Translate button
translateButton.addEventListener("click", async () => {

    const text = inputText.value.trim();

    const source = sourceLanguage.value;

    const target = targetLanguage.value;


    // Check if input is empty
    if (!text) {

        message.textContent =
            "Please enter some text.";

        translatedText.value = "";

        return;
    }


    // Same language
    if (source === target) {

        translatedText.value = text;

        message.textContent =
            "Source and target languages are the same.";

        return;
    }


    message.textContent = "Translating...";

    translateButton.disabled = true;


    try {

        const response = await fetch(
            "http://localhost:5000/translate",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text,
                    sourceLanguage: source,
                    targetLanguage: target
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.message || "Translation failed"
            );
        }


        translatedText.value =
            data.translatedText;

        message.textContent =
            "Translation completed successfully.";

    } catch (error) {

        console.error(error);

        message.textContent =
            "Translation failed. Please try again.";

    } finally {

        translateButton.disabled = false;
    }
});


// Copy button
copyButton.addEventListener("click", async () => {

    const text = translatedText.value.trim();


    if (!text) {

        message.textContent =
            "Nothing to copy.";

        return;
    }


    try {

        await navigator.clipboard.writeText(text);

        message.textContent =
            "Translation copied to clipboard!";

    } catch (error) {

        console.error(error);

        message.textContent =
            "Unable to copy translation.";
    }
});

// Swap source and target languages
swapButton.addEventListener("click", () => {

    const currentSource = sourceLanguage.value;

    sourceLanguage.value = targetLanguage.value;

    targetLanguage.value = currentSource;

    message.textContent = "Languages swapped.";

});

// Clear input and translation
clearButton.addEventListener("click", () => {

    inputText.value = "";

    translatedText.value = "";

    message.textContent = "";

});