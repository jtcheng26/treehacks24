import { Inter } from "next/font/google";
import HeaderText from "@/components/text/HeaderText";
import InlineInput from "@/components/input/InlineInput";
import { useState } from "react";
import Content from "@/components/content/Content";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [user, setUser] = useState("");
  const [topic, setTopic] = useState("");
  const [started, setStarted] = useState(false);
  function handleStart() {
    setStarted(true);
  }
  function reset() {
    setUser("");
    setTopic("");
    setStarted(false);
  }
  return (
    <main
      className={`flex min-h-screen flex-col items-center pt-24 px-24 transition-all duration-500 ease-in-out ${inter.className} overflow-x-hidden`}
      style={{ paddingTop: started ? 60 : 300 }}
    >
      <div className="z-10 max-w-5xl w-full items-center justify-between lg:flex overflow-x-hidden">
        <div className="flex flex-col space-y-2 w-full">
          <HeaderText shrink={started}>
            I am a{" "}
            <InlineInput value={user} onChange={setUser} disabled={started} />
          </HeaderText>
          <HeaderText>
            Teach me about{" "}
            <InlineInput
              value={topic}
              onChange={setTopic}
              onSubmit={handleStart}
              disabled={started}
            />
          </HeaderText>
          <div className="h-2" />
          {started ? <Content user={user} topic={topic} reset={reset} /> : ""}
        </div>
      </div>
    </main>
  );
}
