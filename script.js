// Starting coins
let coins = 1000;

// Update coin display
function updateCoins() {
  document.getElementById("userCoins").innerText = "💰 Coins: " + coins;
}

// Deposit coins
function deposit() {
  let amount = prompt("Enter deposit amount (coins):");
  if (amount && !isNaN(amount)) {
    coins += parseInt(amount);
    updateCoins();
    alert("✅ Deposit successful!");
  }
}

// Withdraw coins
function withdraw() {
  let amount = prompt("Enter withdraw amount (coins):");
  if (amount && !isNaN(amount)) {
    amount = parseInt(amount);
    if (amount <= coins) {
      coins -= amount;
      updateCoins();
      alert("✅ Withdraw successful!");
    } else {
      alert("❌ Not enough coins!");
    }
  }
}

// Play the game
function playGame(choice) {
  if (coins < 100) {
    alert("❌ Not enough coins to play! Minimum 100 needed.");
    return;
  }

  // Deduct play cost
  coins -= 100;
  updateCoins();

  // Colors list
  let colors = ["red", "green", "blue"];
  let randomColor = colors[Math.floor(Math.random() * colors.length)];

  // Check result
  let resultText = document.getElementById("resultText");
  if (choice === randomColor) {
    coins += 300; // Win reward
    updateCoins();
    resultText.innerText = "🎉 You WON! It was " + randomColor.toUpperCase();
    resultText.style.color = randomColor;
    addHistory("✅ WON (" + randomColor + ")");
  } else {
    resultText.innerText = "😢 You LOST! It was " + randomColor.toUpperCase();
    resultText.style.color = randomColor;
    addHistory("❌ LOST (" + randomColor + ")");
  }
}

// Add game history
function addHistory(text) {
  let historyList = document.getElementById("historyList");
  let li = document.createElement("li");
  li.innerText = text;
  historyList.prepend(li); // latest on top
}

// Initialize
updateCoins();
