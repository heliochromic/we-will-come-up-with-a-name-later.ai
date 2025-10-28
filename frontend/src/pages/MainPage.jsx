import { useState } from "react";
import { Send, Youtube, User, Bot, Loader2 } from "lucide-react";

export default function MainPage({ user, onNavigateToProfile }) {
  const [videoUrl, setVideoUrl] = useState("");
  const [isLoadingTranscript, setIsLoadingTranscript] = useState(false);
  const [chatStarted, setChatStarted] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // --- Симуляція завантаження транскрипту ---
  const handleLoadVideo = async (e) => {
    e.preventDefault();
    if (!videoUrl.trim()) return;

    setIsLoadingTranscript(true);
    setChatStarted(false);

    // Симулюємо запит до backend
    setTimeout(() => {
      setIsLoadingTranscript(false);
      setChatStarted(true);
      setMessages([
        {
          sender: "bot",
          text: `✅ Транскрипт відео "${videoUrl}" завантажено. Можете ставити запитання про зміст.`,
        },
      ]);
    }, 2000);
  };

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    // Симуляція відповіді бота
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: `🤖 Цікава думка! Ви запитали: "${input}".` },
      ]);
    }, 800);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 h-16 flex justify-between items-center">
          <div className="flex items-center">
            <Youtube className="w-7 h-7 text-red-500" />
            <span className="ml-2 font-semibold text-gray-900 text-lg">
              Video RAG Chat
            </span>
          </div>
          <button
            onClick={onNavigateToProfile}
            className="flex items-center space-x-2 text-gray-700 hover:text-gray-900 transition"
          >
            <User className="w-5 h-5" />
            <span>{user?.name}</span>
          </button>
        </div>
      </nav>

      {/* Content */}
      <main className="flex-1 flex flex-col items-center py-8 px-4">
        {!chatStarted ? (
          <div className="w-full max-w-xl bg-white p-8 rounded-2xl shadow-md text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              Введіть посилання на відео
            </h1>
            <p className="text-gray-600 mb-6">
              Після аналізу транскрипту ви зможете ставити запитання про зміст
              відео у форматі чату.
            </p>

            <form onSubmit={handleLoadVideo} className="flex gap-3">
              <input
                type="url"
                required
                placeholder="https://www.youtube.com/watch?v=..."
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-400 focus:border-transparent"
              />
              <button
                type="submit"
                disabled={isLoadingTranscript}
                className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors flex items-center justify-center disabled:opacity-50"
              >
                {isLoadingTranscript ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  "Завантажити"
                )}
              </button>
            </form>
          </div>
        ) : (
          <div className="w-full max-w-3xl bg-white shadow-lg rounded-2xl flex flex-col overflow-hidden">
            {/* Chat area */}
            <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-gray-50">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex items-start space-x-3 ${
                    msg.sender === "user" ? "justify-end" : ""
                  }`}
                >
                  {msg.sender === "bot" && (
                    <div className="flex-shrink-0 bg-blue-100 p-2 rounded-full">
                      <Bot className="w-5 h-5 text-blue-600" />
                    </div>
                  )}
                  <div
                    className={`max-w-[75%] p-3 rounded-lg ${
                      msg.sender === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-gray-200 text-gray-900"
                    }`}
                  >
                    {msg.text}
                  </div>
                  {msg.sender === "user" && (
                    <div className="flex-shrink-0 bg-gray-100 p-2 rounded-full">
                      <User className="w-5 h-5 text-gray-700" />
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Input area */}
            <form
              onSubmit={handleSend}
              className="border-t border-gray-200 p-4 flex items-center gap-3 bg-white"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Напишіть запитання..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="submit"
                className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}
