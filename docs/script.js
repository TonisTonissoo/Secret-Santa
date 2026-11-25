
async function decryptName(code) {
    // Convert URL-safe Base64 into standard Base64
    let base64 = code.trim()
        .replace(/-/g, "+")
        .replace(/_/g, "/");

    if (!/^[A-Za-z0-9+/]+={0,2}$/.test(base64)) {
        throw new Error("Invalid code format");
    }

    base64 = base64.padEnd(
        Math.ceil(base64.length / 4) * 4,
        "="
    );

    // Decode Base64 into bytes
    const combined = Uint8Array.from(
        atob(base64),
        char => char.charCodeAt(0)
    );

    // Key + nonce + authentication tag
    if (combined.length <= 60) {
        throw new Error("Invalid code length");
    }

    // Extract encryption components
    const key = combined.slice(0, 32);
    const nonce = combined.slice(32, 44);
    const ciphertext = combined.slice(44);

    // Import the AES key
    const cryptoKey = await crypto.subtle.importKey(
        "raw",
        key,
        { name: "AES-GCM" },
        false,
        ["decrypt"]
    );

    // Decrypt the recipient's name
    const decrypted = await crypto.subtle.decrypt(
        {
            name: "AES-GCM",
            iv: nonce,
            tagLength: 128
        },
        cryptoKey,
        ciphertext
    );

    return new TextDecoder("utf-8", {
        fatal: true
    }).decode(decrypted);
}


const form = document.getElementById("reveal-form");
const codeInput = document.getElementById("secret-code");
const result = document.getElementById("result");
const recipientName = document.getElementById("recipient-name");
const errorMessage = document.getElementById("error-message");
const hideButton = document.getElementById("hide-button");
const revealButton = form.querySelector("button");


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    errorMessage.hidden = true;
    result.hidden = true;
    revealButton.disabled = true;

    try {
        const name = await decryptName(codeInput.value);

        recipientName.textContent = name;
        codeInput.value = "";

        result.hidden = false;
        form.hidden = true;

    } catch {
        errorMessage.textContent =
            "Invalid secret code. Please try again.";

        errorMessage.hidden = false;

    } finally {
        revealButton.disabled = false;
    }
});


hideButton.addEventListener("click", () => {
    recipientName.textContent = "";
    codeInput.value = "";

    result.hidden = true;
    form.hidden = false;
    errorMessage.hidden = true;

    codeInput.focus();
});
