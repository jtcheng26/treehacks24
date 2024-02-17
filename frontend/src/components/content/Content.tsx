import React, { useRef, useState } from "react";
import { ScaleLoader } from "react-spinners";
import useManim from "../../hooks/useManim";
import Player from "../player/Player";
import ReplayButton from "../button/ReplayButton";
import QuestionInput from "../input/QuestionInput";
import QuizQuestion from "../practice/QuizQuestion";
import ProgressBars from "../progress/ProgressBars";

export const QuizConfig = {
  question: "What is the result of multiplying a 3x2 matrix by a 2x4 matrix?",
  choices: ["3x2 matrix", "2x2 matrix", "3x4 matrix", "Cannot be multiplied"],
  answer: 2,
};

export default function Content({ user, topic, reset }) {
  const { ready, data, update, updateProgress } = useManim(user, topic);
  const [playing, setPlaying] = useState(true);
  const [currentSection, setCurrentSection] = useState(0);
  const [showQuestion, setShowQuestion] = useState(false);
  const [showReplay, setShowReplay] = useState(false);
  const [done, setDone] = useState(false);
  const loading = !ready;
  const playerRef = useRef(null);
  function handleReplay() {
    if (playerRef.current) {
      playerRef.current.seekTo(0);
      setPlaying(true);
    }
  }
  function handleProgress(state) {
    updateProgress(currentSection, state);
    if (state.played === 1) {
      setShowQuestion(true);
      setShowReplay(true);
    }
  }
  function handleQuestion(prompt: string) {
    // TODO: update next video slot
    console.log("Submitted question:", prompt);
  }
  function handleFocus() {
    setPlaying(false);
  }
  function handleUnfocus() {
    if (data[currentSection].progressState.played < 1) setPlaying(true);
  }
  function handleQuizAnswer(correct: boolean) {
    setShowReplay(false);
    setTimeout(() => {
      setShowQuestion(false);
      setTimeout(() => {
        // TODO: set end screen
        if (currentSection < data.length - 1)
          setCurrentSection(currentSection + 1);
        else setDone(true);
      }, 1000);
    }, 3000);
  }
  return (
    <div className="w-full h-full flex flex-col">
      <div
        className={`absolute top-0 left-0 right-0 bottom-0 w-screen h-screen ${
          done ? "backdrop-blur-lg" : "backdrop-blur-0"
        } flex justify-center items-center transition-all duration-200`}
        style={{ zIndex: done ? 1000 : -10, opacity: done ? 1 : 0 }}
      >
        <ReplayButton onClick={reset} visible={done} text='New Lesson' />
      </div>
      <ScaleLoader loading={loading} color="#4EB389" />
      <div className={"flex flex-col space-y-2 transition-all duration-100 overflow-hidden"}>
        <div
          className={`w-full flex justify-center items-center h-[450px] ${
            loading ? "hidden" : "block"
          }`}
        >
          <Player
            url={data[currentSection].video}
            playing={playing}
            playerRef={playerRef}
            onProgress={handleProgress}
          />
          <QuizQuestion
            config={data[currentSection].question.data}
            onAnswer={handleQuizAnswer}
            visible={showQuestion}
          />
        </div>
        <div className="w-full flex flex-row items-center space-x-4 justify-center pb-6">
          <ReplayButton onClick={handleReplay} visible={showReplay} />
          <QuestionInput
            visible={!loading}
            onSubmit={handleQuestion}
            onFocus={handleFocus}
            onUnfocus={handleUnfocus}
          />
        </div>
        <div>
          <ProgressBars
            currentSection={currentSection}
            sections={data}
            visible={!loading}
          />
        </div>
      </div>
    </div>
  );
}
