import { useState } from "react";
import { Send, Video, User, Bot, Loader2, AlertCircle } from "lucide-react";
import { transcriptAPI, chatAPI } from "../services/api";

export default function MainPage({ user, onNavigateToProfile }) {
  const [videoUrl, setVideoUrl] = useState("");
  const [isLoadingTranscript, setIsLoadingTranscript] = useState(false);
  const [chatStarted, setChatStarted] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");
  const [currentChatId, setCurrentChatId] = useState(null);
  const [currentTranscriptId, setCurrentTranscriptId] = useState(null);

  const handleLoadVideo = async (e) => {
    e.preventDefault();
    if (!videoUrl.trim()) return;

    setIsLoadingTranscript(true);
    setError("");
    setChatStarted(false);

    try {
      const transcript = await transcriptAPI.create(videoUrl);
      setCurrentTranscriptId(transcript.transcript_id);

      const chat = await chatAPI.create(transcript.transcript_id);
      setCurrentChatId(chat.chat_id);

      setChatStarted(true);
      setMessages([
        {
          sender: "bot",
          text: `Transcript loaded successfully! You can now ask questions about the video content.`,
        },
      ]);
    } catch (err) {
      setError(err.message || "Failed to load video transcript");
    } finally {
      setIsLoadingTranscript(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || !currentChatId || isSending) return;

    const userMessage = input;
    setInput("");
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setIsSending(true);
    setError("");

    try {
      const response = await chatAPI.sendMessage(currentChatId, userMessage);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: response.llm_message },
      ]);
    } catch (err) {
      setError(err.message || "Failed to send message");
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, I encountered an error. Please try again." },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Navbar */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 h-16 flex justify-between items-center">
          <div className="flex items-center">
            <Video className="w-7 h-7 text-red-500" />
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
              Enter Video URL
            </h1>
            <p className="text-gray-600 mb-6">
              After analyzing the transcript, you can ask questions about the video content in chat format.
            </p>

            {error && (
              <div className="mb-4 bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm flex items-center justify-center">
                <AlertCircle className="w-5 h-5 mr-2" />
                {error}
              </div>
            )}

            <form onSubmit={handleLoadVideo} className="flex gap-3">
              <input
                type="url"
                required
                placeholder="https://www.youtube.com/watch?v=..."
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-400 focus:border-transparent text-gray-900"
              />
              <button
                type="submit"
                disabled={isLoadingTranscript}
                className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoadingTranscript ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  "Load"
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
                placeholder="Ask a question..."
                disabled={isSending}
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <button
                type="submit"
                disabled={isSending}
                className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSending ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}
