/* ================= INFO DATABASE ================= */

const TEST_INFO = {
  encryption: {
    title: "Encryption Integrity Test",
    body: `
<b>Purpose:</b><br>
Validates that AES encryption and decryption operate correctly with MAC verification.<br><br>

<b>Why it matters:</b><br>
Ensures confidentiality and authenticity of messages. Any failure indicates broken cryptography.<br><br>

<b>Architecture:</b><br>
Plaintext → AES-EAX Encrypt → Ciphertext + MAC → Decrypt → Verify MAC → Output<br><br>

<b>Expected Result:</b><br>
PASS if decrypted output matches original and MAC is valid.
`
  },

  tamper: {
    title: "Message Tampering Attack",
    body: `
<b>Purpose:</b><br>
Simulates attacker modifying encrypted message.<br><br>

<b>Why it matters:</b><br>
Detects integrity violations and prevents forged messages.<br><br>

<b>Architecture:</b><br>
Ciphertext → Bit Flip → Decrypt → MAC Check → Reject<br><br>

<b>Expected Result:</b><br>
PASS if tampering is detected and message is rejected.
`
  },

  mitm: {
    title: "Replay / MITM Simulation",
    body: `
<b>Purpose:</b><br>
Simulates replay attacks and intercepted traffic.<br><br>

<b>Why it matters:</b><br>
Prevents attackers from resending captured encrypted messages.<br><br>

<b>Architecture:</b><br>
Captured Ciphertext → Replayed → Nonce Validation → Reject<br><br>

<b>Status:</b><br>
Coming Soon
`
  },

  key: {
    title: "Key Strength Test",
    body: `
<b>Purpose:</b><br>
Evaluates cryptographic strength of AES key.<br><br>

<b>Why it matters:</b><br>
Short keys are vulnerable to brute force attacks.<br><br>

<b>Architecture:</b><br>
AES Key → Length Check → Security Rating<br><br>

<b>Expected Result:</b><br>
256-bit key = VERY STRONG
`
}

};



/* ================= MODAL LOGIC ================= */

function openInfo(key) {
  document.getElementById("infoTitle").innerHTML = TEST_INFO[key].title;
  document.getElementById("infoBody").innerHTML = TEST_INFO[key].body;
  document.getElementById("infoModal").style.display = "flex";
}

function closeInfo() {
  document.getElementById("infoModal").style.display = "none";
}



