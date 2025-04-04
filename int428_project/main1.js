import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { MessageSquare } from "lucide-react";

export default function AIHealthAssistant() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");
    
    setTimeout(() => {
      setMessages((prev) => [...prev, { text: generateResponse(input), sender: "bot" }]);
    }, 1000);
  };

  const generateResponse = (query) => {
    if (query.toLowerCase().includes("prescription")) return "You can check your prescriptions in the records section.";
    if (query.toLowerCase().includes("hospital")) return "Here are some nearby hospitals: Apollo, Fortis, AIIMS.";
    if (query.toLowerCase().includes("treatment")) return "Please specify the treatment you're looking for, and I will assist you.";
    return "I'm here to help with healthcare-related queries. Please ask me anything!";
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white p-4">
      <h1 className="text-2xl font-semibold mb-4">AI Health Assistant</h1>
      <Card className="w-full max-w-md h-[60vh] flex flex-col p-4 overflow-hidden">
        <CardContent className="flex-1 overflow-y-auto space-y-2">
          {messages.map((msg, i) => (
            <div key={i} className={`p-2 rounded-lg ${msg.sender === "bot" ? "bg-gray-700" : "bg-blue-500 text-white"}`}>
              {msg.text}
            </div>
          ))}
        </CardContent>
        <div className="flex items-center gap-2 p-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 bg-gray-800 text-white"
          />
          <Button onClick={handleSend} className="bg-blue-500">
            <MessageSquare size={18} />
          </Button>
        </div>
      </Card>
    </div>
  );
}
