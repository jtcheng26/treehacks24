import React, { useEffect, useState } from "react";

export interface MCQuestionConfig {
  question: string;
  choices: string[];
  answer: number;
}

const letterLabels = ["A", "B", "C", "D", "E"];

export default function MCQuizQuestion({
  config,
  onAnswer,
  visible,
}: {
  config?: MCQuestionConfig;
  onAnswer: (correct: boolean) => void;
  visible: boolean;
}) {
  const [chosen, setChosen] = useState(-1);
  useEffect(() => {
    setChosen(-1);
  }, [config]);
  function handleAnswer(i: number) {
    setChosen(i);
    onAnswer(i === config.answer);
  }
  function choiceStyle(i: number) {
    if (chosen === -1) return "bg-slate-800";
    if (chosen === i && chosen === config.answer) return "bg-primary";
    if (chosen === i && chosen !== config.answer) return "bg-red-500";
    else if (chosen !== config.answer && i === config.answer)
      return "bg-primary";
    else return "bg-slate-800 opacity-50";
  }
  function spanStyle(i: number) {
    if (chosen === -1) return "text-slate-600";
    if (chosen === i && chosen === config.answer) return "text-green-700";
    if (chosen === i && chosen !== config.answer) return "text-red-700";
    else if (chosen !== config.answer && i === config.answer)
      return "bg-primary text-green-700";
    else return "text-slate-600 opacity-50";
  }
  function iconLabel(i: number) {
    if (chosen !== -1 && i === config.answer)
      return (
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
      );
    if (chosen === i && chosen !== config.answer)
      return (
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
      );
    return letterLabels[i];
  }
  return (
    <div
      className="flex flex-col space-y-1 transition-all duration-500 max-h-[470px]"
      style={{ width: visible ? 400 : 10, opacity: visible ? 1 : 0 }}
    >
      <span className="font-bold text-primary">
        {visible ? "Multiple Choice" : ""}
      </span>
      <div className="border-primary border-2 rounded-lg p-4 flex-col flex space-y-4">
        <span className="text-slate-400">{visible ? config.question : ""}</span>
        <div className="space-y-2">
          {config.choices
            .slice(0, Math.min(5, config.choices.length))
            .map((answer, i) => (
              <div
                className={`${choiceStyle(
                  i
                )} h-12 text-sm flex flex-row items-center px-3 rounded-lg overflow-hidden ${
                  chosen === -1
                    ? "hover:brightness-125 hover:scale-90 transition-all ease-in-out duration-200 cursor-pointer"
                    : ""
                }`}
                key={answer}
                onClick={() => handleAnswer(i)}
              >
                <span className={`mr-3 font-bold ${spanStyle(i)}`}>
                  {iconLabel(i)}
                </span>
                {visible ? answer : ""}
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
