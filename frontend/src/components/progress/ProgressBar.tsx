import { Section } from "@/hooks/useManim";
import React from "react";
import { PulseLoader } from "react-spinners";

export default function ProgressBar({
  active,
  section,
  visible = true,
}: {
  active: boolean;
  section: Section;
  visible: boolean;
}) {
  if (!section.ready && active && visible)
    return (
      <span className="col-span-1 flex justify-center items-center">
        <PulseLoader
          color={
            section.title.slice(0, 11) === "Explanation"
              ? "rgb(251 146 60)"
              : "rgb(78 179 137)"
          }
          size="8px"
        />
      </span>
    );
  if (!visible) return "";
  return (
    <div className="flex flex-col items-center justify-end col-span-1 text-xs space-y-1">
      <span
        className={`font-bold ${
          section.title.slice(0, 11) === "Explanation"
            ? "text-orange-400"
            : "text-primary"
        } transition-all duration-200`}
        style={{
          opacity:
            active || section.title.slice(0, 11) === "Explanation" ? 1 : 0,
        }}
      >
        {section.title}
      </span>
      <div
        className="bg-slate-700 rounded-full h-2 relative transition-all duration-200"
        style={{ width: visible ? "100%" : "0" }}
      >
        <div
          className={`absolute top-0 bottom-0 left-0 right-0 rounded-full ${
            section.title.slice(0, 11) === "Explanation"
              ? "bg-orange-400"
              : "bg-primary"
          } h-2 transition-all duration-1000 ease-linear`}
          style={{ width: section.progressState.played * 100 + "%" }}
        />
      </div>
    </div>
  );
}
