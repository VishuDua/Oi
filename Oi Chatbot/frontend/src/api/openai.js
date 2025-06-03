export async function sendChatMessage(messages) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("🤖 [Mock Reply] This is a simulated GPT-4 response.");
    }, 800);
  });
}
