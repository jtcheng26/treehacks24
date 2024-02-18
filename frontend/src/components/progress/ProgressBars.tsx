import React from "react";
import { MCQuestionConfig } from "../practice/MCQuizQuestion";
import { Section } from "@/hooks/useManim";
import ProgressBar from "./ProgressBar";

export default function ProgressBars({
  sections,
  visible = true,
  currentSection,
}: {
  sections: Section[];
  visible: boolean;
  currentSection: number;
}) {
  const gridCol = {
    0: "grid-cols-1",
    1: "grid-cols-1",
    2: "grid-cols-2",
    3: "grid-cols-3",
    4: "grid-cols-4",
    5: "grid-cols-5",
    6: "grid-cols-6",
    7: "grid-cols-7",
    8: "grid-cols-8",
    9: "grid-cols-9",
    10: "grid-cols-10",
    11: "grid-cols-11",
    12: "grid-cols-12",
  };
  return (
    <div
      className={`grid ${
        sections.length in gridCol ? gridCol[sections.length] : "grid-cols-1"
      } w-full gap-2`}
    >
      {sections.map((s, i) => (
        <ProgressBar
          key={s.title}
          active={currentSection >= i}
          section={s}
          visible={visible}
        />
      ))}
    </div>
  );
}
