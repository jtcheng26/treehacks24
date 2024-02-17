import React from "react";
import { MCQuestionConfig } from "../practice/QuizQuestion";
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
  return (
    <div className="grid grid-cols-2 w-full gap-2">
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
