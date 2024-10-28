async function encrypt() {
    const plaintext = document.getElementById('plaintext').value;
    const key = document.getElementById('key').value;

    // Перевірка, чи введено значення
    if (!plaintext || !key) {
        document.getElementById('ciphertext').innerText = "Будь ласка, введіть текст і ключ.";
        return;
    }

    const response = await fetch('http://localhost:5000/encrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ plaintext, key })
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById('ciphertext').innerText = data.ciphertext; // Виводимо зашифрований текст
    } else {
        document.getElementById('ciphertext').innerText = data.error || "Помилка при шифруванні.";
    }
}

async function decrypt() {
    const ciphertext = document.getElementById('ciphertextInput').value;
    const key = document.getElementById('keyDecrypt').value;

    // Перевірка, чи введено значення
    if (!ciphertext || !key) {
        document.getElementById('decryptedText').innerText = "Будь ласка, введіть зашифрований текст і ключ.";
        return;
    }

    const response = await fetch('http://localhost:5000/decrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ciphertext, key })
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById('decryptedText').innerText = data.plaintext; // Виводимо розшифрований текст
    } else {
        document.getElementById('decryptedText').innerText = data.error || "Помилка при розшифруванні.";
    }
}
