import React, { useEffect, useState } from "react";
import QuestionInput from "../input/QuestionInput";
import { BarLoader } from "react-spinners";
import { postQuestionAnswer } from "../requests/post";

export interface TextQuestionConfig {
  question: string;
}

const UNANSWERED = 0;
const CORRECT = 2;
const INCORRECT = 1;
const LOADING = 3;

export default function TextQuizQuestion({
  config,
  onAnswer,
  visible,
}: {
  config?: TextQuestionConfig;
  onAnswer: (correct: boolean, question: string, callback?: () => void) => void;
  visible: boolean;
}) {
  const [state, setState] = useState(UNANSWERED);
  useEffect(() => {
    setState(UNANSWERED);
  }, [config]);
  async function handleAnswer(answer: string, callback: () => void) {
    console.log("Submitting quiz answer", answer);
    setState(LOADING);
    // TODO: query answer
    const res = await postQuestionAnswer(config.question, answer);
    if ((await res.text()) === "NO") {
      setState(INCORRECT);
      onAnswer(false, config.question, callback);
    } else {
      setState(CORRECT);
      onAnswer(true, config.question, callback);
    }
  }
  return (
    <div
      className="flex flex-col space-y-1 transition-all duration-500 max-h-[470px]"
      style={{ width: visible ? 400 : 10, opacity: visible ? 1 : 0 }}
    >
      <span className="font-bold text-primary">
        {visible ? "Brief Response" : ""}
      </span>
      <div className="border-primary border-2 rounded-lg p-4 flex-col flex space-y-4">
        <span className="text-slate-400">{visible ? config.question : ""}</span>
        <QuestionInput
          onSubmit={handleAnswer}
          maxWidth={"100%"}
          placeholder="Type your answer..."
        />
        <BarLoader loading={state === LOADING} color="#4EB389" width="100%" />
        {state === CORRECT ? (
          <div className="w-full p-4 bg-primary rounded-lg flex justify-center items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m4.5 12.75 6 6 9-13.5"
              />
            </svg>
          </div>
        ) : state === INCORRECT ? (
          <div className="w-full p-4 bg-red-500 rounded-lg flex justify-center items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18 18 6M6 6l12 12"
              />
            </svg>
          </div>
        ) : (
          ""
        )}
      </div>
    </div>
  );
}
